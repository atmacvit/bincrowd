from torch.nn.modules import Module
import torch
import math
class Log_Loss(Module):
    def __init__(self, device):
        super(Log_Loss, self).__init__()
        self.device = device

    def forward(self,outputs,targets,bins,batch_size):
        loss = torch.zeros([batch_size],requires_grad= True).to(self.device)
        bin_low = torch.zeros([batch_size],requires_grad= True).to(self.device)
        bin_high = torch.zeros([batch_size],requires_grad= True).to(self.device)
        greater_mask = outputs > targets
        lesser_mask = outputs < targets        

        for ind,target in enumerate(targets):
            for i in range(len(bins)-1):
                if target.item() != 0:
                    if target.item()>bins[i] and target.item()<=bins[i+1]:
                        bin_low[ind] = bins[i] 
                        bin_high[ind] = bins[i+1]
                else:
                    if target.item()>=bins[i] and target.item()<=bins[i+1]: 
                        bin_low[ind] = bins[i]
                        bin_high[ind] = bins[i+1]
        
        k =1
        
        loss = greater_mask * torch.max(torch.tensor(k* torch.log(1+ torch.abs(outputs - targets)),dtype=torch.float32, device=self.device, requires_grad=True), (outputs - bin_high)) + lesser_mask * torch.max(torch.tensor(k* torch.log(1+ torch.abs(outputs - targets)),dtype=torch.float32, device=self.device, requires_grad=True), (bin_low - outputs))
        return loss.mean()        
