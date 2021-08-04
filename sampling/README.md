## Minibatch Sampling (Stage 3) -- Sec 3.3

In this folder a demo of how the images should be sampled from bins is provided as a gif below.

| Round Robin Sampling | Random Sampling |
|----------- | ---------- |
|![rr](roundrobin.gif)| ![rs](randomsampling.gif)|

The demo code for [DM Count](https://github.com/cvlab-stonybrook/DM-Count) is included in [```crowd.py```](crowd.py) , which is modified version of the original repo implementation. The procedure of normal data load has been replaced by loading from epoch wise json files as shown in [link](https://github.com/atmacvit/bincrowd/blob/6d133d14391e5f542547cae7ce2a7bfb188562d0/sampling/crowd.py#L101)

The dataset-wise epoch json files can be found at :
Add zenodo link here

<!-- ### Round Robin Sampling
![rr](roundrobin.gif)

### Random Sampling
![rs](randomsampling.gif) -->