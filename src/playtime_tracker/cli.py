"""Command-line bootstrap for the tracker daemon and one-shot commands."""
from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from playtime_tracker.services.tracker_service import TrackerService
from playtime_tracker.services.library_service import LibraryService
from playtime_tracker.config.settings import load_settings


def _configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ptlm", description=__doc__)
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("daemon", help="run the background playtime tracker")
    sub.add_parser("scan", help="rescan all configured stores")

    show = sub.add_parser("show", help="print the merged library")
    show.add_argument("--min-minutes", type=int, default=0)
    return parser


async def _run(args: argparse.Namespace) -> int:
    settings = load_settings()
    if args.command == "daemon":
        tracker = TrackerService(settings)
        await tracker.run_forever()
        return 0
    if args.command == "scan":
        library = LibraryService(settings)
        count = await library.rescan_all()
        print(f"imported {count} titles")
        return 0
    if args.command == "show":
        library = LibraryService(settings)
        for row in await library.iter_library(min_minutes=args.min_minutes):
            hours = row.total_seconds / 3600
            print(f"{hours:9.1f}h  {row.store:8s}  {row.title}")
        return 0
    return 2


def main() -> int:
    args = _build_parser().parse_args()
    _configure_logging(args.verbose)
    try:
        return asyncio.run(_run(args))
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())