import os
import imageio


def generate_gif(src_img_dir, out_gif_path, img_duration):
    images = []
    img_num_list = []
    for img_name in os.listdir(src_img_dir):
        if img_name.endswith(".png"):
            img_elev = int(img_name.split(".")[0].replace("cm", ""))
            img_num_list.append(img_elev)
            temp_var = img_name.split(".")[0]
    for img_num in sorted(img_num_list):
        file_path = os.path.join(src_img_dir, str(img_num) + "cm.png")
        images.append(imageio.imread(file_path))
    imageio.mimsave(out_gif_path, images, duration=img_duration)


if __name__ == "__main__":

    src_img_dir = "iitgn_new_screenshots"
    out_gif_path = "/home/naman/Desktop/side_projects/flood_sim/iitgn_new_gif2.gif"
    img_duration = 0.033

    generate_gif(src_img_dir, out_gif_path, img_duration)
