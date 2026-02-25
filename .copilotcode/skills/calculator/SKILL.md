---
name: calculator
description: Advanced mathematical computation and formula processing skill. Use this skill when users need to: (1) Perform complex mathematical calculations beyond basic arithmetic, (2) Work with mathematical formulas and expressions, (3) Perform statistical analysis and data processing, (4) Solve algebraic, calculus, or linear algebra problems, (5) Process numerical data with mathematical operations.
---

# Calculator

## Overview

This skill enables advanced mathematical computation and formula processing, supporting complex calculations, statistical analysis, and mathematical problem-solving across various domains including algebra, calculus, statistics, and linear algebra.

## Core Capabilities

### 1. Advanced Mathematical Calculations

Perform complex mathematical operations beyond basic arithmetic:

```python
import math
import numpy as np
from scipy import integrate, optimize

# Example: Solve quadratic equation ax² + bx + c = 0
def solve_quadratic(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant >= 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return x1, x2
    else:
        return None  # Complex roots

# Example: Calculate derivative numerically
def numerical_derivative(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

# Example: Numerical integration
def integrate_function(f, a, b):
    result, error = integrate.quad(f, a, b)
    return result
```

### 2. Statistical Analysis

Use [`scripts/statistics.py`](scripts/statistics.py) for comprehensive statistical operations:

- Descriptive statistics (mean, median, mode, standard deviation)
- Probability distributions
- Hypothesis testing
- Correlation and regression analysis
- Data visualization

Example usage:
```python
from scripts.statistics import StatisticsCalculator

calc = StatisticsCalculator()
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

mean = calc.mean(data)
std_dev = calc.standard_deviation(data)
correlation = calc.correlation(data1, data2)
```

### 3. Formula Parsing and Evaluation

Use [`scripts/formula_parser.py`](scripts/formula_parser.py) for parsing and evaluating mathematical expressions:

```python
from scripts.formula_parser import FormulaParser

parser = FormulaParser()

# Parse and evaluate expressions
result = parser.evaluate("2 * x + 3", x=5)  # Returns 13
result = parser.evaluate("sin(pi/2)")  # Returns 1.0
result = parser.evaluate("sqrt(16) + 2^3")  # Returns 12.0
```

### 4. Matrix Operations

Perform linear algebra operations:

```python
import numpy as np

# Matrix operations
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Matrix multiplication
C = np.dot(A, B)

# Matrix inverse
A_inv = np.linalg.inv(A)

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

# Determinant
det_A = np.linalg.det(A)
```

## Workflow

### For Simple Calculations

1. Use Python's built-in math operations or the `math` module
2. Return the result directly to the user

### For Complex Calculations

1. Identify the type of calculation needed
2. Choose the appropriate script or library:
   - Statistics → use [`scripts/statistics.py`](scripts/statistics.py)
   - Formula evaluation → use [`scripts/formula_parser.py`](scripts/formula_parser.py)
   - Advanced math → use [`scripts/advanced_calculator.py`](scripts/advanced_calculator.py)
3. Execute the calculation
4. Present the result with clear explanation

### For Formula Reference

Consult [`references/math_formulas.md`](references/math_formulas.md) for common mathematical formulas and their applications.

## Best Practices

1. **Precision**: Always consider numerical precision and rounding errors
2. **Units**: Clearly specify and track units of measurement
3. **Validation**: Validate input parameters before calculation
4. **Error Handling**: Handle edge cases (division by zero, invalid domains, etc.)
5. **Explanation**: Provide clear explanations of calculation methods and results

## Resources

### scripts/
- [`advanced_calculator.py`](scripts/advanced_calculator.py) - Advanced mathematical functions (calculus, optimization, etc.)
- [`statistics.py`](scripts/statistics.py) - Statistical analysis tools
- [`formula_parser.py`](scripts/formula_parser.py) - Mathematical expression parser and evaluator

### references/
- [`math_formulas.md`](references/math_formulas.md) - Comprehensive mathematical formula reference
- [`calculation_patterns.md`](references/calculation_patterns.md) - Common calculation patterns and best practices

## Examples

### Example 1: Solving a System of Linear Equations

```python
import numpy as np

# System: 2x + 3y = 8, x - y = -1
A = np.array([[2, 3], [1, -1]])
b = np.array([8, -1])

# Solve using numpy
solution = np.linalg.solve(A, b)
print(f"x = {solution[0]}, y = {solution[1]}")
```

### Example 2: Statistical Analysis

```python
from scripts.statistics import StatisticsCalculator
import numpy as np

# Sample data
data = [23, 25, 27, 29, 31, 33, 35, 37, 39, 41]

calc = StatisticsCalculator()
print(f"Mean: {calc.mean(data)}")
print(f"Median: {calc.median(data)}")
print(f"Standard Deviation: {calc.standard_deviation(data)}")
print(f"Variance: {calc.variance(data)}")
```

### Example 3: Calculus Operations

```python
from scripts.advanced_calculator import AdvancedCalculator

calc = AdvancedCalculator()

# Define function f(x) = x^2
def f(x):
    return x**2

# Calculate derivative at x=3
derivative = calc.derivative(f, 3)  # Result: 6

# Calculate definite integral from 0 to 2
integral = calc.integrate(f, 0, 2)  # Result: 8/3