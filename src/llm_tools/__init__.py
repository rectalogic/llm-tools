# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: Apache-2.0

import click
import llm

from .brave_search import BraveSearch
from .docker_bash import DockerBash
from .google_news import GoogleNews
from .call_llm import CallLLM
from .jina import JinaReadURL

@llm.hookimpl
def register_tools(register):
    register(llm.Tool(GoogleNews()))
    register(llm.Tool(CallLLM()))
    register(llm.Tool(JinaReadURL))

    try:
        register(llm.Tool(BraveSearch()))
    except llm.NeedsKeyException as e:
        click.secho(f"Skipping `brave_search` tool: {str(e)}", dim=True, italic=True, err=True)

    try:
        register(llm.Tool(DockerBash()))
    except ValueError as e:
        click.secho(f"Skipping `bash` tool: {str(e)}", dim=True, italic=True, err=True)
