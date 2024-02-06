
import streamlit as st
import pandas as pd
import template1_working as t


st.set_page_config(
    page_title="Jack Recommends...",
    page_icon="🎬",
    layout="wide")

st.markdown(""" <style> div.stButton > button:first-child { background-color: rgb(227, 87, 146); } </style>""", unsafe_allow_html=True) 



def header(url):
     st.markdown(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

st.sidebar.title("Explore Feature")
st.sidebar.write("Go back to Your Selection")
st.sidebar.caption("[Click Here to go back to your own recommendations🖱️](http://localhost:8501/)")

# load the dataset with the books

#df_books = pd.read_csv('recommendations/BX-Books.csv', sep=';', encoding='latin-1', low_memory=False)

df_films = pd.read_csv('BBC_merged1.csv' , header = 0, sep=',',
                     na_values = ['na', '-', '.', ''], low_memory=False)





# select a book to kickstart the interface

if 'id' not in st.session_state:
  st.session_state['id'] = 5



df_film = df_films[df_films['id'] == st.session_state['id']]

df_1 = pd.read_csv('other_cluster.csv', sep=',')
#df = pd.read_csv('recommendations/recommendations-most-reviewed copy.csv', sep=';', encoding='latin-1', dtype=object)
df_1 = df_1[["id"]]
df_1 = df_1.merge(df_films, on='id')
df_1 = df_1.head(6)
#t.recommendations(df_1)

st.markdown("<h2 style='text-align: center; color: white;'>Expand Your Horizons</h2>", unsafe_allow_html=True)

inf, selection = st.columns([2,2])

with selection:
  # display the image - replace by the moving selection of Jack
  st.image(df_1['image'].iloc[0])

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
  


st.subheader("")

# create a cover and info column to display the selected book
#cover, info = st.columns([2, 3])

info, cover = st.columns([1, 3])


#not interactive yet, works on user 2 for now
#fix with session state
st.subheader("Jack's Top Recommendations")
df = pd.read_csv('other_cluster.csv', sep=',')
#df = pd.read_csv('recommendations/recommendations-most-reviewed copy.csv', sep=';', encoding='latin-1', dtype=object)
df = df[["id"]]
df = df.merge(df_films, on='id')
df = df.head(5)
t.recommendations(df)

st.subheader('Documentaries')
df = pd.read_csv('BBC/documentaries_userdata.csv', sep=',')
df = df.rename(columns={"Unnamed: 0": "id"})  #problem in unnamed, possible to merge by title, but then duplicates present
#df = df[['id']] 
#df = df.merge(df_films, on='id') #id
    #alterntive with 'title' - comment out the two lines above
df = df[['title']] 
df = df.merge(df_films, on='title').drop_duplicates() #id
df = df.head(6)
t.recommendations(df)



st.subheader('Comedies')
df = pd.read_csv('BBC/documentaries_userdata.csv', sep=',')
df = df.rename(columns={"Unnamed: 0": "id"})
df = df[['id']]
df = df.merge(df_films, on='id') #id
df = df.head(6)
t.recommendations(df)

st.subheader('Films')
df = pd.read_csv('BBC/films_userdata.csv', sep=',')
df = df.rename(columns={"Unnamed: 0": "id"})  
df = df[['id']]
df = df.merge(df_films, on='id') #id
df = df.head(6)
t.recommendations(df)

st.subheader('Science and Nature')
df = pd.read_csv('BBC/science-and-nature_userdata.csv', sep=',')
df = df.rename(columns={"Unnamed: 0": "id"})
df = df[['id']]
df = df.merge(df_films, on='id') #id
df = df.head(6)
t.recommendations(df)

st.subheader('Sports')
df = pd.read_csv('BBC/sports_userdata.csv', sep=',')
df = df.rename(columns={"Unnamed: 0": "id"})
df = df[['id']]
df = df.merge(df_films, on='id') #id
df = df.head(6)
t.recommendations(df)

st.caption("*Jack is a fictional character")

#st.markdown("<h2 style='text-align: center; color: white;'>Expand Your Horizons</h2>", unsafe_allow_html=True)

#st.markdown(
#            "###### [![this is an image link](https://informitv.com/wordpress/wp-content/uploads/2021/10/BBC-iPlayer.png)](https://www.bbc.co.uk/iplayer)"
#        )





#m = 
#b = st.button("test")
