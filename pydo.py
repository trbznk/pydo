import os
import re
import argparse

from dataclasses import dataclass
from pathlib import Path

# TODO: first example
# TODOO: second example
# TODOOO: third example

parser = argparse.ArgumentParser("pydo")
parser.add_argument("target", type=Path)
args = parser.parse_args()

# TODO: inverse priority
TARGET = args.target
SUPPORTED_TYPES = ["py"]


class Colors:
    BLANK = ""
    RED = "\033[0;31m"
    YELLOW = "\033[1;33m"
    END = "\033[0m"


@dataclass
class TODO:
    text: str
    priority: int
    path: str
    line: int

    def __str__(self):
        if self.priority == 1:
            color = Colors.BLANK
        elif self.priority == 2:
            color = Colors.YELLOW
        else:
            color = Colors.RED
        return f"{color}{self.path}:{self.line} {self.text}{Colors.END}"


def parse_file(path):
    results = []
    prog = re.compile("# TODO+: .+$")
    with open(path) as f:
        for i, line in enumerate(f.read().splitlines()):
            x = re.search(prog, line)
            if x:
                raw = x.group()
                text = raw.split(":", 1)[-1][1:]
                priority = len(raw.split(":", 1)[0].split("D")[-1])
                # TODOOO: truncate the path if to long
                results.append(TODO(
                    text,
                    priority,
                    path,
                    i+1
                ))
    return results


todos = []

if TARGET.is_file():
    todos += parse_file(TARGET)
else:
    for dirpath, dirnames, filenames in os.walk(TARGET):
        for filename in filenames:
            filetype = filename.rsplit(".", 1)[-1]
            if filetype in SUPPORTED_TYPES:
                path = os.path.join(dirpath, filename)
                todos += parse_file(path)


todos.sort(key=lambda todo: todo.priority, reverse=True)

for todo in todos:
    print(todo)
