def parse_order(text):
    size, copies = text.split(':')
    return size.strip().upper(), int(copies)

def file_size_average(sizes_csv):
    values = [int(r) for r in sizes_csv.split(',')]
    return sum(values) // len(values)

def payable_amount(text):
    amount, discount = text.split('|')
    total = float(amount) * 1.18 - float(discount)
    return max(total, 0)

def main():
    print("==== Running parse_order ====")
    user_input = input("Enter print size:copies (e.g. 4x6:25): ")
    result = parse_order(user_input)
    print("Size and Copies:", result)

    print("\n==== Running file_size_average ====")
    user_input = input("Enter file sizes in MB as CSV (e.g. 4,8,12): ")
    result = file_size_average(user_input)
    print("Average File Size:", result)

    print("\n==== Running payable_amount ====")
    user_input = input("Enter amount|discount (e.g. 450|50): ")
    result = payable_amount(user_input)
    print("Payable Amount:", result)

if __name__ == "__main__":
    main()
