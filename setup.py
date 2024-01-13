from setuptools import setup

# read the contents of your README file
with open('cli/README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    print(long_description)

setup(
    name="indexgen",
    version="0.1.3",
    packages=['cli'],
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        indexgen=cli.main:cli
    """,
    long_description=long_description,
    long_description_content_type='text/markdown',
    description = "A utility CLI to generate a hyperlinked table of contents for your Git repositories, outputting as a navigable Markdown file.",
    author = "Aiman Fatima",
    author_email = "aimanfatimadl@gmail.com",
)
