# 3.2 Revisiting Stage 2 (Creating Data splits) -- Sec 3.2

This folder contains the method in which the data-splits are created. This procedure partions the count range into balanced strata (bins) using Bayesian optimality criterion (Sec 3). The procedure can be summarised as shown below.



Optimal Bins for different datasets are:

| Dataset name | Bins |
|---------|--------------------|
| NWPU | ```[0.0, 0.5, 2.5, 5.5, 10.5, 18.5, 31.5, 53.5, 90.5, 152.5, 256.5, 429.5, 717.5, 1197.5, 1997.5, 3330.5, 5552.5, 9255.5, 15426.0]```|
| UCF | ```[49.0, 49.5, 51.5, 55.5, 62.5, 73.5, 92.5, 123.5, 175.5, 261.5, 405.5, 644.5, 1043.5, 1708.5, 2816.5, 4662.5, 7738.5, 12865.0]``` |
| STA | ```[33.0, 33.5, 35.5, 38.5, 43.5, 51.5, 64.5, 85.5, 120.5, 178.5, 275.5, 436.5, 704.5, 1151.5, 1897.5, 3139.0]``` |
| STB | ```[13.0, 13.5, 15.5, 19.5, 25.5, 36.5, 54.5, 83.5, 132.5, 214.5, 351.5, 578.0]``` |






Algorithm Block 1 |  Algorithm block 2
:-------------------------:|:-------------------------:
![algo](algorithm1.jpg) | ![algo2](algorithm2.jpg)




## Procedure for generating bins:
### Step 1

First put your dataset txt in form of ```image_name,image_count``` in a ```.txt```, for a demo you can look into the folder [```dataset_txt```](binning/dataset_txt). As an example we have provided the txt files for NWPU,UCF-QNRF, STA and STB datasets.

### Step 2
To start the training run

   ```
   python train.py -d ./dataset_txt/Train_nwpu.txt -f multinomial
   ``` 

If you want to get bins on your dataset, change the ```-d``` argument to that path of your datasets information stored ```.txt``` format. The ```-f``` argument helps choose between the fitness functions (```multinomial,poisson```).

### Step 3

After training (Step 2) there are best files generated in the ```select_best``` folder. To print out the top two best binning configurations, run the following code

```
python generate_bins.py  -d ./dataset_txt/Train_nwpu.txt -f multinomial
```
Here ```-d``` corresponds to dataset and ```-f``` corresponds to fitness function.

The folder structure of the codes in this folder is:
```
.
├── dataset_txt             # All files of dataset are in this folder.
│   ├── *.txt               # Dataset-wise txts 
│   └── ...
├── select_best             # After running the train.py file the best configs are stored in this (dataset-split-wise).
├── test_jsons              # While running the files generated are stored in here.
├── train_jsons             # While running the files generated are stored in here.
├── bayesian_blocks.py      # Modified version of bayesian blocks to fit our use case.
├── generate_bins.py        # This file is used to generate bins after training is over.
├── load_data.py            # For loading data
├── multinomial.py          # For multinomal distribution
├── poisson.py              # For poisson distribution
├── seeds_10.txt            # Fixing the seeds of the data splits.
├── select_best.py          # script that selects the best bin and is called in generate_bins.py
└── train.py                # For generating the bins split wise.
```
