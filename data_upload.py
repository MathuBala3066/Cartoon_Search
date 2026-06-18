from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://postgres:Mathu%4012345@localhost:5432/Cartoon_Data')

df =pd.read_csv('Cartoon_datasets.csv')

df.to_sql('Cartoon_Details', engine, if_exists='replace', index=False)

print("Data uploaded successfully!")