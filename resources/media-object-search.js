/* Static annual-audit search. The catalog and fallback are generated together. */
(() => {
  'use strict';

  function normalize(value) {
    return String(value).normalize('NFKD').replace(/\p{M}/gu, '')
      .toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
  }

  function search(records, query) {
    const normalized = normalize(query);
    const terms = normalized.split(' ').filter(Boolean);
    return records.map(record => {
      const key = normalize(record.key);
      const title = normalize(record.title);
      const haystack = `${title} ${key}`;
      const rank = !normalized ? 4 : key === normalized ? 0 : title === normalized ? 1
        : key.startsWith(normalized) || title.startsWith(normalized) ? 2 : 3;
      return {record, rank, matches: terms.every(term => haystack.includes(term))};
    }).filter(row => row.matches).sort((a, b) => a.rank - b.rank
      || b.record.sample_end.localeCompare(a.record.sample_end)
      || b.record.year - a.record.year
      || a.record.title.localeCompare(b.record.title)
      || a.record.key.localeCompare(b.record.key)).map(row => row.record);
  }

  function validateCatalog(catalog) {
    if (catalog?.schema !== 'alpha60-media-object-search/1'
        || !Array.isArray(catalog.records) || !catalog.records.length) {
      throw new Error('Invalid search catalog');
    }
    const urls = new Set();
    for (const row of catalog.records) {
      if (typeof row.title !== 'string' || typeof row.key !== 'string'
          || !/^[a-z0-9][a-z0-9._-]*$/.test(row.key) || !Number.isInteger(row.year)
          || !/^\d{4}-\d{2}-\d{2}$/.test(row.sample_start)
          || !/^\d{4}-\d{2}-\d{2}$/.test(row.sample_end)
          || row.url !== `https://alpha60-devops.github.io/alpha60-results-${row.year}/docs/itemized/${row.key}-sample-cache-audit.html`
          || urls.has(row.url)) {
        throw new Error('Invalid search result');
      }
      urls.add(row.url);
    }
    return catalog.records;
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {normalize, search, validateCatalog};
    return;
  }
  const script = document.currentScript;
  const form = document.getElementById('media-search-form');
  if (!form || !script) return;
  const input = document.getElementById('media-search-query');
  const status = document.getElementById('media-search-status');
  const list = document.getElementById('media-search-results');
  const fallback = document.getElementById('media-search-fallback');
  const more = document.getElementById('media-search-more');
  const catalogUrl = new URL(script.dataset.catalog, document.baseURI);
  let records = [];
  let limit = 50;

  function render() {
    const matches = search(records, input.value);
    const visible = matches.slice(0, limit);
    list.replaceChildren();
    for (const record of visible) {
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.href = record.url;
      link.textContent = `${record.title} — ${record.key}`;
      const detail = document.createElement('span');
      detail.className = 'media-search-detail';
      detail.textContent = `${record.year} results · Sample ${record.sample_start} to ${record.sample_end}`;
      item.append(link, detail);
      list.append(item);
    }
    status.textContent = matches.length
      ? `${matches.length} ${matches.length === 1 ? 'audit' : 'audits'} found. Showing ${visible.length}.`
      : 'No matching media objects. Try fewer words or a collection key.';
    more.hidden = matches.length <= limit;
    more.textContent = `Show ${Math.min(50, matches.length - limit)} more results`;
  }

  fetch(catalogUrl).then(response => {
    if (!response.ok) throw new Error(`Catalog request failed: ${response.status}`);
    return response.json();
  }).then(catalog => {
    records = validateCatalog(catalog);
    input.value = new URL(location.href).searchParams.get('q') || '';
    form.hidden = false;
    list.hidden = false;
    fallback.hidden = true;
    input.addEventListener('input', () => { limit = 50; render(); });
    form.addEventListener('submit', event => {
      event.preventDefault();
      const url = new URL(location.href);
      if (input.value.trim()) url.searchParams.set('q', input.value.trim());
      else url.searchParams.delete('q');
      history.replaceState(null, '', url);
      limit = 50;
      render();
    });
    more.addEventListener('click', () => { limit += 50; render(); });
    render();
  }).catch(() => {
    status.textContent = 'Search could not load. Browse the audit links below.';
    form.hidden = true;
    list.hidden = true;
    more.hidden = true;
    fallback.hidden = false;
  });
})();
