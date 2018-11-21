# pylint: disable=missing-docstring

import ast
import operator as python_operator


_OPERATORS = {
    ast.Add: python_operator.add,
    ast.Div: python_operator.truediv,
    ast.Mult: python_operator.mul,
    ast.Pow: python_operator.pow,
    ast.Sub: python_operator.sub,
    ast.USub: python_operator.neg,
}


def _evaluate(node, names):
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Name):
        return names[node.id]
    elif isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand, names=names)
        return _OPERATORS[type(node.op)](operand)
    elif isinstance(node, ast.BinOp):
        operand_left = _evaluate(node.left, names=names)
        operand_right = _evaluate(node.right, names=names)
        return _OPERATORS[type(node.op)](operand_left, operand_right)
    else:
        raise Exception(node)


def evaluate_expression(expr_str, names):
    expr = ast.parse(expr_str, mode='eval')
    return _evaluate(expr.body, names=names)
