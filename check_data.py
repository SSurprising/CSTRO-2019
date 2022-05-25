import os
import numpy as np
import torch
import SimpleITK as sitk
from collections import Counter

# data_dir = '/home/zjm/Data/HaN_OAR/'
# data_dir = '/home/zjm/Data/HaN_OAR_256/'
# data_dir = '/home/zjm/Data/HaN_OAR_raw/chiasm_pituitary/'
data_dir = '/home/zjm/Data/HaN_OAR_raw/four_organ/'
# data_dir = '/home/zjm/Data/HaN_OAR_raw/chiasm_pituitary/subset1/01/'

# center [223,295] for four organs, max size 72 * 69
spacing_couter_flag = True
intensity_flag = False
small_region_flag = False
organ_size_flag = True

organ_slice_number = []
intensity_chiasm_list = []
intensity_pituitary_list = []

organ_size_chiasm    = []
organ_size_pituitary = []


if spacing_couter_flag:
    thickness = []
    spacing = []

if small_region_flag:
    slice_count_chiasm_list = []
    slice_count_pituitary_list = []

idx_x_list = []
idx_y_list = []

image_size = []

for subset in os.listdir(data_dir):
    print('\nDataset:', subset)
    for patient in os.listdir(data_dir + subset):
        image = sitk.ReadImage(data_dir + subset + '/' + patient + '/image.nii')
        label = sitk.ReadImage(data_dir + subset + '/' + patient + '/label.nii')

        img_arr = sitk.GetArrayFromImage(image)
        label_arr = sitk.GetArrayFromImage(label)

        # print('patien:', patient)
        image_size.append(img_arr.shape[0])
        # print('labels:', np.unique(label_arr))

        idx = np.where(label_arr != 0)
        idx_min = min(idx[0])
        idx_max = max(idx[0])

        idx_x_list.append([np.min(idx[1]), np.max(idx[1])])
        idx_y_list.append([np.min(idx[2]), np.max(idx[2])])

        organ_slice_number.append(idx_max - idx_min + 1)

        # print('imgagee spaceing:', image.GetSpacing())
        # print('--------------------------------\n')

        if small_region_flag:
            idx_chiasm = np.where(label_arr == 1)
            idx_pituitary = np.where(label_arr == 2)

            slice_count_chaism = Counter(idx_chiasm[0])
            slice_count_pituitary = Counter(idx_pituitary[0])
            slice_count_chiasm_list += slice_count_chaism.values()
            slice_count_pituitary_list += slice_count_pituitary.values()

            print(slice_count_chaism, slice_count_pituitary)


        if spacing_couter_flag:
            thickness.append(image.GetSpacing()[-1])
            spacing.append(image.GetSpacing()[:-1])

        if intensity_flag:
            label_chiasm_temp = np.zeros(label_arr.shape, label_arr.dtype)
            label_pituitary_temp = np.zeros(label_arr.shape, label_arr.dtype)

            idx_chiasm = np.where(label_arr == 1)
            idx_pituitary = np.where(label_arr == 2)

            label_chiasm_temp[idx_chiasm] = 1
            label_pituitary_temp[idx_pituitary] = 1

            count_chiasm = len(idx_chiasm[0])
            count_pituitary = len(idx_pituitary[0])

            intensity_mean_chiasm = (label_chiasm_temp * img_arr).sum() / count_chiasm
            intensity_mean_pituitary = (label_pituitary_temp * img_arr).sum() / count_pituitary

            intensity_chiasm_list.append(intensity_mean_chiasm)
            intensity_pituitary_list.append(intensity_mean_pituitary)

        if organ_size_flag:
            idx_chiasm    = np.where(label_arr == 1)
            idx_pituitary = np.where(label_arr == 2)

            organ_size_chiasm.append([max(idx_chiasm[0])-min(idx_chiasm[0])+1, max(idx_chiasm[1])-min(idx_chiasm[1])+1, max(idx_chiasm[2])-min(idx_chiasm[2])+1])
            organ_size_pituitary.append([max(idx_pituitary[0])-min(idx_pituitary[0])+1, max(idx_pituitary[1])-min(idx_pituitary[1])+1, max(idx_pituitary[2])-min(idx_pituitary[2])]+1)

if organ_size_flag:
    print('chiasm size', organ_size_chiasm)
    print('pituitary size', organ_size_pituitary)


if spacing_couter_flag:
    print('thickness:', Counter(thickness))
    print('spacing:', Counter(spacing))

# the number of slices for a patient varies from 82 to 120 (22 organs)
# the number of slices for a patient varies from 1 to 7 (chiasm and pituitary)
print(organ_slice_number)
print(Counter(organ_slice_number))

if intensity_flag:
    print('mean intensity of chiasm for each patient:', intensity_chiasm_list, 'min:', np.min(intensity_chiasm_list), 'max:', np.max(intensity_chiasm_list))
    print('mean intensity of pituitary for each patient:', intensity_pituitary_list, 'min:', np.min(intensity_pituitary_list), 'max:', np.max(intensity_pituitary_list))
    print('mean intensity of chiasm for all patients:', np.mean(intensity_chiasm_list))
    print('mean intensity of pituitary for all patients:', np.mean(intensity_pituitary_list))

idx_x_list = np.array(idx_x_list)
idx_y_list = np.array(idx_y_list)
print(idx_x_list.shape)
print(idx_y_list.shape)
print('x:', np.min(idx_x_list), np.max(idx_x_list))
print('y:', np.min(idx_y_list), np.max(idx_y_list))

print('img shape', Counter(image_size))

print('slice_count_chiasm_list', slice_count_chiasm_list)
print(min(slice_count_chiasm_list), max(slice_count_chiasm_list))
print('slice_count_pituitary_list', slice_count_pituitary_list)
print(min(slice_count_pituitary_list), max(slice_count_pituitary_list))


