import argparse
import sys

from src.ingestion.drive_client import get_drive_files
from src.ingestion.calendar_client import get_calendar_events
from src.ingestion.tasks_client import get_all_tasks

from src.processing.normalizer import normalize_calendar, normalize_drive, normalize_tasks
from src.processing.matcher import match_files_to_tasks
from src.engine.prioritizer import prioritize
from src.interface.interactive import display
from src.state import dismissed


def build_parser():
    parser = argparse.ArgumentParser(
        prog="academic-prioritizer",
        description="Prioritize your academic tasks from Google Tasks, Calendar, and Drive.",
        add_help=True,
    )
    parser.add_argument("--hide", "-ht", metavar="ID", help="Permanently hide an item by its ID.")
    parser.add_argument("--unhide", "-uh", metavar="ID", help="Unhide a previously hidden item by its ID.")
    parser.add_argument("--list-hidden", action="store_true", help="List all permanently hidden items.")
    return parser


def cmd_hide(task_id):
    dismissed.hide(task_id, label="(hidden via CLI)")
    print(f"Hidden: {task_id}")


def cmd_unhide(task_id):
    success = dismissed.unhide(task_id)
    if success:
        print(f"Unhidden: {task_id}")
    else:
        print(f"ID not found in hidden list: {task_id}")


def cmd_list_hidden():
    hidden = dismissed.get_all_hidden()
    if not hidden:
        print("No hidden items.")
        return
    print("\nHidden items:")
    print("-" * 40)
    for task_id, label in hidden.items():
        print(f"  {task_id}  —  {label or '(no label)'}")


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.list_hidden:
        cmd_list_hidden()
        sys.exit(0)

    if args.hide:
        cmd_hide(args.hide)
        sys.exit(0)

    if args.unhide:
        cmd_unhide(args.unhide)
        sys.exit(0)

    print("Fetching data...")

    raw_tasks = get_all_tasks()
    events    = get_calendar_events()
    files     = get_drive_files()

    tasks       = normalize_tasks(raw_tasks)
    event_tasks = normalize_calendar(events)
    drive_files = normalize_drive(files)

    all_tasks = tasks + event_tasks
    match_files_to_tasks(all_tasks, drive_files)

    visible = dismissed.filter_hidden(all_tasks)
    ranked  = prioritize(visible)
    display(ranked)


if __name__ == "__main__":
    main()
