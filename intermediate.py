def run_intermediate():
    import re

    print("\n--- PHASE 4: INTERMEDIATE CODE ---\n")

    temp = 1
    with open("input.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if "+" in line:
            lhs, rhs = line.split("=")
            a, b = rhs.split("+")
            print(f"t{temp} = {a.strip()} + {b.strip()}")
            print(f"{lhs.strip()} = t{temp}")
            temp += 1
        elif "=" in line:
            print(line)
