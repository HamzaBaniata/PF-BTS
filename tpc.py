from multiprocessing import Process


class Tpc:

    def __init__(self, tpc_capacity):
        self.tpc_capacity = tpc_capacity
        self.vms = list()
        self.tasks = list()

    def receive_tasks(self, tasks):
        self.tasks = tasks

    def receive_vms(self, vms):
        self.vms = vms

    def validate_process(self):
        if sum(self.tasks) / self.tpc_capacity <= 80:
            print("Tasks will be performed in the TPC with Total Execution Time of " + str(
                sum(self.tasks) / self.tpc_capacity))
            return True
        return False

    def process_smart_contracts(self, contracts, tasks, vms, queue, start):
        processes = list()
        for algorithm, count in contracts.items():
            for i in range(count):
                process = Process(target=algorithm, args=(tasks, vms, queue, start))
                process.start()
                processes.append(process)
        for SC in processes:
            SC.join()
