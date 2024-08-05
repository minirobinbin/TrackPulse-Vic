import operator
from shutil import ExecError
from tracemalloc import stop
from cycler import V
from discord.ext import commands, tasks
from discord import app_commands
import discord
import json
import requests
import re
import asyncio
import threading
import queue
from datetime import datetime
import time
import csv
import random
import pandas as pd
from typing import Literal, Optional
import typing
import enum
from re import A
from io import StringIO
import numpy as np
import io

from utils import trainset
from utils.search import *
from utils.colors import *
from utils.stats import *
from utils.pageScraper import *
from utils.trainImage import *
from utils.checktype import *
from utils.rareTrain import *
from utils.montagueAPI import *
from utils.map.map import *
from utils.game.lb import *
from utils.trainlogger.main import *
from utils.trainset import *
from utils.trainlogger.stats import *
from utils.trainlogger.ids import *
from utils.unixtime import *
from utils.pastTime import *
from utils.routeName import *
from utils.trainlogger.graph import *
from utils.locationFromNumber import *
from utils.photo import *

'''print(routes_list(0))
print(routes_list(3))'''
line = 'Ballarat-Wendouree - Melbourne via Melton'
line = line.replace(" ","%20")
json_info_str = route_api_request(line, "3")
print(json_info_str)
'''print(getUrl(f'/v3/routes/?route_name="Ballarat-Wendouree - Melbourne via Melton"&route_types=3'))
print(getUrl(f'/v3/routes/?route_name=Belgrave&route_types=0'))'''
