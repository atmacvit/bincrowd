# Wisdom of (Binned) Crowds
<!-- Add the arvix and conference paper link here once available-->

### Official Implementation of ACMMM'21 paper "Wisdom of (Binned) Crowds: A Bayesian Stratification Paradigm for Crowd Counting"


The idea behind our work is to tackle the high variance of error that is ignored when considering de facto statistical performance measures like (MSE,MAE) for performance evaluation in the crowd counting domain. Our recipe involves finding strata that are optimal in a Bayesian sense and later systematically modifying the standard crowd counting pipeline to incorporate decrease of variance at each step.





## Overview Diagram

![here](images/main.jpg) 

## Step 1 : Data Preparation & Splits (Stages(1,2)) / Binning 


<img align="left" width="300" height="200" src="images/bin_demo.jpg">

### How to find bins for new dataset

In our paradigm the first step is to create strata over the count range to enable balanced data splits.
We recommend to divide the entire range of counts into strata which are optimal in Bayesian sense, and later sample images that belong to these strata. The procedure for data split generation is provided in the folder named [```binning```](binning).


<br />

## Step 2 : Minibatch Sampling (Stage 3) 

<img align="left" width="350" height="200" src="images/sampling_demo.jpg">

### How to sample the minibatch from bins
Next step in our paradigm is to sample from these bins. We exeprimented with two differnt ways of choosing the bin, they are :

```
    1. Round Robin sampling
    2. Random sampling
```

For a simple visualisation of the procedure you can refer to the folder named [```sampling```](sampling). In the same folder, we present a demo on how to include the sampling into any general procedure.

<br />

## Step 3 : Optimization (Stage 4) 

<img align="left" width="300" height="415" src="images/opt_demo.jpg">

### How to include strata aware optimization in your network

The next step of the procedure is to include strata aware optimization into any network. We add this loss as an additive loss along with a scaleable hyper parameter (λ<sub>1</sub> in Sec 3.4) to the original network's loss function. The idea behind adoption of strata aware optimization is to reduce variance. A pyTorch implementation of that optimization is provided in this folder named [```optimization```](optimization).

<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />

## Step 4 : Evaluation (Stage-5) 

<img align="left" width="250" height="392" src="images/eval_demo.jpg">

### How to evaluate your networks performance at a bin level 

<!-- Add a notebook that takes the model and architecture loads it returns the mean and std and if a dataset name and its bins are provided generates the bin level plots (like our website) and plots that shows its performance sample wise across the count range. -->

The final step in our paradigm is to have a better represented evaulation metric. The generally used MAE conceals standard deviation, to bring out this we evaluate the performance at a strata-level (mean and std) and a pooled mean and std. The folder [```evaluation```](evaluation) consists of a notebook to do the same. 


<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />


To include your network in our work please create a pull request with the name ``` <your_network_name>```. 
Fill up the details of your network in the following format, and add it into the description:
```
Network name:
Conference or arxiv link:
Github repo:
Contact email:
```
Attach a file with the name ```<your_network_name_dataset_name>.txt```, replace ```your_network_name``` with your networks name and ```dataset_name ``` with the dataset name on which results of the file correspond to. The file should contain row-wise information in the following format:

```
image_name_1 , predicted_1
image_name_2 , predicted_2
.
.
.
image_name_n , predicted_n
```
Here ```image_name_i``` can be a ```string``` or an ```int``` that refers to the input image name to the network and ```predicted_i``` refers to the count predicted by your network from the ```image_name_i```.

<!-- Add the citation here once available -->

### Citation
If you are using our work, Please cite us at :
```
@inproceedings{10.1145/3474085.3475522,
author = {Sravya Vardhani Shivapuja, Mansi Pradeep Khamkar, Divij Bajaj, Ganesh Ramakrishnan, Ravi Kiran Sarvadevabhatla},
title = {Wisdom of (Binned) Crowds: A Bayesian Stratification Paradigm
for Crowd Counting
},
booktitle = {Proceedings of the 2021 ACM Conference on Multimedia},
year = {2021},
location = {Virtual Event, China},
publisher = {ACM},
address = {China},
}

```
