import requests
from pydantic import BaseModel


class Wiki:
    class WikiPage(BaseModel):
        url: str
        article: str

    def __init__(self) -> None:
        self.start_point = self.get_random_wiki_page()
        self.end_point = self.get_random_wiki_page()

    def get_random_wiki_page(self) -> WikiPage:
        url = self.get_random_url()
        article = self.extract_article_from_url(url)
        return self.WikiPage(url=url, article=article)

    def get_random_url(self) -> requests.Response:
        return requests.get("https://en.wikipedia.org/wiki/Special:Random").url

    def extract_article_from_url(self, url: str) -> str:
        article = url.split("/")[-1]
        article = article.replace("_", " ")
        return article

    def change_start_point(self):
        self.start_point = self.get_random_wiki_page()

    def change_end_point(self):
        self.end_point = self.get_random_wiki_page()
