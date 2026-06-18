from backend.agent.tools import calculator_tool


def test_addition():
    assert calculator_tool.invoke("2 + 3") == "5"


def test_subtraction():
    assert calculator_tool.invoke("10 - 4") == "6"


def test_multiplication():
    assert calculator_tool.invoke("12 * 4") == "48"


def test_division():
    assert calculator_tool.invoke("10 / 4") == "2.5"


def test_power():
    assert calculator_tool.invoke("2 ** 8") == "256"


def test_negative_number():
    assert calculator_tool.invoke("-5 + 3") == "-2"


def test_chained_operations():
    assert calculator_tool.invoke("2 + 3 * 4") == "14"


def test_invalid_syntax_returns_error():
    result = calculator_tool.invoke("not valid math !!!")
    assert "Error" in result


def test_blocked_import_returns_error():
    result = calculator_tool.invoke("__import__('os')")
    assert "Error" in result


def test_string_input_returns_error():
    result = calculator_tool.invoke("'hello' + 'world'")
    assert "Error" in result
