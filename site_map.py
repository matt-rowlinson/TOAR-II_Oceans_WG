#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_map(df):

    f = plt.figure(figsize=(10,5))
    ax = f.add_subplot( projection=ccrs.EqualEarth(),aspect='auto' )
    ax.stock_img()
    for n,s in enumerate(df.index):
        if s in ['Neumayer']:
            continue
        ax.scatter( df.loc[s]['lon'],  df.loc[s]['lat'], marker='*', s=400, c='gold', edgecolor='k', 
                    transform=ccrs.PlateCarree(), label=s )
        yoffset=-7 if s in ['Hateruma'] else -5
        xoffset= 10 if s in ['Neumayer','Cape Grim'] else 4

        ax.text( df.loc[s]['lon']+xoffset,  df.loc[s]['lat']+yoffset, s, transform=ccrs.PlateCarree() )
    
    plt.tight_layout()
    plt.savefig('plots/sitemap.png')
    plt.close()
    return

def main():
    df = pd.read_csv( 'toar-II_test_sites.csv', index_col=0 )
    print( df )
    df = df.transpose()
    
    plot_map(df)

if __name__ == "__main__":
    main()
