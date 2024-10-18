# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- suggest udev rules when permissions are insufficient to set backlight's brightness

### Changed
- made module `acpi_backlight.evaluate` private
- `acpi_backlight.backlight_eval`: raise `ValueError` instead of `Exception`
  when expression contains prohibited specifier or operator

### Removed
- compatibility with `python3.7` & `python3.8`

TODO document commits before 2022-06-16

[Unreleased]: https://github.com/fphammerle/acpi-backlight/compare/0.2.0...HEAD
[0.2.0]: https://github.com/fphammerle/acpi-backlight/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/fphammerle/acpi-backlight/releases/tag/0.1.0
