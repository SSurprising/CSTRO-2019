#!/usr/bin/env bash

CUDA_VISIBLE_DEVICES=0 python train.py \
    --model_name='UNet'\
    --data_path='/home/zjm/Data/HaN_OAR_raw/four_organ/' \
    --output_dir='/home/zjm/Project/segmentation/BLSC_2D/outputs/' \
    --val_subset='subset5' \
    --epochs=1000\
    --learning_rate=1e-4 \
    --num_organ=4 \
    --slice_size=128 \
    --resolution 512 512 \
    --HU_upper_threshold=300 \
    --HU_lower_threshold=-100 \
    --train \
    --loss='ce' \
    --batch_size=1 \
    --repeat_times='524_1' \
    --slice_expand=4 \
    --show_test_loss \
    --crop_size 128 128 \
#    --auxiliary_loss \
#    --lw=0.1 \
