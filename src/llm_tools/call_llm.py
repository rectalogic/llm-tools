# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: Apache-2.0
from functools import cached_property
from typing import Annotated, Optional

import llm

class CallLLM:
    """Chat with a large language model."""

    __name__ = "call_llm"

    @cached_property
    def conversation(self) -> llm.Conversation:
        model = llm.get_model()
        return model.conversation()

    def __call__(
        self,
        prompt: Annotated[str, "The prompt chat text to send to the LLM model."],
    ) -> str:
        return self.conversation.prompt(prompt).text()
