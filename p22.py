import matplotlib.pyplot as plt
from collections import deque

class Process:
    def __init__(self, id, arrive_time, burst, io_burst, priority):
        self.id = id
        self.arrive_time = arrive_time
        self.burst = burst
        self.io_burst = io_burst
        self.priority = priority
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0
        self.return_time = 0
        self.completed = False
        self.processing_time = 0

# Processes data: [Process Name, Arrival Time, CPU Burst Time, I/O Burst Time, Priority]
Processes_data = [
    ['P1', 0, 15, 5, 3],
    ['P2', 1, 23, 14, 2],
    ['P3', 3, 14, 6, 3],
    ['P4', 4, 16, 15, 1],
    ['P5', 6, 10, 13, 0],
    ['P6', 7, 22, 4, 1],
    ['P7', 8, 28, 10, 2]
]

# Convert Processes_data to instances of Process class
Processes = [Process(*process_data) for process_data in Processes_data]

# Gantt chart function (unchanged)
def gantt_chart(gantt_chart_data, title):
    fig, gnt = plt.subplots()
    gnt.set_title(title)
    gnt.set_xlabel("Time Unit")
    gnt.set_ylabel("Processes")

    process_indices = {p.id: i + 1 for i, p in enumerate(Processes)}

    max_time = max(start_time + burst_time for _, start_time, burst_time in gantt_chart_data)

    for process_id, start_time, burst_time in gantt_chart_data:
        gnt.broken_barh([(start_time, burst_time)], (process_indices[process_id] - 0.5, 1), facecolors=('darkcyan'))

    y_ticks = range(1, len(Processes) + 1)
    gnt.set_yticks(y_ticks)
    gnt.set_yticklabels([p.id for p in Processes])
    gnt.set_ylim(0.5, len(Processes) + 0.5)

    x_ticks = range(0, max_time + 1, 5)
    gnt.set_xticks(x_ticks)
    gnt.set_xlim(0, max_time)

    gnt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

def preemptive_priority_scheduling(processes):
    ready_queue = deque()
    current_time = 0
    time_quantum = 2
    aging_threshold = 5

    remaining_burst = {process.id: process.burst for process in processes}
    aging_time = {process.id: 0 for process in processes}
    completed_processes = []
    process_index = 0
    num_processes = len(processes)
    gantt_chart_data = []

    while len(completed_processes) < num_processes:
        while process_index < num_processes and processes[process_index].arrive_time <= current_time:
            process = processes[process_index]
            ready_queue.append(process)
            process_index += 1

        if not ready_queue:
            current_time = processes[process_index].arrive_time
            continue

        ready_queue = deque(sorted(ready_queue, key=lambda x: (x.priority, x.arrive_time)))
        process = ready_queue.popleft()
        process_id = process.id
        burst_time = remaining_burst[process_id]

        gantt_chart_data.append((process_id, current_time, current_time + burst_time))  # Store start and end times

        if burst_time <= time_quantum:
            current_time += burst_time
            remaining_burst[process_id] = 0
            completed_processes.append(process_id)
            print(f"({process_id}, {current_time - burst_time}, {current_time}) ", end="")

            # Calculate waiting and turnaround time
            process.waiting_time = current_time - process.arrive_time - process.burst
            process.turnaround_time = current_time - process.arrive_time
        else:
            current_time += time_quantum
            remaining_burst[process_id] -= time_quantum
            print(f"({process_id}, {current_time - time_quantum}, {current_time})", end="")

            for p in ready_queue:
                if p.id != process_id:
                    aging_time[p.id] += 1
                    if aging_time[p.id] >= aging_threshold:
                        p.priority -= 1
                        aging_time[p.id] = 0

            ready_queue.append(process)

    print("\nAll processes have completed their execution.")
    #gantt_chart(gantt_chart_data, "Preemptive Priority Scheduling Gantt Chart")

    # Calculate average waiting time and average turnaround time
    total_waiting_time = sum(process.waiting_time for process in processes)
    total_turnaround_time = sum(process.turnaround_time for process in processes)
    average_waiting_time = total_waiting_time / num_processes
    average_turnaround_time = total_turnaround_time / num_processes

    print(f"Average Waiting Time: {average_waiting_time}")
    print(f"Average Turnaround Time: {average_turnaround_time}")

preemptive_priority_scheduling(Processes)
