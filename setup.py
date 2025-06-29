"""python setup script"""

import setuptools

setuptools.setup(
    name="acpi-backlight",
    use_scm_version=True,
    author="Fabian Peter Hammerle",
    author_email="fabian@hammerle.me",
    url="https://github.com/fphammerle/acpi-backlight",
    packages=["acpi_backlight"],
    entry_points={
        "console_scripts": [
            "acpi-backlight-eval=acpi_backlight:_main",
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        # .github/workflows/python.yml
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",  # <3.9 untested
    install_requires=[],
    tests_require=["pytest"],
)
