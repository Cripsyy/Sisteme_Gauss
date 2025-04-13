import re
import math
from functools import reduce

system = []
matrix = []
gauss_steps = []
main_vars = []
sec_vars = []
vars_list = []
vars_index = 0
variables_dict = {}
matrix_type = " "

def input_system():
    while True:
        equation = input()
        if equation != "":
            system.append(equation)
        else:
            break
        print("Introduceti alta ecuatie sau Enter pentru a opri")
    return system

def print_system(system):
    for i in range(0, len(system)):
        print(f"{{{system[i]}")

def print_matrix(matrix, vars):
    for row in matrix:
        print(row)
    print(vars, "\n")

def parse_equations(inp):
    vars = []  # List to store all unique variables
    pr_mtr = {}  # Dictionary to store coefficients
    results = []  # List to store the constant terms

    for i, formula in enumerate(inp):
        # Remove all spaces and split into left and right parts
        formula = formula.replace(" ", "").replace("−", "-")  # replace − with - because yes
        parts = formula.split("=")
        results.append(
            int(parts[1]) if float(parts[1]).is_integer() else float(parts[1]))  # Store the constant term as a float

        # Split the left-hand side into terms
        terms = re.findall(r'([+-]?[0-9]*\.?[0-9]*\*?[a-zA-Z]+\d*)', parts[0])

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

            if coef != 0 and var not in vars:
                # Add variable to the list if not already present
                vars.append(var)

            # Store coefficient
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
            return False  # Cannot swap, no colum to the right
        # Swap the current colum with the colum to the right
        index += 1

    # Interchange the colums
    for row in range(n):
        matrix[row][current_index], matrix[row][index] = matrix[row][index], matrix[row][current_index]

    # Interchange the variables
    vars[current_index], vars[index] = vars[index], vars[current_index]
    vars_list.append(vars.copy())

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

def calculate_matrix(matrix, index):
    temp_matrix = [row[:] for row in matrix]
    n = len(temp_matrix)
    m = len(temp_matrix[0])

    # Every value in the matrix that is not on the pivot row or column is calculated with the rectangle method
    for rows in range(n):
        for cols in range(m):
            if rows != index and cols != index:
                temp_matrix[rows][cols] = temp_matrix[rows][cols] * temp_matrix[index][index] - temp_matrix[rows][index] * temp_matrix[index][cols]
    # Pivot column is replaced with zeros
    for j in range(n):
        if j != index:
            temp_matrix[j][index] = 0

    return temp_matrix

def calculate_variables(matrix, vars):
    global matrix_type
    global main_vars
    global sec_vars

    row_simplification(matrix, vars)
    n = len(matrix)
    m = len(matrix[0]) - 1
    variables_dict = {}  # Dictionary to store variables and their values
    GREEK_LETTERS = ["α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ"]
    TYPES = ["simplu", "dublu", "triplu", "cvadruplu", "cvintuplu", "sextuplu", "septuplu", "octuplu", "nonutuplu", "decuplu"]
    sec_index = 0
    pivot_pos= []

    for row in range(n):
        if matrix[row][row] != 0:
            pivot_pos.append(vars[row])

    for row in range(n):
        main_var = None
        cnt = 0
        solution = f"({str(matrix[row][-1])}"  # Start as a string to handle symbolic substitution

        for col in range(row, m):
            cnt += 1
            if matrix[row][col] != 0:
                if vars[col] in pivot_pos and vars[col] not in main_vars and cnt == 1:
                    main_var = vars[col]  # The first variable in the equation is the main one
                    main_vars.append(main_var)
                elif vars[col] not in pivot_pos:
                    # Assign a secondary variable name if not already assigned
                    variables_dict[vars[col]] = GREEK_LETTERS[sec_index]
                    sec_vars.append(vars[col])
                    sec_index += 1

                    # Append the secondary variable term as a string
                    solution += f" +{-1 * matrix[row][col]}{variables_dict[vars[col]]}"
                elif matrix[col][col+1] != 0:
                    solution += f" +{-1 * matrix[row][col]}"

        # Append the main variables
        solution += f") / {matrix[row][row]}"
        variables_dict[main_var] = simplify(solution)

    variables_dict.pop(None, None)
    print(variables_dict)
    keys = list(variables_dict.keys())
    keys.sort()
    variables_dict = {i: variables_dict[i] for i in variables_dict.keys()}

    if sec_index == 0:
        print("Sistemul este compatibil determinat")
        matrix_type = "Sistemul este compatibil determinat"
    else:
        print(f"Sistemul este compatibil {TYPES[sec_index - 1]} nedeterminat")
        matrix_type = f"Sistemul este compatibil {TYPES[sec_index - 1]} nedeterminat"

    print(f"Variabilele principale: {', '.join(main_vars)}")
    if sec_index != 0:
        print(f"Variabilele secundare: {', '.join(sec_vars)}")
    globals()["variables_dict"] = variables_dict
    return variables_dict  # Return the computed variables

