#! /usr/bin/env python3
"""This manages the connection to MongoDB"""

# Shh pylint
#pylint: disable=C0103
from pymongo import MongoClient
from helpers.util import from_config_yaml

__all__ = ["db", "client"]

client = MongoClient(from_config_yaml('db'))
db = client.logs
