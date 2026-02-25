# Calculation Patterns and Best Practices

## Common Calculation Workflows

### Pattern 1: Data Analysis Pipeline

```python
from scripts.statistics import StatisticsCalculator

# 1. Load and validate data
data = [23, 25, 27, 29, 31, 33, 35, 37, 39, 41]
if not data or len(data) < 2:
    raise ValueError("Insufficient data")

# 2. Calculate descriptive statistics
calc = StatisticsCalculator()
stats = {
    'mean': calc.mean(data),
    'median': calc.median(data),
    'std_dev': calc.standard_deviation(data),
    'variance': calc.variance(data)
}

# 3. Check for outliers (using Z-score method)
mean = stats['mean']
std = stats['std_dev']
outliers = [x for x in data if abs(calc.z_score(x, mean, std)) > 3]

# 4. Present results
print(f"Dataset Statistics:")
for key, value in stats.items():
    print(f"  {key}: {value}")
if outliers:
    print(f"  Outliers detected: {outliers}")
```

### Pattern 2: Optimization Problem

```python
from scripts.advanced_calculator import AdvancedCalculator

calc = AdvancedCalculator()

# 1. Define the objective function
def cost_function(x):
    # Example: minimize (x-5)^2 + 10
    return (x - 5)**2 + 10

# 2. Set initial guess
x0 = 0

# 3. Find minimum
result = calc.minimize(cost_function, x0)

# 4. Validate and present results
if result.success:
    print(f"Optimal solution: x = {result.x[0]}")
    print(f"Minimum value: {result.fun}")
else:
    print(f"Optimization failed: {result.message}")
```

### Pattern 3: Formula Evaluation with Variables

```python
from scripts.formula_parser import FormulaParser

parser = FormulaParser()

# 1. Define formula and variables
formula = "sqrt(x^2 + y^2)"  # Distance formula
variables = {'x': 3, 'y': 4}

# 2. Validate inputs
for var, value in variables.items():
    if not isinstance(value, (int, float)):
        raise TypeError(f"Variable {var} must be numeric")

# 3. Evaluate formula
try:
    result = parser.evaluate(formula, **variables)
    print(f"Formula: {formula}")
    print(f"Variables: {variables}")
    print(f"Result: {result}")
except Exception as e:
    print(f"Evaluation error: {e}")
```

### Pattern 4: Numerical Integration

```python
from scripts.advanced_calculator import AdvancedCalculator

calc = AdvancedCalculator()

# 1. Define function to integrate
def f(x):
    return x**2

# 2. Set integration bounds
a, b = 0, 2

# 3. Calculate integral
result, error = calc.integrate(f, a, b)

# 4. Present with error estimate
print(f"∫[{a},{b}] x² dx = {result}")
print(f"Estimated error: {error}")
print(f"Theoretical value: {(b**3 - a**3)/3}")
```

## Best Practices

### 1. Input Validation

Always validate inputs before computation:

```python
def safe_divide(a, b):
    """Safely divide with validation"""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numeric")
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
```

### 2. Error Handling

Use try-except blocks for numerical operations:

```python
import math

def safe_sqrt(x):
    """Calculate square root with error handling"""
    try:
        if x < 0:
            raise ValueError("Cannot compute square root of negative number")
        return math.sqrt(x)
    except ValueError as e:
        print(f"Error: {e}")
        return None
```

### 3. Precision Management

Be aware of floating-point precision:

```python
import math

# Bad: Direct equality comparison
if 0.1 + 0.2 == 0.3:  # False!
    print("Equal")

# Good: Use tolerance
tolerance = 1e-9
if abs((0.1 + 0.2) - 0.3) < tolerance:
    print("Equal within tolerance")

# Good: Use math.isclose (Python 3.5+)
if math.isclose(0.1 + 0.2, 0.3):
    print("Equal")
```

### 4. Performance Optimization

Use NumPy for large datasets:

```python
import numpy as np

# Slow: Python loops
data = list(range(1000000))
result = sum([x**2 for x in data])

# Fast: NumPy vectorization
data_np = np.array(data)
result_np = np.sum(data_np**2)
```

### 5. Unit Consistency

Always track and convert units:

```python
def calculate_speed(distance_km, time_hours):
    """Calculate speed with clear units"""
    if time_hours <= 0:
        raise ValueError("Time must be positive")
    
    speed_kmh = distance_km / time_hours
    speed_ms = speed_kmh * (1000 / 3600)  # Convert to m/s
    
    return {
        'km/h': speed_kmh,
        'm/s': speed_ms
    }
```

