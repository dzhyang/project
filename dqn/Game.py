from enum import Enum
import numpy as np
from itertools import product
import random
from queue import Queue

class Camp(Enum):
    Red=1 #+
    Black=-1 #-


class Game():
    _checkerBoard=[]
    _visibility=[[11 for col in range(4)] for row in range(4)]
    _camp=Camp.Red
    _render=Queue(20)
    _needrender=False
    def __init__(self,camp):
        self._camp=camp
        
        

    @staticmethod
    def init_CheckerBoard():
        chessMans=[x for x in range(1,9)]
        chessMans.extend(range(-8,0))

        for x in range(0,4):
            Game._checkerBoard.append([])
            for y in range(0,4):
                index=random.randint(0,len(chessMans)-1)
                Game._checkerBoard[x].append(chessMans.pop(index))
        
    
    def __call__(self,action):
        x1,y1,x2,y2=action
        isfolw=(x1==x2 and y1==y2)
        if (not isfolw) and (Game._visibility[x1][y1]==11 or Game._visibility[x2][y2]==11):
            return 0,False,False

        if isfolw and Game._visibility[x1][y1]==11:
            Game._visibility[x1][y1]=0
            Game._render.put([x1,y1,Game._checkerBoard[x1][y1]])
            Game._needrender=True
            return 0,True,False
        
        locationCurrent=Game._checkerBoard[x1][y1]
        locationNext=Game._checkerBoard[x2][y2]

        if (locationCurrent*self._camp.value)<=0 or (locationNext*self._camp.value)>0:
            return 0,False,False
        
        current=abs(locationCurrent)
        next_=abs(locationNext)
        Game._checkerBoard[x1][y1]=0
        if current>=next_:
            Game._checkerBoard[x2][y2]=locationCurrent
            Game._render.put([x1,y1,0])
            Game._render.put([x2,y2,locationCurrent])
            Game._needrender=True
            return next_,True,self._isDone()
        else:
            Game._render.put([x2,y2,0])
            Game._render.put([x1,y1,Game._checkerBoard[x2][y2]])
            Game._needrender=True
            return -current,True,self._isDone()

    def getState(self):
        state=[]
        for x in range(0,4):
            state.append([])
            for y in range(0,4):
               state[x].append(Game._checkerBoard[x][y] if Game._visibility[x][y]==0 else Game._visibility[x][y])
        return state

    def _isDone(self):
        red=0
        black=0
        for x in range(0,4):
            for y in range(0,4):
                if Game._visibility[x][y]!=0:
                    return False
                if Game._checkerBoard[x][y]>0:
                    red+=1
                elif Game._checkerBoard[x][y]<0:
                    black+=1
                if red!=0 and black!=0:
                    return False
        return True
                    



        

