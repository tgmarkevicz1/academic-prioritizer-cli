from src.ingestion.drive_client import get_drive_files
from src.ingestion.calendar_client import get_calendar_events

from src.processing.normalizer import normalize_calendar, normalize_drive
from src.engine.prioritizer import prioritize
from src.interface.cli import display


def main():
    print("Fetching data...")

    events = get_calendar_events()
    files = get_drive_files()

    tasks = []
    tasks += normalize_calendar(events)
    tasks += normalize_drive(files)

    ranked = prioritize(tasks)

    display(ranked)


if __name__ == "__main__":
    main()
