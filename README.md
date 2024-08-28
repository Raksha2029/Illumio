# Illumio
Illumio Technical Assessment

# Flow Log Tagging

## Project Overview

This project is designed to parse and analyze flow log data, tagging each log entry based on a lookup table. The tags are determined by the combination of the destination port (`dstport`) and protocol present in the log entries. The program generates two output CSV files:

1. `TagCounts.csv`: This file contains the count of each tag.
2. `PortProtocolCombinationCounts.csv`: This file contains the count of each unique port and protocol combination.

## Assumptions

- **Log Format**: The program supports only the default flow log format, specifically version 2 logs. Any deviation from this format or version is not supported.
- **Log Version**: Only flow logs with version 2 are processed. If another version is encountered, the log entry is skipped.
- **Log Structure**: Each log entry is expected to have the following structure: `version account-id eni-id srcaddr dstaddr srcport dstport protocol packets bytes start-time end-time action log-status`.
- **Lookup Table Format**: The lookup table should be a CSV file with three columns: `dstport`, `protocol`, and `tag`. Protocol values should be provided as strings (e.g., `tcp`, `udp`, `icmp`).
- **Case Insensitivity**: Tagging is case-insensitive, meaning `TCP` and `tcp` are treated as the same.
- **Untagged Logs**: If no match is found for a given `dstport` and protocol combination, the log is tagged as `Untagged`.
- **Output Format**: The output files `TagCounts.csv` and `PortProtocolCombinationCounts.csv` are saved in CSV format.

## File Structure

- `flow_logs.txt`: Input file containing flow log data.
- `lookup_table.csv`: Input file containing the lookup table for tags.
- `cleaned_flow_logs.txt`: Intermediate file storing cleaned flow logs after processing.
- `TagCounts.csv`: Output file containing tag counts.
- `PortProtocolCombinationCounts.csv`: Output file containing port/protocol combination counts.
- `clean_flow_logs.py`: Script to clean the `flow_logs.txt` file.
- `main.py`: Main script to process flow logs and generate the output files.
- `abstract_based_log_processor.py`: Contains the refactored code using Abstract Base Classes (ABCs) and principles to handle log processing, lookup table reading, and report generation.

## Requirements

- Python 3.x

## Setup

### 1. Install Required Dependencies

No external libraries are needed; the project uses Python's built-in modules.

## How to Run the Program

### 1. Clean the Flow Log File
Run the script to clean the 'flow_logs.txt' file.

python 'clean_flow_logs.py'

This script will generate 'cleaned_flow_logs.txt' with cleaned flow log data.

### 2. Process Flow Logs and Generate Outputs

python main.py (or) python abstract_based_log_processor.py

Run the main script to process the cleaned files and generate the output files.

### Output Files

- **TagCounts.csv**: Contains the counts of each tag.
- **PortProtocolCombinationCounts.csv**: Contains the counts of each unique port/protocol combination.

## Tests Conducted

- **Log Format Testing**: The program was tested with various flow log formats. Only version 2 logs with the expected default format were processed successfully. Logs with missing fields or incorrect formats were skipped with appropriate error messages.
- **Tagging Accuracy**: The tagging mechanism was tested to ensure accurate tagging based on the dstport and protocol combinations.
- **Case Insensitivity**: Tagging is case-insensitive, meaning `TCP` and `tcp` are treated as the same.
- **Performance Testing**: The program was tested with large log files (up to 10 MB) to ensure it handles large datasets efficiently.

## Refactored Code Description

This refactored version of the project employs Abstract Base Classes (ABCs) and adheres to SOLID principles to enhance modularity and maintainability.

 - **AbstractLogProcessor** : Defines an abstract base class with methods for reading logs, processing data, and generating reports.
 - **FlowLogProcessor** : Implements the abstract base class to handle flow log processing, including reading log files, applying the lookup table, and generating CSV reports for tag counts and port/protocol combinations.
 - **LookupTableReader**: A utility class to read and parse the lookup table, creating a dictionary for quick tag lookups based on destination port and protocol.

The modular design allows for easy extension and maintenance, following principles like Single Responsibility, Open/Closed, and Dependency Inversion.

## Analysis

- The program efficiently handles large datasets due to its line-by-line processing of flow logs and the use of Python's built-in data structures ('dict' and 'defaultdict'). This makes the code both memory efficient and scalable.
- The decision to separate cleaning and processing into distinct scripts ('clean_flow_logs.py', and 'main.py') improves modularity and maintainability, making it easier to understand, test, and modify each component.
- Error handling is implemented to gracefully skip malformed log lines or invalid lookup table entries, ensuring the program can handle imperfect data without crashing.

## Future Enhancements

- **Support for Custom Log Formats**: Extend the program to handle custom log formats by adding a configuration file or additional command-line options.
- **Version Compatibility**: Add support for different log versions by parsing the version field and applying version-specific processing rules.
- **Enhanced Logging**: Implement a logging mechanism to capture detailed processing information and error messages, aiding in troubleshooting and auditing.
- **Unit Tests**: Develop unit tests for each function to ensure robustness and correctness of the codebase.

## Conclusion

This project provides a robust framework for tagging and analyzing flow log data using a lookup table. It demonstrates how to clean, parse, and process log files efficiently while handling potential data imperfections gracefully. The output files provide valuable insights into network traffic patterns, which can be useful for security analysis, monitoring, and compliance reporting.


