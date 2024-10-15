# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: Apache-2.0
from functools import cached_property
from typing import Annotated

import httpx


class JinaReadURL:
    """Read the contents of a URL converted to markdown."""

    __name__ = "read_url"

    # https://jina.ai/reader/
    JINA_READER_URL = "https://r.jina.ai/"

    @cached_property
    def client(self) -> httpx.Client:
        return httpx.Client(
            headers={"Accept-Encoding": "gzip"}
        )

    def __call__(
        self,
        url: Annotated[str, "The URL to be read."],
    ) -> str:
        response = self.client.get(self.JINA_READER_URL + url)
        response.raise_for_status()
        return response.text
