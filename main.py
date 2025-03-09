def readSys():
    system = []
    while True:
        equation = input()
        if equation == "0":
            break
        system.append(equation)
        print("Introduceti alta ecuatie sau 0 pentru a opri")
    return system

def displaySys(system):
    for i in range(0, len(system)):
        print(f"{{ {system[i]}")

def sysToMat(system):
    variables = []


def main():
    print("Introduceti ecuatiile sistemului: ")
    system = readSys()
    print("Ecuatiile introduse sunt:", displaySys(system))

main()