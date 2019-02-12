#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 09:52:55 2018

@author: jimwaldo
"""

import json

def get_unique_ids(fin, id_set):
    for l in fin:
        try:
            jl = json.loads(l)
            if 'id' in jl:
                id_set.add(jl['id'])
        except():
            continue
    return id_set
