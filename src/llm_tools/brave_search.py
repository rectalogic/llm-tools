# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: Apache-2.0
from typing import Annotated, Optional

import httpx
from llm.models import _get_key_mixin

# Based on https://docs.llamaindex.ai/en/stable/api_reference/tools/brave_search/


class BraveSearch(_get_key_mixin):
    """Make a query to the Brave Search engine to receive a list of results."""

    __name__ = "brave_search"

    key: Optional[str] = None
    needs_key: Optional[str] = "brave_search"
    key_env_var: Optional[str] = "BRAVE_API_KEY"

    SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

    def __init__(self):
        key = self.get_key()
        if not key:
            raise ValueError("Brave Search requires an API key.")
        self.client = httpx.Client(
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": key,
            }
        )

    def __call__(
        self,
        query: Annotated[str, "The query to be passed to Brave Search."],
        search_lang: Annotated[str, 'The search language preference (ISO 639-1), default is "en".'] = "en",
        num_results: Annotated[int, "The number of search results returned in response, default is 5."] = 5,
    ) -> str:
        response = self.client.get(
            self.SEARCH_URL,
            params={
                "q": query,
                "search_lang": search_lang,
                "count": num_results,
            },
        )
        response.raise_for_status()
        return response.text
