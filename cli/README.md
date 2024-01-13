## Hyperlinked Index Markdown / Github Repo Table of Contents Generator

## Description
The Hyperlinked Index MD Generator is a command-line tool designed to create a structured and navigable markdown document that serves as a comprehensive index for your github project directories. This tool generates a clickable markdown index, organizing files and folders in a user-friendly format, which is especially beneficial for large and complex projects.

Motivation for this project: I maintain a repository where I push all my data structure and algorithm problems, as well as my LeetCode practice exercises. I wanted to use a navigable index as my README because I wished to see all the problems I've solved on the main GitHub project page. A hyperlinked table of contents seemed like a good idea, but I couldn't find any robust solution for it. Hence, I created this project.

If you want to use the UI directly, [check this out](https://github.com/aimanfatima/hyperlinked-index-md-generator)

## Features
- Generates a markdown file with a linked index of directories and files.
- Allows exclusion of specified files and directories using patterns.
- Option to specify the output file name.
- Simple and easy-to-use command-line interface.

## Installation

To install the Hyperlinked Index MD Generator and use it, follow these steps:

1. Install the package 

```
    pip install indexgen
```

## Usage

To use the Hyperlinked Index MD Generator, run the following command in your terminal:

```
    indexgen generate [OPTIONS]
```

### Options:
- `-o`, `--output` TEXT: Output markdown file name. If not specified, the output will be printed to the console.
- `-i`, `--ignore` TEXT: Patterns of files or directories to ignore. This option can be repeated to specify multiple patterns.

### Example:
Generate an index for the current directory and output to `index.md`, ignoring all `.log` files:

```
    indexgen generate --output index.md --ignore "*.log"
```

If you want to run this command for a repository located elsewhere

```
    indexgen generate "<location/to/any/git/repo>"
```

And then, simply copy the markdown file contents to you project and push it.

## Contributing
Contributions to the Hyperlinked Index MD Generator are welcome!

## License
This project is licensed under the [GNU GENERAL PUBLIC LICENSE](https://github.com/aimanfatima/hyperlinked-index-md-generator/blob/main/LICENSE).

## Acknowledgments
- Special thanks to [Bootstrap](https://getbootstrap.com/) and [Click](https://click.palletsprojects.com/en/7.x/) for making the UI and CLI functionality straightforward and robust.