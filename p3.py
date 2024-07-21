import matplotlib.pyplot as plt

# Processes data: [Process Name, Arrival Time, CPU Burst Time, I/O Burst Time, Priority]
Processes = [
    ['P1', 0, 15, 5, 3],
    ['P2', 1, 23, 14, 2],
    ['P3', 3, 14, 6, 3],
    ['P4', 4, 16, 15, 1],
    ['P5', 6, 10, 13, 0],
    ['P6', 7, 22, 4, 1],
    ['P7', 8, 28, 10, 2]
]

# Time limit
timeLimit = 230

# Gantt chart function
def ganttChart(ganttChartData, title):
    fig, gnt = plt.subplots()
    gnt.set_title(title)
    gnt.set_xlabel("Time Unit")
    gnt.set_ylabel("Processes")

    process_indices = {p[0]: i + 1 for i, p in enumerate(Processes)}

    for process_id, start_time, burst_time in ganttChartData:
        gnt.broken_barh([(start_time, burst_time)], (process_indices[process_id] - 0.5, 1), facecolors=('darkcyan'))

    y_ticks = range(1, len(Processes) + 1)
    gnt.set_yticks(y_ticks)
    gnt.set_yticklabels([p[0] for p in Processes])
    gnt.set_ylim(0.5, len(Processes) + 0.5)

    x_ticks = range(0, timeLimit, 5)
    gnt.set_xticks(x_ticks)
    gnt.set_xlim(0, timeLimit)

    gnt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

# Multilevel Feedback Queue Scheduling
def multilevelFeedbackQueue():
    queues = [[] for _ in range(3)]
    waitQueue = []
    ganttChartData = []
    processing = None
    time_quantum = [8, 16, -1]  # Time quantum for each level (-1 means FCFS)
    sumWaitTime = 0
    sumTurnAroundTime = 0

    # Process control fields initialization
    for p in Processes:
        p.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # Adding [Wait Time, Turnaround Time, IO Timer, Aging Timer, Effective Priority, Queue Level, Processing Time, Time Slice]

    for time in range(timeLimit):
        # Time calc
        for queue in queues:
            for process in queue:
                process[5] += 1  # Aging timer
                process[6] += 1  # IO Timer

        for process in waitQueue:
            process[6] += 1  # IO Timer

        # Check for arriving processes
        for process in Processes:
            if process[1] == time:
                queues[0].append(process)
                process[10] = process[4]

        # Move process from waitQueue to readyQueue when I/O burst is done
        waitQueueTemp = waitQueue.copy()
        for process in waitQueueTemp:
            process[7] += 1  # Aging timer
            if process[7] == process[3]:  # If I/O burst is done
                waitQueue.remove(process)
                queues[process[12]].append(process)
                process[7] = 0

        # If CPU is free, schedule the next process
        if not processing:
            for i in range(3):
                if queues[i]:
                    processing = queues[i].pop(0)
                    processing[12] = i
                    break
            processingTime = 0

        if processing:
            processingTime += 1
            processing[8] += 1

            if (time_quantum[processing[12]] != -1 and processingTime == time_quantum[processing[12]]) or processing[8] == processing[2]:
                ganttChartData.append((processing[0], time - processingTime + 1, processingTime))
                sumTurnAroundTime += processingTime

                if processing[8] == processing[2]:
                    waitQueue.append(processing)
                    processing = None
                else:
                    if processing[12] < 2:
                        processing[12] += 1
                    queues[processing[12]].append(processing)
                    processing = None

                processingTime = 0

    displayResults(ganttChartData, "Multilevel Feedback Queue Scheduling", sumWaitTime, sumTurnAroundTime, len(Processes))

# Function to display the Gantt chart
def displayResults(ganttChartData, title, sumWaitTime, sumTurnAroundTime, processCount):
    print(f"\n{title}:")
    print("  Average waiting time =", sumWaitTime / processCount)
    print("  Average turnaround time =", sumTurnAroundTime / processCount)
    ganttChart(ganttChartData, title)

# Run the algorithm
multilevelFeedbackQueue()
