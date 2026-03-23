from src.processing.scorer import score

def prioritize(tasks):
    return sorted(tasks, key=lambda t: score(t), reverse=True)
