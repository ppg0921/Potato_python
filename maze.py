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
    def __init__(self, filepath, caroridir = Direction.NORTH):
        # TODO : read file and implement a data structure you like

        # For example, when parsing raw_data, you may create several Node objects.
        # Then you can store these objects into self.nodes.
        # Finally, add to nd_dict by {key(index): value(corresponding node)}
        self.cmds = ""
        self.raw_data = pandas.read_csv(filepath).values
        self.nodes = []
        # key: index, value: the correspond nodedf = pandas.read_csv(filepath)
        self.nd_dict = dict()
        # self.nodes.append(Node(-1))
        df = pandas.read_csv(filepath)
        self.nodeNum, column_count = df.shape
        self.shortPath = LifoQueue(self.nodeNum+3)
        self.actionQueue = Queue(self.nodeNum+3)
        self.carDirection = caroridir 
        # print("nodeNum: ", self.nodeNum)
        # print("maze[1][4]: ", df[Direction_maze[1]][4])
        for i in range(self.nodeNum):
            tmpNode = Node(df["index"][i])
            for j in range(1, 5):
                if pandas.isna(df[Direction_maze[j]][i]) is False:
                    tmpNode.setSuccessor(int(df[Direction_maze[j]][i]), j)
            self.nodes.append(tmpNode)
            self.nd_dict[i+1] = self.nodes[i]
        print(self.nd_dict)

    def getActionQueue(self):
        return self.actionQueue
    
    def getStartPoint(self):
        if (len(self.nd_dict) < 2):
            print("Error: the start point is not included...")
            return 0
        return self.nd_dict[1]

    def getNodeDict(self):
        return self.nd_dict

    def BFS(self, nd):
        # TODO : design your data structure here for your algorithm
        # TODO : Tips : return a sequence of nodes from the node to the nearest unexplored deadend

        unprocessed = Queue(self.nodeNum)
        # finalPath = LifoQueue(self.nodeNum)
        distance = np.zeros(self.nodeNum+1)
        previous = np.zeros(self.nodeNum+1)
        unprocessed.put(nd.getIndex())
        distance[nd.getIndex()] = 1
        deadIndex = 0

        while unprocessed.empty() is False:
            tmpNode = self.nd_dict[unprocessed.get()]
            nowDis = distance[tmpNode.getIndex()]
            for adj in tmpNode.getSuccessors():
                Succ = int(adj[0])
                if distance[Succ] == 0:
                    unprocessed.put(Succ)
                    distance[Succ] = nowDis+1
                    previous[Succ] = tmpNode.getIndex()
                    if self.nd_dict[Succ].getAdjNum() == 1 and self.nd_dict[Succ].getDeadVisited() == False:
                        print("Deadend found... Node ", Succ)
                        self.nd_dict[Succ].DeadVisited()
                        deadIndex = Succ
                if deadIndex != 0:
                    break
            if deadIndex != 0:
                break

        currIndex = deadIndex
        
        while self.shortPath.empty() is False:
            self.shortPath.get()
        if(deadIndex != 0):
            while currIndex != nd.getIndex():
                self.shortPath.put(currIndex)
                currIndex = previous[int(currIndex)]
                # print(currIndex)
                # print("here1")
            self.shortPath.put(currIndex)       # put start point
            return deadIndex

        return -1

    def BFS_2(self, nd_from, nd_to):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        
        unprocessed = Queue(self.nodeNum)
        # finalPath = LifoQueue(self.nodeNum)
        distance = np.zeros(self.nodeNum+1)
        previous = np.zeros(self.nodeNum+1)
        unprocessed.put(nd_from.getIndex())
        distance[nd_from.getIndex()] = 1
        Found = False

        while unprocessed.empty() is False:
            tmpNode = self.nd_dict[unprocessed.get()]
            # print(tmpNode.getIndex())
            nowDis = distance[tmpNode.getIndex()]
            for adj in tmpNode.getSuccessors():
                Succ = adj[0]

                if distance[Succ] == 0:
                    unprocessed.put(Succ)
                    distance[Succ] = nowDis+1
                    previous[Succ] = tmpNode.getIndex()
                    # print("previous[", Succ, "] = ", tmpNode.getIndex())
                    if Succ == nd_to.getIndex():
                        print("Finish node found... Node ", Succ)
                        Found = True
                if Found:
                    break
            if Found:
                break

        currIndex = nd_to.getIndex()
        while self.shortPath.empty() is False:
            self.shortPath.get()
        # print("nd_from.getIndex()", nd_from.getIndex())
        while int(currIndex) != int(nd_from.getIndex()):
            self.shortPath.put(currIndex)
            # print("currIndex: ", currIndex)
            currIndex = previous[int(currIndex)]
        self.shortPath.put(nd_from.getIndex())

        return None

    def getAction(self, car_dir, nd_from, nd_to, first = False):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the nd_to is the Successor of nd_to
        # If not, print error message and return 0
        if nd_from.isSuccessor(nd_to.getIndex()):
            to_dir = nd_from.getDirection(nd_to.getIndex())
            
            if first:
                return Action.ADVANCE, to_dir


            if car_dir == to_dir:
                return Action.ADVANCE, to_dir
            if car_dir == Direction.NORTH:
                if to_dir == Direction.SOUTH:
                    return Action.U_TURN, to_dir
                if to_dir == Direction.EAST:
                    return Action.TURN_RIGHT, to_dir
                if to_dir == Direction.WEST:
                    return Action.TURN_LEFT, to_dir
            if car_dir == Direction.SOUTH:
                if to_dir == Direction.NORTH:
                    return Action.U_TURN, to_dir
                if to_dir == Direction.WEST:
                    return Action.TURN_RIGHT, to_dir
                if to_dir == Direction.EAST:
                    return Action.TURN_LEFT, to_dir
            if car_dir == Direction.WEST:
                if to_dir == Direction.EAST:
                    return Action.U_TURN, to_dir
                if to_dir == Direction.NORTH:
                    return Action.TURN_RIGHT, to_dir
                if to_dir == Direction.SOUTH:
                    return Action.TURN_LEFT, to_dir
            if car_dir == Direction.EAST:
                if to_dir == Direction.WEST:
                    return Action.U_TURN, to_dir
                if to_dir == Direction.SOUTH:
                    return Action.TURN_RIGHT, to_dir
                if to_dir == Direction.NORTH:
                    return Action.TURN_LEFT, to_dir
        else:
            print("Not adjacent... (from getAction)")
        
        return None

    def getActions(self, nodes, First = False):
        # TODO : given a sequence of nodes, return the corresponding action sequence
        # Tips : iterate through the nodes and use getAction() in each iteration
        if nodes.empty() is False:
            nowNode = self.nd_dict[nodes.get()]
            nextNode = self.nd_dict[nodes.get()]
            # print("Car_dir:", self.carDirection)
            car_new_action, self.carDirection = self.getAction(self.carDirection, nowNode, nextNode, first = First)
            self.actionQueue.put(car_new_action)
            # print("Car_dir:", self.carDirection)
            # print("car_new_action: ", car_new_action)
            while nodes.empty() is False:
                nowNode = nextNode
                nextNode = self.nd_dict[nodes.get()]
                # print("nextNode.Index: ", nextNode.getIndex())
                # print("nowNode.Index: ", nowNode.getIndex())
                car_new_action, self.carDirection = self.getAction(self.carDirection, nowNode, nextNode)
                # print("here1")
                self.actionQueue.put(car_new_action)
                
                # print("actionQueue.put ", car_new_action)
                # print("Car_dir:", self.carDirection)
            # print("here2")
        if nodes.empty() is True:
            self.actionQueue.put(Action.HALT)
            # print("actionQueue.put ", Action.HALT)
        
        return None

    def actions_to_str(self, actions):
        # cmds should be a string sequence like "fbrl....", use it as the input of BFS checklist #1
        cmd = "fbrls"
        cmds = ""
        for action in actions:
            cmds += cmd[action-1]
        print(cmds)
        return cmds
    
    def putCmdtoCmds(self):
        while self.actionQueue.empty() is False:
            tmpAction = self.actionQueue.get()
            # print(tmpAction)
            if tmpAction == Action.U_TURN:
                self.cmds += "b"
            elif tmpAction == Action.ADVANCE:
                self.cmds += "f"
            elif tmpAction == Action.TURN_LEFT:
                self.cmds += "l"
            elif tmpAction == Action.TURN_RIGHT:
                self.cmds += "r"
        return None

    def strategy(self, nd):
        return self.BFS(nd)

    def ShortRoute(self, nd_from, nd_to):
        self.BFS_2(nd_from, nd_to)
        self.getActions(self.shortPath, First = True)
        self.putCmdtoCmds()
    
    def DeadEndTraversal(self, nd_start, nd_end):
        startIndex = nd_start.getIndex()
        nd_start.DeadVisited()
        nd_end.DeadVisited()
        currNode = nd_start
        dead = self.BFS(currNode)
        while dead != -1:
            self.getActions(self.shortPath, currNode.getIndex() == startIndex)
            self.putCmdtoCmds()
            # while(self.actionQueue.empty() is False):
            #     tmpAction = self.actionQueue.get()
            #     # print(tmpAction)
            #     if tmpAction == Action.U_TURN:
            #         print("b")
            #     elif tmpAction == Action.ADVANCE:
            #         print("f")
            #     elif tmpAction == Action.TURN_LEFT:
            #         print("l")
            #     elif tmpAction == Action.TURN_RIGHT:
            #         print("r")
            print("end of BFS to dead end ", dead)
            currNode = self.nd_dict[dead]
            oldDead = dead
            dead = self.BFS(currNode)
        print("end of all BFS to deadends...")
        self.putCmdtoCmds()
    
        self.BFS_2(self.nd_dict[oldDead], self.nd_dict[10])
        self.getActions(self.shortPath, currNode.getIndex() == startIndex)
        self.putCmdtoCmds()
        # print("here")
        #self.putCmdtoCmds()
        # while(self.actionQueue.empty() is False):
        #     tmpAction = self.actionQueue.get()
        #     # print(tmpAction)
        #     if tmpAction == Action.U_TURN:
        #         print("b")
        #     elif tmpAction == Action.ADVANCE:
        #         print("f")
        #     elif tmpAction == Action.TURN_LEFT:
        #         print("l")
        #     elif tmpAction == Action.TURN_RIGHT:
        #         print("r")
        
        print("End of BFS_2...")



