#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
import sys


RELENG_DIR = Path(__file__).parent.resolve()
ROOT_DIR = RELENG_DIR.parent


@dataclass
class FridaVersion:
    name: str
    major: int
    minor: int
    micro: int
    nano: int
    commit: str


def main(argv: list[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", type=Path, default=ROOT_DIR)
    args = parser.parse_args()

    version = detect(args.repo)
    print(version.name)


def detect(repo: Path) -> FridaVersion:
    description = subprocess.run(["git", "describe", "--tags", "--always", "--long"],
                                 cwd=repo,
                                 capture_output=True,
                                 encoding="utf-8").stdout

    tokens = description.strip().replace("-", ".").split(".")
    if len(tokens) > 1:
        (major, minor, micro, nano, commit) = tokens
        major = int(major)
        minor = int(minor)
        micro = int(micro)
        nano = int(nano)
        if nano > 0:
            micro += 1
    else:
        major = 0
        minor = 0
        micro = 0
        nano = 0
        commit = tokens[0]

    if nano == 0 and len(tokens) != 1:
        version_name = f"{major}.{minor}.{micro}"
    else:
        version_name = f"{major}.{minor}.{micro}-dev.{nano - 1}"

    return FridaVersion(version_name, major, minor, micro, nano, commit)


if __name__ == "__main__":
    main(sys.argv)
