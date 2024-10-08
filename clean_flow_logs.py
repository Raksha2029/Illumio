# -*- coding: utf-8
def print_file_contents(filename):
    """Print the contents of the given file."""
    print(f"Contents of {filename}:")
    with open(filename, 'r') as file:
        for line in file:
            print(line, end='')
    print("\n" + "-" * 50 + "\n")

def clean_flow_logs(input_filename, output_filename):
    # Print contents of the file before cleaning
    print_file_contents(input_filename)

    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            line = line.strip()  # Removing leading/trailing whitespace
            if line and not line.startswith("#"):  # Ignore empty lines and comments
                outfile.write(line + '\n')

    # Print contents of the file after cleaning
    print_file_contents(output_filename)
    print(f"Cleaned flow logs written to {output_filename}")

if __name__ == '__main__':
    clean_flow_logs('flow_logs.txt', 'cleaned_flow_logs.txt')

