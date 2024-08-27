import re

def extract_constants(equation):
    # Remove spaces for easier processing
    equation = equation.replace(' ', '')
    
    # Split the equation into left and right parts
    left, right = equation.split('=')
    
    # Define a regex pattern to match constants (terms without 'X')
    pattern = r'([+-]?\d*\.?\d+)(?!\*X)'
    
    # Find all matches in both parts of the equation
    left_constants = re.findall(pattern, left)
    right_constants = re.findall(pattern, right)
    
    # Convert matches to floats and sum them up
    left_sum = sum(float(num) for num in left_constants)
    right_sum = sum(float(num) for num in right_constants)
    
    # Calculate the net constant term by moving all terms to the left side
    net_constant = left_sum - right_sum
    
    return net_constant

equation = "5 + 4 * X + X^2 = X^2"
constant = extract_constants(equation)
print(f"Net constant term: {constant}")
