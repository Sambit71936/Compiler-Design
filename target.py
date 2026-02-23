def run_targe():
    print("\n--- PHASE 6: TARGET CODE ---\n")

    print("Enter statements one by one.")
    print("Type 'exit' to stop.\n")

    lines = []
    while True:
        line = input(">> ").strip()
        if line.lower() == "exit":
            break
        if line:
            lines.append(line)

    for line in lines:
        if "=" in line:
            lhs, rhs = line.split("=")
            print("LOAD", rhs.strip())
            print("STORE", lhs.strip())


if __name__ == "__main__":
    run_targe()
