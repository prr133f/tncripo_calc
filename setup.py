from setuptools import setup

setup(
    name="myapp",
    version="1.0",
    scripts=["main.py"],
    entry_points={"console_scripts": ["myapp=main:main"]},
)
