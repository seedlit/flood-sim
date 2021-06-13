"""
Flood Simulation - identifying which areas will be inundated first.
Author: Naman Jain
        naman.jain@btech2015.iitgn.ac.in
        www.namanji.wixsite.com/naman/
"""

import os
from multiprocessing import Pool
from src.generated_flooded_shps import generate_flooded_shp
from src.generate_screenshots import save_water_logged_img
from src.generate_gif import save_gif_with_pil


if __name__ == "__main__":

    # define inputs ---------------------------------------
    dem_path = ""  # path to DSM (Digital Surface Model) tif image
    rgb_tif_path = ""  # path to corresponding RGB tif image
    out_dir = ""  # path to the out directory where files will be generated
    num_processes = 1  # to utilise multiprocessing. Increase to speed up process.
    start_water_level_cm = (
        16250  # lower elevation values in DSM (Digital Surface Model)
    )
    end_water_level_cm = 16800  # upper elevation values in DSM (Digital Surface Model)
    step_size_cm = 10  # rise water level by this amount in each step
    gif_duration = 30  # time in seconds for the generated gif
    water_opaqueness_factor = (
        0.7  # 0 means absolute transparent, 1 means absolute opaque
    )

    # -------------------------------------------------------
    # this part generates the flooded tifs and shapfiles
    print("Generating the flooded DEMs and shapefiles")
    flooded_files_out_dir = os.path.join(out_dir, "flooded_tifs_and_shps")
    os.makedirs(flooded_files_out_dir, exist_ok=True)
    task_list = []
    for i in range(
        start_water_level_cm, end_water_level_cm + step_size_cm, step_size_cm
    ):
        task_list.append([dem_path, i / 100, out_dir])
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
            task_list.append([rgb_tif_path, shp_path, out_dir, water_opaqueness_factor])
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
