#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# Based on: https://github.com/jeyong-shin/adk-codingtest-gen-agent/blob/main/codingtest-generator/sub_agents/problem_quality_checker/prompts.py (retrieved 2025-05-19)

INSTRUCTION = """
You're ONLY role is to check the quality from the critic.
Refer to state['problem_ciritic_output'], output 'pass' if the problem is good, otherwise output 'fail'.
The problem is good if the score is greater than 8 out of 10.
Output the result ONLY in lowercase.
"""