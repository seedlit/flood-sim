"""
Flood Simulation - identifying which areas will be inundated first.
Author: Naman Jain
        naman.jain@btech2015.iitgn.ac.in
        www.namanji.wixsite.com/naman/
"""

import os
from multiprocessing import Pool
import gdal
import numpy as np
import argparse
from src.generate_flooded_shps import generate_flooded_shp
from src.generate_screenshots import save_water_logged_img
from src.generate_gif import save_gif_with_pil


def get_lower_elev(dsm_path, lower_percentile=5):
    dsm_array = gdal.Open(dsm_path).ReadAsArray()
    return int(np.percentile(dsm_array, lower_percentile) * 100)


def get_upper_elev(dsm_path, upper_percentile=95):
    dsm_array = gdal.Open(dsm_path).ReadAsArray()
    return int(np.percentile(dsm_array, upper_percentile) * 100)


if __name__ == "__main__":

    # define inputs ---------------------------------------
    parser = argparse.ArgumentParser(description="Simulate water inundation")
    parser.add_argument(
        "--dsm", help="path to DSM (Digital Surface Model) tif image", type=str
    )
    parser.add_argument("--rgb", help="path to corresponding RGB tif image", type=str)
    parser.add_argument(
        "--num_processes",
        default=1,
        help="No. of processes to run in parallel. Increase to speed up processing",
    )
    parser.add_argument(
        "--start_elev",
        default=0,
        help="lower threshold of elevation values in DSM for simulation",
    )
    parser.add_argument(
        "--end_elev",
        default=0,
        help="upper threshold of elevation values in DSM for simulation",
    )
    parser.add_argument(
        "--step_size", default=10, help="rise water level by this amount in each step"
    )
    parser.add_argument(
        "--gif_duration", default=30, help="time in seconds for the generated gif"
    )
    parser.add_argument(
        "--opaqueness",
        default=0.7,
        help="water opaqueness factor; 0 means absolute transparent, 1 means absolute opaque",
    )

    args = parser.parse_args()
    dem_path = args.dsm
    rgb_tif_path = args.rgb
    num_processes = args.num_processes
    start_water_level_cm = args.start_elev
    end_water_level_cm = args.end_elev
    step_size_cm = args.step_size
    water_opaqueness_factor = args.opaqueness
    gif_duration = args.gif_duration
    out_dir = "generated_results"

    # update start and end elevation thresholds if required
    if start_water_level_cm == 0:
        start_water_level_cm = get_lower_elev(dem_path)
    if end_water_level_cm == 0:
        end_water_level_cm = get_upper_elev(dem_path)

    # -------------------------------------------------------
    # this part generates the flooded tifs and shapfiles
    print("Generating the flooded DEMs and shapefiles")
    flooded_files_out_dir = os.path.join(out_dir, "flooded_tifs_and_shps")
    os.makedirs(flooded_files_out_dir, exist_ok=True)
    task_list = []
    for i in range(
        start_water_level_cm, end_water_level_cm + step_size_cm, step_size_cm
    ):
        task_list.append([dem_path, i / 100, flooded_files_out_dir])
    print("Files for total {} sea rise levels will be generated".format(len(task_list)))
    p = Pool(num_processes)
    p.starmap(generate_flooded_shp, task_list)
    p.close()
    p.join()

    # this part generates screenshots --------------------------------------------
    print("Generating screenshots")
    screenshots_dir = os.path.join(out_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    task_list = []
    for filename in os.listdir(flooded_files_out_dir):
        if filename.endswith(".shp"):
            shp_path = os.path.join(flooded_files_out_dir, filename)
            task_list.append(
                [rgb_tif_path, shp_path, screenshots_dir, water_opaqueness_factor]
            )
    print("total {} screenshots will be generated".format(len(task_list)))
    p = Pool(num_processes)
    p.starmap(save_water_logged_img, task_list)
    p.close()
    p.join()

    # this part generates the gif using generated screenshots -----------------------
    print("Generating GIF")
    out_gif_path = os.path.join(out_dir, "generated_gif.gif")
    save_gif_with_pil(screenshots_dir, out_gif_path, gif_duration)
    print("FINISHED!")
    print("Generated GIF at: ", out_gif_path)
