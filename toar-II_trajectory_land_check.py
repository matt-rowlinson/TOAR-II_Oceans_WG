#!/usr/bin/env python3
#SBATCH --job-name=oceanic_check
#SBATCH --ntasks=1
#SBATCH --mem=16Gb
#SBATCH --partition=nodes
#SBATCH --time=04:00:00
import sys
sys.path.append('/mnt/lustre/users/mjr583/TOAR-II')
import land_mask
import xarray as xr
import os
import pandas as pd

def find_file_list(path, substrs):
    ## Find all available trajectory files for ##
    ## particular site and date (using string) ##
    file_list =[]
    for root, directory, files in os.walk(path):
        for f in files:
            for s in substrs:
                if s in f:
                    file_list.append(os.path.join(root, f))
    file_list.sort()
    return file_list

def oceanic_airmass(f, days=5):
    ## For each file read coordinates of released particles and get the average ##
    ## trajectory each time step. Then loop through timesteps to check is_land  ##
    ## until reaching the chosen maximum time in seconds (e.g. 3 days=259200s)  ##

    ds = xr.open_dataset( f, decode_times=False )
    secs = ds.seconds_since_release.values
    lats = ds['Latitude' ].mean(axis=1).values
    lons = ds['Longitude'].mean(axis=1).values
    alts = ds['Altitude' ].mean(axis=1).values

    is_oceanic = 1.
    for d, x, y, z in zip( secs, lons, lats, alts):
        if d <= (days * 86400):
            if z < 1000.:
                if land_mask.is_land( x, y ):
                    is_oceanic = 0.
                    #print( x, y )
        else:
            return ds.title[-12:], is_oceanic

##############################-MAIN-SCRIPT-#####################################
def main():
    site    ='mace_head'    ## Select site for analysis 
    run_for = "20"          ## Select year/s. For all years I can just use "20"
    days    = 5             ## Number of days to check only oceanic
    
    ## Generate list of files
    path = f'/mnt/lustre/users/mjr583/flexpart/{site}/netcdfs/'
    print( path, run_for )
    file_list = find_file_list( path, [run_for] )
    
    ## For each file for n days determine whether trajectory passed over land 
    ## oceanic==1, land==0 
    dates=[] ; results=[] 
    for f in file_list:
        date, result =  oceanic_airmass( f, days=days ) 
        dates.append( date )
        results.append( result )
    
    ## Convert result to dataframe and save to csv file
    df = pd.DataFrame( { 'is_oceanic' : results } , index=dates )
    df.to_csv(f'csv_files/{site}_{days}days_{run_for}.csv')
    
if __name__=="__main__":
    main()
