import os

# Read events from event.txt
events = {}
with open('event.txt', 'r') as f:
    for line in f:
        event_id, event_name, priority = line.strip().split()
        events[event_name] = int(priority)

# Read process events from output.txt
processes = {}
with open('output.txt', 'r') as f:
    # Skip the header row
    next(f)
    for line in f:
        fields = line.strip().split()
        pid = int(fields[6])
        event_name = fields[5]
        if pid not in processes:
            processes[pid] = {'event': '', 'priority': 0}
        if event_name in events and events[event_name] > processes[pid]['priority']:
            processes[pid]['event'] = event_name
            processes[pid]['priority'] = events[event_name]

# Kill processes with high priority events
threshold = 3
for pid in processes:
    if processes[pid]['priority'] > threshold:
        os.kill(pid, 9)
        print(f"Killed process with PID {pid} due to high priority event: {processes[pid]['event']} ({processes[pid]['priority']})")
