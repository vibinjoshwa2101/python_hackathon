"""
PyMongo utility — database connection and collection helper.
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

_client = None


def get_client() -> MongoClient:
    """Return a cached MongoClient instance."""
    global _client
    if _client is None:
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        _client = MongoClient(uri)
        try:
            _client.admin.command("ping")
        except ConnectionFailure as exc:
            raise RuntimeError("MongoDB is not reachable. Check MONGO_URI.") from exc
    return _client


def get_db():
    """Return the main database handle."""
    db_name = os.getenv("MONGO_DB_NAME", "tourist_db")
    return get_client()[db_name]


def get_collection(name: str):
    """
    Return a collection by name, creating it dynamically if it doesn't exist.
    MongoDB creates collections lazily, so this just returns the collection object.
    """
    db = get_db()
    return db[name]


def list_collections() -> list[str]:
    """Return all collection names in the database."""
    return get_db().list_collection_names()


def drop_collection(name: str) -> None:
    """Drop a collection by name (use with caution)."""
    get_db().drop_collection(name)
