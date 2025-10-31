import threading
from datetime import datetime, timezone
from typing import Dict, Optional


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

    # Comments (skeleton for future use)
    def next_comment_id(self) -> str:
        with self._comments_lock:
            self._comment_counter += 1
            return str(self._comment_counter)

    def create_comment(self, data: Dict) -> Dict:
        with self._comments_lock:
            comment_id = self.next_comment_id()
            comment = {
                "id": comment_id,
                "ad_id": data.get("ad_id"),
                "username": data.get("username"),
                "text": data.get("text"),
                "created_at": self.now_iso(),
            }
            self.comments[comment_id] = comment
            return comment


# Global state instance and helper functions used by views
STATE = InMemoryState()


def create_user(username: str, password_hash: str) -> Dict:
    return STATE.create_user(username, password_hash)


def get_user(username: str) -> Optional[Dict]:
    return STATE.get_user(username)


def user_exists(username: str) -> bool:
    return STATE.user_exists(username)
