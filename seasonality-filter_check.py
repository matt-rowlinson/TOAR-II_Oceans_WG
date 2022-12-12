import pandas as pd
import numpy as np
import glob 
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
##############################-MAIN-SCRIPT-#####################################
import sys
def data_loss(f):
    site = f[43:-14]
    days = f[-13:-12]
     
    df = pd.read_csv( f, index_col=0)
    df.index = pd.to_datetime( df.index, format='%Y%m%d%H%M' )
    mons = [[12,1,2],[3,4,5],[6,7,8],[9,10,11]]
    a_=[]
    for s in range( 4):
        d = df[df.index.month.isin( mons[s] )]
        ocean = d.is_oceanic[d.is_oceanic==1.].count()#.values
        land  = d.is_oceanic[d.is_oceanic==0.].count()#.values
    
        a = np.round( land / (ocean+land) * 100, 2 )
        a_.append( a )
    #print( f'At {site} using {days}days:', a, '% of data removed' )
    return site, days, a_ 

def main():
    sites=['cvao', 'mace_head','cape_grim','minamitorishima',
           'hateruma','tudor_hill','ragged_point']
    path = '/mnt/lustre/users/mjr583/TOAR-II/csv_files'
    first=True
    for site in sites:
        v=[]
        for f in sorted(glob.glob( f'{path}/{site}_5days_all.csv')):
            site, days, pc = data_loss(f)
            #v.append( pc )
            print( pc )
        if first:
            df = pd.DataFrame( {site:pc}, index=['DJF','MAM', 'JJA', 'SON'])
            first=False
        else:
            df[site] = pc
    print( df )
    plot( df )

def plot(df):
    df.columns=['Cape Verde','Mace Head','Cape Grim','Minamitorishima',
                'Hateruma','Tudor Hill','Ragged Point']
    df=df.transpose() 
    df.plot.bar(figsize=(8,6), rot=45, colormap='viridis')
    plt.ylabel( '% data removed by land filter' )
    plt.tight_layout()
    plt.savefig( 'plots/seasonality_land-filter.bar.png')
    plt.close()
    return

if __name__=="__main__":
    main()
