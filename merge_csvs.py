
import pandas as pd
import glob
dfs=[]
for infile in sorted(glob.glob('/users/mjr583/scratch/TOAR-II/CVAO_5days*.csv')):
    df=pd.read_csv(infile, index_col=0)
    dfs.append(df)

df=pd.concat(dfs)
df.to_csv('/users/mjr583/scratch/TOAR-II/CVAO_5days_all.csv',sep=",",header='column_names') 
