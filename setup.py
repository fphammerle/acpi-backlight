""" python setup script """

import setuptools

setuptools.setup(
    name='acpi-backlight',
    use_scm_version=True,
    author='Fabian Peter Hammerle',
    author_email='fabian@hammerle.me',
    url='https://github.com/fphammerle/acpi-backlight',
    packages=['acpi_backlight'],
    setup_requires=['setuptools_scm'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
)
