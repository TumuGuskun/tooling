from dataclasses import dataclass, field
import subprocess
import sys
from typing import Any, Optional, Union, List, Tuple, Dict


@dataclass
class GumCommand:
    base_command: str
    flags: List[str] = field(default_factory=list)
    kv_pairs: Dict[str, str] = field(default_factory=dict)
    gum_command_args: List[str] = field(default_factory=list)

    @property
    def command(self) -> List[str]:
        command = ["env", "BOLD=false", "UNDERLINE=false", "gum"]
        command.append(self.base_command)
        command.extend(self.flags)
        command.extend([f"{key}={value}" for key, value in self.kv_pairs.items()])
        command.extend(self.gum_command_args)
        return command

    def add_flag(self, flag: str) -> None:
        self.flags.append(flag)

    def add_key_value_pair(self, key: str, value: str) -> None:
        self.kv_pairs[key] = value

    def add_command_args(self, *args: str) -> None:
        self.gum_command_args.extend(args)


def clear_last_line():
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()


def gum_confirm(message: Optional[str] = None) -> bool:
    gum_command = GumCommand(base_command="confirm")
    if message:
        gum_command.add_command_args(message)

    result = subprocess.run(gum_command.command).returncode
    return result == 0


def gum_choose(
    choices: List[Any],
    message: Optional[str] = None,
    limit: int = 1,
    minimum: int = 1,
) -> Tuple[Optional[int], Optional[Union[str, List[str]]]]:
    norm_choices = [str(c).strip() for c in choices]
    if message:
        print(message)
    gum_command = GumCommand(base_command="choose")
    if limit > 0:
        gum_command.add_key_value_pair(key="--limit", value=str(limit))
    else:
        gum_command.add_flag(flag="--no-limit")
    gum_command.add_command_args(*norm_choices)
    result = subprocess.run(
        gum_command.command, stdout=subprocess.PIPE, text=True
    ).stdout.strip()
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
    gum_command = GumCommand(base_command="input")
    if message:
        gum_command.add_key_value_pair(key="--prompt", value=f"{message}: ")
    if default:
        gum_command.add_key_value_pair(key="--placeholder", value=default)
    result = subprocess.run(
        gum_command.command, stdout=subprocess.PIPE, text=True
    ).stdout.strip()
    return result or str(default)
