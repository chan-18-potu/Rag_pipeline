# confidence_check.py

SIMILARITY_THRESHOLD = 0.7  # tune later

def is_confident(distances):
    if not distances.any():
        return False
    return min(distances) <= SIMILARITY_THRESHOLD
