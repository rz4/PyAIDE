#!/usr/bin/python3
'''
Project: PyAIDE
File: BoardEnviro.py
Author: Rafael Zamora
Version: 1.0.0
Last Update: 7/17/2016

Change Log:
-ADDED set parameter functions v1.0.0
'''

from PyAIDE import Enviro

class BoardEnviro(Enviro):
    """ BoardEnviro is an environment made for multiple agents.
    The only agent task is to reach the FinalPos.
    The agent is to do this using the up, down, left, and right actions.

    The following functions can be used to set parameters of the environment:
    * setBoardSize(length, width) - sets dimensions of board
    * setInitialPos(x, y) - sets initial position of agents
    * setFinalPos(x, y) - sets final position of agents

    """

    def __init__(self):
        super().__init__()
        self.width = 25
        self.length = 25
        self.initPos = (0,0)
        self.finalPos = (self.width-1, self.length-1)

    def initEnviro(self):
        self.legalActs = ["LEFT", "RIGHT", "UP", "DOWN"]
        self.state["Width"] = self.width
        self.state["Height"] = self.length
        self.state["InitPos"] = self.initPos
        self.state["FinalPos"] = self.finalPos
        self.state["AgentsPos"] = {}
        for a in self.agents: self.state["AgentsPos"][a.__class__.__name__] = list(self.state["InitPos"])
        self.tasks.append(self.state["FinalPos"])

    def percept_to_Agent(self, agent):
        percept = tuple(self.state["AgentsPos"][agent.__class__.__name__])
        agent.sense(percept)

    def act_to_Enviro(self, agent):
        act = agent.act()
        agentPos = self.state["AgentsPos"][agent.__class__.__name__]
        if act == self.legalActs[0]:#LEFT
            if agentPos[0] > 0:
                agentPos[0] -= 1
        elif act == self.legalActs[1]:#RIGHT
            if agentPos[0] < self.state["Width"]-1:
                agentPos[0] += 1
        elif act == self.legalActs[2]:#UP
            if agentPos[1] > 0:
                agentPos[1] -= 1
        elif act == self.legalActs[3]:#DOWN
            if agentPos[1] < self.state["Height"]-1:
                agentPos[1] += 1

    def render(self, canvas, state):
        tsize = (canvas.winfo_width() / state["Width"]) - 0.02
        for x in range(state["Width"]):
            for y in range(state["Height"]):
                x1, y1 = tsize/10 + (x*tsize), tsize/10 + (y*tsize)
                canvas.create_rectangle(x1, y1, x1 + (9/10)*tsize, y1 + (9/10)*tsize, fill = "blue")
        x1, y1 = tsize/10 + (state["FinalPos"][0]*tsize) , tsize/10 +(state["FinalPos"][1]*tsize)
        canvas.create_rectangle(x1, y1, x1 + (9/10)*tsize, y1 + (9/10)*tsize, fill = "green")
        for a in state["AgentsPos"]:
            agentPos = state["AgentsPos"][a]
            x1, y1 = tsize/10 + (agentPos[1]*tsize) , tsize/10 +(agentPos[0]*tsize)
            canvas.create_rectangle(x1, y1, x1 + (9/10)*tsize, y1 + (9/10)*tsize, fill = "red")
            canvas_id = canvas.create_text(x1 + (1/10)*tsize, y1 + (3/10)*tsize, anchor="nw")
            canvas.itemconfig(canvas_id, text=a)
            canvas.insert(canvas_id, 12, "")

    def setBoardDimen(self, length, width):
        self.length = length
        self.width = width

    def setInitialPos(self, x, y):
        self.initPos = (x,y)

    def setFinalPos(self, x, y):
        self.finalPos = (x,y)
