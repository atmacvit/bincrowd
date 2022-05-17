import numpy as np  
# Defining main function
def GAME(L,predMap , gt):
    M = predMap.shape[0] //(2**L)
    N = predMap.shape[1] //(2**L)
    gameMae = 0
    tiles_pred = [predMap[x:x+M,y:y+N] for x in range(0,predMap.shape[0],M) for y in range(0,predMap.shape[1],N)]
    tiles_gt = [gt[x:x+M,y:y+N] for x in range(0,gt.shape[0],M) for y in range(0,gt.shape[1],N)]
    for i in range(len(tiles_pred)):
        gameMae += abs(np.sum(tiles_pred[i])-np.sum(tiles_gt[i]))
    return gameMae

  
  
# # Using the special variable 
# # __name__
# if __name__=="__main__":
#     pts = [[2,2],[2,4],[5,6],[7,6],[7,7],[3,3]]
#     gt = np.zeros((15,15))
#     for pt in pts:
#         gt[pt[0]][pt[1]] = 1
#     # gt[tuple(pts)] = 1
#     print("hey there")
#     img  = np.zeros((15,15))
#     # L is 2 this means there will be 4^2 = 16 blocks.
#     print(gt)
#     GAME(3,img, gt)