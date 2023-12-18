import pandas as pd
import datetime

def jobtime() -> datetime:
  sa_time = datetime.datetime.now()
  jobtime = datetime.datetime.strptime(sa_time.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
  return jobtime

# def clean_func (col, clean_col):
#   col.columns = col.columns.str.lower()
#   for i, j in clean_col.items():
#     col.columns = col.columns.str.replace(i, j, regex=True)
#   return col

def standarized_columns(df: pd.DataFrame) -> pd.DataFrame:
    replace = {' ' : '_',
               '-' : '_',
               '.' : '_',
               ' ' : '_',
               '__' : ''}
    
    df.columns = df.columns.str.lower()
    for i, j in replace.items():
        df.columns = df.columns.str.replace(i, j, regex=False)
    df["job_insertdate"] = jobtime()
    return df