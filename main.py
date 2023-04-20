import maze as mz
from score import ScoreboardFake, Scoreboard
from BTinterface import BTinterface

import numpy as np
import pandas
import time
import sys
import os
import keyboard as kb

def main():
    maze = mz.Maze("data/maze_3_2-1.csv")
    point = Scoreboard("POTATO1", "http://140.112.175.18:3000")
    # point = ScoreboardFake("your team name", "data/fakeUID.csv")
    
    # interf.start()
    # TODO : Initialize necessary variables
    StartIndex = 2
    FinishIndex = 6
    remember=-1
    len=0
    UIDstring = ""
    CommandString = ""
    if (sys.argv[1] == '0'):
        print("Mode 0: for treasure-hunting")
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
        
    elif (sys.argv[1] == '1'):
        interf = BTinterface()
        interf.start()
        
        print("Mode 1: Self-testing mode.")
        
        maze.DeadEndTraversal(StartIndex, FinishIndex)
        maze.CmdAppend("h")
        print(maze.getCmds())
        CommandString = maze.getCmds()
        # for i in range(maze.getCmdLen()):
        #     interf.send_action(CommandString[i])
        
        
        
        # interf.send_action(maze.getCmdLen())
        # interf.send_action("P")
        interf.send_action(maze.getCmds())

        while(True):
            UIDstring = interf.get_UID()
            if UIDstring!=0:
                UIDstring = UIDstring[2:]
                print("UIDstring:", UIDstring)
                point.add_UID(UIDstring.upper())
                UIDstring = 0

            if kb.is_pressed("w"):
                interf.send_action("f")
            elif kb.is_pressed("a"):
                interf.send_action("l")
            elif kb.is_pressed("s"):
                interf.send_action("b")
            elif kb.is_pressed("d"):
                interf.send_action("r")
            elif kb.is_pressed("h"):
                interf.send_action("h")
            # else:
            #     interf.send_action("h")
        
        
        
        # TODO: You can write your code to test specific function.
        

if __name__ == '__main__':
    main()
