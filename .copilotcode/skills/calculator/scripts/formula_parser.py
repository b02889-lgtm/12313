#!/usr/bin/env python3
"""
Formula Parser - Mathematical expression parser and evaluator
Safely evaluates mathematical expressions with variable support
"""

import math
import operator
import ast


class FormulaParser:
    """Mathematical formula parser and evaluator"""
    
    def __init__(self):
        # Supported operators
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }
        
        # Supported functions
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sqrt': math.sqrt,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'abs': abs,
            'round': round,
            'ceil': math.ceil,
            'floor': math.floor,
            'min': min,
            'max': max,
        }
        
        # Supported constants
        self.constants = {
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau,
            'inf': float('inf'),
        }

    def evaluate(self, expression, **variables):
        """
        Evaluate a mathematical expression string
        
        Args:
            expression: Mathematical expression (e.g., "2 * x + sin(pi/2)")
            **variables: Variable values (e.g., x=5, y=10)
            
        Returns:
            Result of the calculation
        """
        try:
            # Combine constants and variables
            context = self.constants.copy()
            context.update(variables)
            
            # Parse and evaluate
            tree = ast.parse(expression, mode='eval')
            return self._eval(tree.body, context)
        except Exception as e:
            raise ValueError(f"Error evaluating formula '{expression}': {str(e)}")

    def _eval(self, node, context):
        """Recursive evaluator for AST nodes"""
        if isinstance(node, ast.Num):  # Number
            return node.n
        elif isinstance(node, ast.Constant):  # Python 3.8+ constant
            return node.value
        elif isinstance(node, ast.Name):  # Variable
            if node.id in context:
                return context[node.id]
            raise ValueError(f"Unknown variable: {node.id}")
        elif isinstance(node, ast.BinOp):  # Binary operation (a + b)
            op_type = type(node.op)
            if op_type in self.operators:
                return self.operators[op_type](
                    self._eval(node.left, context),
                    self._eval(node.right, context)
                )
        elif isinstance(node, ast.UnaryOp):  # Unary operation (-a)
            op_type = type(node.op)
            if op_type in self.operators:
                return self.operators[op_type](self._eval(node.operand, context))
        elif isinstance(node, ast.Call):  # Function call (sin(x))
            func_name = node.func.id
            if func_name in self.functions:
                args = [self._eval(arg, context) for arg in node.args]
                return self.functions[func_name](*args)
            raise ValueError(f"Unknown function: {func_name}")
            
        raise ValueError(f"Unsupported operation: {type(node).__name__}")


def main():
    """Example usage"""
    parser = FormulaParser()
    
    # Test cases
    expressions = [
        ("2 + 3 * 4", {}),
        ("sin(pi/2)", {}),
        ("sqrt(16) + 2^3", {}),
        ("x * y + 5", {'x': 2, 'y': 3}),
        ("log10(100)", {}),
        ("max(10, 20, 5)", {}),
    ]
    
    print("Formula Parser Examples:")
    print("-" * 30)
    
    for expr, vars in expressions:
        try:
            result = parser.evaluate(expr, **vars)
            vars_str = f" with {vars}" if vars else ""
            print(f"Expression: {expr}{vars_str}")
            print(f"Result: {result}")
            print("-" * 30)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()