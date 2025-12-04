import argparse
from itertools import groupby

DIVIDER_SYMBOL = "="
DIVIDER_COUNT = 15

class CustomAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if isinstance(values, list):
            values = []
            for v in values:
                print(v)
                values += parse_ports(v)

        setattr(namespace, self.dest, values)

def create_result(name, ports):
    print(DIVIDER_SYMBOL * DIVIDER_COUNT)
    print("TEST:", name)
    print(DIVIDER_SYMBOL * DIVIDER_COUNT)
    print("Ports succeeded:")
    for port in ports:
        print(f"    {port}")
    print()

def create_result_single(name, b):
    print(DIVIDER_SYMBOL * DIVIDER_COUNT)
    print("TEST:", name)
    print(DIVIDER_SYMBOL * DIVIDER_COUNT)
    print("Succes:", b)
    print()

def create_result_for_icmp(name, types):
    print(DIVIDER_SYMBOL * DIVIDER_COUNT)
    print("TEST:", name)
    print(DIVIDER_SYMBOL * DIVIDER_COUNT)
    print("Types succeeded:")
    for type in types:
        print(f"    {type}")
    print()

def compress_ranges(nums):
    if not nums:
        return []
    nums = sorted(set(nums))  # sort and deduplicate
    ranges = []
    for _, group in groupby(enumerate(nums), lambda x: x[0] - x[1]):
        group = [g[1] for g in group]
        if len(group) == 1:
            ranges.append(str(group[0]))
        else:
            ranges.append(f"{group[0]}-{group[-1]}")
    return ranges

def parse_ports(value: str):
    """
    Parse single port or range (e.g., '80' or '1200-1300').
    Returns a list of ints.
    """
    if "-" in value:
        start, end = value.split("-", 1)
        start, end = int(start), int(end)
        if start > end:
            raise argparse.ArgumentTypeError(f"Invalid range: {value}")
        return list(range(start, end + 1))
    else:
        port = int(value)
        return [port]