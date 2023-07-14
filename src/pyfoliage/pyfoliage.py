from tqdm import tqdm
import pandas as pd
import numpy as np
from PIL import Image, ExifTags
from scipy import ndimage
from multiprocessing import Pool
import glob
import matplotlib.pyplot as plt

def __get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


def cc_image(image, red_green_max=0.95, blue_green_max=0.95, ExG_min=20, plot=False):
    """Returns a binary mask of the image based on the green canopy cover, as described in Patrignani and Ochsner (2015).

    Args:
        image (str): Path to the image.
        red_green_max (float, optional): Maximum value for the red/green ratio. Defaults to 0.95.
        blue_green_max (float, optional): Maximum value for the blue/green ratio. Defaults to 0.95.
        ExG_min (int, optional): Minimum value for the ExG index. Defaults to 20.

    Returns:
        np.array: Binary mask of the image.

    References:
        Patrignani, A. and Ochsner, T.E. (2015), Canopeo: A Powerful New Tool for Measuring Fractional Green Canopy Cover. Agronomy Journal, 107: 2312-2320. https://doi.org/10.2134/agronj15.0150
    """
    # Load the image
    img = Image.open(image)

    # Convert the image into a numpy array
    np_img = np.array(img)

    # Split into channels
    r, g, b = np_img[...,0], np_img[...,1], np_img[...,2]

    # Calculate ratios and ExG
    red_green_ratio = r.astype(float) / (g.astype(float) + 1e-10)
    blue_green_ratio = b.astype(float) / (g.astype(float) + 1e-10)
    ExG = 2*g - r - b

    # Classify pixels
    bw = np.logical_and(red_green_ratio < red_green_max, blue_green_ratio < blue_green_max, ExG > ExG_min)
    bw = ndimage.binary_opening(bw, structure=np.ones((10, 10))).astype(int)

    # If plot is True, display the images and print the canopy cover percentage
    if plot:
        # Calculate the canopy cover percentage
        cc_percent = np.mean(bw) * 100

        # Create subplots
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))

        # Plot the original image
        ax[0].imshow(img)
        ax[0].set_title('Original Image')

        # Plot the masked image
        ax[1].imshow(bw, cmap='gray')
        ax[1].set_title('Masked Image')

        # Set super title with the canopy cover percentage
        plt.suptitle(f'Canopy cover percentage: {cc_percent}%', fontsize=16)

        # Extract EXIF data for footer
        exif_data = img._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                if tag in ExifTags.TAGS:
                    # Add footer text with date/time and GPS info if available
                    if ExifTags.TAGS[tag]=='DateTimeOriginal':
                        fig.text(0.5, 0.04, f'Date/Time: {value}', ha='center')
                    if ExifTags.TAGS[tag]=='GPSInfo':
                        fig.text(0.5, 0.01, f'GPS Info: {value}', ha='center')

        # Show the plots
        plt.show()

    return bw

def process_image(args):
    image, red_green_max, blue_green_max, ExG_min, parse_metadata, save_mask = args
    # Check if image has a valid extension for PIL
    if not image.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.gif')):
        return None
    try:
        bw = cc_image(image, red_green_max, blue_green_max, ExG_min)
        data = {'image': image, 'canopy_cover': (np.sum(bw) / float(bw.size))}
        if parse_metadata:
            img = Image.open(image)
            metadata = img._getexif()
            if metadata:
                # Check if date/time data is available
                if 36867 in metadata:
                    data['date_time'] = metadata[36867]
                # check if geolocation data is available
                if 34853 in metadata:
                    if 2 in metadata[34853] and 4 in metadata[34853] and 1 in metadata[34853] and 3 in metadata[34853]:
                        data['latitude'] = __get_decimal_from_dms(metadata[34853][2], metadata[34853][1])
                        data['longitude'] = __get_decimal_from_dms(metadata[34853][4], metadata[34853][3])
        if save_mask:
            data['mask'] = bw.astype(np.uint8)
        return data
    except:
        print("Error processing image: {}".format(image))
        return None

def canopy_cover(images, red_green_max=0.95, blue_green_max=0.95, ExG_min=20, parse_metadata=True, save_mask=False, parallel=False):
    """Returns a pandas dataframe with the canopy cover values for each image.

    Args:
        images (str or list): Path to the image list of paths or directory can be specified using wildcards (*) in the string. See [glob](https://docs.python.org/3/library/glob.html) for more information.
        red_green_max (float, optional): Maximum value for the red/green ratio. Defaults to 0.95.
        blue_green_max (float, optional): Maximum value for the blue/green ratio. Defaults to 0.95.
        ExG_min (int, optional): Minimum value for the ExG index. Defaults to 20.
        parse_metadata (bool, optional): Whether to parse the metadata of the image. Defaults to True.
        save_mask (bool, optional): Whether to save the mask of the image. Defaults to False.
        parallel (bool, optional): Whether to use parallel processing. Defaults to False.

    Returns:
        pd.DataFrame: Pandas dataframe with the canopy cover values for each image.
    """
    # check if is string and is a directory
    if isinstance(images, str) and "*" in images:
        images = glob.glob(images)
    elif isinstance(images, str):
        images = [images]

    args = [(image, red_green_max, blue_green_max, ExG_min, parse_metadata, save_mask) for image in images]

    if parallel:
        with Pool() as p:
            canopy_cover_rows = list(tqdm(p.imap(process_image, args), total=len(images), desc="Processing images", unit="image"))
    else:
        canopy_cover_rows = list(tqdm(map(process_image, args), total=len(images), desc="Processing images", unit="image"))

    canopy_cover_rows = [row for row in canopy_cover_rows if row is not None]
    results = pd.DataFrame(canopy_cover_rows)
    return results