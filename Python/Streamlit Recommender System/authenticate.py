import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import json

#def save_activities():
#  with open('activities.json', 'w') as outfile:
#    json.dump(st.session_state['activities'], outfile)

def authenticate():

	#0. Load users
	df_users = pd.read_json('users.json')

	#def save_activities():
	#with open('users.json', 'w') as outfile:
	#	json.dump(st.session_state['users'], outfile)
	# function that processes an activity
	#def activity(id, activity):
  	#	data = {'content_id': id, 'activity': activity, 'user_id': st.session_state['user'], 'datetime': str(datetime.datetime.now())}
  	# add to the session state
  	#	st.session_state['activities'].append(data)
  # directly save the activities
  	#	save_activities()
	
	#1. retrieve user credentials
	names = df_users['name'].tolist()
	passwords = df_users['password'].tolist()

	#2. create a hash for each passwords so that we do not send these in the clear
	hashed_passwords = stauth.Hasher(passwords).generate()

	#3. create the authenticator which will create an authentication session cookie with an expiry interval
	authenticator = stauth.Authenticate(names, names, hashed_passwords, 'streamlit-auth-0','streamlit-auth-0-key',cookie_expiry_days=1)

	#4. display the login form in the sidebar 
	name, authentication_status, username = authenticator.login('Login','sidebar')

	#5. the streamlit_authenticator library keeps state of the authentication status in streamlit's st.session_state['authentication_status']

	# > if the authentication succeeded (i.e. st.session_state['authentication_status'] == True)
	if st.session_state['authentication_status']:
		# display name on the sidebar
		with st.sidebar:
			st.text("Welcome  " + name)			

		# set user id in session state
		user_id = int(df_users[df_users['name'] == name]['id'].iloc[0])
		st.session_state['user'] = user_id
		st.session_state['name'] = name
	
		
	# > if the authentication failed
	elif st.session_state['authentication_status'] == False:
		# write an error message on the sidebar
		with st.sidebar:
			st.error('Username/password is incorrect')

	# > if there are no authentication attempts yet (e.g., first time visitors)
	elif st.session_state['authentication_status'] == None:
		# write an warning message on the sidebar
		with st.sidebar:
			st.write("______________________")			
			st.warning('If you are new here, Please enter your username and password in the sidebar')
			username1 = st.text_input('User Name', ' ')
			pass1 = st.text_input('Password', ' ')
			# #st.write('Welcome', username1)
			names.append(username1)
			passwords.append(pass1)
	return name

			
			
