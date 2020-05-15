## Generating Synthetis Singapore Car Plates
This repository has been edited from: [https://github.com/szad670401/end-to-end-for-chinese-plate-recognition](https://github.com/szad670401/end-to-end-for-chinese-plate-recognition). The contents of this repository are as follows:
 1. Purpose
 2. Usage Guide

## 1. Purpose
This was created to create synthetic data on OCR of Singapore Car Plates from surveilance footage. After creating the synthetic data, I labelled it with labelImg (Guide here: [https://github.com/tzutalin/labelImg](https://github.com/tzutalin/labelImg)). The XML files were then converted to a CSV file to be used for training.

I then used EfficientDet from [https://github.com/xuannianz/EfficientDet](https://github.com/xuannianz/EfficientDet) to detect the letters and classify it, reaching an accuracy of 96%.

The weights of the network and the training configuration can be found here: [INSERT LINK]

## 2. Usage Guide
There are 3 main files:

 1. `aug.py` 

Consists of the augmentations used for generating the images. Although other augmentations are available, I used 3 main augmentation techniques - Rotation, adding Background Environment and also adding Gaussian Noise.

2. `plate_generator.py`

Used to generate Singapore car plates as strings which are then used to write on an image

3. `main.py`

Main driver code that controls how the plate strings are written on the bitmaps, using which fonts and which augmentations. 2 arguments are needed - `num_plates` which indicate number of plates to be generated, `dir` to indicate output directory. An example command to run this will be as such:

    python main.py --num_plates 30 --dir plates
