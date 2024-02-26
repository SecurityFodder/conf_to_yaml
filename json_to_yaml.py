import json
import yaml
import os

def convert_json_to_yaml(json_file_path, output_directory="usecases"):
    """Converts a JSON file containing saved searches into individual YAML files within a directory.

    Args:
        json_file_path (str): Path to the input JSON file.
        output_directory (str, optional): Name of the output directory. Defaults to "usecases".
    """

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for section_name, section_data in data.items():
        file_path = os.path.join(output_directory, f"{section_name}.yaml")
        with open(file_path, 'w') as outfile:
            yaml.dump(section_data, outfile)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert JSON saved searches to individual YAML files.")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("-o", "--output_dir", help="Optional output directory (default: usecases)")
    args = parser.parse_args()

    convert_json_to_yaml(args.input_file, args.output_dir)
