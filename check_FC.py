import os
import numpy as np
import torch
import SimpleITK as sitk
from collections import Counter

data_dir = '/home/zjm/Data/HaN_OAR_raw/four_organ/'

# [0.5%, 99.5%] min -54, max:123
foreground = []
for subset in os.listdir(data_dir):
    for patient in os.listdir(data_dir + subset):
        print(patient)
        image = sitk.ReadImage(data_dir + subset + '/' + patient + '/image.nii')
        label = sitk.ReadImage(data_dir + subset + '/' + patient + '/label.nii')

        img_arr = sitk.GetArrayFromImage(image)
        label_arr = sitk.GetArrayFromImage(label)

        idx = np.where(label_arr != 0)
        for i in range(len(idx[0])):
            foreground.append(img_arr[idx[0][i], idx[1][i], idx[2][i]])

print('Num:', len(foreground))

foreground.sort()
upper = int(0.995 * len(foreground))
lower = int(0.05 * len(foreground))
print(foreground[0], foreground[1])
print(foreground[lower], foreground[upper])

