from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple


@dataclass
class Ad:
    id: str
    source_url: str
    title: Optional[str]
    image_url: Optional[str]
    published_at: Optional[datetime]
    category: str
    view_count: int
    created_at: datetime
    updated_at: datetime


class AdsStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._ads_by_id: Dict[str, Ad] = {}
        self._id_by_url: Dict[str, str] = {}

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _normalize_url(self, url: str) -> str:
        return url.strip()

    def to_public(self, ad: Ad) -> Dict:
        return {
            "id": ad.id,
            "source_url": ad.source_url,
            "title": ad.title,
            "image_url": ad.image_url,
            "published_at": ad.published_at.isoformat() if ad.published_at else None,
            "category": ad.category,
            "view_count": ad.view_count,
            "created_at": ad.created_at.isoformat(),
            "updated_at": ad.updated_at.isoformat(),
        }

    def get_list(
        self,
        sort: str = "popular",
        category: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> Tuple[List[Dict], int]:
        with self._lock:
            ads: List[Ad] = list(self._ads_by_id.values())

            # Category filter: treat empty/"Все"/"All" as no filter
            if category is not None:
                cat_norm = category.strip().lower()
                if cat_norm and cat_norm not in ("все", "all"):
                    ads = [a for a in ads if (a.category or "").strip().lower() == cat_norm]

            # Popularity strictly equals view_count for now
            if sort == "date":
                # Newest first, None at the end
                ads.sort(
                    key=lambda a: (
                        a.published_at is None,
                        a.published_at or datetime.min.replace(tzinfo=timezone.utc),
                    ),
                    reverse=True,
                )
            else:
                ads.sort(key=lambda a: a.view_count, reverse=True)

            total = len(ads)
            start = max(0, int(offset))
            end = start + max(1, int(limit))
            slice_ads = ads[start:end]
            return [self.to_public(a) for a in slice_ads], total

    def resolve(self, url: str, avito_fetch_fn) -> Tuple[Dict, bool]:
        """Resolve ad by source_url. Returns (ad_dict, created: bool)."""
        normalized = self._normalize_url(url)
        with self._lock:
            existing_id = self._id_by_url.get(normalized)
            if existing_id:
                ad = self._ads_by_id.get(existing_id)
                return self.to_public(ad), False  # type: ignore

        # Not found, create
        fetched = avito_fetch_fn(normalized) or {}
        title = fetched.get("title")
        image_url = fetched.get("image_url")
        category = fetched.get("category") or "Без категории"

        published_at = None
        fetched_published = fetched.get("published_at")
        if isinstance(fetched_published, str) and fetched_published:
            try:
                if fetched_published.endswith("Z"):
                    fetched_published = fetched_published[:-1] + "+00:00"
                dt = datetime.fromisoformat(fetched_published)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                published_at = dt.astimezone(timezone.utc)
            except Exception:
                published_at = None

        now = self._now()
        new_ad = Ad(
            id=str(uuid.uuid4()),
            source_url=normalized,
            title=title,
            image_url=image_url,
            published_at=published_at,
            category=category,
            view_count=0,
            created_at=now,
            updated_at=now,
        )

        with self._lock:
            self._ads_by_id[new_ad.id] = new_ad
            self._id_by_url[normalized] = new_ad.id
            return self.to_public(new_ad), True

    def get_and_increment(self, ad_id: str) -> Optional[Dict]:
        with self._lock:
            ad = self._ads_by_id.get(ad_id)
            if not ad:
                return None
            ad.view_count += 1
            ad.updated_at = self._now()
            return self.to_public(ad)

    def get_public(self, ad_id: str) -> Optional[Dict]:
        """Return ad public dict by id without changing counters."""
        with self._lock:
            ad = self._ads_by_id.get(ad_id)
            if not ad:
                return None
            return self.to_public(ad)


# Singleton in-memory store
ads_store = AdsStore()
