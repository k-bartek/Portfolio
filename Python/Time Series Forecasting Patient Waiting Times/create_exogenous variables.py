
import pandas as pd
import numpy as np
import datetime
import holidays

#insert the current intershift df
start_date = df_i['%datum'].iloc[0]
end_date = df_i['%datum'].iloc[-1]


# Create a DatetimeIndex with hourly frequency
datetime_index = pd.date_range(start=start_date, end=end_date, freq='H')
df = pd.DataFrame({'datetime': datetime_index})


#make a day out of datetime
df['datetime'] = pd.to_datetime(df['datetime'])
df['datetime1'] = pd.to_datetime(df['datetime'])


#add calendar data 
def add_Feature_Columns(data_frame):
    
    # Add min, hour, day of week (monday = 0) and date
    ____
    # Add season (winter = 1)
    ____
    # Add holiday as well (day = -1)
    now = datetime.datetime.now()
    holidays_nl = holidays.Netherlands(years = list(range(2018, now.year+1)))
    data_frame['holiday'] = data_frame['date'].isin(holidays_nl).astype(int)
    #data_frame['week_day'] = data_frame['date'].isin(holidays_nl).astype(int) * -1
    data_frame.loc[data_frame['holiday'] == 1, 'week_day'] = -1
    data_frame = data_frame.drop(columns= ['holiday'])
    
add_Feature_Columns(df)



#add dummies
#week day dummies
df_encoded = pd.get_dummies(df['week_day'], prefix='Day')
df = pd.concat([df, df_encoded], axis=1)

#season dummies
_____

df.set_index('datetime', inplace=True)

#add open
#create variable open that takes on val 1 when Day_-1 is 1 or Day_5 or Day_6 are 1, or the  time in index is in 00:00:00 - 8:00:00 or 17:00:00-00:00:00
df['open'] = _______
df['open'] = df['open'].astype(int)


#shifts end and start
_______


#add number of shifts from shift schedules - this part of code was modified from the original code done by @Jackie
df_sp=df_i[['start_shift','end_shift']]
# Group the data by start_shift and end_shift and count the number of shifts for each period
df_sc = df_sp.groupby(['start_shift', 'end_shift']).size().reset_index(name='Number of Shifts')

# Create an empty list to store the matched values
shift_counts = []

# Iterate over each row in df
for _, row_t in df.iterrows():
    start = row_t['datetime1'] 
    
    # Find the corresponding row in df_sc where the start falls between start_shift and end_shift
    matched_row = df_sc[(df_sc['start_shift'] <= start) & (start <= df_sc['end_shift'])]
    
    # Check if a match is found
    if not matched_row.empty:
        # Append the Number of Shifts values to the lists
        it=matched_row['Number of Shifts']
        total = it.sum()
        shift_counts.append(total)
       
    else:
        # If no match is found, append NaN values
        shift_counts.append(pd.NA)
        

# Add the Number of Shifts and rooster_shiftcode_int columns to df

____

#save the df
___

