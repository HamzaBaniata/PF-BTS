import random
import numpy as np
import json
import time


def ant_algorithm(tasks, vms, queue, start):
    tasks = tasks
    vms = vms
    num_task = len(tasks)
    num_vms = len(vms)
    list_of_best_individual_assignments = []
    utilization_matrix = []
    best_usage_ant = 10000000
    with open("input.json") as json_file:
        data = json.load(json_file)
        num_task = data["Num_Task"]
        num_vms = data["Num_VMs"]
        one_min_cost_of_vm = data["One_min_Cost_of_VM"]
    result = num_task / num_vms
    utilization_matrix = np.zeros([num_task, num_vms])

    def compute_utilization_matrix():
        for ut in range(num_task):
            for ut2 in range(num_vms):
                utilization_matrix[ut][ut2] = tasks[ut] / vms[ut2]
        return utilization_matrix
    compute_utilization_matrix()
    with open("input.json") as json_file:
        data = json.load(json_file)
        num_ants = data["Num_Ants"]
        evaporation = data["Evaporation"]

    def sum_column(m, column):
        summation = 0
        for i in range(len(tasks)):
            summation = summation + m[i][column - 1]
        return summation

    def sum_row(m, row):
        summation = 0
        for i in range(len(vms)):
            summation = summation + m[row - 1][i]
        return summation

    def change_pheromone_matrix_to_local(v):
        max_row = np.amax(v, axis=1)
        v_modified = np.zeros((num_task, num_vms))
        for i in range(len(tasks)):
            for j in range(len(vms)):
                if v[i][j] != max_row[i]:
                    v_modified[i][j] = 0
                else:
                    v_modified[i][j] = 1
        return v_modified

    def find_assignment(arr):
        r = list()
        for i in range(len(tasks)):
            for k in range(len(vms)):
                if arr[i, k] > 0:
                    r.append((i + 1, k + 1))
        return r
    best_ant_assignment = np.ones((num_task, num_vms))
    pheromon_matrix = np.ones((num_task, num_vms))
    best_ant = 0
    for k in range(num_ants):
        print("\n\n*******\nAnt number " + str(k + 1) + " started\n*******\n")
        local = np.zeros([len(tasks), len(vms)])
        while np.sum(local) < num_task:
            index = random.randint(0, num_vms)
            row_num = random.randint(0, num_task)
            while sum_column(local, index) >= result or sum_row(local, row_num) >= 1:
                index = random.randint(0, num_vms)
                row_num = random.randint(0, num_task)
            local[row_num - 1][index - 1] = 1
        print('The usage is :')
        local_usage = sum(np.sum(utilization_matrix * local, axis=0))
        print(local_usage)
        local_iteration_matrix = local
        passing = False
        for it in range(len(vms)):
            for t in range(len(tasks)):
                if not passing:
                    if local_iteration_matrix[t, it] == 1:
                        local_iteration_matrix[t, it-1] = 1
                        local_iteration_matrix[t, it] = 0
                        if sum(np.sum((local_iteration_matrix * utilization_matrix), axis=0)) < local_usage:
                            local = local_iteration_matrix
                            local_usage = sum(np.sum(utilization_matrix * local, axis=0))
                            print("A new Local Matrix with usage of " + str(local_usage) + " had been built.")
                            passing = True
        print('The final LOCAL matrix of this ant is as following with usage of:' + str(local_usage))
        print(local)
        print("The pheromon matrix has been updated as follows: ")
        pheromon_matrix = (1 - evaporation) * pheromon_matrix
        for t in range(len(tasks)):
            for p in range(len(vms)):
                if local[t, p] != 0:
                    mod = sum_row(pheromon_matrix, t)
                    if mod == 0:
                        mod = num_vms * num_task / 1000
                    prob = pheromon_matrix[t][p] / mod
                    pheromon_matrix[t][p] = 1 + round((pheromon_matrix[t][p] + (prob / num_ants)), 2)
        list_of_best_individual_assignments.append(local)
        print(pheromon_matrix.reshape(num_task, num_vms))
        print(" Ant Number: " + str(k + 1) + " finished its iterations.")
    time_consumption = sum(np.sum(utilization_matrix * change_pheromone_matrix_to_local(pheromon_matrix), axis=0))
    cost = time_consumption * one_min_cost_of_vm / 60
    best_usage = time_consumption
    best_cost = cost
    best_schedule = utilization_matrix * change_pheromone_matrix_to_local(pheromon_matrix)
    print("****************\n****************\nThe suggested assignment by the majority of ants:")
    print(find_assignment(best_schedule))
    print("\nThe time consumption of the virtual machines to perform the requested"
          " tasks equals (according to the pheromone matrix): ")
    print(str(best_usage) + " seconds" + "\n         = " + str(best_usage / 60) + " minutes \n         = " + str(
        best_usage / 3600) + " hours.")
    print("Total estimate cost of VMs in the cloud = ")
    print(str(best_cost) + " $\n****************\n****************")
    for i in range(len(list_of_best_individual_assignments)):
        if sum(np.sum(utilization_matrix * list_of_best_individual_assignments[i], axis=0)) < sum(
                np.sum(utilization_matrix * best_ant_assignment, axis=0)):
            best_ant_assignment = list_of_best_individual_assignments[i]
            best_ant = i
            best_usage_ant = sum(
                np.sum(utilization_matrix * change_pheromone_matrix_to_local(
                    list_of_best_individual_assignments[i]), axis=0))
    print("The best individual assignment is proposed by ant number " + str(best_ant + 1))
    print("The approximate Time consumption of VRs as proposed by the best Ant is: (" + str(
        best_usage_ant) + ") second(s)\n, with the following assignment:")
    print(find_assignment(best_ant_assignment))
    if best_usage_ant < best_usage:
        queue.put(["ACO", best_usage_ant, (time.time() - start)])
    else:
        queue.put(["ACO", best_usage, (time.time() - start)])
