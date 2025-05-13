import os
import profile
import sys
import logging
from dotenv import load_dotenv
from typing import Literal
from pydantic import BaseModel, model_validator
from langgraph.graph import StateGraph, START, END
from langchain_together import ChatTogether
from utils import get_logger

logger = get_logger(__name__)

# Validate required environment variables
load_dotenv()
required_env_vars = ['TOGETHER_API_KEY', 'TAVILY_API_KEY']
for var in required_env_vars:
	if not os.getenv(var):
		raise ValueError(f'{var} is not set. Please add it to your environment variables.')

profile = None 
job_list = None

class State(BaseModel):
	action: Literal['SETUP', 'FIND', 'APPLY']
	roles: list[str] = [] 

	@model_validator(mode='before')
	def validate_action_transition(cls, data: dict) -> dict:
		action = data.get('action')
		if action and action not in ['SETUP', 'FIND', 'APPLY']:
			logger.error("action must be either SETUP, FIND, or APPLY")
		return data

	@model_validator(mode='after')
	def validate_roles(self) -> 'State':
		if self.action and self.action != 'SETUP' and not self.roles:
			logger.error("roles must not be empty for non-SETUP actions")
		return self

def create_state(action: str, roles: list[str] = None) -> State:
	return State(action=action, roles=roles or [])

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
	if state.action == 'SETUP' or not profile:
		return 'setup'
	elif state.action == 'FIND' or not job_list:
		return 'find'
	elif state.action == 'APPLY':
		return 'apply'
	return END

def setup_action_decision(state: State):
	if state.action == 'FIND' or not job_list:
		return 'find'
	elif state.action == 'APPLY':
		return 'apply'
	return END

def find_action_decision(state: State):
	if not profile:
		return 'setup'
	elif state.action == 'APPLY':
		return 'apply'
	return END

def apply_action_decision(state: State):
	if not profile:
		return 'setup'
	elif state.action == 'APPLY':
		return 'apply'
	return END

# start of the graph
job_pilot_builder.add_conditional_edges(START, init_action_decision)

# intermediatetates
job_pilot_builder.add_conditional_edges('setup', setup_action_decision)
job_pilot_builder.add_conditional_edges('find', find_action_decision)
job_pilot_builder.add_conditional_edges('apply', apply_action_decision)

# End of the graph
job_pilot_builder.add_edge('apply', END) 
job_pilot_builder.add_edge('find', END)
job_pilot_builder.add_edge('setup', END)


job_pilot = job_pilot_builder.compile()

# Run the agent
job_pilot.invoke(
    create_state('APPLY', [])
)

from IPython.display import Image, display

display(Image(job_pilot.get_graph().draw_mermaid_png()))