import os
from photocropper import Photo
from tqdm import tqdm

AVERAGE_COLOR = [134.97261671, 112.81255394,  71.81577089]


def change_decimal_sep(filepath, sep=","):
    with open(filepath, "r") as f:
        content = f.read()
    content = content.replace(".", ",")
    
    with open(filepath, "w") as file:
        file.write(content)
    

def compute_all_brightness(root_dir='photos', pic_ext='png', result_file='brightness.csv', sep=";", decimal_sep="."):
    
    with open(result_file, "w") as f:
        for (root,dirs,files) in tqdm(os.walk(root_dir, topdown=True)):
            # sub_dir, subsub_dir = root.split("/")[-2], root.split("/")[-1]
            if files:
                _, sub_dir, subsub_dir = root.split("/")
                fish_number = subsub_dir.split("_")[-1]
                f.write(f"{fish_number}{sep}")

            for filename in sorted(files):
                if filename.endswith(f".{pic_ext}"):
                    # Create the real path from where the script is run
                    path = os.path.join(root, filename)
                    maphoto = Photo(path)
                    maphoto.crop_background(average_color=AVERAGE_COLOR)  # Set the background_color to black by default
                    maphoto.no_black_and_white()   # Transforms the image into an array without any black or white pixels                   
                    br = maphoto.brightness

                    # Get rid of the file extension
                    # filename = filename.split(".")[0]
                    
                    f.write(f"{br}{sep}")
            f.write("\n")
    if decimal_sep != ".":
        change_decimal_sep(filepath=result_file, sep=decimal_sep)


if __name__ == "__main__":
    # If the variables below are the same as the keyword arguments you can ommit them
    # This is just an example
    root = "photos"
    ext = "png"
    result = "test_brighhtness.csv"
    sep = ";"
    decimal_separator = ","
    compute_all_brightness(root, ext, result, sep, decimal_separator)
