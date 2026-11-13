"""Writes events.json: 30 JSON log lines (every 3rd is a 500 ERROR) for aws logs put-log-events."""
import json
import random
import time

now = int(time.time() * 1000)
events = []
for i in range(1, 31):
    code = 500 if i % 3 == 0 else 200
    msg = {
        "level": "ERROR" if code == 500 else "INFO",
        "statusCode": code,
        "path": random.choice(["/api/orders", "/api/users", "/health"]),
        "latencyMs": random.randint(40, 1500),
        "user": random.choice(["alice", "bob", "carol"]),
    }
    events.append({"timestamp": now + i, "message": json.dumps(msg)})

with open("events.json", "w") as f:
    json.dump(events, f)
print("wrote", len(events), "events (10 with statusCode 500)")
