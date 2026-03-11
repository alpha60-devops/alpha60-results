import sys
import os
import json
import glob

def generate_html_list(input_dir):
    # Keep track of where the script was run so we save output.txt there
    original_dir = os.getcwd()
    output_file = os.path.join(original_dir, "output.txt")

    # 1. cd into directory
    try:
        os.chdir(input_dir)
    except FileNotFoundError:
        print(f"Error: Directory '{input_dir}' not found.")
        sys.exit(1)

    # 2. set molist to output from '*cumulative.json'
    molist = []
    json_files = glob.glob('*cumulative.json')
    
    if not json_files:
        print(f"Error: No *cumulative.json files found in {input_dir}")
        sys.exit(1)

    for file in json_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Extract '.collection_key' safely
                if 'collection_key' in data:
                    molist.append(str(data['collection_key']))
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON in {file}. Skipping.")

    # 3, 4, 5. Write to the return file
    with open(output_file, 'w', encoding='utf-8') as out_f:
        # 3. insert "<ul>" to return file
        out_f.write("<ul>\n")
        
        # 4. for each member of molist, add "<li>" + molist item + "</li>"
        for item in molist:
            if item.strip():  # Skip entirely blank keys
                out_f.write(f"  <li>{item}</li>\n")
        
        # 5. insert "</ul>" to return file
        out_f.write("</ul>\n")

    # 6. return file
    return output_file

if __name__ == "__main__":
    # Ensure the user passed exactly one argument (the script name counts as arg 0)
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <input_directory>")
        sys.exit(1)
        
    target_directory = sys.argv[1]
    result_file_path = generate_html_list(target_directory)
    print(f"Success! File generated at: {result_file_path}")
    
