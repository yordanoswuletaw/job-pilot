import os
import profile
import sys
import logging
from tarfile import ENCODING
from tkinter import N
from dotenv import load_dotenv
from typing import Literal
from langchain_core.runnables.config import P
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_together import ChatTogether

# Validate required environment variables
load_dotenv()
required_env_vars = ['TOGETHER_API_KEY', 'TAVILY_API_KEY']
for var in required_env_vars:
	if not os.getenv(var):
		raise ValueError(f'{var} is not set. Please add it to your environment variables.')

profile = None 
job_list = None
class State(TypedDict):
	action: Literal['SETUP', 'FIND', 'APPLY', 'FIND_AND_APPLY']
	roles: list[str]

def setup(state: State):
	global profile 
	profile = 'SETUPed'
	print(profile, '!!!')
	return state

def find(state: State):
	global job_list
	job_list = ['job 1', 'job2']
	print(job_list)
	return state

def apply(state: State):
	print('Applied!!!')
	return state

job_pilot_builder = StateGraph(State)
# take resume then fill out profile fileds for future use
job_pilot_builder.add_node('setup', setup)
# find and save opportunities
job_pilot_builder.add_node('find', find)
# apply for opportunities
job_pilot_builder.add_node('apply', apply)


def init_action_decision(state: State):
	if state['action'] == 'SETUP' or not profile:
		return 'setup'
	elif state['action'] == 'FIND' or not job_list:
		return 'find'
	elif state['action'] == 'APPLY':
		return 'apply'
	return END

def setup_action_decision(state: State):
	if state['action'] == 'FIND' or not job_list:
		return 'find'
	elif state['action'] == 'APPLY':
		return 'apply'
	return END

def find_action_decision(state: State):
	if not profile:
		return 'setup'
	elif state['action'] == 'APPLY':
		return 'apply'
	return END

# start of the graph
job_pilot_builder.add_conditional_edges(START, init_action_decision)

# intermediatetates
job_pilot_builder.add_conditional_edges('setup', setup_action_decision)
job_pilot_builder.add_conditional_edges('find', find_action_decision)

# End of the graph
job_pilot_builder.add_edge('apply', END) 
job_pilot_builder.add_edge('find', END)
job_pilot_builder.add_edge('setup', END)


job_pilot = job_pilot_builder.compile()

# Run the agent
job_pilot.invoke(
    {'action': 'APPLY', 'roles': []}
)

from IPython.display import Image, display

display(Image(job_pilot.get_graph().draw_mermaid_png()))