#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

from util.gum import gum_input, gum_choose



def main():
    # install gum and gh
    command = ['brew', 'install', 'gum', 'gh']
    subprocess.run(command, stdout=subprocess.PIPE, text=True)

    # install pip reqs
    command = ['pip3', 'install', '-r', 'requirements.txt']
    subprocess.run(command, stdout=subprocess.PIPE, text=True)

    _, env_choice = gum_choose(choices=['.bashrc', '.zshrc', 'other'], message="Choose your env setup file")
    if env_choice == 'other':
        env_file_path = gum_input(message="Please enter the full path to your env config file", default="~/.zshrc")
    else:
        env_file_path = f'{Path.home()}/{env_choice}'

    with open(env_file_path, 'r') as env_file:
        skip_env_file_write = 'export BOLD=false' in env_file.read()

    if not skip_env_file_write:
        with open(env_file_path, 'a') as env_file:
            # stupid gum constants
            env_file.write('export BOLD=false\n')
            env_file.write('export UNDERLINE=false\n')

            # put the scripts file in path
            script_folder = os.path.dirname(os.path.realpath(__file__))
            env_file.write(f'export PATH="$PATH:{script_folder}"\n')
    
    command = ['gh', 'auth', 'login']
    subprocess.run(command)


if __name__ == "__main__":
    main()
