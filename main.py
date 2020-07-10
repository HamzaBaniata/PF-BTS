import time
from multiprocessing import Queue
from ant_alg import ant_algorithm
import json
from first_come_first import first_come_first
from short_job_first import shortest_job
from round_robin import findmaxtime
from end_user import User
from cloud import Cloud
from tpc import Tpc
from blockchain import Blockchain
from blockchain import Block


class Input:
    def __init__(self, data):
        self.num_task = data["Num_Task"]
        self.num_vms = data["Num_VMs"]
        self.tpc_capacity = data["TPC_Capacity"]
        self.minimum_length_of_task = data["minimum_length_of_task"]
        self.maximum_length_of_task = data["maximum_length_of_task"]
        self.minimum_capacity_of_vm = data["minimum_capacity_of_vm"]
        self.maximum_capacity_of_vm = data["maximum_capacity_of_vm"]
        self.contracts = {
            ant_algorithm: data["ant_alg_count"],
            first_come_first: data["first_come_first_count"],
            findmaxtime: data["round_robin_count"],
            shortest_job: data["short_job_first_count"]
        }


def read_data():
    with open("input.json") as json_file:
        data = json.load(json_file)
        return Input(data)


def init(data):
    user = User()
    user.create_tasks(data=data)

    cloud = Cloud()
    cloud.create_vms(data=data)

    return user, cloud


def queue_to_list(queue):
    result = []
    while queue.qsize() > 0:
        result.append(queue.get())
    return result


def print_result(result, elapsed, checkpoint1, checkpoint2, blockchain):
    for i in range(len(result)):
        print("SmartContract number: " + str(i+1) +
              " resulted the following ['used optimization algorithm', Optimal Schedule time, SC run time]:")
        if result[i][1] < checkpoint1:
            checkpoint1 = result[i][1]
            checkpoint2 = result[i][0]
        print(result[i])
    print("Best Optimal Schedule is provided by a Miner who ran " + checkpoint2 +
          " algorithm, with >> \napproximate execution time of the proposed assignment = " + str(checkpoint1))
    print(
        'Optimal Schedules received from miners in approximately ' + str({round(elapsed, 3)}) + 'second(s)')
    print('Total time from TPC receiving the tasks from EndUsers>>'
          '\n>>until result are back to TPC from cloud ' + str(round(elapsed + checkpoint1, 3)) + 'second(s)')
    print("The following blocks were added to the publicly available blockchain:")
    for i in range(len(result)):
        blockchain.mine(Block(result[i]))
        print("*****\nBlock no." + str(blockchain.blocks[i+1].blockNo) + " is " + str(
            blockchain.blocks[i+1].transactions))
        print("timestamp of Block no." + str(blockchain.blocks[i+1].blockNo) + " is " + str(
            blockchain.blocks[i+1].timestamp))
        print("nonce of Block no." + str(blockchain.blocks[i+1].blockNo) + " is " + str(blockchain.blocks[i+1].nonce))
        print("The hash of Block no." + str(blockchain.blocks[i+1].blockNo) + " is " + str(
            blockchain.blocks[i+1].hash()) + "\n*****")


if __name__ == '__main__':
    data = read_data()
    user, cloud = init(data)

    tasks = user.tasks
    vms = cloud.vms

    tpc = Tpc(data.tpc_capacity)
    user.send_tasks(tpc)
    cloud.send_vms(tpc)
    start = time.time()
    if tpc.validate_process():
        print('Simulation finished in ' + str(time.time() - start) + 'second(s)')
    else:
        queue = Queue()
        blockchain = Blockchain()
        tpc.process_smart_contracts(data.contracts, tasks, vms, queue, start)
        checkPoint1 = (data.num_task * data.maximum_length_of_task) / (data.minimum_capacity_of_vm)
        checkPoint2 = 'Hamza'
        elapsed = time.time() - start
        result = queue_to_list(queue)
        print_result(result, elapsed, checkPoint1, checkPoint2, blockchain)
