#!/usr/bin/env python3
#SBATCH --job-name=footprints
#SBATCH --ntasks=1
#SBATCH --mem=16Gb
#SBATCH --partition=nodes
#SBATCH --time=02:30:00
#SBATCH --output=Logs/footprints_%A.log
import sys
sys.path.append('/mnt/lustre/users/mjr583/TOAR-II')
import land_mask
import xarray as xr
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def find_file_list(path, substrs):
    ## Find all available trajectory files for ##
    ## particular site and date (using string) ##
    file_list =[]
    for root, directory, files in os.walk(path):
        for f in files:
            for s in substrs:
                if s in f[:6]:
                    file_list.append(os.path.join(root, f))
    file_list.sort()
    return file_list

def footprint(site, f, days=5):
    ## For each file read coordinates of released particles and get the average ##
    ## trajectory. Return lat/lon coordiantes for that trajectory.              ##

    ds = xr.open_dataset( f, decode_times=False )
    secs = ds.seconds_since_release.values
    lats = ds['Latitude' ].mean(axis=1).values[:days*8]
    lons = ds['Longitude'].mean(axis=1).values[:days*8]
    alts = ds['Altitude'].mean(axis=1).values[:days*8]

    k = alts < 1000.
    if site=='minamitorishima':
        k = (alts<1000)&(lons>100)
        return lons[k], lats[k]
    return lons[k], lats[k]

def plot(site, lons, lats, s_dict):
    f = plt.figure(figsize=(10,5))
    ax = f.add_subplot( projection=ccrs.EqualEarth(),aspect='auto' )
    ax.stock_img()
    tick=0
    for n,s in enumerate(lons):
        cs = s_dict[site[n]]['cs']
        ax.plot( lons[n],  lats[n], alpha=.2, c=cs[tick], 
                    transform=ccrs.PlateCarree() )
        if tick < 4:
            tick += 1
        else:
            tick = 0
    plt.tight_layout()
    return ax


##############################-MAIN-SCRIPT-#####################################
def main():
    sites=['cvao', 'cape_grim', 'ragged_point', 'mace_head', 'tudor_hill',
           'minamitorishima', 'neumayer','hateruma']
    days_=[3,5,7,9]
    seas = [ ["201612","201601","201602"],
             ["201603","201604","201605"], 
             ["201606","201607","201608"], 
             ["201609","201610","201611"] ]
    ss = ['DJF','MAM','JJA','SON']

    s_dict = {
            'cvao' : { 'cs' : ["#ffffb2",'#fecc5c','#fd8d3c','#f03b20','#bd0026'] }, 
            'tudor_hill' : { 'cs' : ['#a1d99b','#74c476','#41ab5d','#238b45','#005a32'] },
            'ragged_point' : { 'cs' : ['#cccccc','#969696','#636363','#252525', 'dimgray'] },
            'mace_head' : { 'cs' : ['#feebe2','#fbb4b9','#f768a1','#c51b8a','#7a0177'] },
            'cape_grim' : { 'cs' : ['#feedde','#fdbe85','#fd8d3c','#e6550d','#a63603'] },
            'minamitorishima' : { 'cs' : ['#cccccc','#969696','#636363','#252525', 'dimgray'] },
            'hateruma' : { 'cs' : ['#fee5d9','#fcae91','#fb6a4a','#de2d26','#a50f15']},
            'neumayer' : { 'cs' : ['#f2f0f7','#cbc9e2','#9e9ac8','#756bb1','#54278f']}
            }
    for days in days_:
        for nn, run_for in enumerate(seas):
            print( days, ss[nn] )
            lons=[] ; lats=[] ; sit_=[]
            for n, site in enumerate(sites):
                ## Generate list on files
                path = f'/mnt/lustre/users/mjr583/flexpart/{site}/netcdfs/'
                file_list = find_file_list( path, run_for )
                
                for f in file_list:
                    #print( f )
                    lon, lat =  footprint( site, f , days=days ) 
                    lons.append( lon )
                    lats.append( lat )
                    sit_.append( site)
                
            ax = plot( sit_, lons, lats, s_dict )
            ax.text( -181, 58, f'{ss[nn]} \n{days} days', fontsize=20, weight='bold', transform=ccrs.PlateCarree() )
            plt.savefig(f'plots/{ss[nn]}.footprints.{days}days.png')
            plt.close()

if __name__=="__main__":
    main()
