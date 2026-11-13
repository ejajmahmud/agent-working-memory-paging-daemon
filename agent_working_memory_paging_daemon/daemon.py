"""Virtual working memory paging daemon with LRU eviction."""
import time
from typing import Dict, List, Optional, Tuple, Any

class MemoryPage:
    def __init__(self, page_id: str, content: Any, dirty: bool = False):
        self.page_id = page_id
        self.content = content
        self.dirty = dirty
        self.last_accessed = time.time()

class MemoryPagingDaemon:
    """Virtual memory manager enforcing max page capacity with LRU swapping."""

    def __init__(self, max_pages_in_ram: int = 4):
        self.max_pages_in_ram = max_pages_in_ram
        self.ram: Dict[str, MemoryPage] = {}
        self.swap_store: Dict[str, Any] = {}
        self.page_fault_count = 0

    def put(self, page_id: str, content: Any):
        if page_id in self.ram:
            page = self.ram[page_id]
            page.content = content
            page.dirty = True
            page.last_accessed = time.time()
            return

        if len(self.ram) >= self.max_pages_in_ram:
            self._evict_lru()

        self.ram[page_id] = MemoryPage(page_id, content, dirty=True)

    def get(self, page_id: str) -> Optional[Any]:
        if page_id in self.ram:
            page = self.ram[page_id]
            page.last_accessed = time.time()
            return page.content

        # Page fault: retrieve from swap
        if page_id in self.swap_store:
            self.page_fault_count += 1
            content = self.swap_store[page_id]
            if len(self.ram) >= self.max_pages_in_ram:
                self._evict_lru()
            self.ram[page_id] = MemoryPage(page_id, content, dirty=False)
            del self.swap_store[page_id]
            return content

        return None

    def _evict_lru(self):
        lru_id = min(self.ram.keys(), key=lambda k: self.ram[k].last_accessed)
        evicted = self.ram.pop(lru_id)
        self.swap_store[lru_id] = evicted.content

    def status(self) -> Dict[str, int]:
        return {
            "ram_pages": len(self.ram),
            "swap_pages": len(self.swap_store),
            "page_faults": self.page_fault_count
        }
