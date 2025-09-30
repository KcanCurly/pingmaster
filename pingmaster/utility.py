from itertools import groupby

DIVIDER_SYMBOL = "="
DIVIDER_COUNT = 15

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
    nums = sorted(set(nums))  # sort and deduplicate
    ranges = []
    for _, group in groupby(enumerate(nums), lambda x: x[0] - x[1]):
        group = [g[1] for g in group]
        if len(group) == 1:
            ranges.append(str(group[0]))
        else:
            ranges.append(f"{group[0]}-{group[-1]}")
    return ranges