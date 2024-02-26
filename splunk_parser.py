import configparser
import re
import argparse
import json
import logging

logging.basicConfig(level=logging.DEBUG)


def preprocess_config(input_file_path, output_file_path):
    """Preprocesses the config file, removing comments, handling multiline values, escaping stray '%', 
    preserves newlines between options, adds a newline before each section header (except the first),
    and writes the result to a new file.
    """

    with open(input_file_path, 'r') as input_file, \
            open(output_file_path, 'w') as output_file:

        in_stanza = False
        processed_lines = []

        for line in input_file:
            stripped_line = line.strip()

            # Early Exit for Empty Lines and Comments
            if not stripped_line or stripped_line.startswith('#'):
                continue

            # Section Headers
            if stripped_line.startswith('['):
                if processed_lines:  # Add a newline if not the first header
                    processed_lines.append('\n')
                in_stanza = True
                processed_lines.append(line)

            # Options within Stanzas
            elif in_stanza:
                if stripped_line.endswith('\\'):
                    processed_lines.append(stripped_line[:-1])
                else:
                    # Preserve original newline within stanzas
                    processed_lines.append(line)

            # Blank lines and Other Lines
            else:
                # Optional: Add newline back if it was originally present
                if stripped_line:
                    processed_lines.append(line)  # Preserve original newline
                else:
                    # Add a newline for blank lines
                    processed_lines.append('\n')

        output_file.write(''.join(processed_lines))
        logging.debug(f"Preprocessed data written to: {output_file_path}")

        # Return the preprocessed content
        return ''.join(processed_lines).replace('%', '%%')


def parse_savedsearches(config_content):
    """Parses the preprocessed config content."""
    saved_searches = {}
    config = configparser.ConfigParser()
    logging.debug(f"Reading {config_content}")
    config.read_string(config_content)

    for section in config.sections():
        logging.debug(f"Parsing {section}")
        saved_searches[section] = {}
        for key, value in config.items(section):
            # Handle escaped newlines
            value = re.sub(r"\\n", "\n", value)
            saved_searches[section][key] = value

    logging.debug(f"Parsed dictionary:\n{saved_searches}")
    return saved_searches


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse a Splunk savedsearches.conf file")
    # Renamed argument
    parser.add_argument(
        "input_file", help="Path to the savedsearches.conf file")
    parser.add_argument(
        "-o", "--output", help="Output file for preprocessed data")
    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        raw_config = file.read()

    preprocessed_config = preprocess_config(
        args.input_file, args.output)  # Pass both input and output
    result = parse_savedsearches(preprocessed_config)

    if args.output:
        # If you want to output the parsed result as well, modify this section
        with open(args.output + "_parsed.json", 'w') as outfile:  # Add suffix to parsed output
            json.dump(result, outfile, indent=4)
        logging.debug(f"Parsed data written to: {args.output}_parsed.json")
