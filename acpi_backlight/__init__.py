import argparse
import pathlib

import acpi_backlight._evaluate

_ACPI_BACKLIGHT_ROOT_DIR_PATH = pathlib.Path("/sys/class/backlight")


class Backlight:

    # pylint: disable=too-few-public-methods; does not count properties

    def __init__(self, name: str = "intel_backlight"):
        self._device_name = name
        self._acpi_dir_path = _ACPI_BACKLIGHT_ROOT_DIR_PATH.joinpath(name)

    @property
    def _brightness_path(self) -> pathlib.Path:
        return self._acpi_dir_path.joinpath("brightness")

    @property
    def _max_brightness_path(self) -> pathlib.Path:
        return self._acpi_dir_path.joinpath("max_brightness")

    @property
    def _brightness_absolute(self) -> int:
        return int(self._brightness_path.read_text(encoding="ascii"))

    @_brightness_absolute.setter
    def _brightness_absolute(self, brightness_absolute: int):
        try:
            self._brightness_path.write_text(str(brightness_absolute), encoding="ascii")
        except PermissionError as exc:
            raise PermissionError(
                "Insufficient permissions to set brightness of backlight."
                "\nConsider adding the following udev rules:"
                f'\nACTION=="add", SUBSYSTEM=="backlight"'
                f', KERNEL=="{self._device_name}"'
                f', RUN+="/bin/chgrp video /sys$devpath/brightness"'
                f'\nACTION=="add", SUBSYSTEM=="backlight"'
                f', KERNEL=="{self._device_name}"'
                f', RUN+="/bin/chmod g+w /sys$devpath/brightness"'
            ) from exc

    @property
    def _max_brightness_absolute(self) -> int:
        return int(self._max_brightness_path.read_text(encoding="ascii"))

    @property
    def brightness_relative(self) -> float:
        return self._brightness_absolute / self._max_brightness_absolute

    @brightness_relative.setter
    def brightness_relative(self, brightness_relative: float) -> None:
        self._brightness_absolute = round(
            max(0, min(1, brightness_relative)) * self._max_brightness_absolute
        )


def backlight_eval(expr_str: str) -> None:
    backlight = acpi_backlight.Backlight()
    # pylint: disable=protected-access; internal module
    backlight.brightness_relative = acpi_backlight._evaluate.evaluate_expression(
        expr_str=expr_str, names={"b": backlight.brightness_relative}
    )
    print(backlight.brightness_relative)


def _main() -> None:
    argparser = argparse.ArgumentParser()
    argparser.add_argument("expr_str")
    args = argparser.parse_args()
    backlight_eval(expr_str=args.expr_str)
