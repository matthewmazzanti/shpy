from typing import Any, Self
import subprocess as sp
import io
import sys
import json
from shutil import which

class Builder:
    def __init__(self, *args: str):
        self.cmd: tuple[*str] = args
        self.pipe: Any = None
        self.out: Any = sys.stdout

    def __getattr__(self, cmd) -> Self:
        return Builder(*self.cmd, cmd)

    def __call__(self, *args: str) -> Self:
        self.cmd = (*self.cmd, *args)
        return self

    def __str__(self) -> str:
        return stdout(self)

    def __or__(self, other) -> Self:
        if isinstance(other, io.IOBase):
            self.out = other
            return self

        return other.__ror__(self)

    def __ror__(self, other) -> Self:
        self.pipe = other
        return self

def run(b: Builder):
    sp.run(
        b.cmd,
        check=True,
        stdin=pipe_from(b.pipe),
        stdout=b.out
    )


def stdout(b: Builder) -> str:
    proc = sp.run(
        b.cmd,
        check=True,
        stdin=pipe_from(b.pipe),
        stdout=sp.PIPE
    )

    return proc.stdout.decode()

def run_json(b: Builder) -> Any:
    # TODO: Use a file for this...
    return json.loads(str(b))

def show(b: Builder) -> str:
    res = " ".join(b.cmd)
    if b.pipe and isinstance(b.pipe, Builder):
        res = f"{show(b.pipe)} | {res}"

    return res

def pipe_from(b: Builder | io.IOBase) -> Any:
    if b is None:
        return None

    if isinstance(b, io.IOBase):
        return b

    proc = sp.Popen(
        b.cmd,
        stdin=pipe_from(b.pipe),
        stdout=sp.PIPE
    )
    return proc.stdout

class ExecutableError(Exception):
    pass

class DSL:
    def __getattr__(self, cmd):
        exe = which(cmd)
        if exe is None:
            raise ExecutableError(f'No such command: "{cmd}"')
        return Builder(exe)

builder = DSL()
