import ast
import operator
from langchain_core.tools import tool
from backend.rag.retriever import retrieve


@tool
def retriever_tool(query: str) -> str:
    """Search the uploaded documents for information relevant to the query."""
    return retrieve(query)


@tool
def calculator_tool(expression: str) -> str:
    """Evaluate a mathematical expression. Input must be a valid arithmetic expression e.g. '12 * 4.5'."""
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return allowed_operators[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return allowed_operators[type(node.op)](_eval(node.operand))
        else:
            raise TypeError(f"Unsupported expression type: {type(node)}")

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval(tree.body)
        return str(result)
    except Exception as e:
        return f"Error: {e}"
