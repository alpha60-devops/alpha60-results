#!/usr/bin/env python3
"""Build regional Top N tables from committed annual cumulative geography.

One country reduction feeds all regions. N only limits presentation; the ledger
retains every ranked object. No CSV, network access, or ITU adjustment is needed.
"""
import argparse
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
from datetime import date
from decimal import Decimal, localcontext
from fractions import Fraction
import gzip
import hashlib
import json
from multiprocessing import get_context
import os
from pathlib import Path
import re
import shutil
import subprocess

DEFAULT_TOP_N = 50
ROLES = ('downloaders', 'uploaders')
REGIONS = ('africa-60', 'asia-28', 'usa-can', 'eur-27')
LABELS = dict(zip(REGIONS, ('Africa-60', 'Asia-28', 'USA + CAN', 'EUR-27')))
EUR27 = 'AUT BEL BGR HRV CYP CZE DNK EST FIN FRA DEU GRC HUN IRL ITA LVA LTU LUX MLT NLD POL PRT ROU SVK SVN ESP SWE'.split()
CSS = '''/* Regional tables keep the main site's Izzi typography. */
.region-rankings { overflow-wrap: anywhere; }
.region-table-scroll { overflow-x: auto; max-width: 100%; margin: 1.5rem 0; }
.region-table-scroll:focus-visible { outline: 3px solid #175b8c; outline-offset: 3px; }
.region-table-scroll table { display: table; min-width: 850px; width: 100%; margin: 0; }
.region-table-scroll thead { display: table-header-group; }
.region-table-scroll tbody { display: table-row-group; }
.region-table-scroll tr { display: table-row; }
/* Override the shared stylesheet's mobile width: 100% !important. */
.region-table-scroll th, .region-table-scroll td { display: table-cell; width: auto !important; }
.region-table-scroll td::before { display: none; }
.region-table-scroll code { white-space: normal; overflow-wrap: anywhere; }
'''


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def dump(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode()


def state(repo):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args], text=True)
    return {'commit': git('rev-parse', 'HEAD').strip(),
            'tracked': set(git('ls-files', '-z').split('\0')),
            'dirty': set(git('diff', '--name-only', '-z', 'HEAD').split('\0'))}


def read_bytes(repo, version, relative, sources):
    if relative not in version['tracked'] or relative in version['dirty']:
        raise ValueError(f'Uncommitted analytical input: {repo / relative}')
    raw = (repo / relative).read_bytes()
    sources.append({'repository': repo.name, 'commit': version['commit'], 'path': relative,
                    'sha256': sha(raw),
                    'url': f'https://github.com/alpha60-devops/{repo.name}/blob/{version["commit"]}/{relative}'})
    return raw


def read(repo, version, relative, sources):
    raw = read_bytes(repo, version, relative, sources)
    return json.loads(gzip.decompress(raw) if relative.endswith('.gz') else raw)


def region_definitions(root):
    repo = root / 'alpha60-results'
    refs = []
    definition = read(repo, state(repo), 'resources/h15-v3/h15-v3.generated.json', refs)
    result = {}
    for key in REGIONS:
        if key in ('africa-60', 'asia-28'):
            codes = sorted(r['code'] for r in definition['country_sets'][key])
            source = {**refs[0], 'definition_id': definition['definition_id']}
            note = 'Existing project country-code boundary.'
        elif key == 'usa-can':
            codes = ['CAN', 'USA']
            source = {'type': 'approved-user-specification', 'date': '2026-09-25',
                      'url': 'https://github.com/bdekoz/alpha60/blob/main/docs/development/20260925_alpha60_results_github_pages_v4.md'}
            note = 'Exactly USA and CAN; separately coded territories are not added.'
        else:
            codes = sorted(EUR27)
            source = {'type': 'official-EU-membership', 'url': 'https://european-union.europa.eu/easy-read_en',
                      'verified_date': '2026-09-25', 'source_updated_date': '2026-01-01'}
            note = 'Fixed current EU member-country ISO-3 codes for every sample year. GBR and separately coded territories are not added.'
        expected = {'africa-60': 60, 'asia-28': 28, 'usa-can': 2, 'eur-27': 27}[key]
        if len(codes) != len(set(codes)) or len(codes) != expected or not all(re.fullmatch('[A-Z]{3}', c) for c in codes):
            raise ValueError(f'Invalid membership for {key}')
        if key == 'asia-28' and 'TWN' not in codes:
            raise ValueError('Asia-28 must include TWN')
        result[key] = {'label': LABELS[key], 'country_codes': codes, 'source': source, 'note': note}
    return {'schema_version': 1, 'definition_id': 'region-rankings-20260925-v1', 'regions': result}


