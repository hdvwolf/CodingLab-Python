import json
import requests
import xml.etree
import math
import pickle
import sys
import builtins

from Fibo import fib, fib2

#def fib(n):    # write Fibonacci series up to n
#    a, b = 0, 1
#    while a < n:
#        print(a, end=' ')
#        a, b = b, a+b
#    print()

#def fib2(n):   # return Fibonacci series up to n
#    result = []
#    a, b = 0, 1
#    while a < n:
#        result.append(a)
#        a, b = b, a+b
#    return result

#s = fib2(100)
#print(fib(100))
#print(fib2(600))

#s=math.pi
#print(s)



#scope_test()
#print("In global scope:", spam)

#def howManySwaps(arr):
    # Write your code here
arr =[8,3,2,4]
n=len(arr)
temp_arr = arr
#i,j =0,0
#for i in range(n-1):
for j in range(n-1):
    if temp_arr[j] > temp_arr[j+1]:
        temp_arr[j],temp_arr[j+1] = arr[j+1],arr[j]
#        j=j+1
#        i=i+1
print(temp_arr)
print(j+1)
#print(j)

8324
3824
2834
2384
2348