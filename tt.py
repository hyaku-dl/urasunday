# import re
# import inquirer

# # def vfn(answers, current):
# #     try:
# #         inquirer.Path(
# #             "config_file",
# #             "/home/whine/whi_ne/1/coding",
# #             path_type=inquirer.Path.DIRECTORY
# #         ).validate(current)
# #     except inquirer.errors.ValidationError:
# #         raise ValueError("Invalid path")

# # ip = inquirer.text(
# #     message="Enter path to dowload it to",
# #     validate = vfn
# # )

# # print(ip)

# questions = [
#     inquirer.Path(
#         "path",
#         "/home/whine/whi_ne/1/coding/",
#         path_type=inquirer.Path.DIRECTORY
#     )
# ]

# answers = inquirer.prompt(questions)

# print(answers)

import os
import sys

import click

if sys.platform == "win32":
    ddir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'Manga')
else:
    ddir = os.path.join(os.path.expanduser('~'), "Manga")

@click.command()
@click.option('--name', prompt=True, default=ddir)
def hello(name=ddir):
    click.echo(f"Hello {name}!")

hello()