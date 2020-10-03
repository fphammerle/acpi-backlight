import pytest

from acpi_backlight import Backlight

# pylint: disable=protected-access
# pylint: disable=redefined-outer-name; fixture


def test_init_default():
    backlight = Backlight()
    assert backlight._acpi_dir_path == "/sys/class/backlight/intel_backlight"


@pytest.mark.parametrize("name", ["intel_backlight", "other"])
def test_init(name):
    backlight = Backlight(name=name)
    assert backlight._acpi_dir_path == "/sys/class/backlight/{}".format(name)


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
    tmp_path, max_brightness, brightness_absolute_str, expected_brightness_relative
):
    backlight = Backlight()
    backlight._acpi_dir_path = str(tmp_path)
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
    tmp_path, max_brightness, brightness_relative, expected_brightness_abs_str
):
    backlight = Backlight()
    backlight._acpi_dir_path = str(tmp_path)
    tmp_path.joinpath("max_brightness").write_text(str(max_brightness))
    backlight.brightness_relative = brightness_relative
    assert tmp_path.joinpath("brightness").read_text() == expected_brightness_abs_str
