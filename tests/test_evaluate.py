import pytest

from acpi_backlight._evaluate import evaluate_expression


@pytest.mark.parametrize(
    ("expr_str", "names", "expected"),
    [
        ("0", {}, 0),
        ("0.0", {}, 0),
        ("1.0", {}, 1),
        ("-1", {}, -1),
        ("0.1 + 0.2", {}, 0.3),
        ("0.3 - 0.2", {}, 0.1),
        ("0.2 * 3", {}, 0.6),
        ("0.6 / 3", {}, 0.2),
        ("0.6 / 3 + 0.1", {}, 0.3),
        ("(0.6 - 0.2) / 2", {}, 0.2),
        ("b", {"b": 0.4}, 0.4),
        ("-b", {"b": 0.3}, -0.3),
        ("0.1 + b", {"b": 0.2}, 0.3),
    ],
)
def test_evaluate_expression(expr_str, names, expected):
    assert expected == pytest.approx(evaluate_expression(expr_str, names))


@pytest.mark.parametrize(
    "expr_str",
    [
        'read("/proc/cpuinfo")',
        "os.exit(42)",
        'os.system("echo evil")',
        "0.__class__",
        "None.__class__",
        'eval("1")',
    ],
)
def test_evaluate_expression_fail(expr_str):
    with pytest.raises(Exception):
        evaluate_expression(expr_str, {})
