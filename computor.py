import re
import sys


def parse_polynomial(equation):
    # Split the equation into left and right parts
    left, right = equation.split('=')
    left_terms = parse_terms(left)
    right_terms = parse_terms(right)
    # Move all terms to the left side
    for power, coeff in right_terms.items():
        left_terms[power] = left_terms.get(power, 0) - coeff

    return left_terms


def parse_terms(expression):
    terms = {}
    # Find all terms in the expression
    matches = re.findall(r'([+-]?\s*\d*\.?\d*)\s*\*\s*X\^(\d+)', expression)
    for match in matches:
        if '.' in match[0]:
            coeff = float(match[0].replace(' ', ''))
        else:
            coeff = int(match[0].replace(' ', ''))
        power = int(match[1])
        terms[power] = terms.get(power, 0) + coeff
    return terms


def solve_polynomial(terms):
    degree = max(terms.keys())
    if all(coeff == 0 for coeff in terms.values()):
        return "Polynomial degree: 0\nEach real number is a solution."
    if degree > 2:
        return (
            f"Polynomial degree: {degree}\n"
            "The polynomial degree is strictly greater than 2, "
            "I can't solve."
        )

    if degree == 2:
        a = terms.get(2, 0)
        b = terms.get(1, 0)
        c = terms.get(0, 0)
        discriminant = b**2 - 4*a*c
        if discriminant > 0:
            sol1 = (-b + discriminant**0.5) / (2*a)
            sol2 = (-b - discriminant**0.5) / (2*a)
            return (
                f"Polynomial degree: {degree}\n"
                f"Discriminant is strictly positive, the two solutions are:\n{round(sol2, 6)}\n{round(sol1, 6)}"
            )
        elif discriminant == 0:
            sol = -b / (2*a)
            return (
                f"Polynomial degree: 2\n"
                f"Discriminant is zero, the solution is:\n"
                f"{sol}"
            )
        else:
            sol1 = f"(-{b} + i√{-discriminant}) / {2*a}"
            sol2 = f"(-{b} - i√{-discriminant}) / {2*a}"
            return (
                f"Polynomial degree: 2\n"
                f"Discriminant is strictly negative, the two complex solutions are: \n" + sol1 + "\n" + sol2
            )

    if degree == 1:
        b = terms.get(1, 0)
        c = terms.get(0, 0)
        sol = -c / b
        return f"Polynomial degree: 1\nThe solution is:\n{sol}"

    return "Polynomial degree: 0\nNo solution."


def main():
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments.")
        return
    eq = sys.argv[1]
    # eq = "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"  # 2 solutions
    # eq = "5 * X^0 + 4 * X^1 = 4 * X^0" # 1 solution
    # eq = "42 * X^0 = 42 * X^0" # infinite solutions
    # eq = "8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0" # I can't solve
    # eq = "1 * X^1 + 4 * X^2 = -4 * X^0 " # negative discriminant
    terms = parse_polynomial(eq)
    reduced_form = ""
    for index, (power, coeff) in enumerate(sorted(terms.items())):
        if coeff >= 0:
            sign = " + " if index > 0 else ""
        else:
            sign = " - "
        reduced_form += f"{sign}{abs(coeff)} * X^{power}"
    print(f"Reduced form: {reduced_form} = 0")
    print(solve_polynomial(terms))


if __name__ == "__main__":
    main()
