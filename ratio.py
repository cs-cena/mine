# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 22:13:31 2019

@author: Administrator
"""
def ratio(rr):
    list = [0.015625,0.046875,0.09375,0.15625,0.1875,0.1875,0.15625,0.09375,0.046875,0.015625]
    list1 = [0,1,2,3,4,5,6,7,8,9]
    list2 = [0,4,5,6,10,11,12,16,17,18]
    list3 = [0,7,8,9,16,17,18,25,26,27]
    list4 = [0,10,11,12,22,23,24,34,35,36]
    list5 = [0,13,14,15,28,29,30,43,44,45]
    list6 = [0,16,17,18,34,35,36,52,53,54]
    
    ratio = 0
    
    for i1 in range(0,10):
        a1 = list1[i1]
        for i2 in range(0, 10):
            a2 = list2[i2]
            for i3 in range(0, 10):
                a3 = list3[i3]
                for i4 in range(0, 10):
                    a4 = list4[i4]
                    for i5 in range(0, 10):
                        a5 = list5[i5]
                        for i6 in range(0, 10):
                            a6 = list6[i6]
                            a = a1+a2+a3+a4+a5+a6
                            if a == rr:
                                ratio+= list[i1]*list[i2]*list[i3]*list[i4]*list[i5]*list[i6]
    return ratio

def rat():
    
    list1 = [0,1,2,3]
    list2 = [0,4,5,6]
    list3 = [0,7,8,9]
    list4 = [0,10,11,12]
    list5 = [0,13,14,15]
    list6 = [0,16,17,18]
    
    box = []
    
    
    
    
if __name__ == '__main__':
    
    s = 0
    for i in [80]:
        s+=ratio(i)
    print(s)
    
    

    
    
    
    
    
    
    
    
    
    