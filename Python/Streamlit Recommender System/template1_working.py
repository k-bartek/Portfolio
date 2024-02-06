import streamlit as st
from random import random
import json
import pandas as pd
import numpy as np
import csv
import math

df_films = pd.read_csv('BBC_merged1.csv' , header = 0, sep=',',
                     na_values = ['na', '-', '.', ''], low_memory=False)

df3 = pd.read_csv('all_picked.csv' , header = 0, sep=',',
                     na_values = ['na', '-', '.', ''], low_memory=False)
 
# set film session state
def select_film(id):
  st.session_state['id'] = id
  print(id)

# set film session state
def liked(id):
  st.session_state['id'] = id
  if (math.isnan(df3['user1'].loc[id])):
    value = 0
  else:
    value = df3['user1'].loc[id]
  if (value == -1.25):
    value = -0.25
  elif (value == -1):
    value = 1
  elif (value == -0.75):
    value = 1.25
  elif (value == -0.25):
    value = 0.75
  elif (value == 0):
    value = 1
  elif (value == 0.25):
    value = 1.25
  elif (value == 0.75):
    value = 0.75
  elif (value == 1):
    value = 1
  elif (value == 1.25):
    value = 1.25
  df3['user1'].loc[id] = value
  print(df3['user1'].loc[id])
  print(id)


def disliked(id):
  st.session_state['id'] = id
  if (math.isnan(df3['user1'].loc[id])):
    value = 0
  else:
    value = df3['user1'].loc[id]
  if (value == -1.25):
    value = -1.25
  elif (value == -1):
    value = -1
  elif (value == -0.75):
    value = -0.75
  elif (value == -0.25):
    value = -1.25
  elif (value == 0):
    value = -1
  elif (value == 0.25):
    value = -0.75
  elif (value == 0.75):
    value = -1.25
  elif (value == 1):
    value = -1
  elif (value == 1.25):
    value = -0.75
  df3['user1'].loc[id] = value
  print(df3['user1'].loc[id])
  print(id)

def tile_item(column, item):
  with column:
    #st.button(, key=random(), on_click=select_film, args=(item['id'], ))
    
    #st.image(item['image'], use_column_width='always')

    button_1, button_2, empt_1, empt_2 = st.columns([1,1,1,1])

    with button_1:
      like_button = st.button('👍' , key=random(), on_click=liked, args=(item['id'],  ), type="secondary", use_container_width= False) #change the on_click functions to working with df
    with button_2:
      dislike_button = st.button('👎' , key=random(), on_click=disliked, args=(item['id'], ), type="secondary", use_container_width= False)
    
    st.image(item['image'], use_column_width='always')
    #st.caption(item['title'])
    st.button(item['title'] , key=random(), on_click=select_film, args=(item['id'], ), use_container_width=True)
    #st.button('Watch 🎬', key=random(), on_click=select_film, args=(item['id'], )) #ISBN 🎬



def recommendations(df):

  # check the number of items
  nbr_items = df.shape[0]

  if nbr_items != 0:    

    # create columns with the corresponding number of items
    columns = st.columns(nbr_items)

    # convert df rows to dict lists
    items = df.to_dict(orient='records')

    # apply tile_item to each column-item tuple (created with python 'zip')
    any(tile_item(x[0], x[1]) for x in zip(columns, items))



