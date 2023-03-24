import os
import signal
import time
import subprocess

# read the events file and create a dictionary to store the priorities
events_file = "event.txt"
event_priorities = {}
with open(events_file) as f:
    for line in f:
        if not line.strip():  # skip empty lines
            continue
        event_id, event_name = line.strip().split()
        event_priorities[event_name] = int(event_id)

# create the logs directory if it doesn't exist
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# process the output file continuously
output_file = "output.txt"
while True:
    with open(output_file) as f:
        try:
            next(f)  # skip the header row
        except StopIteration:
            # file is empty or has been completely read, wait and continue
            time.sleep(0.1)
            continue
        high_priority_event_detected = False
        for line in f:
            fields = line.strip().split()
            pid = int(fields[6])
            event = fields[4]
            print(pid)
            event_priority = event_priorities.get(event, 0)
            log_file = os.path.join(logs_dir, f"{pid}.log")
            with open(log_file, "a") as log:
                log.write(f"{event}\n")
            if event_priority > 0:
                print(f"Process {pid} generated high priority event: {event}")
                high_priority_event_detected = True
        if high_priority_event_detected:
            print("Stopping process...")
            subprocess.run(["kill", "-STOP", str(pid)])
            print("Process stopped")
            print("Do you want to continue its execution? (y/n)")
            response = input().strip().lower()
            if response == "y":
                subprocess.run(["kill", "-CONT", str(pid)])
                print(f"Process {pid} resumed")
            else:
                subprocess.run(["kill", "-KILL", str(pid)])
                print(f"Process {pid} killed")
    time.sleep(0.1)  # wait for 100 ms before processing the file again
