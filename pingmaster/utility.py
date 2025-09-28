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

def compress_ranges(nums):
    if not nums:
        return ""

    nums = sorted(nums)  # make sure the list is sorted
    ranges = []
    start = prev = nums[0]

    for n in nums[1:]:
        if n == prev + 1:
            # still consecutive
            prev = n
        else:
            # end of a range
            if start == prev:
                ranges.append(f"{start}")
            else:
                ranges.append(f"{start}-{prev}")
            start = prev = n

    # add the last range
    if start == prev:
        ranges.append(f"{start}")
    else:
        ranges.append(f"{start}-{prev}")

    return ranges