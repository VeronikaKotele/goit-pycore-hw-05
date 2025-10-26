import sys
from collections import Counter
from datetime import datetime
from typing import Iterator

def load_logs_generator(file_path: str) -> Iterator[str]: #instead of load_logs because storing all logs in memory is inefficient
    try:
        with open(file_path, 'r') as log_file:
            for line in log_file:
                yield line.strip()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

"""Parse logs in format %Y-%m-%d %H:%M:%S level message."""
def parse_log_line(line: str) -> dict:
    log_levels = {'INFO', 'ERROR', 'DEBUG', 'WARNING'}
    parts = line.split(' ', 4)
    log_entry = {}
    log_entry['timestamp'] = datetime.strptime(parts[0] + ' ' + parts[1], "%Y-%m-%d %H:%M:%S")
    log_entry['level'] = next((level for level in log_levels if level in parts[2]), 'UNKNOWN')
    log_entry['message'] = parts[3].strip() if len(parts) > 3 else ''
    return log_entry

def display_log_counts(counts: dict):
    print(f"{'Рівень логування':<17} | {'Кількість':<8}")
    print("-" * 18 + "|" + "-" * 9)
    for level, count in counts.items():
        print(f"{level:<17} | {count:<8}")

def parse_logs(file_path, filter_level=None):
    level_counts = Counter()
    filtered_logs = []

    for line in load_logs_generator(file_path):
        log = parse_log_line(line)
        level = log['level']
        level_counts[level] += 1 #instead of count_logs_by_level(logs: list) -> dict because we dont's store all logs in memory
        if (filter_level and level == filter_level): #instead of filter_logs_by_level(logs: list, level: str) -> list because we dont's store all logs in memory
            filtered_logs.append(line)

    display_log_counts(level_counts)

    if filter_level:
        print(f"\nДеталі логів для рівня '{filter_level}':")
        for log in filtered_logs:
            print(log)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_logs.py <log_file_path> [log_level]")
        sys.exit(1)

    log_file_path = sys.argv[1]
    log_level = sys.argv[2].upper() if len(sys.argv) > 2 else None

    parse_logs(log_file_path, log_level)