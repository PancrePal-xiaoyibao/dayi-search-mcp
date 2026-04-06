from typing import Protocol


class DetailProvider(Protocol):
    type_name: str

    def parse_detail_html(self, *, detail_url: str, html: str, keyword: str) -> dict:
        ...
