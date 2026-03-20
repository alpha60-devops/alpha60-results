#!/usr/bin/env python3

"""
compare_geojson.py – Compare two GeoJSON Point files by a pivot property.

Usage:
    python compare_geojson.py file_a.geojson file_b.geojson \
        --swarm downloaders \
        --field size \
        --prefix my-run \
        [--geopivot geoname_id | country_code]

Outputs (all GeoJSON FeatureCollections):
    <prefix>-disappeared.geojson   – pivot values only in file_a
    <prefix>-emergent.geojson      – pivot values only in file_b
    <prefix>-intersection.geojson  – pivot values in both; properties carry
                                     delta values (b − a) for every numeric
                                     subfield of --swarm, plus a
                                     <swarm>_<field>_delta convenience key.
"""

import argparse
import json
import sys
from pathlib import Path

# 20260320
# ported gemini initial chat simplified to claude sonnet 4.6


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_geojson(path: str) -> dict:
    """Load a GeoJSON file and return the parsed dict."""
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def parse_swarm_blob(raw) -> dict:
    """
    The downloaders / uploaders property is stored as a JSON *string*
    inside the Feature's properties dict.  Parse it and return a plain
    dict with numeric values (non-numeric values are left as-is).
    """
    if isinstance(raw, str):
        blob = json.loads(raw)
    elif isinstance(raw, dict):
        blob = raw
    else:
        blob = {}
    return {k: (v if not isinstance(v, str) else v) for k, v in blob.items()}


def index_by_pivot(features: list, pivot: str) -> dict:
    """Return {pivot_value: Feature} mapping.  Last-write wins on duplicates."""
    return {str(f["properties"][pivot]): f for f in features}


def compute_delta(blob_a: dict, blob_b: dict) -> dict:
    """
    Return a dict of (b − a) for every key that exists in *both* blobs
    and whose values are both numeric.  Keys that are only in one blob
    are carried through as-is with a suffix indicating which file they
    came from.
    """
    delta = {}
    all_keys = set(blob_a) | set(blob_b)
    for k in sorted(all_keys):
        va = blob_a.get(k)
        vb = blob_b.get(k)
        if va is None:
            delta[f"{k}_b_only"] = vb
        elif vb is None:
            delta[f"{k}_a_only"] = va
        elif isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            delta[k] = vb - va
        else:
            # Non-numeric – keep both sides
            delta[f"{k}_a"] = va
            delta[f"{k}_b"] = vb
    return delta


def is_null_island(feature: dict, pivot: str) -> bool:
    """
    Return True for degenerate features that should be elided:
      geometry.coordinates == [0, 0]  AND  properties.<pivot> == ""
    """
    try:
        coords = feature["geometry"]["coordinates"]
        pval   = feature["properties"].get(pivot, None)
        return coords[0] == 0 and coords[1] == 0 and pval == ""
    except (KeyError, TypeError, IndexError):
        return False


def filter_features(features: list, pivot: str) -> tuple[list, int]:
    """Return (kept, n_elided) after removing null-island features."""
    kept, elided = [], 0
    for f in features:
        if is_null_island(f, pivot):
            elided += 1
        else:
            kept.append(f)
    return kept, elided


def make_feature_collection(features: list, extra_meta: dict | None = None) -> dict:
    """Wrap a list of GeoJSON Features in a FeatureCollection."""
    fc = {
        "type": "FeatureCollection",
        "features": features,
    }
    if extra_meta:
        fc.update(extra_meta)
    return fc


