## Point Cloud Scene Completion Baselines

This repository is a fork of the
[Stanford 3D Object Point Cloud Completion Benchmark](https://github.com/lynetcha/completion3d)
that implements various deep learning methods for point cloud completion
including PCN, TopNet, and FoldingNet.

## Building Facade Dataset

Get the original building facade dataset with 11 scenes (input + ground truth) [here](https://www.dropbox.com/s/nvatmp1hz3yot57/facade_original.zip?dl=0).

To use the building facade dataset processed according to the Completion3D format, download and extract the [zip](https://www.dropbox.com/s/jfm9s0wd73t05k2/facade_16384.zip?dl=0) file into the *data* directory.
The dataset consists of 467 training and 11 validation point cloud pairs stored in H5 format, with each point cloud containing 16384 points.
The point cloud pairs are made up of a partial point cloud (stored under the *partial* directory) and a complete point cloud (stored under the *gt* directory).

## Training

Follow the [instructions](tensorflow-setup.md) to setup a Tensorflow Python environment.
Next, run the script [train\_facade.sh](tensorflow/train_facade.sh) to start training.
The script will train multiple networks with the building facade dataset according to a cross-validation scheme
(i.e. 10 scenes are used for training and 1 scene is used for validation for each of the 11 scenes).
The trained models and predictions will be saved in the *tensorflow/results/facade* directory.
Modify the *NET* parameter in the training script to train with different network architectures including
PCN, TopNet, and FoldingNet.

## Evaluation

Run the Python script [convertH5ToPLY.py](tensorflow/convertH5ToPLY.py) to convert the H5 result files to the PLY format that will be used for evaluation.
The predicted point clouds will be rescaled and transformed back to the coordinate system of the original input point clouds.
The [fix\_color.py](tensorflow/fix_color.py) script is used internally to assign color channels to the predicted point cloud based on nearest neighbor search from the input point cloud.

Use the [get\_accuracy.py](tensorflow/get_accuracy.py) script to compute evaluation metrics such as voxel precision, voxel recall, F1-score, position RMSE and color RMSE.
Note that the ground truth point cloud should come from the original building facade dataset (before conversion to the Completion3D format).

```
python get_accuracy.py data/facade_original/01_mason_east_gt.ply baselines/PCN/01_mason_east.ply
```

## Results

The following directories contain the result point clouds after training with the building facade dataset
(Upsampled refers to the case where the number of points is increased to 1000000 using mesh-based resampling).

- [PCN](https://www.dropbox.com/sh/jl0b7zt0de9itiv/AABrVtArTSl6hsmQ0R36hf0ia?dl=0)
- [PCN upsampled](https://www.dropbox.com/sh/h34r4oiba6eh935/AAD7cP-c_Z7Ju_0NYD49CVgca?dl=0)
- [TopNet](https://www.dropbox.com/sh/jokluwc83lizoe8/AAAyN6Gwf2gwlzsSAco3PFrza?dl=0)
- [TopNet upsampled](https://www.dropbox.com/sh/qmn0il3vadmixdk/AADdxyMHE0tN93mYT6wgIyAea?dl=0)
- [FoldingNet](https://www.dropbox.com/sh/bxo9hnqk6ro2p0l/AAAl1EkaC_S8VA1pXZbkbvo0a?dl=0)
- [FoldingNet upsampled](https://www.dropbox.com/sh/hhgfy70d35zri41/AABNNw66DVIGR3c0b2Q-seCGa?dl=0)
