# Wisdom of (Binned) Crowds
<!-- Add the arvix and conference paper link here -->

### Official Implementation of ACMMM'21 paper "Wisdom of (Binned) Crowds: A Bayesian Stratification Paradigm for Crowd Counting"

## Overview Diagram

![here](images/main.jpg) 

## Data Preparation & Splits (Stages(1,2)) / Binning
### How to find bins for new dataset

We recommend to divide the entire range of data into strata to later sample images from these strata. The procedure for data split generation is provided in the folder binning.

## Minibatch Sampling (Stage 3)
### How to sample the minibatch from bins

We explored two methods of sampling images from strata.
1. Round Robin sampling
2. Random sampling
For a simple visualisation of the procedure you can refer to the folder sampling.


## Optimization (Stage 4)
## How to include strata aware optimisation in your model
Add details of how to add the loss function ( the loss function defined file should be placed in this folder) 

## Evaluation (Stage-5)
## How to evaluate your networks performance at a bin level 

Add a notebook that takes the model and architecture loads it returns the mean and std and if a dataset name and its bins are provided generates the bin level plots (like our website) and plots that shows its performance sample wise across the count range.
