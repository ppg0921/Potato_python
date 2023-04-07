from node import *
import numpy as np
import csv
import pandas
from enum import IntEnum
import math
from queue import Queue
from queue import LifoQueue

Direction_maze = {1: "North", 2: "South", 3: "West", 4: "East"}


class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    def __init__(self, filepath):
        # TODO : read file and implement a data structure you like

        # For example, when parsing raw_data, you may create several Node objects.
        # Then you can store these objects into self.nodes.
        # Finally, add to nd_dict by {key(index): value(corresponding node)}

        self.raw_data = pandas.read_csv(filepath).values
        self.nodes = []
        # key: index, value: the correspond nodedf = pandas.read_csv(filepath)
        self.nd_dict = dict()
        # self.nodes.append(Node(-1))
        df = pandas.read_csv(filepath)
        self.nodeNum, column_count = df.shape
        self.shortPath = LifoQueue(self.nodeNum)
        self.actionQueue = Queue(self.nodeNum)
        print("nodeNum: ", self.nodeNum)
        print("maze[1][4]: ", df[Direction_maze[1]][4])
        for i in range(self.nodeNum):
            tmpNode = Node(df["index"][i])
            for j in range(1, 5):
                if pandas.isna(df[Direction_maze[j]][i]) is False:
                    tmpNode.setSuccessor(int(df[Direction_maze[j]][i]), j)
            self.nodes.append(tmpNode)
            self.nd_dict[i+1] = self.nodes[i]
        print(self.nd_dict)

    def getStartPoint(self):
        if (len(self.nd_dict) < 2):
            print("Error: the start point is not included.")
            return 0
        return self.nd_dict[1]

    def getNodeDict(self):
        return self.nd_dict

    def BFS(self, nd):
        # TODO : design your data structure here for your algorithm
        # TODO : Tips : return a sequence of nodes from the node to the nearest unexplored deadend

        unprocessed = Queue(self.nodeNum)
        # finalPath = LifoQueue(self.nodeNum)
        distance = np.zeros(self.nodeNum)
        previous = np.zeros(self.nodeNum)
        unprocessed.put(nd.getIndex())
        distance[nd.getIndex()] = 1
        deadIndex = 0

        while unprocessed.empty() is False:
            tmpNode = self.nd_dict[unprocessed.get()]
            nowDis = distance[tmpNode.getIndex()]
            for adj in tmpNode.getAdjNum():
                Succ = tmpNode.getSuccessors[adj][0]
                if distance[Succ] == 0:
                    unprocessed.put(Succ)
                    distance[Succ] = nowDis+1
                    previous[Succ] = tmpNode.getIncex()
                    if self.nd_dict[Succ].getAdjNum == 1 and self.nd_dict[Succ].getDeadVisited() == False:
                        print("Deadend found... Node ", Succ)
                        self.nd_dict[Succ].DeadVisited()
                        deadIndex = Succ
                if deadIndex != 0:
                    break
            if deadIndex != 0:
                break

        currIndex = deadIndex

        while self.shortPath.empty() is True:
            self.shortPath.get()
        while currIndex != nd.getIndex():
            self.shortPath.put(currIndex)
            currIndex = previous[currIndex]

        return None

    def BFS_2(self, nd_from, nd_to):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        
        unprocessed = Queue(self.nodeNum)
        # finalPath = LifoQueue(self.nodeNum)
        distance = np.zeros(self.nodeNum)
        previous = np.zeros(self.nodeNum)
        unprocessed.put(nd_from.getIndex())
        distance[nd_from.getIndex()] = 1
        Found = False

        while unprocessed.empty() is False:
            tmpNode = self.nd_dict[unprocessed.get()]
            nowDis = distance[tmpNode.getIndex()]
            for adj in tmpNode.getAdjNum():
                Succ = tmpNode.getSuccessors[adj][0]
                if distance[Succ] == 0:
                    unprocessed.put(Succ)
                    distance[Succ] = nowDis+1
                    previous[Succ] = tmpNode.getIncex()
                    if Succ == nd_to.getIndex():
                        print("Finish node found... Node ", Succ)
                        Found = True
                if Found:
                    break
            if Found:
                break

        currIndex = nd_to.getIndex()
        while self.shortPath.empty() is True:
            self.shortPath.get()
        while currIndex != nd_from.getIndex():
            self.shortPath.put(currIndex)
            currIndex = previous[currIndex]

        return None

    def getAction(self, car_dir, nd_from, nd_to):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the nd_to is the Successor of nd_to
        # If not, print error message and return 0
        if nd_from.isSuccessor(nd_to.getIndex()):
            to_dir = nd_from.getDirection(nd_to.getIndex())
            if car_dir == to_dir:
                return 1
            if car_dir*to_dir == 2 or car_dir*to_dir == 12:
                return 2
            if to_dir == car_dir+2 or to_dir == car_dir-1 or to_dir == car_dir-3:
                return 4
            if to_dir == car_dir-2 or to_dir == car_dir+1 or to_dir == car_dir+3:
                return 3
        else:
            print("Not adjacent... (from getAction)")
        
        return None

    def getActions(self, nodes):
        # TODO : given a sequence of nodes, return the corresponding action sequence
        # Tips : iterate through the nodes and use getAction() in each iteration
        if nodes.empty() is False:
            
            nowNode = self.nd_dict[nodes.get()]
            nextNode = self.nd_dict[nodes.get()]
            car_dir = nowNode.getDirection(nextNode)
            self.actionQueue.put(car_dir)
            while nodes.empty() is False:
                nowNode = nextNode
                nextNode = self.nd_dict[nodes.get()]
                self.actionQueue.put(self.getAction(car_dir, nowNode, nextNode))
        
        
        return None

    def actions_to_str(self, actions):
        # cmds should be a string sequence like "fbrl....", use it as the input of BFS checklist #1
        cmd = "fbrls"
        cmds = ""
        for action in actions:
            cmds += cmd[action-1]
        print(cmds)
        return cmds

    def strategy(self, nd):
        return self.BFS(nd)

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_from, nd_to)


if __name__ == '__main__':
    testMaze = Maze('./data/small_maze.csv')
