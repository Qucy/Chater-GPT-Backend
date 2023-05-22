from pydantic import BaseModel
from typing import Optional, List


class Source(BaseModel):
    id: Optional[str]
    name: str

class Article(BaseModel):
    source: Source
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    urlToImage: Optional[str]
    publishedAt: str
    content: Optional[str]

    def __str__(self):
        author = self.author if self.author else "unknown"
        return "title:[" + self.title + "]; author:[" +  author + "]; published at:[" + self.publishedAt + "];"

class News(BaseModel):
    articles: List[Article]