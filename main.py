import re


def read_system():
    system = []
    while True:
        equation = input()
        if equation != "":
            system.append(equation)
        else:
            break
        print("Introduceti alta ecuatie sau Enter pentru a opri")
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
        results.append(
            int(parts[1]) if float(parts[1]).is_integer() else float(parts[1]))  # Store the constant term as a float

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

            if not coef_part:
                coef = int(sign + '1')
            elif float(coef_part).is_integer():
                coef = int(sign + coef_part)
            else:
                coef = float(sign + coef_part)

            if coef != 0:
                # Add variable to the list if not already present
                if var not in vars:
                    vars.append(var)

                # Store the coefficient in the dictionary
                pr_mtr[(i, var)] = coef

    vars.sort()

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


def switch_cols(matrix, current_index, vars):
    n = len(matrix)
    m = len(matrix[0]) - 1
    index = current_index
    row = current_index
    # Check if the current row is the last row
    while matrix[row][index] == 0:
        if index + 1 >= m:
            return False # Cannot swap, no collum to the right
        # Swap the current collum with the collum to the right
        index += 1

    # Interchange the collums
    for row in range(n):
        matrix[row][current_index], matrix[row][index] = matrix[row][index], matrix[row][current_index]

    # Interchange the variables
    vars[current_index], vars[index] = vars[index], vars[current_index]

    return matrix


def switch_rows(matrix, current_index):
    n = len(matrix)
    index = current_index
    col = current_index
    # Check if the current row is the last row
    while matrix[index][col] == 0:
        if index + 1 >= n:
            return False  # Cannot swap, no row below
        # Swap the current row with the row below
        index += 1

    # Interchange the rows
    matrix[current_index], matrix[index] = matrix[index], matrix[current_index]
    return True


def gauss(matrix,vars):
    n = len(matrix)

    for index in range(n):
        pivot = matrix[index][index]

        if pivot == 0:
            # Attempt to swap rows
            if not switch_rows(matrix, index):
                # Handle the case where swapping rows is not possible
                if not switch_cols(matrix, index, vars):
                    print("Sistemul este imcompatibil")
                    break
            for row in matrix:
                print(row)
            print(vars, "\n")
        else:
            #copiere linie pivot
            #coloana pivot inlocuit cu 0
            #regula dreptunghiului
            pass

    return matrix


def main():
    print("Introduceti ecuatiile sistemului: ")
    # system = read_system()
    system = [
        "3z = 5",
        "2*x+0.1y -5z = 5",
        "5x-0y+7z = 5"
    ]
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

    # modify_rows(matrix, 0)
    print()
    gauss(matrix,vars)


main()