def reduce_sample(job):
    repo, version, key = job
    sources = []
    meta = read(repo, version, f'data/json/{key}-cumulative.json', sources)
    geo = read(repo, version, f'data/geojson.cumulative/{key}-cumulative-aggregate.geojson.gz', sources)
    read_bytes(repo, version, f'docs/itemized/{key}-sample-cache-audit.md', sources)
    assert meta['collection_key'] == geo['id'] == key
    assert geo['duration_type'] == 'cumulative' and geo['duration_index'] == 0
    assert geo['swarm_geo_partition_by'] == 'hexagon'
    assert geo['swarm_hexagon_resolution'] == 5 and geo['swarm_size_min'] == 3
    assert geo['datestamp'] == meta['sample_duration']
    start, end = meta['sample_duration'].split('-to-')
    assert date.fromisoformat(start) <= date.fromisoformat(end)
    countries = defaultdict(lambda: dict.fromkeys(ROLES, 0))
    hosting = defaultdict(lambda: dict.fromkeys(ROLES, 0))
    for feature in geo['features']:
        props = feature['properties']
        code = props['country_code']
        for role in ROLES:
            values = json.loads(props[role]) if isinstance(props[role], str) else props[role]
            count, hosted = values['size'], values['hosting']
            assert type(count) is int and type(hosted) is int and 0 <= hosted <= count
            countries[code][role] += count
            hosting[code][role] += hosted
    world = {role: sum(v[role] for v in countries.values()) for role in ROLES}
    return {'key': key, 'name': meta['collection_name'], 'collection_id': meta['collection_id'],
            'repository_year': int(repo.name[-4:]), 'sample_year': meta['sample_year_start'],
            'start': start, 'end': end, 'sample_days': meta['sample_days'],
            'calendar_days': (date.fromisoformat(end) - date.fromisoformat(start)).days + 1,
            'data_version': meta['data_version'], 'geojson_version': geo['data_version'],
            'ip_geolocation_version': meta['ip_geolocation_version'], 'features': len(geo['features']),
            'world': world, 'countries': dict(sorted(countries.items())),
            'hosting_by_country': dict(sorted(hosting.items())),
            'companion_json_world': {role: meta['collection_cumulative']['unique_btiha']['u' + role + '_total'] for role in ROLES},
            'sources': sources,
            'audit_url': f'https://alpha60-devops.github.io/{repo.name}/docs/itemized/{key}-sample-cache-audit.html'}


def identity(row):
    return {k: row[k] for k in ('key', 'repository_year', 'start', 'end')}


def regional(row, definition, role='downloaders'):
    return sum(row['countries'].get(code, {}).get(role, 0) for code in definition['country_codes'])


def calculate_rankings(samples, definitions):
    grouped = defaultdict(list)
    for row in samples:
        grouped[row['key']].append(row)
    selected, duplicates = [], []
    for key, rows in sorted(grouped.items()):
        rows.sort(key=lambda r: (r['end'], r['start'], r['repository_year']), reverse=True)
        selected.append(rows[0])
        if len(rows) > 1:
            duplicates.append({'key': key, 'retained': identity(rows[0]), 'discarded': [identity(r) for r in rows[1:]]})
    excluded = [{**identity(r), 'reason': 'zero worldwide downloader denominator'} for r in selected if not r['world']['downloaders']]
    eligible = [r for r in selected if r['world']['downloaders']]
    rankings = {}
    for key, definition in definitions['regions'].items():
        ordered = sorted(eligible, key=lambda r: (-Fraction(regional(r, definition), r['world']['downloaders']), -r['world']['downloaders'], r['key']))
        rankings[key] = [{'rank': n, 'key': r['key'], 'repository_year': r['repository_year'],
                          'regional_weight': regional(r, definition), 'world_weight': r['world']['downloaders']}
                         for n, r in enumerate(ordered, 1)]
    return [identity(r) for r in selected], duplicates, excluded, rankings


