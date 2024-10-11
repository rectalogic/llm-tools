import enum
import json
from functools import cached_property
from typing import Annotated, Optional

from gnews import GNews


class NewsType(enum.Enum):
    KEYWORD = "keyword"
    LOCATION = "location"
    WEBSITE = "website"
    TOP_NEWS = "top_news"


class GoogleNews:
    """Query Google News to retrieve current news articles."""

    __name__ = "google_news"

    @cached_property
    def google_news(self) -> GNews:
        return GNews()

    def __call__(
        self,
        news_type: Annotated[
            NewsType,
            "The type of news to search for. "
            "`keyword` means `query` is a simple keyword to search. "
            "`location` means `query` is a city, state or country. "
            "`website` means query is a news website domain e.g. `cnn.com`. "
            "`top_news` does not require a `query`, it returns top news stories.",
        ],
        query: Annotated[
            Optional[str], "The search query term. The value depends on the specified `news_type`."
        ] = None,
    ):
        news_type_ = NewsType(news_type)
        if news_type_ is NewsType.KEYWORD:
            news = self.google_news.get_news(query)
        elif news_type_ is NewsType.LOCATION:
            news = self.google_news.get_news_by_location(query)
        elif news_type_ is NewsType.WEBSITE:
            news = self.google_news.get_news_by_site(query)
        elif news_type_ is NewsType.TOP_NEWS:
            news = self.google_news.get_top_news()
        else:
            raise ValueError(f"Invalid `news_type` {news_type}")
        return json.dumps(news)
