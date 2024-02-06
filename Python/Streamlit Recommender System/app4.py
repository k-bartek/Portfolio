import streamlit as st
import pandas as pd
import template1_working as t
import authenticate as a
from streamlit_option_menu import option_menu
import math
import get_recomms as g
import random

def finished(id):
  if (math.isnan(t.df3['user1'].loc[id])):
    value = 0
  else:
    value = t.df3['user1'].loc[id]
  if (value == -1.25):
    value = -0.75
  elif (value == -1):
    value = -0.75
  elif (value == -0.75):
    value = -0.75
  elif (value == -0.25):
    value = 0.25
  elif (value == 0):
    value = 0.25
  elif (value == 0.25):
    value = 0.25
  elif (value == 0.75):
    value = 1.25
  elif (value == 1):
    value = 1.25
  elif (value == 1.25):
    value = 1.25
  t.df3['user1'].loc[id] = value

  print(t.df3['user1'].loc[id])
  print(id)

def not_finished(id):
  print(id, '37')
  if (math.isnan(t.df3['user1'].loc[id])):
    value = 0
  else:
    value = t.df3['user1'].loc[id]
  if (value == -1.25):
    value += 0
  elif (value == -1):
    value = -1.25
  elif (value == -0.75):
    value = -1.25
  elif (value == -0.25):
    value = -0.25
  elif (value == 0):
    value = -0.25
  elif (value == 0.25):
    value = -0.25
  elif (value == 0.75):
    value += 0
  elif (value == 1):
    value = 0.75
  elif (value == 1.25):
    value = 0.75
  t.df3['user1'].loc[id] = value

  print(t.df3['user1'].loc[id])
  print(id, '63')
  

st.set_page_config(
    page_title="BBC Main",
    page_icon="📽️",
    layout="wide")
 
st.sidebar.title("Explore Feature")
with st.sidebar:
  col1, col2, col3 = st.columns(3)
  with col1:
    st.write(' ')
  with col2:
    st.image("https://i.guim.co.uk/img/media/d35d6212a3ce2cfd6d0eba984eb78bd562af8d68/0_103_6720_4032/master/6720.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=5632f8fca342fdec1e46bfa01c63249f", width = 100)
  with col3:
    st.write(' ')
st.sidebar.write("Explore what Jack likes. Click on the globe 🌍 above or " + "[here 🖱️](http://localhost:8501/app3)")
st.sidebar.caption("___________________________________")



#log in
user_id = a.authenticate()

if user_id == None:
  g.recomm('user1')

else:
#get recommendations
  g.recomm(user_id)

# load the dataset

df_films = pd.read_csv('BBC_merged1.csv' , header = 0, sep=',',
                     na_values = ['na', '-', '.', ''], low_memory=False)




# create a session state
if 'user' not in st.session_state:
  st.session_state['user'] = 0

if 'activity' not in st.session_state:
  st.session_state['activity'] = 0 #users_activities


# select a film to kickstart the interface
if 'id' not in st.session_state:
  st.session_state['id'] = 5



df_film = df_films[df_films['id'] == st.session_state['id']]


#top panel
selected = option_menu(
  menu_title=None,
  options=["Your Recommendations", "Documentaries", "Comedy", "A-Z", "TV Guides", "My Programmes"],
  icons = ['chevron_down', 'chevron_down', 'chevron_down', 'chevron_down', 'chevron_down'],
  default_index=0,
  orientation="horizontal",
  styles={
  "container": {"padding": "0!important", "background-color": "black"},
  "nav-link": {"font-size": "11px", "text-align": "left", "margin":"0px", "--hover-color": "#E35792"},
  "nav-link-selected": {"background-color": "#E35792"}
  })

info, cover = st.columns([1, 2.5]) #1,3 originally, might be better

with cover:
  # display the image
  st.image(df_film['image'].iloc[0])

with info:
  # display the book information
  st.title(df_film['title'].iloc[0])
  st.markdown(df_film['category'].iloc[0])
  st.caption(str(df_film['description'].iloc[0]) + ' | ' + df_film['duration_txt'].iloc[0])
  center_button = st.button('Watch Now', use_container_width= True, type="primary")

  button1, button2 = st.columns([1,1])

  with button1:
    finished_button = st.button('Finished', on_click=finished, args=(st.session_state['id'],  ), use_container_width= True, type="secondary")
  with button2:
    not_finished_button = st.button('Not Finished', on_click=not_finished, args=(st.session_state['id'],  ), use_container_width= True, type="secondary")


