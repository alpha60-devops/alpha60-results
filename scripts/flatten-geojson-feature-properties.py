#!/usr/bin/env python

import json
import sys
import os

def flatten_geojson(input_path):
    # Determine output filename based on input
    file_root, file_ext = os.path.splitext(input_path)
    output_path = f"{file_root}_flattened{file_ext}"

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Process each feature in the collection
        for feature in data.get('features', []):
            props = feature.get('properties', {})

            # Process 'downloaders' string into individual dl_ properties
            if 'downloaders' in props and isinstance(props['downloaders'], str):
                try:
                    dl_obj = json.loads(props['downloaders'])
                    for key, value in dl_obj.items():
                        props[f'dl_{key}'] = value
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse downloaders string for feature in {props.get('city', 'Unknown')}")

            # Process 'uploaders' string into individual ul_ properties
            if 'uploaders' in props and isinstance(props['uploaders'], str):
                try:
                    ul_obj = json.loads(props['uploaders'])
                    for key, value in ul_obj.items():
                        props[f'ul_{key}'] = value
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse uploaders string for feature in {props.get('city', 'Unknown')}")

        # Save the updated GeoJSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"Successfully created: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename.geojson>")
    else:
        flatten_geojson(sys.argv[1])
