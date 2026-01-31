import time

def prune_old_events(events, window_seconds):
    cutoff = time.time() - window_seconds
    return [(ts, val) for ts, val in events if ts >= cutoff]
