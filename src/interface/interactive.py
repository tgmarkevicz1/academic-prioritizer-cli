from datetime import datetime, timezone
from src.processing.scorer import score
from src.state import dismissed


def _fmt_time(dt):
    """Format a datetime to a readable local time string. Cross-platform safe."""
    local = dt.astimezone()
    hour = local.strftime("%I").lstrip("0") or "0"
    day  = local.strftime("%d").lstrip("0") or "0"
    return local.strftime(f"{hour}:%M %p, %a %b {day}")


def _format_event_time(event_time):
    if not event_time:
        return ""
    return _fmt_time(event_time)


def _format_deadline(deadline):
    if not deadline:
        return "no due date"
    now = datetime.now(timezone.utc)
    days_left = (deadline - now).days
    date_str = _fmt_time(deadline).split(",")[1].strip()
    if days_left < 0:
        return f"{date_str} (overdue)"
    elif days_left == 0:
        return f"{date_str} (due today)"
    elif days_left == 1:
        return f"{date_str} (tomorrow)"
    else:
        return f"{date_str} ({days_left}d)"


def _priority_label(s):
    if s >= 10:
        return "HIGH"
    elif s >= 4:
        return "MED"
    elif s >= 0:
        return "LOW"
    else:
        return "EVENT"


def display(tasks):
    if not tasks:
        print("\nNo tasks or events to display.")
        return

    while True:
        print("\n=== TODAY'S PRIORITIES ===\n")

        task_items  = [t for t in tasks if t.source == "task"]
        event_items = [t for t in tasks if t.source == "event"]

        numbered = []

        if task_items:
            print("  TASKS")
            print("  " + "-" * 44)
            for t in task_items:
                s = score(t)
                label = _priority_label(s)
                idx = len(numbered) + 1
                numbered.append(t)

                deadline_str = _format_deadline(t.deadline)
                match_str = ""
                if t.matched_files:
                    files_preview = ", ".join(t.matched_files[:2])
                    match_str = f"  → {files_preview}"

                list_str = f"[{t.list_title}] " if t.list_title else ""
                print(f"  {idx:>2}. [{label}] {list_str}{t.name}")
                print(f"        due: {deadline_str}{match_str}")

        if event_items:
            print()
            print("  UPCOMING  (meetings & classes)")
            print("  " + "-" * 44)
            for t in event_items:
                idx = len(numbered) + 1
                numbered.append(t)
                time_str = _format_event_time(t.event_time)
                print(f"  {idx:>2}. [EVENT] {t.name}  @  {time_str}")

        print()
        print("  Commands: <number> to select  |  q to quit")
        print()

        raw = input("  > ").strip().lower()

        if raw == "q":
            print("Bye!")
            break

        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(numbered):
                selected = numbered[idx - 1]
                _item_menu(selected)
                tasks = dismissed.filter_hidden(tasks)
                if not tasks:
                    print("\nAll items hidden.")
                    break
            else:
                print(f"  Invalid number. Enter 1–{len(numbered)}.")
        else:
            print("  Unknown input. Enter a number or 'q'.")


def _item_menu(task):
    print()
    print(f"  Selected : {task.name}")
    print(f"  ID       : {task.task_id or '(none)'}")
    print()
    print("  [h] Hide permanently  |  [b] Back")
    print()

    raw = input("  > ").strip().lower()

    if raw == "h":
        if task.task_id:
            dismissed.hide(task.task_id, task.name)
            print(f"  Hidden: \"{task.name}\"")
            print(f"  To unhide later: python -m src.main -uh {task.task_id}")
        else:
            print("  Cannot hide — this item has no ID.")
    elif raw == "b":
        pass
    else:
        print("  Unknown input, going back.")