if __name__ == '__main__':
    testMaze = Maze('./data/maze_4_3-2.csv')
    # testMaze.DeadEndTraversal(testMaze.nd_dict[1], testMaze.nd_dict[10])
    testMaze.ShortRoute(testMaze.nd_dict[1], testMaze.nd_dict[10])
    print(testMaze.cmds)
    
    # startIndex = 1
    # testMaze.nd_dict[startIndex].deadVisited = True;
    # currNode = testMaze.nd_dict[startIndex]
    # dead = testMaze.BFS(currNode)
    # while dead != -1:
    #     testMaze.getActions(testMaze.shortPath, currNode.getIndex() == startIndex)
    #     while(testMaze.actionQueue.empty() is False):
    #         tmpAction = testMaze.actionQueue.get()
    #         # print(tmpAction)
    #         if tmpAction == Action.U_TURN:
    #             print("b")
    #         elif tmpAction == Action.ADVANCE:
    #             print("f")
    #         elif tmpAction == Action.TURN_LEFT:
    #             print("l")
    #         elif tmpAction == Action.TURN_RIGHT:
    #             print("r")
    #     print("end of BFS to dead end ", dead)
    #     currNode = testMaze.nd_dict[dead]
    #     dead = testMaze.BFS(currNode)
    # print("end of all BFS to deadends...")
    
        
        
    # testMaze.BFS_2(testMaze.nd_dict[dead], testMaze.nd_dict[10])
    # testMaze.getActions(testMaze.shortPath)
    # while(testMaze.actionQueue.empty() is False):
    #     tmpAction = testMaze.actionQueue.get()
    #     # print(tmpAction)
    #     if tmpAction == Action.U_TURN:
    #         print("b")
    #     elif tmpAction == Action.ADVANCE:
    #         print("f")
    #     elif tmpAction == Action.TURN_LEFT:
    #         print("l")
    #     elif tmpAction == Action.TURN_RIGHT:
    #         print("r")
        
        
    
    # print(testMaze.shortPath)
    # print(testMaze.nd_dict[5].getIndex())
