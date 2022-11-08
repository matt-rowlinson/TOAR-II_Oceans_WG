import cartopy.io.shapereader as shpreader
import shapely.geometry as sgeom
from shapely.ops import unary_union
from shapely.prepared import prep

land_shp_fname = shpreader.natural_earth(resolution='10m',
                                               category='physical', name='land')

land_geom = unary_union(list(shpreader.Reader(land_shp_fname).geometries()))
land = prep(land_geom)

def is_land(x, y, res="50m"):
    return land.contains(sgeom.Point(x, y))


def main():
    
    land_example  = is_land( -0.238, 53.872)
    ocean_example = is_land(  0.069, 53.872)
    print( land_example  )
    print( ocean_example )


if __name__=="__main__":
    main()
