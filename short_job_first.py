import time


def shortest_job(tasks, vms, queue, start):
    burst_times = tasks
    vms = vms
    assignment1 = [0] * len(vms)
    for i in range(len(vms)):
        assignment1[i] = 0
    for i in range(0, len(burst_times) - 1):
        for j in range(0, len(burst_times) - i - 1):
            if burst_times[j] > burst_times[j + 1]:
                temp = burst_times[j]
                burst_times[j] = burst_times[j + 1]
                burst_times[j + 1] = temp
    vm_counter = 0
    j = 0
    while sum(burst_times) != 0:
        if burst_times[j] != 0:
            assignment1[vm_counter] += burst_times[j]
            vm_counter += 1
            burst_times[j] = 0
            if vm_counter == len(vms):
                vm_counter = 0
        j += 1
        if j == len(burst_times):
            j = 0

    for i in range(len(vms)):
        s = assignment1[i] / vms[i]
        assignment1[i] = s
    max_assignment_time1 = sum(assignment1)
    queue.put(["SJF", max_assignment_time1, (time.time() - start)])
