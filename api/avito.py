import re
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
from datetime import datetime, timezone


DEFAULT_CATEGORY = "Без категории"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
)


def _normalize_space(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = re.sub(r"\s+", " ", value)
    return text.strip()


def _try_parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    v = value.strip()
    # Try ISO 8601 first
    try:
        # Support trailing 'Z'
        if v.endswith("Z"):
            v = v[:-1] + "+00:00"
        dt = datetime.fromisoformat(v)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass

    # Try common patterns like 'YYYY-MM-DD HH:MM:SS'
    for fmt in [
        "%Y-%m-%d %H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d.%m.%Y %H:%M",
        "%d.%m.%Y",
    ]:
        try:
            dt = datetime.strptime(v, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception:
            continue
    return None


def fetch_avito_data(url: str) -> Dict[str, Optional[str]]:
    """
    Fetch and parse data from an Avito ad page.
    Strategy:
    - title: meta property="og:title" or <title>
    - image_url: meta property="og:image" or main image tag
    - published_at: try meta tags (itemprop="datePublished", property="article:published_time", name="date")
    - category: breadcrumbs/metadata else DEFAULT_CATEGORY
    Returns keys: title, image_url, published_at (ISO string or None), category
    """
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=6,
            allow_redirects=True,
        )
        resp.raise_for_status()
    except Exception:
        return {
            "title": None,
            "image_url": None,
            "published_at": None,
            "category": DEFAULT_CATEGORY,
        }

    try:
        soup = BeautifulSoup(resp.text, "html.parser")

        # Title
        title = None
        og_title = soup.find("meta", attrs={"property": "og:title"})
        if og_title and og_title.get("content"):
            title = og_title.get("content")
        elif soup.title and soup.title.string:
            title = soup.title.string
        title = _normalize_space(title) if title else None

        # Image
        image_url = None
        og_image = soup.find("meta", attrs={"property": "og:image"})
        if og_image and og_image.get("content"):
            image_url = og_image.get("content")
        if not image_url:
            # Try common image selectors
            img = soup.find("img", attrs={"itemprop": "image"}) or soup.find("img")
            if img:
                image_url = img.get("src") or img.get("data-src") or None
        image_url = image_url.strip() if isinstance(image_url, str) else image_url

        # Published at
        published_at_dt = None
        for selector in [
            ("meta", {"itemprop": "datePublished"}, "content"),
            ("meta", {"property": "article:published_time"}, "content"),
            ("meta", {"name": "date"}, "content"),
            ("time", {"itemprop": "datePublished"}, "datetime"),
        ]:
            tag = soup.find(selector[0], attrs=selector[1])
            if tag and tag.get(selector[2]):
                published_at_dt = _try_parse_datetime(tag.get(selector[2]))
                if published_at_dt:
                    break
        published_at = published_at_dt.isoformat() if published_at_dt else None

        # Category
        category = None
        # Try breadcrumbs
        breadcrumb = soup.find(attrs={"data-marker": "breadcrumb"})
        if breadcrumb:
            items = breadcrumb.find_all("a")
            if items:
                category = _normalize_space(items[-1].get_text())
        if not category:
            og_type = soup.find("meta", attrs={"property": "og:type"})
            if og_type and og_type.get("content"):
                category = _normalize_space(og_type.get("content"))
        if not category:
            category = DEFAULT_CATEGORY

        return {
            "title": title,
            "image_url": image_url,
            "published_at": published_at,
            "category": category,
        }
    except Exception:
        return {
            "title": None,
            "image_url": None,
            "published_at": None,
            "category": DEFAULT_CATEGORY,
        }
