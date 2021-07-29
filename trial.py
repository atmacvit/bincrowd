def maxAlternatingSum(arr, n):
 
    # initialize sum to 0
    max_sum = 0
     
    i = 0
     
    while i<n:
        current_max = arr[i]
        k = i
         
        while k<n and ((arr[i]>0 and arr[k]>0)
        or (arr[i]<0 and arr[k]<0)):
             
            current_max = max(current_max, arr[k])
             
            k+= 1
         
        # calculate the sum
        max_sum+= current_max
         
        i = k
         
    # return the final result
    return max_sum
 
for i in range(6):
    print(maxAlternatingSum(arr=[1,-2,3,4,5], n=i))