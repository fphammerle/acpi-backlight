# acpi-backlight

## setup

```sh
pip3 install --user --upgrade acpi-backlight
```

## usage

```sh
acpi-backlight-eval 1  # max brightness
acpi-backlight-eval 0.5  # 50% brightness
acpi-backlight-eval 1/4  # 25% brightness
acpi-backlight-eval 'b + 0.1'
acpi-backlight-eval 'b - 1/20'
acpi-backlight-eval 'b * 1.1'
```
