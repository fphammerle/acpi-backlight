""" python setup script """

import setuptools

setuptools.setup(
    name='acpi-backlight',
    use_scm_version=True,
    author='Fabian Peter Hammerle',
    author_email='fabian@hammerle.me',
    url='https://github.com/fphammerle/acpi-backlight',
    packages=['acpi_backlight'],
    entry_points={'console_scripts': [
        'acpi-backlight-eval=acpi_backlight:main',
    ]},
    setup_requires=['setuptools_scm'],
    tests_require=['pytest'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
)
