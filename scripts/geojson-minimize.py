#!/usr/bin/env python

import json
import os
import sys
import argparse

def minify_geojson(input_filepath):
    """Reads a GeoJSON file and writes a minified version."""
    
    if not os.path.exists(input_filepath):
        print(f"Error: The file '{input_filepath}' does not exist.")
        sys.exit(1)

    # Automatically generate the output filename (e.g., map.geojson -> map.min.geojson)
    base_name, ext = os.path.splitext(input_filepath)
    output_filepath = f"{base_name}.min{ext}"

    try:
        # Read the original GeoJSON data
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            geojson_data = json.load(infile)

        # Write the data back out with stripped whitespace
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            json.dump(geojson_data, outfile, separators=(',', ':'))
            
        print(f"Success! Minified GeoJSON saved to: '{output_filepath}'")

    except json.JSONDecodeError:
        print("Error: The input file is not a valid JSON/GeoJSON file.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Set up argparse to handle the command-line argument
    parser = argparse.ArgumentParser(description="Strip whitespace from a GeoJSON file to minify it.")
    parser.add_argument("input_file", help="Path to the GeoJSON file you want to minify")
    
    args = parser.parse_args()
    
    minify_geojson(args.input_file)
    
