import requests
from pydantic import BaseModel


class Wiki:
    WIKI_URL = "https://en.wikipedia.org/wiki/Special:Random"

    class WikiPage(BaseModel):
        url: str
        article: str

    def __init__(self) -> None:
        self.start_point = self.get_random_wiki_page()
        self.end_point = self.get_random_wiki_page()

    def get_random_wiki_page(self) -> WikiPage:
        url = self._get_random_url()
        article = self._extract_article_from_url(url)
        return self.WikiPage(url=url, article=article)

    def change_start_point(self):
        self.start_point = self.get_random_wiki_page()

    def change_end_point(self):
        self.end_point = self.get_random_wiki_page()

    def _get_random_url(self) -> requests.Response:
        return requests.get(self.WIKI_URL).url

    def _extract_article_from_url(self, url: str) -> str:
        article = url.split("/")[-1]
        article = article.replace("_", " ")
        return article
