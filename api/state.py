import threading
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional, List


class InMemoryState:
    """
    Thread-safe in-memory storage for users, ads, and comments.
    This data is kept in-process and will be lost on restart.
    """

    def __init__(self) -> None:
        self.users: Dict[str, Dict] = {}
        self.ads: Dict[str, Dict] = {}
        self.comments: Dict[str, Dict] = {}

        self._users_lock = threading.Lock()
        self._ads_lock = threading.Lock()
        self._comments_lock = threading.Lock()

        self._ad_counter = 0
        self._comment_counter = 0

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    # Users
    def user_exists(self, username: str) -> bool:
        with self._users_lock:
            return username in self.users

    def create_user(self, username: str, password_hash: str) -> Dict:
        with self._users_lock:
            if username in self.users:
                raise ValueError("User already exists")
            user = {
                "username": username,
                "password_hash": password_hash,
                "created_at": self.now_iso(),
            }
            self.users[username] = user
            return user

    def get_user(self, username: str) -> Optional[Dict]:
        with self._users_lock:
            return self.users.get(username)

    # Ads (skeleton for future use)
    def next_ad_id(self) -> str:
        with self._ads_lock:
            self._ad_counter += 1
            return str(self._ad_counter)

    def create_ad(self, data: Dict) -> Dict:
        with self._ads_lock:
            ad_id = self.next_ad_id()
            now = self.now_iso()
            ad = {
                "id": ad_id,
                "source_url": data.get("source_url"),
                "title": data.get("title"),
                "image_url": data.get("image_url"),
                "published_at": data.get("published_at"),
                "category": data.get("category"),
                "view_count": data.get("view_count", 0),
                "created_at": now,
                "updated_at": now,
            }
            self.ads[ad_id] = ad
            return ad

    # Comments
    def create_comment(self, data: Dict) -> Dict:
        with self._comments_lock:
            comment_id = str(uuid.uuid4())
            comment = {
                "id": comment_id,
                "ad_id": data.get("ad_id"),
                "username": data.get("username"),
                "text": data.get("text"),
                "created_at": self.now_iso(),
            }
            self.comments[comment_id] = comment
            return comment

    def list_comments_by_ad(self, ad_id: str) -> List[Dict]:
        with self._comments_lock:
            items = [c for c in self.comments.values() if c.get("ad_id") == ad_id]
            items.sort(key=lambda c: c.get("created_at") or "")  # ASC by created_at
            return list(items)


# Global state instance and helper functions used by views
STATE = InMemoryState()


def create_user(username: str, password_hash: str) -> Dict:
    return STATE.create_user(username, password_hash)


def get_user(username: str) -> Optional[Dict]:
    return STATE.get_user(username)


def user_exists(username: str) -> bool:
    return STATE.user_exists(username)


def create_comment(ad_id: str, username: str, text: str) -> Dict:
    return STATE.create_comment({"ad_id": ad_id, "username": username, "text": text})


def list_comments(ad_id: str) -> List[Dict]:
    return STATE.list_comments_by_ad(ad_id)
