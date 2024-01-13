from setuptools import setup

setup(
    name="hyperlinked-index-md-generator",
    version="0.1.0",  # Add a version
    packages=['cli'],  # Specify your package(s)
    install_requires=[
        "Click",
        "requests",
    ],
    entry_points="""
        [console_scripts]
        indexgen=cli.main:cli
    """,
)
