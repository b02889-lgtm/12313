#!/usr/bin/env python3
"""
Advanced Calculator - Complex mathematical operations
Supports calculus, optimization, and advanced mathematical functions
"""

import math
import numpy as np
from scipy import integrate, optimize, special


class AdvancedCalculator:
    """Advanced mathematical calculator with calculus and optimization support"""
    
    def __init__(self):
        self.precision = 1e-6
    
    def derivative(self, f, x, h=1e-5):
        """
        Calculate numerical derivative of function f at point x
        
        Args:
            f: Function to differentiate
            x: Point at which to calculate derivative
            h: Step size (default: 1e-5)
            
        Returns:
            Approximate derivative value
        """
        return (f(x + h) - f(x - h)) / (2 * h)
    
    def integrate(self, f, a, b):
        """
        Calculate definite integral of function f from a to b
        
        Args:
            f: Function to integrate
            a: Lower bound
            b: Upper bound
            
        Returns:
            tuple: (result, error_estimate)
        """
        result, error = integrate.quad(f, a, b)
        return result, error
    
    def solve_equation(self, f, x0, method='newton'):
        """
        Solve equation f(x) = 0 using numerical methods
        
        Args:
            f: Function to find root of
            x0: Initial guess
            method: Solving method ('newton', 'brentq', 'fsolve')
            
        Returns:
            Root of the equation
        """
        if method == 'newton':
            return optimize.newton(f, x0)
        elif method == 'fsolve':
            return optimize.fsolve(f, x0)[0]
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def minimize(self, f, x0):
        """
        Find minimum of function f starting from x0
        
        Args:
            f: Function to minimize
            x0: Initial guess (can be scalar or array)
            
        Returns:
            OptimizeResult object with minimum point
        """
        return optimize.minimize(f, x0)
    
    def maximize(self, f, x0):
        """
        Find maximum of function f starting from x0
        
        Args:
            f: Function to maximize
            x0: Initial guess (can be scalar or array)
            
        Returns:
            OptimizeResult object with maximum point
        """
        return optimize.minimize(lambda x: -f(x), x0)
    
    def taylor_series(self, f, x0, n_terms=5):
        """
        Calculate Taylor series approximation of f around x0
        
        Args:
            f: Function to approximate
            x0: Point around which to expand
            n_terms: Number of terms in series
            
        Returns:
            Coefficients of Taylor series [a0, a1, a2, ...]
        """
        coefficients = []
        for n in range(n_terms):
            # Calculate nth derivative numerically
            def nth_derivative(x):
                if n == 0:
                    return f(x)
                h = 1e-5
                if n == 1:
                    return (f(x + h) - f(x - h)) / (2 * h)
                # Higher derivatives (simplified approximation)
                return self.derivative(lambda t: self.derivative(f, t), x)
            
            coeff = nth_derivative(x0) / math.factorial(n)
            coefficients.append(coeff)
        
        return coefficients
    
    def solve_quadratic(self, a, b, c):
        """
        Solve quadratic equation ax² + bx + c = 0
        
        Args:
            a, b, c: Coefficients of quadratic equation
            
        Returns:
            tuple: (x1, x2) or None if no real solutions
        """
        discriminant = b**2 - 4*a*c
        
        if discriminant < 0:
            # Complex roots
            real_part = -b / (2*a)
            imag_part = math.sqrt(-discriminant) / (2*a)
            return (complex(real_part, imag_part), complex(real_part, -imag_part))
        elif discriminant == 0:
            # One solution
            x = -b / (2*a)
            return (x, x)
        else:
            # Two real solutions
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return (x1, x2)
    
    def factorial(self, n):
        """Calculate factorial of n"""
        if n < 0:
            raise ValueError("Factorial not defined for negative numbers")
        return math.factorial(int(n))
    
    def combination(self, n, k):
        """Calculate binomial coefficient C(n,k) = n! / (k!(n-k)!)"""
        return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))
    
    def permutation(self, n, k):
        """Calculate permutation P(n,k) = n! / (n-k)!"""
        return math.factorial(n) // math.factorial(n - k)
    
    def gcd(self, a, b):
        """Calculate greatest common divisor"""
        return math.gcd(int(a), int(b))
    
    def lcm(self, a, b):
        """Calculate least common multiple"""
        return abs(int(a) * int(b)) // self.gcd(a, b)


def main():
    """Example usage"""
    calc = AdvancedCalculator()
    
    # Example 1: Solve quadratic equation
    print("Example 1: Solve x² - 5x + 6 = 0")
    roots = calc.solve_quadratic(1, -5, 6)
    print(f"Roots: x1 = {roots[0]}, x2 = {roots[1]}")
    
    # Example 2: Calculate derivative
    print("\nExample 2: Derivative of f(x) = x² at x = 3")
    f = lambda x: x**2
    derivative = calc.derivative(f, 3)
    print(f"f'(3) ≈ {derivative}")
    
    # Example 3: Calculate integral
    print("\nExample 3: Integral of x² from 0 to 2")
    result, error = calc.integrate(f, 0, 2)
    print(f"∫₀² x² dx ≈ {result} (error: {error})")
    
    # Example 4: Find minimum
    print("\nExample 4: Find minimum of f(x) = (x-2)²")
    g = lambda x: (x - 2)**2
    min_result = calc.minimize(g, 0)
    print(f"Minimum at x = {min_result.x[0]}")
    
    # Example 5: Factorial and combinations
    print("\nExample 5: Calculate 5! and C(10,3)")
    print(f"5! = {calc.factorial(5)}")
    print(f"C(10,3) = {calc.combination(10, 3)}")


if __name__ == "__main__":
    main()