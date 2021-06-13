import os
import imageio
from PIL import Image


def generate_gif(src_img_dir, out_gif_path, img_duration):
    images = []
    img_num_list = []
    for img_name in os.listdir(src_img_dir):
        if img_name.endswith(".png"):
            img_elev = int(img_name.split(".")[0].replace("cm", ""))
            img_num_list.append(img_elev)
    for img_num in sorted(img_num_list):
        file_path = os.path.join(src_img_dir, str(img_num) + "cm.png")
        images.append(imageio.imread(file_path))
    imageio.mimsave(out_gif_path, images, duration=img_duration)


def save_gif_with_pil(src_img_dir, out_gif_path, duration):
    images = []
    img_num_list = []
    for img_name in os.listdir(src_img_dir):
        if img_name.endswith(".png"):
            img_elev = int(img_name.split(".")[0].replace("cm", ""))
            img_num_list.append(img_elev)
    for img_num in sorted(img_num_list):
        file_path = os.path.join(src_img_dir, str(img_num) + "cm.png")
        images.append(Image.open(file_path))
    images[0].save(
        out_gif_path,
        save_all=True,
        append_images=images[1:],
        optimize=True,
        duration=duration,
        loop=0,
    )


if __name__ == "__main__":

    src_img_dir = "screenshots_cropped"
    out_gif_path = (
        "/home/naman/Desktop/side_projects/flood_sim/iitgn_new_hostels_flood_sim.gif"
    )

    # img_duration = 0.033
    # generate_gif(src_img_dir, out_gif_path, img_duration)

    gif_duration = 30
    save_gif_with_pil(src_img_dir, out_gif_path, gif_duration)
