import time

quantum = 5


def findmaxtime(tasks, vms, queue, start):
    tasks = tasks
    vms = vms
    remaining_bt = tasks
    vms_local = [0] * len(vms)
    for i in range(len(vms)):
        vms_local[i] = 0
    j = 0
    vm_counter = 0
    while sum(remaining_bt) != 0:
        if 0 < remaining_bt[j] <= quantum:
            vms_local[vm_counter] += remaining_bt[j]
            remaining_bt[j] = 0
            vm_counter += 1
            if vm_counter == len(vms):
                vm_counter = 0
        else:
            if 0 < remaining_bt[j] > quantum:
                remaining_bt[j] -= quantum
                vms_local[vm_counter] += quantum
                vm_counter += 1
                if vm_counter == len(vms):
                    vm_counter = 0
        j += 1
        if j == len(remaining_bt):
            j = 0
    for i in range(len(vms)):
        vms_local[i] = vms_local[i]/vms[i]
    max_assignment_time = sum(vms_local)
    queue.put(["RR", max_assignment_time, (time.time() - start)])
