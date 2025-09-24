import pandas as pd

df = pd.read_excel("uber_ride_data.xlsx")

#Handling Missing Values 

df.loc[df['Trip_Status'] == "Completed", 'cancellation_reason'] = None 

if 'Trip_Status' in df.columns and 'cancellation_reason' in df.columns:
    df.loc[
        (df['Trip_Status'] == 'Cancelled') &
        (df['cancellation_reason'].isna() | (df['cancellation_reason'].str.strip() == "")),'cancellation_reason'
    ] = "Unknown"

#Updating Columns
#Calculate total trips per user

trip_count = df['user_id'].value_counts().reset_index()
trip_count.columns = ['user_id','trip_count']

#Merge into main dataset

df = df.merge(trip_count, on = 'user_id', how = 'left')

#Classification of cutomer_type

def classify_customer(trip_counts):
    if trip_counts == 1:
        return "New"
    elif trip_counts <= 5:
        return "Occasional"
    elif trip_counts <= 13:
        return "Regular"
    else:
        return "Loyal"

df['customer_type'] = df['trip_count'].apply(classify_customer)

df = df.drop(columns=['trip_count'])

#Fix Data Types

df['trip_date'] = pd.to_datetime(df['trip_date']).dt.date
# df['trip_time'] = pd.to_datetime(df['trip_time']).dt.time


df.to_excel("uber_ride_data.xlsx", index=False)