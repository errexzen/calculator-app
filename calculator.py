"""Business logic for calculator operations and expression evaluation."""

from __future__ import annotations

import ast
from decimal import Decimal, DivisionByZero, InvalidOperation
from typing import Union


Number = Union[int, float, Decimal]


class CalculatorError(Exception):
    """Base exception for calculator-related errors."""


class DivisionByZeroError(CalculatorError):
    """Raised when a division by zero is attempted."""


class InvalidExpressionError(CalculatorError):
    """Raised when an expression is invalid or unsupported."""


class Calculator:
    """Provides mathematical operations and safe expression evaluation."""

    @staticmethod
    def add(a: Number, b: Number) -> Decimal:
        return Decimal(str(a)) + Decimal(str(b))

    @staticmethod
    def subtract(a: Number, b: Number) -> Decimal:
        return Decimal(str(a)) - Decimal(str(b))

    @staticmethod
    def multiply(a: Number, b: Number) -> Decimal:
        return Decimal(str(a)) * Decimal(str(b))

    @staticmethod
    def divide(a: Number, b: Number) -> Decimal:
        denominator = Decimal(str(b))
        if denominator == 0:
            raise DivisionByZeroError("Cannot divide by zero.")
        return Decimal(str(a)) / denominator

    def evaluate_expression(self, expression: str) -> Decimal:
        """Safely evaluates a basic arithmetic expression.

        Supported operators: +, -, *, / and unary +/-.
        """
        cleaned_expression = expression.strip().replace("×", "*").replace("÷", "/")
        if not cleaned_expression:
            raise InvalidExpressionError("Expression is empty.")

        try:
            tree = ast.parse(cleaned_expression, mode="eval")
            return self._eval_node(tree.body)
        except DivisionByZeroError:
            raise
        except (SyntaxError, TypeError, ValueError, InvalidOperation, DivisionByZero) as exc:
            raise InvalidExpressionError("Invalid calculation.") from exc

    def _eval_node(self, node: ast.AST) -> Decimal:
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)

            if isinstance(node.op, ast.Add):
                return self.add(left, right)
            if isinstance(node.op, ast.Sub):
                return self.subtract(left, right)
            if isinstance(node.op, ast.Mult):
                return self.multiply(left, right)
            if isinstance(node.op, ast.Div):
                return self.divide(left, right)
            raise InvalidExpressionError("Unsupported operator.")

        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return operand
            if isinstance(node.op, ast.USub):
                return -operand
            raise InvalidExpressionError("Unsupported unary operator.")

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return Decimal(str(node.value))

        raise InvalidExpressionError("Unsupported expression.")
