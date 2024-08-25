import logging
import re
from dataclasses import dataclass
from pathlib import Path

import requests

from config import get_settings


_loger = logging.getLogger(__name__)
_loger.addHandler(logging.StreamHandler())
_loger.addHandler(logging.FileHandler(filename="log.txt"))
_loger.setLevel(logging.DEBUG)


@dataclass
class FailedToDownloadUrl:
    url: str
    status_code: int


def _download_url(url: str) -> tuple[str | None, FailedToDownloadUrl | None]:
    response = requests.get(url)
    if response.status_code != 200:
        return None, FailedToDownloadUrl(url=url, status_code=response.status_code)
    return response.text, None


def _extract_links_from_html(html: str, base_url: str) -> set[str]:
    # https://regex101.com/r/XyZ4eA/1
    return {
        f"{base_url}{_match.group(1)}"
        for _match in re.finditer(r'<a ?href="(\/.+)">(.+)<\/a>', html)
    }


def _get_save_path(url: str) -> Path:
    url = url.lstrip("https://").lstrip("http://").rstrip("/")
    paths = url.split("/")
    if len(paths) == 1:
        return Path(url) / "index.html"
    return Path(url) / "content.html"


def _save_page(url: str, html: str, output_dir: Path, base_url: str) -> Path:
    save_path = output_dir / _get_save_path(url)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    # fix theme - lazy way to just point at the original url
    html = re.sub(r'"(\/theme\/.+)"', rf"{base_url}\g<1>", html)
    with save_path.open("w") as f:
        f.write(html)
    return save_path


def main():
    settings = get_settings()
    settings.output_dir.mkdir(exist_ok=True)

    visited_pages = set()
    pages_to_visit = {settings.url_to_start_with}
    failed_downloads: list[FailedToDownloadUrl] = []
    skipped_urls = set()
    debug_counter = 0

    while pages_to_visit and debug_counter < float("inf"):
        debug_counter += 1
        url = pages_to_visit.pop()
        page_html, error = _download_url(url)
        visited_pages.add(url)
        if error:
            failed_downloads.append(error)
            _loger.warning(
                f"Failed to save page {url}. Status code {error.status_code}"
            )
            continue

        links_on_page = _extract_links_from_html(page_html, settings.base_url)
        for link in links_on_page:
            if link in skipped_urls:
                continue
            for excluded_path in settings.paths_to_exclude:
                if excluded_path in link:
                    _loger.debug(f"Skipping url {link} due to {excluded_path}")
                    skipped_urls.add(link)
                    break
            if (
                link not in skipped_urls
                and link not in visited_pages
                and link not in pages_to_visit
            ):
                pages_to_visit.add(link)

        _save_page(url, page_html, settings.output_dir, settings.base_url)
        _loger.info(f"Visited and saved page {url}")

    _loger.info(f"Downloaded {len(visited_pages)} pages! :3")


if __name__ == "__main__":
    main()
