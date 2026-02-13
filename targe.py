def run_targe():
    print("\n--- PHASE 6: TARGET CODE ---\n")

    with open("input.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        if "=" in line:
            lhs, rhs = line.split("=")
            print("LOAD", rhs.strip())
            print("STORE", lhs.strip())
