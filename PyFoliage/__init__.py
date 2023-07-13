import cv2
import numpy as np

def mask_image(image, red_green_max=0.95, blue_green_max=0.95, ExG_min=20):
    # Load the image
    img = cv2.imread(image)

    # Split into channels
    b, g, r = cv2.split(img)

    # Calculate ratios and ExG
    red_green_ratio = r.astype(float) / g.astype(float)
    blue_green_ratio = b.astype(float) / g.astype(float)
    ExG = 2*g - r - b

    # Classify pixels
    bw = np.logical_and(red_green_ratio < red_green_max, blue_green_ratio < blue_green_max, ExG > ExG_min)

    return bw

def canopy_cover(images, **kwargs):
    """Calculate canopy cover for one or more images.

    Args:
        images (str or list): A string or list of strings containing the paths
            to the images to be processed.
        **kwargs: Keyword arguments

    Returns:
        (pd.DataFrame): A pandas DataFrame containing the canopy cover values and available metadata.
    """


    # If images is a string, convert it to a list.
    if isinstance(images, str):
        images = [images]

    # Create an empty list to store the canopy cover values.
    canopy_cover_values = []

    # Loop through the images.
    for image in images:
        bw = mask_image(image, **kwargs)
        canopy_cover_values.append(np.mean(bw))

    return canopy_cover_values