### 6. Documentation

Document assumptions and limitations:

```python
def compound_interest(principal, rate, time, compounds_per_year=1):
    """
    Calculate compound interest.
    
    Args:
        principal: Initial amount (must be positive)
        rate: Annual interest rate as decimal (e.g., 0.05 for 5%)
        time: Time period in years (must be positive)
        compounds_per_year: Number of times interest compounds per year
        
    Returns:
        Final amount after compound interest
        
    Assumptions:
        - Rate is constant over time
        - No additional deposits or withdrawals
        
    Example:
        >>> compound_interest(1000, 0.05, 2, 12)
        1104.94
    """
    if principal <= 0 or time <= 0:
        raise ValueError("Principal and time must be positive")
    if compounds_per_year < 1:
        raise ValueError("Compounds per year must be at least 1")
    
    return principal * (1 + rate/compounds_per_year)**(compounds_per_year * time)
```

## Common Pitfalls

### 1. Integer Division
```python
# Python 2 behavior (avoid)
result = 5 / 2  # Returns 2 in Python 2

# Python 3 behavior (correct)
result = 5 / 2   # Returns 2.5
result = 5 // 2  # Returns 2 (floor division)
```

### 2. Floating Point Accumulation
```python
# Bad: Accumulation error
total = 0
for i in range(1000000):
    total += 0.1
# total might not be exactly 100000.0

# Better: Use integer arithmetic when possible
total_cents = 0
for i in range(1000000):
    total_cents += 10
total = total_cents / 100
```

### 3. Domain Errors
```python
import math

# Bad: No validation
result = math.sqrt(x)  # Fails if x < 0

# Good: Validate domain
if x < 0:
    raise ValueError("Cannot compute square root of negative number")
result = math.sqrt(x)
```

### 4. Division by Zero
```python
# Bad: No check
average = sum(values) / len(values)

# Good: Check for empty list
if not values:
    raise ValueError("Cannot compute average of empty list")
    print("Cannot compute average of empty list")
    return Non
    return None
average = sum(values) / len(values)
```

## Testing Strategies

### Unit Testing Example
```python
import unittest
from scripts.advanced_calculator import AdvancedCalculator

class TestAdvancedCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = AdvancedCalculator()
    
    def test_quadratic_two_roots(self):
        roots = self.calc.solve_quadratic(1, -5, 6)
        self.assertAlmostEqual(roots[0], 3.0)
        self.assertAlmostEqual(roots[1], 2.0)
    
    def test_factorial(self):
        self.assertEqual(self.calc.factorial(5), 120)
        with self.assertRaises(ValueError):
            self.calc.factorial(-1)
    
    def test_derivative(self):
        f = lambda x: x**2
        derivative = self.calc.derivative(f, 3)
        self.assertAlmostEqual(derivative, 6.0, places=4)
        self.assertAlmostEqual(self.calc.derivative(f, 3, order=2), 2.0, places=4)
        self.assertAlmostEqual(self.calc.derivative(f, 3, order=3), 0.0, places=4)
        self.assertAlmostEqual(self.calc.derivative(f, 3, order=4), 0.0, places=4)
        self.assertAlmostEqual(self.calc.derivative(f, 3, order=5), 0.0, places=4)
        self.assertAlmostEqual(self.calc.derivative(f, 3, order=6), 0.0, places=4)
        self.assertAlmostEqual(self.calc.derivative(f, 3, order=7), 0.0, places=4)self.assertAlmostEqual(self.calc.derivative(f, 3, order=8), 0.0, places=4)
        self.assertAlmostEqual(self.calc.derivative(f, 3, order=9), 0.0, places=4)
        self.assertAlmostEqual(self.calc.derivative(f, 3, order=10), 0.0, places=4)
        print("All tests passed!")
        print("All tests passed!")
        print("All tests passed!")

if __name__ == '__main__':
    unittest.main()
```

## Performance Tips

1. **Use appropriate data structures**: NumPy arrays for numerical data, lists for mixed types
2. **Vectorize operations**: Use NumPy/SciPy functions instead of loops
3. **Cache expensive computations**: Store results that will be reused
4. **Use generators for large datasets**: Avoid loading everything into memory
5. **Profile before optimizing**: Measure to find actual bottlenecks

## Resources

For more complex calculations:
- SciPy documentation: https://docs.scipy.org/
- NumPy documentation: https://numpy.org/doc/
- Mathematical formulas: See [`math_formulas.md`](math_formulas.md)