def collect(root, workers):
    definitions = region_definitions(root)
    versions, jobs = {}, []
    for year in range(2017, 2027):
        repo = root / f'alpha60-results-{year}'
        version = state(repo)
        versions[str(year)] = version['commit']
        keys = {p.name.removesuffix('-cumulative.json') for p in (repo / 'data/json').glob('*-cumulative.json')}
        geos = {p.name.removesuffix('-cumulative-aggregate.geojson.gz') for p in (repo / 'data/geojson.cumulative').glob('*-cumulative-aggregate.geojson.gz')}
        audits = {p.name.removesuffix('-sample-cache-audit.md') for p in (repo / 'docs/itemized').glob('*-sample-cache-audit.md')}
        if not keys or keys != geos or keys != audits:
            raise ValueError(f'Incomplete annual input inventory: {year}')
        jobs.extend((repo, version, key) for key in sorted(keys))
    samples = []
    with ProcessPoolExecutor(max_workers=workers, mp_context=get_context('spawn')) as pool:
        for row in pool.map(reduce_sample, jobs):
            samples.append(row)
            if len(samples) % 50 == 0:
                print(f'Reduced {len(samples)}/{len(jobs)} annual samples', flush=True)
    for year, commit in versions.items():
        current = state(root / f'alpha60-results-{year}')
        if current['commit'] != commit or any(ref['path'] in current['dirty'] for r in samples if r['repository_year'] == int(year) for ref in r['sources']):
            raise ValueError(f'Inputs changed during reduction: {year}')
    selected, duplicates, excluded, rankings = calculate_rankings(samples, definitions)
    source = {'filename': Path(__file__).name, 'sha256': sha(Path(__file__).read_bytes())}
    return {'schema_version': 3, 'calculation_date': date.today().isoformat(), 'calculation_generator': source,
            'definitions': definitions, 'definition_sha256': sha(dump(definitions)),
            'repositories': versions, 'metric': 'Cumulative regional downloader weight / worldwide geographic downloader weight',
            'samples': samples, 'selected_samples': selected, 'duplicates': duplicates,
            'excluded_zero_denominator': excluded, 'rankings': rankings}


def load_ledger(path):
    raw = path.read_bytes()
    data = json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)
    if data.get('schema_version') != 3:
        raise ValueError('--from-ledger requires the consolidated schema-3 ledger')
    if sha(dump(data['definitions'])) != data['definition_sha256']:
        raise ValueError('Definition digest mismatch')
    for row in data['samples']:
        for role in ROLES:
            if any(type(v[role]) is not int or v[role] < 0 for v in row['countries'].values()) or sum(v[role] for v in row['countries'].values()) != row['world'][role]:
                raise ValueError(f'Invalid country rollup: {row["key"]}')
    selected, duplicates, excluded, rankings = calculate_rankings(data['samples'], data['definitions'])
    if (selected, duplicates, excluded, rankings) != (data['selected_samples'], data['duplicates'], data['excluded_zero_denominator'], data['rankings']):
        raise ValueError('Ledger sample selection or rank ordering is inconsistent')
    if set(rankings) != set(REGIONS):
        raise ValueError('The consolidated ledger must contain all four regions')
    return data


def percentage(numerator, denominator):
    with localcontext() as context:
        context.prec = 40
        return f'{Decimal(100) * numerator / denominator:.2f}%'


