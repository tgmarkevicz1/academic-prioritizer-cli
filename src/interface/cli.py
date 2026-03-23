from src.processing.scorer import score

def display(tasks):
    print("\n=== TODAY'S PRIORITIES ===\n")

    for task in tasks[:10]:
        s = score(task)

        if s >= 10:
            level = "HIGH"
        elif s >= 5:
            level = "MED"
        else:
            level = "LOW"

        print(f"[{level}] {task.name} (score: {s})")
