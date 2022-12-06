#!/usr/bin/env python3
import os
import subprocess


def main():
    # install gum and gh
    command = ["brew", "install", "--quiet", "gum", "gh"]
    subprocess.run(command, stdout=subprocess.PIPE, text=True)

    # install pip reqs
    command = ["pip3", "install", "-r", "python_requirements.txt"]
    subprocess.run(command, stdout=subprocess.PIPE, text=True)

    env_file_path = input(
        "Please enter your full path to your .zshrc/.bashrc. e.g. /Users/timgaskin/.zshrc: "
    )

    with open(env_file_path, "r") as env_file:
        skip_env_file_write = "export BOLD=false" in env_file.read()

    if not skip_env_file_write:
        with open(env_file_path, "a") as env_file:
            # stupid gum constants
            env_file.write("export BOLD=false\n")
            env_file.write("export UNDERLINE=false\n")

            # put the scripts file in path
            script_folder = os.path.dirname(os.path.realpath(__file__))
            env_file.write(f'export PATH="$PATH:{script_folder}"\n')

        command = ["source", env_file_path]
        subprocess.run(command, stdout=subprocess.PIPE, text=True)

    command = ["gh", "auth", "login"]
    subprocess.run(command)


if __name__ == "__main__":
    main()
