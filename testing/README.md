
### Pretrained models 

The pretrained models that were used to prepare results for different datasets and networks are given in the following zenodo links. The testing demo script for DMCount is provided in this folder.

The original testing code was taken from the [```DM Count repo```](https://github.com/cvlab-stonybrook/DM-Count) and modified.

Step 1 : Download the pretrained model

| Network name | link |
| ------------ |-----|
| BL (NWPU,UCF,STA,STB) | [here](https://zenodo.org/record/5176794/preview/wisdom_of_binned_crowds.zip#tree_item2) |
| DM Count (NWPU,UCF,STA,STB) | [here](https://zenodo.org/record/5176794/preview/wisdom_of_binned_crowds.zip#tree_item19) |
| SCARNet (NWPU,UCF,STA,STB) | [here](https://zenodo.org/record/5176794/preview/wisdom_of_binned_crowds.zip#tree_item36) |
| SDCNet (NWPU,UCF,STA,STB) | [here](https://zenodo.org/record/5176794/preview/wisdom_of_binned_crowds.zip#tree_item53) |
| SFANet (NWPU,UCF,STA,STB) | [here](https://zenodo.org/record/5176794/preview/wisdom_of_binned_crowds.zip#tree_item70) |

Step 2 : Give the data path and the model path as arguments.

Code to test the model :

```
python test.py --dataset <nwpu,qnrf,sta,stb> --model-path <local path to the stored model> --data-path <local path of the data location>
```

This code generates a txt file with the name ```img_name_targ_pred.txt``` this file contains the list of counts as :

```
image_name_1 , target_1, predicted_1
image_name_2 , target_2, predicted_2
.
.
.
image_name_n , target_n, predicted_n
```
Here ```image_name_i``` can be a ```string``` or an ```int``` that refers to the input image name to the network and ```predicted_i``` refers to the count predicted by your network from the ```image_name_i```, and ```target_i``` represents its ground truth.

We encourage you to send us a pull request [```here```](https://github.com/atmacvit/bincrowd/pulls) following the format mentioend [```here```](https://github.com/atmacvit/bincrowd#pull-request) to include your network in our work.

