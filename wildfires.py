import sqlite3
import pandas as pd
import numpy as np
import datetime as dt
import xlrd
import re 

pattern = r'\d'


conn = sqlite3.connect('wildfires.sqlite')
c = conn.cursor()
query = '''select *, DATE('1899-12-30' + DISCOVERY_DATE) as DISCOVERED_DATE,
DATE('1899-12-30' + CONT_DATE) as CONTAINED_DATE 
from fires limit 10000
	'''
df = pd.read_sql_query(query, conn)
cols = ['SOURCE_SYSTEM_TYPE', 'SOURCE_SYSTEM',
       'NWCG_REPORTING_AGENCY', 'NWCG_REPORTING_UNIT_ID',
       'NWCG_REPORTING_UNIT_NAME', 'FIRE_NAME',
       'FIRE_YEAR', 'DISCOVERED_DATE', 'DISCOVERY_DOY',
       'DISCOVERY_TIME', 'STAT_CAUSE_CODE', 'STAT_CAUSE_DESCR', 'CONTAINED_DATE',
       'CONT_DOY', 'CONT_TIME', 'FIRE_SIZE', 'FIRE_SIZE_CLASS', 'LATITUDE',
       'LONGITUDE', 'OWNER_CODE', 'OWNER_DESCR', 'STATE', 'COUNTY',
       'FIPS_CODE', 'FIPS_NAME']
df = df[['DISCOVERED_DATE', 'CONTAINED_DATE', 'STATE', 'FIPS_NAME', 'FIRE_SIZE']]
df['DISCOVERED_DATE'] = pd.to_datetime(df['DISCOVERED_DATE'])
df['CONTAINED_DATE'] = pd.to_datetime(df['CONTAINED_DATE'])
df['DAYS_UNTIL_CONTAINMENT'] = df['CONTAINED_DATE'] - df['DISCOVERED_DATE']  
df['DAYS_UNTIL_CONTAINMENT'] = df['DAYS_UNTIL_CONTAINMENT'].astype('timedelta64[D]')
df = df[df['FIPS_NAME'].isin(['Plumas', 'Siskiyou', 'San Francisco'])]
df = df.set_index('DISCOVERED_DATE', 'CONTAINED_DATE')
df = df.groupby(['STATE', 'FIPS_NAME']).agg({'FIRE_SIZE': ['mean', 'min', 'max'], 'DAYS_UNTIL_CONTAINMENT': ['mean', 'min', 'max']})

print(df)







