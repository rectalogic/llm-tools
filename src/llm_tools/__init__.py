# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: Apache-2.0

import click
import llm

from .brave_search import BraveSearch
from .random_number import random_number


@llm.hookimpl
def register_tools(register):
    register(random_number)
    try:
        register(llm.Tool(BraveSearch()))
    except llm.NeedsKeyException as e:
        click.secho(f"Skipping brave_search tool: {str(e)}", dim=True, italic=True, err=True)
