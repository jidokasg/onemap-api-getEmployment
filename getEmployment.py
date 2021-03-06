#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Employment Status By Planning Area 

import requests
import pandas as pd

##to update with new token
eToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjM5MzQsInVzZXJfaWQiOjM5MzQsImVtYWlsIjoia2VubnkudGd3QGdtYWlsLmNvbSIsImZvcmV2ZXIiOmZhbHNlLCJpc3MiOiJodHRwOlwvXC9vbTIuZGZlLm9uZW1hcC5zZ1wvYXBpXC92MlwvdXNlclwvc2Vzc2lvbiIsImlhdCI6MTU4MjcwNjM3NCwiZXhwIjoxNTgzMTM4Mzc0LCJuYmYiOjE1ODI3MDYzNzQsImp0aSI6ImFlZDg1ZjljYzZmYmM5ZjI0NjE1N2Y5MjI5NTA1NzhjIn0.7HcPC50d_z6c5aoc3Q88dMeIr1jJMHF-VZ47qOfDHH4"
columns = []

##Create Engine with respective SQL Server Credentials
engine = create_engine("mssql+pyodbc://sa:0000@DESKTOP-8DO4T75\SQLEXPRESS/GovStats?driver=SQL+Server+Native+Client+11.0")

with engine.connect() as con: 
    df = pd.DataFrame(con.execute('SELECT * FROM planningArea').fetchall())

##getting all unique columns
    for row in df.iterrows():
        area = row[1][1] #Get Planning Area 
    
        response = requests.get("https://developers.onemap.sg/privateapi/popapi/getEconomicStatus?token=" + eToken + "&planningArea=" + area + "&year=2010")

        for rows in response.json():
            try:
                for keys in rows.keys():
                    columns.append(keys) if keys not in columns else columns
            except:
                pass

    df2 = pd.DataFrame(columns=columns)

    ##populating database
    for row in df.iterrows():
        area = row[1][1] #Get Planning Area 
        
        response = requests.get("https://developers.onemap.sg/privateapi/popapi/getEconomicStatus?token=" + eToken + "&planningArea=" + area + "&year=2010")

        for rows in response.json():
            try:
                df2 = df2.append(rows, ignore_index = True)
            except:
                pass
            
df2.to_sql('employment', con=engine,if_exists='replace')

engine.dispose()
print('done')

