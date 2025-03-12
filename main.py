import re

def read_system():
    system = []
    while True:
        equation = input()
        if equation != "0":
            system.append(equation)
        else:
            break
        print("Introduceti alta ecuatie sau 0 pentru a opri")
    return system

def display_system(system):
    for i in range(0, len(system)):
        print(f"{{{system[i]}")

def parse_equations(inp):
    vars = []  # List to store all unique variables
    pr_mtr = {}  # Dictionary to store coefficients
    results = []  # List to store the constant terms

    for i, formula in enumerate(inp):
        # Remove all spaces and split into left and right parts
        formula = formula.replace(" ", "")
        parts = formula.split("=")
        results.append(int(parts[1]) if float(parts[1]).is_integer() else float(parts[1]))  # Store the constant term as a float

        # Split the left-hand side into terms
        terms = re.findall(r'([+-]?\d*\.?\d*\*?[a-zA-Z]+\d*)', parts[0])

        for term in terms:
            # Handle the sign
            if term.startswith('+') or term.startswith('-'):
                sign = term[0]
                term = term[1:]
            else:
                sign = '+'

            # Split into coefficient and variable
            if '*' in term:
                # Explicit form (e.g., "2*x1" or "0.5*x2")
                coef_part, var = term.split('*')
            else:
                # Implicit form (e.g., "2x1" or "-x2")
                coef_part = re.match(r'(\d*\.?\d*)', term).group(1)
                var = term[len(coef_part):]

            # Handle implicit coefficient (e.g., "x1" -> coefficient is 1)
            if not coef_part:
                coef = int(sign + '1')
            elif float(coef_part).is_integer():
                coef = int(sign + coef_part)
            else:
                coef = float(sign + coef_part)

            # Add variable to the list if not already present
            if var not in vars:
                vars.append(var)

            # Store the coefficient in the dictionary
            pr_mtr[(i, var)] = coef

    return vars, pr_mtr, results

def build_matrix(vars, pr_mtr, results, num_equations):
    # Initialize the matrix with zeros
    matrix = [[0 for _ in range(len(vars) + 1)] for _ in range(num_equations)]

    # Fill the matrix with coefficients and constants
    for i in range(num_equations):
        for j, var in enumerate(vars):
            matrix[i][j] = pr_mtr.get((i, var), 0)
        matrix[i][-1] = results[i]

    return matrix

def main():
    print("Introduceti ecuatiile sistemului: ")
    system = read_system()
    print("Ecuatiile introduse sunt:")
    display_system(system)

    # Parse the equations
    vars, pr_matrix, results = parse_equations(system)

    # Build the matrix
    num_equations = len(system)
    matrix = build_matrix(vars, pr_matrix, results, num_equations)

    # Display the matrix
    print("Variabilele:", vars)
    print("Matricea:")
    for row in matrix:
        print(row)

main()