def front(title):
    return ['---', 'layout: default', 'title: ' + json.dumps(title),
            'author: "Benjamin De Kosnik <bkoz@gnu.org>"',
            'description: "Cumulative downloader geography across the 2017–2026 annual repositories"',
            '---', '', '{::nomarkdown}',
            '<img src="../resources/a60-logo-block-gray.simple.svg?sanitize=true" height="50" width="100" alt="Alpha60">',
            '<link rel="stylesheet" href="../resources/izzi-table-wcag-22.css">',
            '<link rel="stylesheet" href="../resources/region-rankings.css">', '{:/}', '',
            '[Swarm Results](../index.html)', '', '<div class="region-rankings" markdown="1">', '', '# ' + title, '']


def table_start(label):
    return [f'<div class="region-table-scroll" role="region" aria-label="{label}" tabindex="0" markdown="1">', '']


def render_region(data, key, output, ledger, site_mode=True):
    count = data['top_n']; definition = data['definitions']['regions'][key]; label = definition['label']
    ranking = data['rankings'][key]
    lookup = {(r['key'], r['repository_year']): r for r in data['samples']}
    top = [lookup[(r['key'], r['repository_year'])] for r in ranking[:count]]
    title = f'Top {count} media objects by {label} share'
    lines = front(title)
    if site_mode:
        lines += [f'[Region Top {count}](region-top.html)', '']
    lines += [f'Calculated **{data["calculation_date"]}**; table rendered **{data["render_date"]}**.', '',
              f'Ranked **{len(ranking):,} distinct media objects** from the 2017–2026 annual repositories by their cumulative **{label}** downloader share. '
              f'The top {count} sample windows span **{min(r["sample_days"] for r in top)}–{max(r["sample_days"] for r in top)} days**. '
              'Weights describe repeated observed swarm participation, not unique people or completed views.', '']
    lines += table_start(title)
    lines += [f'| Rank | Media object | Sample window | Days | {label} % | {label} downloader weight | Worldwide downloader weight |',
              '| ---: | --- | --- | ---: | ---: | ---: | ---: |']
    for rank, row in enumerate(top, 1):
        name = row['name'] + (' · ' + str(row['collection_id']) if row['collection_id'] else '')
        name = name.replace('|', '\\|')
        weight = regional(row, definition)
        lines.append(f'| {rank} | [{name}]({row["audit_url"]})<br>`{row["key"]}` | {row["start"]} to {row["end"]} | {row["sample_days"]:,} | '
                     f'**{percentage(weight, row["world"]["downloaders"])}** | {weight:,} | {row["world"]["downloaders"]:,} |')
    lines += ['', '</div>', '', '## Definition and method', '',
              f'`{label} % = 100 × {label} cumulative downloader weight / worldwide cumulative downloader weight`.', '',
              f'- **Membership:** {definition["note"]} [Definition source]({definition["source"]["url"]}). Codes: '
              + ', '.join('`' + c + '`' for c in definition['country_codes']) + '.',
              '- **Matching numerator and denominator:** sum `downloaders.size` over the same top-level features in each '
              '`*-cumulative-aggregate.geojson.gz`. The worldwide denominator retains all country codes, including unclassified locations. '
              'Weekly products, nested by-BTIH features and companion cumulative JSON totals are not added to this denominator.',
              '- **Published geography:** H3 resolution 5, minimum swarm size 3; hosting and other network classes remain included. '
              'A common within-object ITU multiplier cancels in the percentage.',
              '- **Scope:** every eligible annual media object, without a contributor-identity, production-country or minimum-volume filter. '
              'Distinct collection keys, including episodes and episode groups, remain separate objects.',
              '- **Order:** exact regional/worldwide fractions descending, then worldwide downloader weight descending, then collection key ascending. '
              'Rounding is for display only. Zero regional weight is valid; zero worldwide downloader denominators are excluded.',
              '- **Comparability:** full available sample windows, inventories, media scopes and geolocation versions differ. '
              'Read the ranking as geographic concentration within each observed sample.', '', '## Coverage and repeated keys', '',
              f'**{len(data["samples"]):,} annual samples**, **{len(data["selected_samples"]):,} retained media objects**, '
              f'**{len(data["excluded_zero_denominator"])}** retained objects excluded for zero worldwide downloader weight. '
              'Cumulative JSON, aggregate GeoJSON and audit inventories match. For a repeated key, retain the latest end date, '
              'then latest start date, then repository year. Samples are not pooled.', '']
    for duplicate in data['duplicates']:
        keep = duplicate['retained']
        old = '; '.join(f'{r["repository_year"]} ({r["start"]} to {r["end"]})' for r in duplicate['discarded'])
        lines.append(f'- `{duplicate["key"]}`: retain {keep["repository_year"]} ({keep["start"]} to {keep["end"]}); supersede {old}.')
    lines += [''] + table_start('Annual source coverage')
    lines += ['| Repository year | Annual samples | Pinned source revision |', '| --- | ---: | --- |']
    for year, commit in sorted(data['repositories'].items()):
        total = sum(r['repository_year'] == int(year) for r in data['samples'])
        lines.append(f'| {year} | {total} | [{commit[:10]}](https://github.com/alpha60-devops/alpha60-results-{year}/tree/{commit}) |')
    relative = Path(os.path.relpath(ledger, output.parent)).as_posix()
    root = output.parent.parent
    ledger_argument = Path(os.path.relpath(ledger, root)).as_posix()
    output_argument = Path(os.path.relpath(output, root)).as_posix()
    command = ['python3 resources/rank-geographic-share.py \\',
               f'  --from-ledger {ledger_argument} \\']
    command += ['  --site . \\'] if site_mode else [
        f'  --region {key} \\', f'  --output {output_argument} \\',
        f'  --ledger {ledger_argument} \\']
    command += [f'  --top {count}']
    lines += ['', '</div>', '', '## Evidence and reproduction', '',
              f'The [shared JSON ledger]({relative}) contains all four complete rankings, all annual country/world totals for both roles, '
              'sample-selection decisions, definitions, source revisions and SHA-256 hashes. '
              '[Resolved region definitions](../data/region-ranking-definitions.json) and '
              '[the generator](../resources/rank-geographic-share.py) are available separately.', '',
              'Render a different N from the same complete ledger:', '', '```bash',
              *command, '```', '',
              'Recalculate from committed annual checkouts with `--source-root /path/to/checkouts --site .` '
              f'and `--top {count}`. Table length does not change the underlying rankings.', '', '</div>', '']
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text('\n'.join(lines))


