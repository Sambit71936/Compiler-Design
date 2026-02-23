def run_intermediate():
    import re

    print("\n--- PHASE 4: INTERMEDIATE CODE ---\n")

    temp = 1
    line = input("Enter the expression: ")

    line = line.strip()
    if "+" in line:
        lhs, rhs = line.split("=")
        a, b = rhs.split("+")
        print(f"t{temp} = {a.strip()} + {b.strip()}")
        print(f"{lhs.strip()} = t{temp}")
    elif "=" in line:
        print(line)


if __name__ == "__main__":
    run_intermediate()
