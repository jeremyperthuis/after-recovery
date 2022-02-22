import click
import os
from src.process_files import processFiles
from src.utils import timeit

@click.command()
# @click.option('--path', prompt='Folder path to analyze.')
@click.option('--group_by_extension', is_flag=True, help="Will group all files by extension in separate folder.")
@click.option('--source_dir', envvar='PATHS', multiple=False,
              type=click.Path())
@click.option('--dest_dir', envvar='PATHS', multiple=False,
              type=click.Path(), required=False)
@timeit
def main(source_dir, dest_dir, group_by_extension):
    processFiles(sourcedir=source_dir, destdir=dest_dir, group_by_extension=group_by_extension)


if __name__ == '__main__':

    main()
    print("OK")