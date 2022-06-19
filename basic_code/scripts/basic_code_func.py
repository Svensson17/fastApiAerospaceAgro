import numpy
import matplotlib.pyplot as plt
import rasterio.mask
from matplotlib import colors
from sentinelloader import Sentinel2Loader
from shapely.geometry import Polygon
import logging
from basic_code.const import user, password


class MidpointNormalize(colors.Normalize):

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return numpy.ma.masked_array(numpy.interp(value, x, y), numpy.isnan(value))


def basic_function(geometry):
    geo_tiff = get_footprint(geometry)
    img_name = show_ndvi(geo_tiff)
    return img_name


def get_footprint(geometry):
    sl = Sentinel2Loader(
        '/Users/user/PycharmProjects/fastApiAerospaceAgro/geojson_files',
        user,
        password,
        apiUrl='https://scihub.copernicus.eu/dhus/',
        showProgressbars=True,
        loglevel=logging.DEBUG
    )
    area = Polygon(geometry['coordinates'][0][0])
    geoTiffs = sl.getRegionHistory(area, 'NDVI', '10m',  '2022-05-23', '2022-05-26')
    for geoTiff in geoTiffs:
        print('Desired image was prepared at')
        print(geoTiff)
    return geoTiffs[0]


def show_ndvi(geo_tiff):
    with rasterio.open(geo_tiff) as source:
        ndvi = source.read(1)

    numpy.seterr(divide='ignore', invalid='ignore')

    # Min/max values from NDVI range for image
    min = numpy.nanmin(ndvi)
    max = numpy.nanmax(ndvi)

    # Custom midpoint for most effective NDVI analysis
    mid = 0.1

    # Color scheme
    colormap = plt.cm.RdYlGn
    norm = MidpointNormalize(vmin=min, vmax=max, midpoint=mid)
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)

    # Specify the input data, colormap, min, max, and norm for the colorbar
    cbar_plot = ax.imshow(ndvi, cmap=colormap, norm=norm)

    # Turn off the display of axis labels
    ax.axis('off')

    # Set a title
    ax.set_title('Normalized Difference Vegetation Index', fontsize=17, fontweight='bold')

    # Configure the colorbar
    fig.colorbar(cbar_plot, orientation='horizontal', shrink=0.65)
    img_name = 'ndvi-image-new.png'

    # Save this plot to an image file
    fig.savefig(img_name, dpi=200, bbox_inches='tight', pad_inches=0.7)
    return img_name
