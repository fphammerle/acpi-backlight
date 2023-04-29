# acpi-backlight

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI Pipeline Status](https://github.com/fphammerle/acpi-backlight/workflows/tests/badge.svg)](https://github.com/fphammerle/acpi-backlight/actions)
![Coverage Status](https://ipfs.io/ipfs/QmP8k5H4MkfspFxQxdL2kEZ4QQWQjF8xwPYD35KvNH4CA6/20230429T090002+0200/s3.amazonaws.com/assets.coveralls.io/badges/coveralls_100.svg)

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
