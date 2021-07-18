# 3.2 Revisiting Stage 2 (Creating Data splits)

This folder contains the method in which the data-splits are created.

Procedure for generating bins:
1. First put your dataset in form of ```image_name,image_count``` in a ```.txt```.
2. Run the ```train.py``` after changing the path at line number 63 ```path path=[r'Val_nwpu_new.txt']```. This generates files in ```select_best``` folder.
3. Run the ```generate_bins.py``` after this by changing the filenames at line number 11 : ```test_ratio_arr =[2053,4106,5133]``` according to the newly geenrated files in ```select_best``` folder.
4. Your best bisn will be printed on the screen.

The folder structure of the codes in this folder is:
```
.
├── dataset_txt             # All files of dataset are in this folder.
│   ├── *.txt               # Dataset-wise txts should be added here from ".\datasets\". 
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