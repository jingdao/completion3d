#!/usr/bin/env bash

# Data Parameters
#DATASET='shapenet'
DATASET='facade'
NPTS=$((1*(16384)))

# Model Parameters
NET='TopNet' #TopNet/Folding/PCN
ENCODER_ID=1 #0 for PointNet, 1 for PCN Encoder
CODE_NFTS=1024
DIST_FUN='chamfer' #emd
NLEVELS=6
NFEAT=8


# Training Parameters
TRAIN=1
EVAL=$((1-$TRAIN))
RESUME=0
BENCHMARK=0
OPTIM='adagrad'
LR=0.5e-2
EPOCHS=100
SAVE_EPOCH=5
TEST_EPOCH=$SAVE_EPOCH
BATCH_SIZE=4
NWORKERS=1

# Data Augmentation
SCALE=0
ROT=1
MIRROR=0.5

PROGRAM="main.py"

for SCENE in 01 02 03 04 05 06 07 08 09 10 11
do
    python -u $PROGRAM --epochs $EPOCHS --lr $LR --batch_size $BATCH_SIZE \
        --nworkers  $NWORKERS --NET $NET --dataset $DATASET --scene $SCENE \
        --pc_augm_scale $SCALE --pc_augm_rot $ROT --pc_augm_mirror_prob $MIRROR \
        --eval $EVAL --optim $OPTIM --code_nfts $CODE_NFTS \
        --resume $RESUME --inpts $NPTS --npts $NPTS --ngtpts $NPTS --ENCODER_ID $ENCODER_ID --dist_fun $DIST_FUN \
        --save_nth_epoch $SAVE_EPOCH --test_nth_epoch $TEST_EPOCH \
        --benchmark $BENCHMARK --NLEVELS $NLEVELS --NFEAT $NFEAT > train_"$NET"_"$SCENE".log
done
