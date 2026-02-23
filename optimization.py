def run_optimization():
    print("\n--- PHASE 5: CODE OPTIMIZATION ---\n")
    print("Enter statements one by one.")
    print("Type 'exit' to stop.\n")

    lines = []

    while True:
        line = input(">> ")
        if line.lower() == "exit":
            break
        lines.append(line.strip())

    print("\nOptimized Code:\n")
    for line in lines:
        print(line)


if __name__ == "__main__":
    run_optimization()
