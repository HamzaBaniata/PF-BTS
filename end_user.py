import random


class User:

    def __init__(self):
        self.tasks = list()

    def create_tasks(self, data):
        print(str(data.num_task) + " tasks had been assigned random power consumption values.")
        for l in range(data.num_task):
            self.tasks.append(random.randint(data.minimum_length_of_task, data.maximum_length_of_task))
            print("Task number (" + str(l + 1) + "): " + str(self.tasks[l]))

    def send_tasks(self, tcp):
        tcp.receive_tasks(tasks=self.tasks)
