import os
import click
import fnmatch
import subprocess

# Global array of hardcoded directories to always ignore
GLOBAL_IGNORE_PATTERNS = ['.git', '*/node_modules', '*/__pycache__']

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("\nWelcome to the index md generator CLI app !!\n")
        click.echo("\nTo see all the commands options, run indexgen --help\n")

@cli.command()
@click.argument('path', default='.', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help="Output markdown file name.")
@click.option('--ignore', '-i', multiple=True, help="Patterns of files or directories to ignore.")
@click.option('--include', '-p', multiple=True, help="Patterns of files to include.")
def generate(path, output, ignore, include):
    """
    Generate a markdown index for the directory structure.
    """
    # Read ignore patterns from .gitignore and merge with command line ignore patterns
    path = os.path.abspath(path)
    gitignore_patterns = read_gitignore(path)
    all_ignore_patterns = list(ignore) + gitignore_patterns + GLOBAL_IGNORE_PATTERNS
    print(all_ignore_patterns)

    markdown_content = generate_index(path, all_ignore_patterns, include)
    # markdown_content = generate_index(path)
    
    if output:
        # Write the content to the output file
        with open(output, 'w') as f:
            f.write(markdown_content)
        click.echo(f'Markdown index written to {output}')
    else:
        # Print the content to the console
        click.echo(markdown_content)
        print("Done")



def is_ignored(path, ignore_patterns, target_directory):
    """
    Check if the given path matches any of the ignore patterns.
    """
    abs_path = os.path.abspath(path)
    rel_path = os.path.relpath(abs_path, target_directory)

    for pattern in ignore_patterns:
        # Handle directory patterns (ending with '/')
        if pattern.endswith('/') and os.path.isdir(abs_path):
            dir_pattern = pattern.rstrip('/')
            # Check if any part of the path matches the directory pattern
            if any(fnmatch.fnmatch(part, dir_pattern) for part in rel_path.split(os.sep)):
                return True

        # Standard fnmatch for other patterns
        elif fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(abs_path), pattern):
            return True

    return False

def get_git_non_ignored_files(directory):
    """ Get a list of both tracked and untracked files not ignored by git. """
    # Get tracked files
    tracked = subprocess.run(
        ['git', '-C', directory, 'ls-files', '-z'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
    )
    tracked_files = tracked.stdout.strip('\x00').split('\x00')

    # Get untracked files
    # untracked = subprocess.run(
    #     ['git', '-C', directory, 'ls-files', '--others', '--exclude-standard', '-z'],
    #     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
    # )
    # untracked_files = untracked.stdout.strip('\x00').split('\x00')

    # Combine and remove empty strings
    # all_files = tracked_files + untracked_files
    all_files = tracked_files
    return [f for f in all_files if f]

def generate_index(directory, ignore_patterns, include_patterns=None):
    # Convert directory to absolute path - doing one level up    
    immediate_folder_name = os.path.basename(directory)
    markdown_content = "# Index of {}\n\n".format(immediate_folder_name)
    listed_directories = set()

    for root, dirs, files in os.walk(directory):
        dirs.sort() # Sort directories alphabetically
        # Apply ignore patterns
        # Filter directories and files based on ignore patterns
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), ignore_patterns, directory)]
        files[:] = [f for f in files if not is_ignored(os.path.join(root, f), ignore_patterns, directory)]

        # Filter files by include patterns
        if include_patterns:
            included_files = [f for f in files if any(fnmatch.fnmatch(f, pattern) for pattern in include_patterns)]
        else:
            included_files = files

        # Skip this directory if no files match the include patterns
        if include_patterns and not included_files:
            continue

        # Break down the root into parts and list each directory if not already listed
        root_parts = os.path.relpath(root, directory).split(os.sep)
        for i in range(len(root_parts)):
            sub_path = os.path.join(directory, *root_parts[:i + 1])
            sub_path_relative = os.path.relpath(sub_path, directory)

            if sub_path not in listed_directories and sub_path_relative != '.':
                indent = '  ' * i
                dir_name = os.path.basename(sub_path)
                link = os.path.join(sub_path_relative).replace(' ', '%20')
                markdown_content += "{}- [{}]({}/)\n".format(indent, dir_name, link)
                listed_directories.add(sub_path)

        # Add files with appropriate indentation
        current_depth = len(root_parts)
        if (len(root_parts) == 1 and root_parts[0] == '.'):
            current_depth = 0
        for f in sorted(included_files):
            print(current_depth)
            file_link = os.path.join(os.path.relpath(root, directory), f).replace(' ', '%20')
            if ((len(root_parts) == 1 and root_parts[0] == '.')):
                markdown_content += "{}- [{}]({})\n".format('  ' * current_depth, f, file_link)
            else:
                markdown_content += "{}  - [{}]({})\n".format('  ' * current_depth, f, file_link)

    return markdown_content


# def generate_index(directory):
#     non_ignored_files = get_git_non_ignored_files(directory)
#     print(non_ignored_files)
#     immediate_folder_name = os.path.basename(os.path.normpath(directory))
#     markdown_content = "# Index of {}\n\n".format(immediate_folder_name)

#     # Sort the files and directories for structured output
#     non_ignored_files.sort()

#     for file_path in non_ignored_files:
#         # Calculate indentation based on directory depth
#         relative_path = os.path.relpath(file_path, directory)
#         depth = relative_path.count(os.sep)
#         indent = '  ' * depth

#         # Create markdown line for file or directory
#         basename = os.path.basename(file_path)
#         markdown_line = "{}- [{}]({})\n".format(indent, basename, file_path)
#         markdown_content += markdown_line

#     return markdown_content



def read_gitignore(directory):
    """
    Reads the .gitignore file in the given directory and returns a list of ignore patterns.
    """
    gitignore_path = os.path.join(directory, '.gitignore')
    if not os.path.exists(gitignore_path):
        return []

    with open(gitignore_path, 'r') as file:
        # Exclude empty lines and lines starting with '#' (comments)
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]


if __name__ == '__main__':
    cli()
