# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: Apache-2.0

import json
import shutil
import subprocess
from typing import Annotated


class DockerBash:
    """Execute a `bash` shell command on the local Linux system."""

    __name__ = "bash"

    def __init__(self):
        self.docker = shutil.which("docker")
        if not self.docker:
            raise ValueError("docker is not installed")
        self.process = subprocess.Popen( # noqa: S603
            [self.docker, "run", "--rm", "-i", "ubuntu:latest", "bash"],
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.process.stdin.write("hostname\n")
        self.process.stdin.flush()
        self.container = self.process.stdout.readline().strip()

    def __call__(self, command_line: Annotated[str, "A `bash` shell command line to execute."]) -> str:
        completed = subprocess.run( # noqa: S603
            [self.docker, "exec", "-i", self.container, "bash", "-c", command_line],
            check=True,
            capture_output=True,
            text=True,
        )

        print("result", completed.stdout, completed.stderr)
        return json.dumps({"stdout": completed.stdout, "stderr": completed.stderr})

    def __del__(self):
        if self.process:
            self.process.terminate()
