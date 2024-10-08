# -*- coding: utf-8 -*-
# Create an abstract base class for processing and generating reports.

from abc import ABC, abstractmethod
import csv
from collections import defaultdict

class AbstractLogProcessor(ABC):
    @abstractmethod
    def read_log(self, filename):
        pass

    @abstractmethod
    def process_log(self):
        pass

    @abstractmethod
    def generate_reports(self):
        pass

# Implement Concrete Classes that adhere to the abstract base class

class FlowLogProcessor(AbstractLogProcessor):
    def __init__(self, log_filename, lookup_table):
        self.log_filename = log_filename
        self.lookup_table = lookup_table
        self.tag_counts = defaultdict(int)
        self.port_protocol_counts = defaultdict(int)

    def read_log(self, filename):
        with open(filename, 'r') as file:
            self.lines = file.readlines()

    def process_log(self):
        for line in self.lines:
            fields = line.split()
            if len(fields) < 8:
                print(f"Skipping malformed line: {line}")
                continue

            try:
                dst_port = int(fields[5].strip())
                protocol = fields[7].strip()
                protocol = 'tcp' if protocol == '6' else 'udp' if protocol == '17' else protocol.lower()

                tag = self.lookup_table.get((dst_port, protocol), 'Untagged')
                self.tag_counts[tag] += 1
                self.port_protocol_counts[(dst_port, protocol)] += 1
            except ValueError as e:
                print(f"Skipping invalid line: {line}, Error: {e}")

    def generate_reports(self):
        self.write_tag_counts('TagCounts.csv')
        self.write_port_protocol_counts('PortProtocolCombinationCounts.csv')

    def write_tag_counts(self, output_filename):
        with open(output_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Tag", "Count"])
            for tag, count in self.tag_counts.items():
                writer.writerow([tag, count])
        print(f"Tag counts written to {output_filename}")

    def write_port_protocol_counts(self, output_filename):
        with open(output_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Port", "Protocol", "Count"])
            for (port, protocol), count in self.port_protocol_counts.items():
                writer.writerow([port, protocol, count])
        print(f"Port/protocol combination counts written to {output_filename}")

class LookupTableReader:
    @staticmethod
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
                    print(f"Skipping invalid row: {row}, Error: {e}")
        return lookup


# main function

def main():
    lookup_table_file = 'lookup_table.csv'
    flow_log_file = 'cleaned_flow_logs.txt'

    # Read the lookup table
    lookup_table = LookupTableReader.read_lookup_table(lookup_table_file)

    # Create and process the flow log
    processor = FlowLogProcessor(flow_log_file, lookup_table)
    processor.read_log(flow_log_file)
    processor.process_log()
    processor.generate_reports()

if __name__ == '__main__':
    main()

