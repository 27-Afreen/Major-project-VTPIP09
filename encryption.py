"""
Privacy-Preserving Learnable Image Encryption Module
=====================================================
Implements the enhanced SKK scheme with:
  1. Negative-Positive Transformation
  2. Color Channel Shuffling
  3. Statistical Smoothing (Median, Mean, Max, Min filters)

Used to encrypt medical images client-side before
sending to cloud server for DNN training.
"""

import cv2
import numpy as np
import os


# ── STEP 1: Negative-Positive Transformation ─────────────────────────────────
def negative_positive_transform(image):
    """
    Inverts pixel values: new_pixel = 255 - pixel
    Obscures the visual content of the image.
    """
    return cv2.bitwise_not(image)


# ── STEP 2: Color Channel Shuffling ──────────────────────────────────────────
def color_shuffle(image, seed=42):
    """
    Randomly shuffles the RGB color channels of the image.
    E.g. [R,G,B] → [B,R,G] based on a random permutation.
    """
    np.random.seed(seed)
    channels = cv2.split(image)
    indices  = np.random.permutation(len(channels))
    shuffled = [channels[i] for i in indices]
    return cv2.merge(shuffled)


# ── STEP 3: Statistical Smoothing Filters ────────────────────────────────────
def apply_median_filter(image, block_size=8):
    """Fills each block with its median value."""
    result = image.copy()
    h, w   = image.shape[:2]
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = image[y:y+block_size, x:x+block_size]
            median_val = np.median(block, axis=(0, 1)).astype(np.uint8)
            result[y:y+block_size, x:x+block_size] = median_val
    return result


def apply_mean_filter(image, block_size=8):
    """Fills each block with its mean value."""
    result = image.copy()
    h, w   = image.shape[:2]
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = image[y:y+block_size, x:x+block_size]
            mean_val = np.mean(block, axis=(0, 1)).astype(np.uint8)
            result[y:y+block_size, x:x+block_size] = mean_val
    return result


def apply_max_filter(image, block_size=8):
    """Fills each block with its maximum value."""
    result = image.copy()
    h, w   = image.shape[:2]
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = image[y:y+block_size, x:x+block_size]
            max_val = np.max(block, axis=(0, 1)).astype(np.uint8)
            result[y:y+block_size, x:x+block_size] = max_val
    return result


def apply_min_filter(image, block_size=8):
    """Fills each block with its minimum value."""
    result = image.copy()
    h, w   = image.shape[:2]
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = image[y:y+block_size, x:x+block_size]
            min_val = np.min(block, axis=(0, 1)).astype(np.uint8)
            result[y:y+block_size, x:x+block_size] = min_val
    return result


# ── FULL ENCRYPTION PIPELINE ─────────────────────────────────────────────────
def encrypt_image(image_path, output_dir, filter_type='median', block_size=8):
    """
    Full SKK encryption pipeline:
      1. Negative-positive transformation
      2. Color channel shuffling
      3. Statistical smoothing (chosen filter)

    Returns:
        enc_filename : filename of the encrypted image saved to output_dir
        original_path: path of the original saved image
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Resize to 256x256 as required by DNN models
    image = cv2.resize(image, (256, 256))

    # Save original
    base_name   = os.path.splitext(os.path.basename(image_path))[0]
    orig_name   = f"orig_{base_name}.png"
    orig_path   = os.path.join(output_dir, orig_name)
    cv2.imwrite(orig_path, image)

    # Step 1: Negative-Positive Transform
    enc = negative_positive_transform(image)

    # Step 2: Color Shuffle
    enc = color_shuffle(enc)

    # Step 3: Statistical Smoothing
    filters = {
        'median': apply_median_filter,
        'mean'  : apply_mean_filter,
        'max'   : apply_max_filter,
        'min'   : apply_min_filter,
    }
    smooth_fn = filters.get(filter_type, apply_median_filter)
    enc = smooth_fn(enc, block_size)

    # Save encrypted image
    enc_name = f"enc_{base_name}.png"
    enc_path = os.path.join(output_dir, enc_name)
    cv2.imwrite(enc_path, enc)

    print(f"[ENCRYPTION] Original  → {orig_path}")
    print(f"[ENCRYPTION] Encrypted → {enc_path}")

    return enc_name, orig_path


# ── QUICK TEST ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        enc, orig = encrypt_image(sys.argv[1], '.', filter_type='median')
        print(f"Done! Encrypted: {enc}")
    else:
        print("Usage: python encryption.py <image_path>")
