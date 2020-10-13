import pandas as pd 
import numpy as np
from collections import defaultdict
import re

pattern = r'([a-zA-Z\-\.\s]+)'

df = pd.read_csv('zillow_home_prices.csv')
col = df.columns

counties = defaultdict(list)

for county in df[col[2]]:
	match = re.findall(pattern, county)
	counties['Counties'].append(match[0])

counties = pd.DataFrame(data=counties)
df = pd.concat([df, counties], axis=1)


df['RegionName'] = df['Counties']
df.rename( columns = {'RegionName': 'Counties'}, inplace=True)


print(df)

