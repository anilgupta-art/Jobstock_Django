from App.models import DropdownGroup, DropdownMaster
from typing import List
from threading import Lock

class DropdownRepository:
    _cache = {}
    _lock = Lock()

    @classmethod
    def get_dropdown_items(cls, group_text: str) -> List[DropdownMaster]:
        key = f"dropdown_{group_text}"
        with cls._lock:
            if key in cls._cache:
                return cls._cache[key]
            try:
                group = DropdownGroup.objects.get(text=group_text, is_active=True)
                items = list(DropdownMaster.objects.filter(group=group, is_active=True).order_by('sort_order', 'text'))
                cls._cache[key] = items
                return items
            except DropdownGroup.DoesNotExist:
                cls._cache[key] = []
                return []

    @classmethod
    def clear_cache(cls):
        with cls._lock:
            cls._cache = {}
