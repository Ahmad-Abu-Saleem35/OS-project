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

    @staticmethod
    def init(processes, length):
        for process in processes:
            process.waiting_time = 0
            process.turnaround_time = 0
            process.response_time = 0
            process.return_time = 0
            process.completed = False
            process.processing_time = 0

# Processes data: [Process Name, Arrival Time, CPU Burst Time, I/O Burst Time, Priority]
Processes = [
    Process('P1', 0, 15, 5, 3),
    Process('P2', 1, 23, 14, 2),
    Process('P3', 3, 14, 6, 3),
    Process('P4', 4, 16, 15, 1),
    Process('P5', 6, 10, 13, 0),
    Process('P6', 7, 22, 4, 1),
    Process('P7', 8, 28, 10, 2)
]

# Time limit for the simulation
timeLimit = 128

# Gantt chart function
def ganttChart(ganttChartData, title):
    fig, gnt = plt.subplots()
    gnt.set_title(title)
    gnt.set_xlabel("Time Unit")
    gnt.set_ylabel("Processes")

    process_indices = {p.id: i + 1 for i, p in enumerate(Processes)}

    for process_id, start_time, burst_time in ganttChartData:
        gnt.broken_barh([(start_time, burst_time)], (process_indices[process_id] - 0.5, 1), facecolors=('darkcyan'))

    y_ticks = range(1, len(Processes) + 1)
    gnt.set_yticks(y_ticks)
    gnt.set_yticklabels([p.id for p in Processes])
    gnt.set_ylim(0.5, len(Processes) + 0.5)

    x_ticks = range(0, timeLimit, 5)
    gnt.set_xticks(x_ticks)
    gnt.set_xlim(0, timeLimit)

    gnt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

def roundRobin(queue, start_time, quantum):
    ganttChartData = []
    time = start_time
    queue = list(queue)  # Convert deque to list for sorting
    while queue and any(process.burst > process.processing_time for process in queue):  # Check if any process needs more CPU time
        for process in queue:
            if process.burst > process.processing_time:  # If the process is not yet completed
                execution_time = min(quantum, process.burst - process.processing_time)
                ganttChartData.append((process.id, time, execution_time))
                process.processing_time += execution_time
                time += execution_time
                if process.processing_time == process.burst:  # If the process is finished
                    queue.remove(process)
        # Re-sort the queue after each round
        queue.sort(key=lambda p: (p.burst, p.arrive_time))
    return ganttChartData, time

def npps_calculate(processes, length):
    time = 0
    quantum = 2
    ganttChartData = []

    processes[0].return_time = processes[0].burst
    processes[0].turnaround_time = processes[0].return_time - processes[0].arrive_time
    processes[0].response_time = 0
    processes[0].completed = True

    ganttChartData.append((processes[0].id, time, processes[0].burst))
    time = processes[0].burst

    while True:
        min_priority = float('inf')
        check = False

        for i in range(1, length):
            if (processes[i].priority < min_priority and
                not processes[i].completed and
                processes[i].arrive_time <= time):
                min_priority = processes[i].priority
                check = True

        if not check:
            break

        same_priority_queue = [p for p in processes if p.priority == min_priority and not p.completed and p.arrive_time <= time]

        if len(same_priority_queue) > 1:
            rr_gantt, time = roundRobin(deque(same_priority_queue), time, quantum)
            ganttChartData.extend(rr_gantt)
            for process in same_priority_queue:
                process.completed = True
                process.return_time = time
                process.turnaround_time = process.return_time - process.arrive_time
                process.waiting_time = process.turnaround_time - process.burst
                process.response_time = process.waiting_time

        else:
            for process in processes:
                if (process.priority == min_priority and
                    not process.completed and
                    process.arrive_time <= time):
                    process.response_time = time - process.arrive_time
                    process.return_time = time + process.burst
                    process.turnaround_time = process.return_time - process.arrive_time
                    process.waiting_time = time - process.arrive_time
                    process.completed = True

                    ganttChartData.append((process.id, time, process.burst))
                    time += process.burst

    return ganttChartData

def NPPS(processes, length):
    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0

    Process.init(processes, length)
    #merge_sort_by_arrive_time(processes, 0, length - 1)
    ganttChartData = npps_calculate(processes, length)

    for i in range(length):
        total_waiting_time += processes[i].waiting_time
        total_turnaround_time += processes[i].turnaround_time
        total_response_time += processes[i].response_time

   # quick_sort_by_return_time(processes, 0, length - 1)

    print("\tNon-preemptive Priority Scheduling Algorithm\n\n")
    ganttChart(ganttChartData, "Gantt Chart for Non-Preemptive Priority Scheduling with Round Robin (q=2)")

    print(f"\n\tAverage Waiting Time     : {total_waiting_time / length:.2f}")
    print(f"\tAverage Turnaround Time  : {total_turnaround_time / length:.2f}")
    print(f"\tAverage Response Time    : {total_response_time / length:.2f}\n")

    print_table(processes, length)

# Function to print table (assuming it's defined elsewhere)
def print_table(processes, length):
    # Your print_table implementation goes here
    pass

# Run the scheduling algorithms and display results
if __name__ == "__main__":
    NPPS(Processes, len(Processes))
