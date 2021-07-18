from torch.nn.modules import Module
import torch
import math

class Log_Loss(Module):
    def __init__(self, use_background, device):
        super(Log_Loss, self).__init__()
        self.device = device
        self.use_bg = use_background
 
    def forward(self,output,target,bins):
        bin_low =0
        bin_high =0

        loss = torch.zeros([1],requires_grad= True).to(self.device)
        for i in range(len(bins)-1):

            if target.item() != 0:
                if target.item()>bins[i] and target.item()<=bins[i+1]:

                    bin_low = bins[i] 
                    bin_high = bins[i+1]
            else:
                if target.item()>=bins[i] and target.item()<=bins[i+1]: 

                    bin_low = bins[i]
                    bin_high = bins[i+1]
        d1 = abs(bin_low - target.item())
        d2 = abs(bin_high - target.item())
        output = torch.tensor(output,dtype=torch.float32, device=self.device,requires_grad=True)
        target = torch.tensor(target,dtype=torch.float32, device=self.device, requires_grad=True)
        bin_high = torch.tensor(bin_high,dtype=torch.float32, device=self.device, requires_grad=True)
        bin_low = torch.tensor(bin_low,dtype=torch.float32, device=self.device, requires_grad=True)

        if output > target:  #closer to higher edge
            loss = torch.max(torch.tensor(math.log(1+ abs(output - target)),dtype=torch.float32, device=self.device, requires_grad=True), (output - bin_high))
        if output < target:  #closer to lower edge
            loss = torch.max(torch.tensor(math.log(1+ abs(output - target)),dtype=torch.float32, device=self.device, requires_grad=True), (bin_low - output))
        return loss
