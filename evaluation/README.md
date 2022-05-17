## Evaluation (Stage-5) -- Sec 3.5
### How to evaluate your networks performance at a bin level 

#### Pooled-MAE and std
This folder consists of link to a [colab notebook](https://colab.research.google.com/drive/1LdNAc5hd0xwbqOZ2oHL007rr1Dw4TPRR?usp=sharing) that helps us evaluate the performance at a bin level. The txt files required for running the notebook are in this [drive folder](https://drive.google.com/drive/folders/1c_6cyqN1g34tvS4uXEISsXkbcugFTBka?usp=sharing)

The Demo plot as in Default Approach , [SOTA](https://deepcount.iiit.ac.in/dashboard#sota) for NWPU Dataset can be found [here](https://colab.research.google.com/drive/1LdNAc5hd0xwbqOZ2oHL007rr1Dw4TPRR#scrollTo=BXpSvI5Mffsc).

The Demo Plot as in Default Approach , [Overall](https://deepcount.iiit.ac.in/dashboard#all) performance of networks in terms of Pooled MAE +/- std can be found [here](https://colab.research.google.com/drive/1LdNAc5hd0xwbqOZ2oHL007rr1Dw4TPRR#scrollTo=lTfYvxePnlyu).

The Demo Plot as in Proposed Approach, [Dataset-wise](https://deepcount.iiit.ac.in/dashboard#dwa) Analysis, RR sampling NWPU can be found [here](https://colab.research.google.com/drive/1LdNAc5hd0xwbqOZ2oHL007rr1Dw4TPRR#scrollTo=7zicWV_2FMFR).

The Demo Plot as in Proposed Approach, [Network-wise](https://deepcount.iiit.ac.in/dashboard#nwa) Analysis on DM Count network for NWPU dataset can be found [here](https://colab.research.google.com/drive/1LdNAc5hd0xwbqOZ2oHL007rr1Dw4TPRR#scrollTo=s-GhdKWZHZan).

If you are interested in using the evaluation procedure for your network, you could make a copy of this [colab notebook](https://colab.research.google.com/drive/1LdNAc5hd0xwbqOZ2oHL007rr1Dw4TPRR?usp=sharing) and use the same.

#### Thresholded Percentage Error Ratio (TPER)

The jupyter notebook ```percentage plot-single network_BL.ipynb``` provides demo for generating the TPER curves. The reuired txt files to run this notebook are also added to this repo inside the ```BL_txt``` folder.


#### Localised Metric - GAME

The ```game_metric.py``` contains the file which you can use to calculate the GAME metric.
