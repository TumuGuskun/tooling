import subprocess
import sys
from typing import Any, Optional, Union, List


def clear_last_line():
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()


def gum_confirm(message: Optional[str] = None) -> bool:
    command = ["gum", "confirm"]
    if message:
        command.append(message)

    result = subprocess.run(command).returncode
    return result == 0


def gum_choose(
    choices: List[Any],
    message: Optional[str] = None,
    limit: int = 1,
    minimum: int = 1,
) -> tuple[Optional[int], Optional[Union[str, List[str]]]]:
    norm_choices = [str(c).strip() for c in choices]
    if message:
        print(message)
    command = ["gum", "choose"]
    if limit > 0:
        command.append(f"--limit={limit}")
    else:
        command.append("--no-limit")
    command.extend(norm_choices)
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True).stdout.strip()
    if message:
        clear_last_line()
    if len(list(filter(bool, result.split("\n")))) < minimum:
        print(f"You must select at least {minimum} choice(s)")
        sys.exit(1)
    if not result:
        return None, None
    if limit == 1:
        return norm_choices.index(result), result
    else:
        return None, result.split("\n")


def gum_input(message: Optional[str] = None, default: Optional[str] = None) -> str:
    command = ["gum", "input"]
    if message:
        command.append(f"--prompt={message}: ")
    if default:
        command.append(f"--placeholder={default}")
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True).stdout.strip()
    return result or str(default)