#not interactive yet, works on user 2 for now
#fix with session state
st.subheader('Your Recommendations')
df = pd.read_csv('same_cluster.csv', sep=',')
#df = pd.read_csv('recommendations/recommendations-most-reviewed copy.csv', sep=';', encoding='latin-1', dtype=object)
df = df[["id"]]
df = df.merge(df_films, on='id')
df = df.head(5)
t.recommendations(df)



df2 = df_films
st.subheader('Documentaries')
df = pd.read_csv('BBC/documentaries_userdata.csv', sep=',')
df = df[['title']] 
join_cols = ['title']
df = pd.merge(df, df2[df2.duplicated(subset=join_cols, keep='first') == False],  on=join_cols)
df = df.head(6)
t.recommendations(df)



st.subheader('Comedies')
df = pd.read_csv('BBC/comedy_userdata.csv', sep=',')
df = df[['title']] 
join_cols = ['title']
df = pd.merge(df, df2[df2.duplicated(subset=join_cols, keep='first') == False],  on=join_cols)
df = df.head(6)
t.recommendations(df)


#Expand your horizons section
#not interactive yet, fixed for user2, fix with session state
st.markdown("<h2 style='text-align: center; color: white;'>Expand Your Horizons</h2>", unsafe_allow_html=True)

selection, empty_space, inf = st.columns([3,1, 2])

with selection:
  df_others = pd.read_csv('other_cluster.csv', sep=',',
                     na_values = ['na', '-', '.', ''], low_memory=False)
  df = df_others[["id"]]
  df = df.merge(df_films, on='id')

  # display the image - replace by the moving selection of Jack - Marielle
  st.image(df['image'].iloc[0])
  


with inf:
  # display the book information
  st.title("Meet Jack")
  st.markdown("See what Jack (70) from Liverpool recommends for you") #change age based on user's age to be more similar?
  em1, em2, em3 = st.columns([1,2,1])
  
  with em2:
    st.image(
            "https://i.guim.co.uk/img/media/d35d6212a3ce2cfd6d0eba984eb78bd562af8d68/0_103_6720_4032/master/6720.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=5632f8fca342fdec1e46bfa01c63249f",
            width=150, ) #image selected based on gender 
    #female alterative: https://cdn.firespring.com/images/aaa70846-b54b-4b5b-b6f3-9c1b11fd4478.jpg
  st.caption("Jack enjoys genres: " + str(df_film['category'].iloc[0])) #should be changed based on his favorie genres
  st.caption("[Click Here To Explore Jack's recommendations🖱️](http://localhost:8501/app3)")


st.subheader('Films')
df = pd.read_csv('BBC/films_userdata.csv', sep=',')
df = df[['title']] 
join_cols = ['title']
df = pd.merge(df, df2[df2.duplicated(subset=join_cols, keep='first') == False],  on=join_cols)
df = df.head(6)
t.recommendations(df)

st.subheader('Science and Nature')
df = pd.read_csv('BBC/science-and-nature_userdata.csv', sep=',')
df = df[['title']] 
join_cols = ['title']
df = pd.merge(df, df2[df2.duplicated(subset=join_cols, keep='first') == False],  on=join_cols)
df = df.head(6)
t.recommendations(df)

st.subheader('Sports')
df = pd.read_csv('BBC/sports_userdata.csv', sep=',')
df = df[['title']] 
join_cols = ['title']
df = pd.merge(df, df2[df2.duplicated(subset=join_cols, keep='first') == False],  on=join_cols)
df = df.head(6)
t.recommendations(df)


#CAN BE USED as an inspiration for new session state with user 
#st.subheader('Recommendations based on Frequently Reviewed Together (frequency)')
#df = pd.read_csv('recommendations/recommendations-seeded-freq.csv', sep=';', encoding='latin-1', dtype=object)
#sbn = st.session_state['ISBN']
#df_recommendations = df[df['book_a'] == isbn].sort_values(by='count', ascending=False)
#df_recommendations = df_recommendations.rename(columns={"book_b": "ISBN"})
#df_recommendations = df_recommendations.merge(df_books, on='ISBN')
#t.recommendations(df_recommendations)


t.df3.to_csv('all_picked.csv')

st.markdown(
            "###### [![this is an image link](https://informitv.com/wordpress/wp-content/uploads/2021/10/BBC-iPlayer.png)](https://www.bbc.co.uk/iplayer)"
        )


