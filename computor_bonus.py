import sys
import re
from fractions import Fraction

def parse_polynomial(equation):
    try:
        left, right = equation.split('=')
    except ValueError:
        raise ValueError("Equation must contain exactly one '=' sign.")
    
    left_terms = parse_terms(left)
    right_terms = parse_terms(right)
    
    for power, coeff in right_terms.items():
        left_terms[power] = left_terms.get(power, 0) - coeff
    
    return left_terms

def parse_terms(expression):
    terms = {}
    expression = expression.replace(' ', '')
    matches = re.findall(r'([+-]?\d*\.?\d*)\*?X?\^?(\d*)', expression)
    for match in matches:
        coeff = match[0]
        power = match[1]
        if coeff == '' or coeff == '+':
            coeff = 1
        elif coeff == '-':
            coeff = -1
        else:
            if '.' in match[0]:
                coeff = float(match[0].replace(' ', ''))
            else:
                coeff = int(match[0].replace(' ', ''))
        power = int(power) if power else 1 if 'X' in match[0] else 0
        terms[power] = terms.get(power, 0) + coeff
    return terms

def solve_polynomial(terms):
    degree = max(terms.keys())
    
    if all(coeff == 0 for coeff in terms.values()):
        return "Polynomial degree: 0\nEach real number is a solution."
    
    if degree > 2:
        return f"Polynomial degree: {degree}\nThe polynomial degree is strictly greater than 2, I can't solve."
    
    if degree == 2:
        a = terms.get(2, 0)
        b = terms.get(1, 0)
        c = terms.get(0, 0)
        discriminant = b**2 - 4*a*c
        if discriminant > 0:
            sol1 = Fraction(-b + discriminant**0.5, 2*a)
            sol2 = Fraction(-b - discriminant**0.5, 2*a)
            return f"Polynomial degree: 2\nDiscriminant is strictly positive, the two solutions are:\n{sol1}\n{sol2}"
        elif discriminant == 0:
            sol = Fraction(-b, 2*a)
            return f"Polynomial degree: 2\nDiscriminant is zero, the solution is:\n{sol}"
        else:
            return f"Polynomial degree: 2\nDiscriminant is strictly negative, no real solutions."
    
    if degree == 1:
        b = terms.get(1, 0)
        c = terms.get(0, 0)
        if b == 0 and c == 0:
            return "Polynomial degree: 1\nEach real number is a solution."
        elif b == 0:
            return "Polynomial degree: 1\nNo solution."
        sol = Fraction(-c, b)
        return f"Polynomial degree: 1\nThe solution is:\n{sol}"
    
    return "Polynomial degree: 0\nNo solution."

def main():

    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments.")
        return
    eq = sys.argv[1]
    try:
        terms = parse_polynomial(eq)
        reduced_form = " + ".join([f"{coeff} * X^{power}" for power, coeff in sorted(terms.items())])
        print(f"Reduced form: {reduced_form} = 0")
        print(solve_polynomial(terms))
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
