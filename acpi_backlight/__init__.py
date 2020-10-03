# pylint: disable=missing-docstring

import argparse
import os

import acpi_backlight.evaluate

_ACPI_BACKLIGHT_ROOT_DIR_PATH = "/sys/class/backlight"


class Backlight:

    # pylint: disable=too-few-public-methods; does not count properties

    def __init__(self, name="intel_backlight"):
        self._acpi_dir_path = os.path.join(_ACPI_BACKLIGHT_ROOT_DIR_PATH, name)

    @property
    def _brightness_path(self):
        return os.path.join(self._acpi_dir_path, "brightness")

    @property
    def _max_brightness_path(self):
        return os.path.join(self._acpi_dir_path, "max_brightness")

    @property
    def _brightness_absolute(self):
        with open(self._brightness_path, "r") as brightness_file:
            return int(brightness_file.read())

    @_brightness_absolute.setter
    def _brightness_absolute(self, brightness_absolute):
        with open(self._brightness_path, "w") as brightness_file:
            return brightness_file.write(str(round(brightness_absolute)))

    @property
    def _max_brightness_absolute(self):
        with open(self._max_brightness_path, "r") as max_brightness_file:
            return int(max_brightness_file.read())

    @property
    def brightness_relative(self):
        return self._brightness_absolute / self._max_brightness_absolute

    @brightness_relative.setter
    def brightness_relative(self, brightness_relative):
        self._brightness_absolute = (
            max(0, min(1, brightness_relative)) * self._max_brightness_absolute
        )


def backlight_eval(expr_str):
    backlight = acpi_backlight.Backlight()
    backlight.brightness_relative = acpi_backlight.evaluate.evaluate_expression(
        expr_str=expr_str, names={"b": backlight.brightness_relative}
    )
    print(backlight.brightness_relative)


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("expr_str")
    args = argparser.parse_args()
    backlight_eval(expr_str=args.expr_str)


if __name__ == "__main__":
    main()