def write_geojson(path: str, fc: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(fc, fh, ensure_ascii=False, indent=2)
    print(f"  wrote {path}  ({len(fc['features'])} features)")


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def build_disappeared(only_in_a: list) -> list:
    """Features that exist only in file_a – pass through unchanged."""
    return list(only_in_a)


def build_emergent(only_in_b: list) -> list:
    """Features that exist only in file_b – pass through unchanged."""
    return list(only_in_b)


def build_intersection(shared_ids: set, index_a: dict, index_b: dict,
                       swarm: str, field: str, pivot: str) -> list:
    """
    For each shared pivot value build a new Feature whose properties are:
        <pivot>, city, country_code  (from either file – they should match)
        <swarm>_delta            dict of (b − a) for every subfield
        <swarm>_<field>_delta    convenience scalar for the requested --field
    """
    features = []
    for pid in sorted(shared_ids):
        feat_a = index_a[pid]
        feat_b = index_b[pid]

        props_a = feat_a["properties"]
        props_b = feat_b["properties"]

        blob_a = parse_swarm_blob(props_a.get(swarm, "{}"))
        blob_b = parse_swarm_blob(props_b.get(swarm, "{}"))

        delta_all = compute_delta(blob_a, blob_b)

        # Scalar convenience value for the requested --field
        va = blob_a.get(field)
        vb = blob_b.get(field)
        if va is not None and vb is not None and \
                isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            field_delta = vb - va
        else:
            field_delta = None

        new_props = {
            pivot:          pid,
            "city":         props_b.get("city") or props_a.get("city"),
            "country_code": props_b.get("country_code") or props_a.get("country_code"),
            # Full per-subfield deltas for both swarm classes
            "downloaders_delta": compute_delta(
                parse_swarm_blob(props_a.get("downloaders", "{}")),
                parse_swarm_blob(props_b.get("downloaders", "{}")),
            ),
            "uploaders_delta": compute_delta(
                parse_swarm_blob(props_a.get("uploaders", "{}")),
                parse_swarm_blob(props_b.get("uploaders", "{}")),
            ),
            # Convenience: delta for the requested --swarm / --field combo
            f"{swarm}_{field}_delta": field_delta,
            # Raw values for reference
            f"{swarm}_{field}_a": va,
            f"{swarm}_{field}_b": vb,
        }

        # Use file_b geometry (more recent); fall back to file_a
        geometry = feat_b.get("geometry") or feat_a.get("geometry")

        features.append({
            "type": "Feature",
            "geometry": geometry,
            "properties": new_props,
        })

    return features


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Compare two GeoJSON Point files by geoname_id and "
                    "produce disappeared / emergent / intersection sets."
    )
    parser.add_argument("file_a", help="Earlier / baseline GeoJSON file")
    parser.add_argument("file_b", help="Later / comparison GeoJSON file")
    parser.add_argument(
        "--swarm",
        required=True,
        choices=["downloaders", "uploaders"],
        help="Primary properties class to evaluate (downloaders or uploaders)",
    )
    parser.add_argument(
        "--field",
        default="size",
        help="Field within the swarm class to use for the scalar delta "
             "(e.g. size, mobile, vpn, …) (default: size)",
    )
    parser.add_argument(
        "--prefix",
        required=True,
        help="Prefix for all output filenames",
    )
    parser.add_argument(
        "--geopivot",
        default="geoname_id",
        choices=["geoname_id", "country_code"],
        help="Feature property to use as the comparison key "
             "(default: geoname_id)",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    print(f"Loading {args.file_a} …")
    data_a = load_geojson(args.file_a)
    print(f"Loading {args.file_b} …")
    data_b = load_geojson(args.file_b)

    feats_a = data_a.get("features", [])
    feats_b = data_b.get("features", [])
    print(f"  file_a: {len(feats_a)} features")
    print(f"  file_b: {len(feats_b)} features")

    index_a = index_by_pivot(feats_a, args.geopivot)
    index_b = index_by_pivot(feats_b, args.geopivot)

    ids_a = set(index_a.keys())
    ids_b = set(index_b.keys())

    only_a   = ids_a - ids_b          # disappeared
    only_b   = ids_b - ids_a          # emergent
    shared   = ids_a & ids_b          # intersection

    print(f"\nSet analysis:")
    print(f"  disappeared  (only in file_a): {len(only_a)}")
    print(f"  emergent     (only in file_b): {len(only_b)}")
    print(f"  intersection (in both):        {len(shared)}")

    # Build outputs
    print(f"\nWriting output files (prefix='{args.prefix}') …")

    disappeared_feats  = build_disappeared([index_a[i] for i in sorted(only_a)])
    emergent_feats     = build_emergent([index_b[i] for i in sorted(only_b)])
    intersection_feats = build_intersection(shared, index_a, index_b,
                                            args.swarm, args.field, args.geopivot)

    # Elide null-island features (coords [0, 0] + empty pivot value)
    disappeared_feats,  n_dis = filter_features(disappeared_feats,  args.geopivot)
    emergent_feats,     n_eme = filter_features(emergent_feats,     args.geopivot)
    intersection_feats, n_int = filter_features(intersection_feats, args.geopivot)
    total_elided = n_dis + n_eme + n_int
    if total_elided:
        print(f"\nElided null-island features: {total_elided} "
              f"(disappeared={n_dis}, emergent={n_eme}, intersection={n_int})")

    # Carry top-level metadata from the source files where useful
    meta = {
        "swarm":    args.swarm,
        "field":    args.field,
        "geopivot": args.geopivot,
        "file_a":   str(args.file_a),
        "file_b":   str(args.file_b),
    }

    write_geojson(
        f"{args.prefix}-disappeared.geojson",
        make_feature_collection(disappeared_feats, meta),
    )
    write_geojson(
        f"{args.prefix}-emergent.geojson",
        make_feature_collection(emergent_feats, meta),
    )
    write_geojson(
        f"{args.prefix}-intersection.geojson",
        make_feature_collection(intersection_feats, meta),
    )

    print("\nDone.")


if __name__ == "__main__":
    main()
