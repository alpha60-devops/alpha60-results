#!/usr/bin/env python

import json
import sys
import os

def flatten_file(input_path):
    """Flattens downloader and uploader strings for a single GeoJSON file."""
    # Determine output filename (e.g., input_flattened.geojson)
    file_root, file_ext = os.path.splitext(input_path)
    if file_ext.lower() not in ['.geojson', '.json']:
        return # Skip non-geojson files
        
    output_path = f"{file_root}_flattened{file_ext}"

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'features' not in data:
            print(f"Skipping {input_path}: Not a standard GeoJSON FeatureCollection.")
            return

        for feature in data['features']:
            props = feature.get('properties', {})

            # Flatten 'downloaders' string with "dl_" prefix
            if 'downloaders' in props and isinstance(props['downloaders'], str):
                try:
                    dl_data = json.loads(props['downloaders'])
                    for k, v in dl_data.items():
                        props[f'dl_{k}'] = v
                except json.JSONDecodeError:
                    pass

            # Flatten 'uploaders' string with "ul_" prefix
            if 'uploaders' in props and isinstance(props['uploaders'], str):
                try:
                    ul_data = json.loads(props['uploaders'])
                    for k, v in ul_data.items():
                        props[f'ul_{k}'] = v
                except json.JSONDecodeError:
                    pass

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Processed: {input_path} -> {output_path}")

    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_file_or_directory>")
        sys.exit(1)

    path = sys.argv[1]

    if os.path.isfile(path):
        flatten_file(path)
    elif os.path.isdir(path):
        print(f"Scanning directory: {path}")
        for filename in os.listdir(path):
            if filename.endswith(".geojson"):
                flatten_file(os.path.join(path, filename))
    else:
        print(f"Error: {path} is not a valid file or directory.")

if __name__ == "__main__":
    main()
