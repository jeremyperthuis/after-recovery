import click
import os
from src.module1 import module1
from src.module2 import module2
import logging
logger = logging.getLogger(__name__)
# Logs
if __name__ == '__main__':
    m = module1()
    m.increment_number()
    f = module2()
    f.increment_number()
    logger.info("test")


#
#
# @click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name', help='The person to greet.')
# @click.option('--verbose', is_flag=True, help="Will print verbose messages.")
# def hello(count, name, verbose):
#     for x in range(count):
#         click.echo(f"Hello {name}!")
#     if verbose:
#         print("VERBOSE")
#
#
# if __name__ == '__main__':
#     LOG.info("test")
#     hello()