def render_site(data, site):
    ledger = site / 'data/region-rankings.json.gz'
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_bytes(gzip.compress(dump(data), mtime=0))
    definitions = {**data['definitions'], 'definition_sha256': data['definition_sha256'],
                   'calculation_generator': data['calculation_generator']}
    (site / 'data/region-ranking-definitions.json').write_bytes(dump(definitions))
    count = data['top_n']
    manifest = {'schema_version': 1, 'top_n': count, 'calculation_date': data['calculation_date'],
                'render_date': data['render_date'], 'eligible_objects': len(data['rankings']['asia-28']),
                'ledger': 'data/region-rankings.json.gz', 'ledger_sha256': sha(ledger.read_bytes()),
                'regions': [{'id': key, 'label': data['definitions']['regions'][key]['label'],
                             'path': f'docs/region-top-{key}.html'} for key in REGIONS]}
    (site / '_data').mkdir(exist_ok=True)
    (site / '_data/region_rankings.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    for key in REGIONS:
        render_region(data, key, site / f'docs/region-top-{key}.md', ledger)
    lines = front(f'Region Top {count}')
    lines += [f'Top **{count}** media objects per region, ranked by the percentage of each object’s cumulative worldwide '
              f'downloader weight located in that region. The shared inventory covers **{len(data["samples"]):,} annual samples** '
              f'and **{manifest["eligible_objects"]:,} eligible distinct media objects** from **2017–2026**.', '',
              '{% for region in site.data.region_rankings.regions %}',
              '- [{{ region.label }}](../{{ region.path }})', '{% endfor %}', '',
              '## Reading the rankings', '',
              'Each regional page shows the sample dates and duration, regional percentage, regional weight and matching worldwide weight. '
              'Media-object links open the selected annual audit pages. These rankings cover all eligible media objects; they are independent '
              'of the contributor-identity group sites.', '',
              'The regions share the same retained sample per collection key and the same worldwide denominator. '
              'Full sample windows and media scopes differ, so the percentages describe geographic concentration rather than '
              'a comparison of audience sizes. Repeated keys use the latest sample end date, then start date, then repository year.', '',
              'EUR-27 uses the fixed 27 current EU member-country ISO-3 codes for every sample year. '
              '[Membership source](https://european-union.europa.eu/easy-read_en). '
              'USA + CAN uses exactly those two country codes. See each table for its complete definition.', '',
              f'Calculated **{data["calculation_date"]}**; rendered **{data["render_date"]}**.', '',
              '[Complete ranking ledger](../data/region-rankings.json.gz) · '
              '[Region definitions](../data/region-ranking-definitions.json) · '
              '[Generator and Top N option](../resources/rank-geographic-share.py)', '', '</div>', '']
    (site / 'docs/region-top.md').write_text('\n'.join(lines))
    index = site / 'index.md'
    text = index.read_text()
    nav = '- [Region Top {{ site.data.region_rankings.top_n }}](docs/region-top.html)\n\n'
    if nav not in text:
        if len(re.findall(r'^- Year$', text, re.M)) != 1:
            raise ValueError('Expected one top-level Year entry in index.md')
        text = text.replace('- Year\n', nav + '- Year\n', 1)
        index.write_text(text)
    resources = site / 'resources'; resources.mkdir(exist_ok=True)
    (resources / 'region-rankings.css').write_text(CSS)
    source = Path(__file__).resolve(); target = resources / source.name
    if source != target.resolve():
        shutil.copyfile(source, target)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--source-root', type=Path)
    source.add_argument('--from-ledger', type=Path)
    parser.add_argument('--site', type=Path, help='Generate the hub, all four tables and navigation manifest')
    parser.add_argument('--region', choices=REGIONS, help='Legacy single-region output mode')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--ledger', type=Path)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--top', type=int, default=DEFAULT_TOP_N)
    args = parser.parse_args(argv)
    if args.top < 1 or args.workers < 1:
        parser.error('--top and --workers must be positive integers')
    if args.site and any((args.region, args.output, args.ledger)):
        parser.error('--site cannot be combined with legacy --region/--output/--ledger')
    if not args.site and not all((args.region, args.output, args.ledger)):
        parser.error('Specify --site, or all of --region/--output/--ledger')
    data = load_ledger(args.from_ledger) if args.from_ledger else collect(args.source_root.resolve(), args.workers)
    eligible = min(map(len, data['rankings'].values()))
    if args.top > eligible:
        parser.error(f'--top must be at most the eligible object count ({eligible})')
    data = deepcopy(data)
    data.update({'top_n': args.top, 'render_date': date.today().isoformat(),
                 'render_generator': {'filename': Path(__file__).name, 'sha256': sha(Path(__file__).read_bytes())}})
    if args.site:
        render_site(data, args.site.resolve())
    else:
        args.ledger.parent.mkdir(parents=True, exist_ok=True)
        raw = dump(data); args.ledger.write_bytes(gzip.compress(raw, mtime=0) if args.ledger.suffix == '.gz' else raw)
        render_region(data, args.region, args.output, args.ledger, site_mode=False)
        parent = args.output.parent.parent
        (parent / 'data').mkdir(exist_ok=True); (parent / 'resources').mkdir(exist_ok=True)
        (parent / 'data/region-ranking-definitions.json').write_bytes(dump(data['definitions']))
        (parent / 'resources/region-rankings.css').write_text(CSS)
        dest = parent / 'resources' / Path(__file__).name
        if dest.resolve() != Path(__file__).resolve():
            shutil.copyfile(Path(__file__), dest)
    print(f'Wrote Top {args.top}: {eligible} ranked objects from {len(data["samples"])} annual samples.', flush=True)


if __name__ == '__main__':
    main()
