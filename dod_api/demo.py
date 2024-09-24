

def rer_arr(arr):
	left = 0
	right = len(arr)-1
	while left < right -1:
		arr[left], arr[right] = arr[right], arr[left]
		left +=1
		right -=1
		return arr
		
       
    
        
        
        
        
arr = [5 ,0, 1, 10, 100,0, 5]
re_arr =  rer_arr(arr)

print(re_arr)


