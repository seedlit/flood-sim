# TODO: ensure same CRS for vector and raster

import os
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio as rio
from rasterio.plot import plotting_extent
import earthpy.plot as ep
from multiprocessing import Pool
import gc


def get_raster_extent(raster_path):
    with rio.open(raster_path) as raster:
        raster_extent = plotting_extent(raster)
        return raster_extent


def get_rio_array(raster_path):
    with rio.open(rgb_tif_path) as raster:
        raster_plt_array = raster.read()
        return raster_plt_array


def get_shp_area(shp_path):
    shp = gpd.read_file(shp_path)
    return round(sum(shp.area), 2)


def save_water_logged_img(rgb_tif_path, src_shp_path, out_dir, shp_transparency_factor):
    try:
        water_level = src_shp_path.split("/")[-1].split(".")[0].split("_")[-1]
        out_img_path = os.path.join(out_dir, "{}.png".format(water_level))
        f, ax = plt.subplots()
        raster_extents = get_raster_extent(rgb_tif_path)
        raster_array = get_rio_array(rgb_tif_path)
        flooded_area = get_shp_area(src_shp_path)        
        ep.plot_rgb(
            raster_array,
            rgb=[0, 1, 2],
            ax=ax,
            title="Water logging at elevation: {}; Area flooded: {} metres square".format(water_level, flooded_area),
            extent=raster_extents,
        )  # Use plotting extent from DatasetReader object
        shp = gpd.read_file(src_shp_path)
        shp.plot(ax=ax, alpha=shp_transparency_factor)
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(12, 9)
        plt.savefig(out_img_path)
        figure.clf()  # for releasing memory
        plt.close()   # for releasing memory
        gc.collect()  # for releasing memory
    except Exception as e:
        print("some error occured in ", shp_path)
        print("error: ", e)


if __name__ == "__main__":

    shp_dir = "/home/naman/Desktop/side_projects/flood_sim/iitgn_results"
    rgb_tif_path = "/home/naman/Desktop/side_projects/flood_sim/data/ortho_3_bands.tif"
    out_dir = "iitgn_new_screenshots"
    num_processes = 2

    os.makedirs(out_dir, exist_ok=True)

    task_list = []
    for filename in os.listdir(shp_dir):
        if filename.endswith(".shp"):
            shp_path = os.path.join(shp_dir, filename)
            task_list.append([rgb_tif_path, shp_path, out_dir, 0.7])                            

    print("total {} screenshots will be generated".format(len(task_list)))
    p = Pool(num_processes)
    p.starmap(save_water_logged_img, task_list)
    p.close()
    p.join()
                
                
            
