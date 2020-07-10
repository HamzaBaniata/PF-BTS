import time


def first_come_first(tasks, vms, queue, start):

    burst_times = tasks
    vms = vms
    assignment2 = [0] * len(vms)
    vm_counter = 0
    j = 0
    while j < len(burst_times):
        assignment2[vm_counter] = assignment2[vm_counter] + burst_times[j]
        vm_counter += 1
        j += 1
        if vm_counter == len(vms):
            vm_counter = 0
    for i in range(len(vms)):
        assignment2[i] = assignment2[i] / vms[i]
    max_assignment_time2 = sum(assignment2)
    queue.put(["FCFS", max_assignment_time2, (time.time() - start)])
