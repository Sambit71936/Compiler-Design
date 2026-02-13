def run_optimization():
    print("\n--- PHASE 5: CODE OPTIMIZATION ---\n")

    with open("input.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        print(line.strip())
