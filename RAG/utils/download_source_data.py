#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os
import requests
from pathlib import Path


url = 'https://raw.githubusercontent.com/LangChain-OpenTutorial/LangChain-OpenTutorial/main/10-Retriever/data/01-vectorstore-retriever-appendix-keywords.txt'
response = requests.get(url)

data_dir = Path(os.path.dirname(__file__)) / "../data"
os.makedirs(data_dir, exist_ok=True)

file_name = url.split('/')[-1]
output_path = data_dir / file_name
with open(output_path, "wb") as f:
  f.write(response.content)
