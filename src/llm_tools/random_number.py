# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: Apache-2.0

import random
import sys
from typing import Annotated


def random_number(
    minimum: Annotated[int, "The minimum value of the random number, default is 0"] = 0,
    maximum: Annotated[
        int, f"The maximum value of the random number, default is {sys.maxsize}."
    ] = sys.maxsize,
) -> str:
    """Generate a random number."""
    return str(random.randrange(minimum, maximum))  # noqa: S311
