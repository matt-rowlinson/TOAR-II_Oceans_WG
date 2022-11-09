import pandas as pd
import numpy as np
import glob 
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
##############################-MAIN-SCRIPT-#####################################

def data_loss(f):
    site = f[43:-14]
    days = f[-13:-12]
     
    df = pd.read_csv( f, index_col=0)
    ocean = df.is_oceanic[df.is_oceanic==1.].count()#.values
    land  = df.is_oceanic[df.is_oceanic==0.].count()#.values
    
    a = np.round( land / (ocean+land) * 100, 2 )
    #print( f'At {site} using {days}days:', a, '% of data removed' )
    return site, days, a 

def main():
    sites=['cvao', 'hateruma','cape_grim','minamitorishima','tudor_hill',
            'mace_head','ragged_point']
    path = '/mnt/lustre/users/mjr583/TOAR-II/csv_files'
    first=True
    for site in sites:
        v=[]
        for f in sorted(glob.glob( f'{path}/{site}_*days_all.csv')):
            site, days, pc = data_loss(f)
            v.append( pc )
        if first:
            df = pd.DataFrame( {site:v}, index=['3 days','5 days', '7 days', '9 days'])
            first=False
        else:
            df[site] = v
    print( df )
    plot( df )

def plot(df):
    df=df.transpose() 
    df.plot.bar(figsize=(8,6), rot=45, colormap='viridis')
    plt.tight_layout()
    plt.savefig( 'TEST.plot.png')
    plt.close()
    return

if __name__=="__main__":
    main()
