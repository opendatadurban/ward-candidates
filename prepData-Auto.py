# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 07:44:48 2021

@author: matta
"""

import pandas as pd
import json
from collections import defaultdict
import tqdm

df = pd.read_csv('IEC_Candidate_list_2021_LGE.csv')

df = df[df['Ward / PR'] == 'Ward']

# df = df.iloc[:100,:]

df['PR List OrderNo / Ward No'] = df['Ward \ List Order']

c = df.columns

#%%
json_doc = defaultdict(list)

for key in df['Ward \ List Order'].unique():
    dfk = df[df['Ward \ List Order'] == key]
    V = []
    for ind, row in dfk.iterrows():
        V.append({x: row[x] for x in c.drop('Ward \ List Order')})
        
    json_doc[str(key)] = V
    
#%%
for _id in df.T:
    data = df.T[_id]
    key = data['Ward \ List Order']
    # for elt in json_doc[key]:
    #     if elt["date"] == data.date:
    #         elt[data.student] = data.grade
    #         break
    # else:
    values = {x: data[x] for x in c.drop('Ward \ List Order')}
    json_doc[key].append(values)

# print(json.dumps(json_doc, indent=4))

#%%

json.dump(json_doc, open('data.json', 'w'))

