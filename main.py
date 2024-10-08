import csv
from collections import defaultdict

# Function to read the lookup table from a CSV file
def read_lookup_table(filename):
    lookup = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                port = int(row['dstport'])
                protocol = row['protocol'].lower()
                tag = row['tag']
                lookup[(port, protocol)] = tag
            except (ValueError, KeyError) as e:
                print(f"Skipping invalid row in lookup table: {row}, Error: {e}")
    return lookup

# Function to process flow logs and apply tags based on the lookup table
def process_flow_logs(log_filename, lookup_table):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)

    with open(log_filename, 'r') as file:
        for line in file:
            fields = line.split()
            if len(fields) < 8:
                print(f"Skipping malformed line in flow log: {line}")
                continue

            try:
                dst_port = int(fields[5].strip())
                protocol = fields[7].strip()
                protocol = 'tcp' if protocol == '6' else 'udp' if protocol == '17' else protocol.lower()

                tag = lookup_table.get((dst_port, protocol), 'Untagged')
                tag_counts[tag] += 1
                port_protocol_counts[(dst_port, protocol)] += 1
            except ValueError as e:
                print(f"Skipping invalid line in flow log: {line}, Error: {e}")

    return tag_counts, port_protocol_counts

# Function to write the tag counts to a CSV file
def write_tag_counts(tag_counts, output_filename):
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tag", "Count"])
        for tag, count in tag_counts.items():
            writer.writerow([tag, count])
    print(f"Tag counts written to {output_filename}")

# Function to write the port/protocol combination counts to a CSV file
def write_port_protocol_counts(port_protocol_counts, output_filename):
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Port", "Protocol", "Count"])
        for (port, protocol), count in port_protocol_counts.items():
            writer.writerow([port, protocol, count])
    print(f"Port/protocol combination counts written to {output_filename}")

# Function to print the contents of a file
def print_file_contents(filename):
    """Print the contents of the given file."""
    print(f"Contents of {filename}:")
    with open(filename, 'r') as file:
        for line in file:
            print(line, end='')
    print("\n" + "-" * 50 + "\n")

# Main function
def main():
    lookup_table_file = 'lookup_table.csv'
    flow_log_file = 'cleaned_flow_logs.txt'
    tag_counts_output_file = 'TagCounts.csv'
    port_protocol_output_file = 'PortProtocolCombinationCounts.csv'

    lookup_table = read_lookup_table(lookup_table_file)

    tag_counts, port_protocol_counts = process_flow_logs(flow_log_file, lookup_table)

    write_tag_counts(tag_counts, tag_counts_output_file)
    write_port_protocol_counts(port_protocol_counts, port_protocol_output_file)

    print_file_contents(tag_counts_output_file)
    print_file_contents(port_protocol_output_file)

if __name__ == '__main__':
    main()

