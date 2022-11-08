import pandas as pd
import numpy as np
import glob 

##############################-MAIN-SCRIPT-#####################################
def main():
    path = '/mnt/lustre/users/mjr583/TOAR-II/csv_files'
    for f in sorted(glob.glob( f'{path}/*_*days_all.csv')):
        site = f[43:-14]
        days = f[-13:-12]
     
        df = pd.read_csv( f, index_col=0)
        ocean = df[df.is_oceanic==1.].count().values
        land  = df[df.is_oceanic==0.].count().values
    
        a = np.round( land / (ocean+land) * 100, 2 )[0]
        print( f'At {site} using {days}days:', a, '% of data removed' )
    
if __name__=="__main__":
    main()