def row_simplification(matrix, vars):
    for row in matrix:
        if (all(value.is_integer()) and value in (0, 1) for value in row):
            row_gcd = reduce(math.gcd, map(int, row))
            if row_gcd == 0:
                continue
            for i in range(len(row)):
                row[i] = int(row[i]) // row_gcd

    print_matrix(matrix, vars)
    gauss_steps.append([row[:] for row in matrix])
    return matrix

def simplify(solution):
    negative = False

    left, right = solution.split(" / ")
    if right[0] == "-":
        negative = True
        right = right[1:]

    left = left.strip("()")
    parts = left.split(" ")
    left = ""
    for part in parts:
        if negative:
            part = "-" + part
        sign = 1
        for char in part:
            if char not in "+-":
                break
            if char == "-":
                sign *= -1
        part = part.strip("+-")
        left += (" + " if sign == 1 else " - ") + part
    left = left.strip("+ ")
    if right == "1":
        return left
    elif len(parts) == 1:
        return f"{left} / {right}"
    else:
        return f"({left}) / {right}"

def gauss(matrix, vars):
    global solution
    global matrix_type

    n = len(matrix)
    print("Calculele cu metoda Gauss:")

    for index in range(n):
        pivot = matrix[index][index]

        if pivot == 0:
            # Attempt to swap rows
            if not switch_rows(matrix, index):
                # Handle the case where swapping rows is not possible
                if not switch_cols(matrix, index, vars):
                    if matrix[index][-1] != 0:
                        matrix_type = "Sistemul este incompatibil"
                        print("Sistemul este incompatibil")
                        return
                    break

        matrix = calculate_matrix(matrix, index)
        gauss_steps.append([row[:] for row in matrix])
        print_matrix(matrix, vars)

    variables_dict = calculate_variables(matrix, vars)
    print(f"Solutia sistemului este: {variables_dict}")

    return matrix

def main():
    global matrix
    print("Introduceti ecuatiile sistemului: ")
    # system = input_system()
    system = [
        # "x+y+z=3",
        # "2x-y+3z=4",
        # "3x+2y-z=4"

        "-x3+4x4=2",
        "x1-2x2+4x3+3x4=4",
        "3x1-6x2+8x3+5x4=0",

        # "3x-6y+12z=6",
        # "-2x+5y-9z=-7",
        # "-x+3y-5z=-4"

        # "3x-3y+2z=0",
        # "6x-6y+4z=0",
        # "4x-4y+3z=0"

    ]
    print("Ecuatiile introduse sunt:")
    print_system(system)

    # Parse the equations
    vars, pr_matrix, results = parse_equations(system)
    vars_list.append(vars.copy())

    # Build the matrix
    num_equations = len(system)
    matrix = build_matrix(vars, pr_matrix, results, num_equations)

    # Display the matrix
    print("Variabilele:", vars)
    print("Matricea sistemului:")
    print_matrix(matrix,vars)
    gauss(matrix, vars)

main()