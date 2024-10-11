# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: Apache-2.0

import json
import shutil
import subprocess
from typing import Annotated, Optional


class DockerBash:
    """Execute a `bash` shell command on the local Linux system."""

    __name__ = "bash"
    container: Optional[str] = None

    def __init__(self):
        self.docker = shutil.which("docker")
        if not self.docker:
            raise ValueError("Unable to find docker command")
        completed = subprocess.run(  # noqa: S603
            [self.docker, "run", "--rm", "--detach", "ubuntu:latest", "/usr/bin/sleep", "infinity"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.container = completed.stdout.strip()

    def __call__(self, command_line: Annotated[str, "A `bash` shell command line to execute."]) -> str:
        completed = subprocess.run(  # noqa: S603
            [self.docker, "exec", self.container, "bash", "-c", command_line],
            capture_output=True,
            text=True,
        )

        result = {"stdout": completed.stdout, "stderr": completed.stderr}
        if completed.returncode != 0:
            result["is_error"] = True
        return json.dumps(result)

    def __del__(self):
        if self.container:
            subprocess.run([self.docker, "stop", self.container])
