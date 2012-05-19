from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='arduino-sketch',
    version=version,
    description="Compile and upload Arduino sketches from command line",
    long_description="""""",
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Embedded Systems",
    ],
    keywords='arduino',
    author='Oliver Tonnhofer',
    author_email='olt@bogosoft.com',
    url='',
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    arduino-sketch = arduino_sketch.app:main
    """,
)
