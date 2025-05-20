#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

# --- Constants ---
MAX_ITERATIONS = 5
MAX_NUM_SEARCH_RESULTS = 5

# --- State Keys ---
STATE_PROBLEM_CRITIC = 'problem_critic_output'
STATE_PROBLEM_GENERATOR = 'problem_generator_output'
STATE_PROBLEM_QUALITY_CHECKER = 'problem_quality_checker_output'
STATE_PROBLEM_SOLVER = 'problem_solver_output'
STATE_TEST_CASE_GENERATOR = 'test_case_generator_output'
STATE_TOPIC_FINDER_AGENT = 'topic_finder_agent_output'
STATE_ROOT_AGENT = 'codingtest_generator_output'

# --- Models ---
CLAUDE_3_HAIKU = 'anthropic.claude-3-haiku-20240307-v1:0'
CLAUDE_3_5_SONNET = 'anthropic.claude-3-5-sonnet-20240620-v1:0'

LLAMA3_8B_INSTRUCT = "meta.llama3-8b-instruct-v1:0"
LLAMA3_70B_INSTRUCT = "meta.llama3-70b-instruct-v1:0"