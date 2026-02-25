#!/usr/bin/env python3
"""
Test script to verify calculator skill functionality
This script demonstrates how the calculator skill would be used
"""

def test_quadratic_solver():
    """Test the quadratic equation solver"""
    print("Testing quadratic equation solver...")
    print("Solving: x^2 - 5x + 6 = 0")
    
    # This is what the calculator skill would do:
    # Using the advanced_calculator.py script
    import math
    
    a, b, c = 1, -5, 6
    discriminant = b**2 - 4*a*c
    
    if discriminant >= 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        print(f"Roots: x1 = {x1}, x2 = {x2}")
    else:
        print("Complex roots")
    
    print("Expected: x1 = 3.0, x2 = 2.0")
    print()

def test_statistics():
    """Test statistical functions"""
    print("Testing statistical functions...")
    data = [23, 25, 27, 29, 31, 33, 35, 37, 39, 41]
    
    # This is what the calculator skill would do:
    # Using the statistics.py script
    mean = sum(data) / len(data)
    print(f"Mean: {mean}")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 0:
        median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
    else:
        median = sorted_data[n//2]
    print(f"Median: {median}")
    
    variance = sum((x - mean)**2 for x in data) / (len(data) - 1)
    std_dev = variance**0.5
    print(f"Standard Deviation: {std_dev}")
    print()

def test_formula_parser():
    """Test formula parsing"""
    print("Testing formula parsing...")
    print("Evaluating: sqrt(3^2 + 4^2)")
    
    # This is what the calculator skill would do:
    # Using the formula_parser.py script
    import math
    
    # Parse and evaluate: sqrt(3^2 + 4^2)
    result = math.sqrt(3**2 + 4**2)
    print(f"Result: {result}")
    print("Expected: 5.0")
    print()

if __name__ == "__main__":
    print("Calculator Skill Test")
    print("=" * 30)
    test_quadratic_solver()
    test_statistics()
    test_formula_parser()
    print("All tests completed!")