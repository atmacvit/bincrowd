## Optimization (Stage 4)

This folder contains script regarding the strata-aware optimzation procedure. The code reuired you to first generate Beysian optimal bins following procedure in the folder named ```binning```. 

In order to combat the high variance of errors issue, we enable data-distribution aware optimization. If the predicted count value lies outside the range of bin, then a linear penality is imposed, where as if the predicted count value lies inside the range of bin a logarithmic penality is imposed. 

You can imbibe the strata-aware optimization in two ways:

1. Using bin aware optimzation along with network-specific loss function (your loss function).
2. Solely using bin aware optimization.

The file ```log_loss.py``` provides the pyTorch based implementation of the loss. Keep in mind that when using the loss function along side a network-specific loss function a hyper-parameter should be used for the log loss function (λ<sub>1</sub> in Sec3.4). This hyperparameter can be tuned for better results.