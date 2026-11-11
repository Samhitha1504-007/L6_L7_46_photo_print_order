import math


def parse_order(text):
    """Parse 'size:copies' (e.g. '4x6:25'). Returns (SIZE, copies) or None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    size, copies = parts[0].strip(), parts[1].strip()
    if not size:
        return None
    try:
        copies = int(copies)
    except ValueError:
        return None
    if copies < 0:
        return None
    return size.upper(), copies


def file_size_average(sizes_csv):
    """Average of comma-separated file sizes in MB. Returns an int or None if invalid."""
    if not isinstance(sizes_csv, str) or not sizes_csv.strip():
        return None
    values = []
    for r in sizes_csv.split(','):
        r = r.strip()
        if not r:
            return None
        try:
            value = int(r)
        except ValueError:
            return None
        if value < 0:
            return None
        values.append(value)
    return sum(values) // len(values)


def payable_amount(text):
    """Amount with 18% GST minus discount, from 'amount|discount'. Returns a float or None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    try:
        amount = float(parts[0])
        discount = float(parts[1])
    except ValueError:
        return None
    if not (math.isfinite(amount) and math.isfinite(discount)):
        return None
    if amount < 0 or discount < 0:
        return None
    total = amount * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(round(total, 2), 0)


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter print size:copies (e.g. 4x6:25): ")
    result = parse_order(user_input)
    print("Size and Copies:", result if result is not None else "Invalid input")

    print("\n==== Running file_size_average ====")
    user_input = input("Enter file sizes in MB as CSV (e.g. 4,8,12): ")
    result = file_size_average(user_input)
    print("Average File Size:", result if result is not None else "Invalid input")

    print("\n==== Running payable_amount ====")
    user_input = input("Enter amount|discount (e.g. 450|50): ")
    result = payable_amount(user_input)
    print("Payable Amount:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
