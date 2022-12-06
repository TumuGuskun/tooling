#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from util.gum import gum_choose, gum_input


def main():
    # install brew reqs
    with open("brew_requirements.txt", "r") as brew_file:
        command = ["brew", "install", "--quiet"]
        command.extend([package.strip() for package in brew_file.readlines()])
        subprocess.run(command, stdout=subprocess.PIPE, text=True)

    # install pip reqs
    command = ["pip3", "install", "-r", "python_requirements.txt"]
    subprocess.run(command, stdout=subprocess.PIPE, text=True)

    _, env_choice = gum_choose(
        choices=[".bashrc", ".zshrc", "other"], message="Choose your env setup file"
    )

    if env_choice == "other":
        env_file_path = gum_input(
            message="Please enter the full path to your env config file",
            default="~/.zshrc",
        )
    else:
        env_file_path = f"{Path.home()}/{env_choice}"

    script_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts")
    )
    with open(env_file_path, "r") as env_file:
        skip_env_file_write = script_folder in env_file.read()

    if not skip_env_file_write:
        with open(env_file_path, "a") as env_file:
            # put the scripts file in path
            env_file.write(f'export PATH="$PATH:{script_folder}"\n')

    command = ["gh", "auth", "login"]
    subprocess.run(command)


if __name__ == "__main__":
    main()
