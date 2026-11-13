"""CLI for agent-working-memory-paging-daemon."""
import sys
import argparse
from .daemon import MemoryPagingDaemon

def main():
    parser = argparse.ArgumentParser(description="Agent Working Memory Paging Daemon CLI")
    parser.add_argument("--demo", action="store_true", help="Run memory paging daemon LRU eviction demo")
    args = parser.parse_args()

    if args.demo:
        daemon = MemoryPagingDaemon(max_pages_in_ram=2)
        daemon.put("page1", "AST Parser State")
        daemon.put("page2", "Semantic Token Table")
        print(f"[*] Loaded 2 pages in RAM: {list(daemon.ram.keys())}")
        daemon.put("page3", "Type Checker Cache")
        print(f"[+] Loaded page3 (Triggered LRU Eviction). RAM: {list(daemon.ram.keys())}, Swap: {list(daemon.swap_store.keys())}")
        content = daemon.get("page1")
        print(f"[+] Read page1 (Triggered Page Fault & Restored): content='{content}'")
        print(f"[+] Daemon status: {daemon.status()}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
