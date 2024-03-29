import pathlib
import unittest.mock
import re

import pytest

from acpi_backlight import Backlight, backlight_eval

# pylint: disable=protected-access
# pylint: disable=redefined-outer-name; fixture


def test_init_default():
    backlight = Backlight()
    assert backlight._acpi_dir_path.as_posix() == "/sys/class/backlight/intel_backlight"


@pytest.mark.parametrize("name", ["intel_backlight", "other"])
def test_init(name):
    backlight = Backlight(name=name)
    assert backlight._acpi_dir_path.as_posix() == "/sys/class/backlight/" + name


def test__brightness_absolute_set_permission_denied() -> None:
    backlight = Backlight()
    with unittest.mock.patch(
        "pathlib.Path.open",
        side_effect=PermissionError(
            "[Errno 13] Permission denied:"
            " '/sys/class/backlight/intel_backlight/brightness'"
        ),
    ), pytest.raises(
        PermissionError,
        match=re.escape(
            "Insufficient permissions to set brightness of backlight."
            "\nConsider adding the following udev rules:"
            '\nACTION=="add", SUBSYSTEM=="backlight", KERNEL=="intel_backlight"'
            ', RUN+="/bin/chgrp video /sys$devpath/brightness"'
            '\nACTION=="add", SUBSYSTEM=="backlight", KERNEL=="intel_backlight"'
            ', RUN+="/bin/chmod g+w /sys$devpath/brightness"'
        ),
    ):
        backlight._brightness_absolute = 42


@pytest.mark.parametrize(
    ("max_brightness", "brightness_absolute_str", "expected_brightness_relative"),
    (
        (100, "0", 0),
        (100, "100", 1),
        (100, "40", 0.4),
        (4096, "2048", 0.5),
        (4096, "3584", 0.875),
    ),
)
def test_brightness_relative_get(
    tmp_path: pathlib.Path,
    max_brightness,
    brightness_absolute_str,
    expected_brightness_relative,
):
    backlight = Backlight()
    backlight._acpi_dir_path = tmp_path
    tmp_path.joinpath("brightness").write_text(brightness_absolute_str)
    tmp_path.joinpath("max_brightness").write_text(str(max_brightness))
    assert backlight.brightness_relative == pytest.approx(expected_brightness_relative)


@pytest.mark.parametrize(
    ("max_brightness", "brightness_relative", "expected_brightness_abs_str"),
    (
        (100, 0, "0"),
        (100, 1, "100"),
        (100, 0.4, "40"),
        (4096, 0.5, "2048"),
        (4096, 0.8, "3277"),
        (100, 1.1, "100"),
        (100, -0.1, "0"),
    ),
)
def test_brightness_relative_set(
    tmp_path: pathlib.Path,
    max_brightness,
    brightness_relative,
    expected_brightness_abs_str,
):
    backlight = Backlight()
    backlight._acpi_dir_path = tmp_path
    tmp_path.joinpath("max_brightness").write_text(str(max_brightness))
    backlight.brightness_relative = brightness_relative
    assert tmp_path.joinpath("brightness").read_text() == expected_brightness_abs_str


@pytest.mark.parametrize(
    ("current_brightness_relative", "expr_str", "expected_new_brightness_relative"),
    (
        (100, "1", 1),
        (100, "0", 0),
        (100, "0.42", 0.42),
        (100, "1/4", 0.25),
        (100, "b * 0.5", 50),
        (100, "b / 2", 50),
        (100, "b + 21", 121),
        (100, "b - 21", 79),
    ),
)
def test_backlight_eval(
    current_brightness_relative, expr_str, expected_new_brightness_relative
):
    with unittest.mock.patch(
        "acpi_backlight.Backlight.brightness_relative",
        new_callable=unittest.mock.PropertyMock,
    ) as property_mock:
        property_mock.return_value = current_brightness_relative
        backlight_eval(expr_str)
    # args and kwargs properties were added in python3.8
    assert all(not call[1] for call in property_mock.call_args_list)
    setter_calls_args = [call[0] for call in property_mock.call_args_list if call[0]]
    assert len(setter_calls_args) == 1, setter_calls_args
    (new_brightness_relative,) = setter_calls_args[0]
    assert new_brightness_relative == pytest.approx(expected_new_brightness_relative)
