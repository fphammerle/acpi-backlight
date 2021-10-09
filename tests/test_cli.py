import pathlib
import unittest.mock

import pytest

import acpi_backlight

# pylint: disable=protected-access; tests


@pytest.mark.parametrize(
    ("expr_str", "brightness"),
    [
        ("0", "0"),
        ("1", "200"),
        ("0.4", "80"),
        ("b / 2 + 0.21", "92"),
        ("b - 1", "0"),
        ("b + 1", "200"),
    ],
)
def test_main(tmp_path: pathlib.Path, expr_str: str, brightness: str):
    acpi_dir_path = tmp_path.joinpath("intel_backlight")
    acpi_dir_path.mkdir()
    acpi_dir_path.joinpath("brightness").write_text("100")
    acpi_dir_path.joinpath("max_brightness").write_text("200")
    with unittest.mock.patch("sys.argv", ["", expr_str]), unittest.mock.patch(
        "acpi_backlight._ACPI_BACKLIGHT_ROOT_DIR_PATH", tmp_path
    ):
        acpi_backlight._main()
    assert acpi_dir_path.joinpath("brightness").read_text() == brightness
