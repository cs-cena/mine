# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:43:09 2020

@author: Administrator
"""

from sklearn.feature_extraction import DictVectorizer
import csv
from sklearn import preprocessing
from sklearn import tree
from sklearn.externals.six import StringIO


with open(r"C:\Users\Administrator\Desktop\1.csv", "r", encoding="utf-8", newline='') as f:
    reader = csv.reader(f)  
    headers = next(reader)
    
    #print(headers)
    
    featureList = []
    labelList = []
    
    for row in reader:
        #print(row[len(row)-1])
        labelList.append(row[len(row)-1])
        rowDict = {}
        for i in range(1, len(row) - 1):
            #print(headers[i])
            rowDict[headers[i]] = row[i]
        featureList.append(rowDict)
    #print(featureList)
            
#特征向量化
vec = DictVectorizer()
dummyX = vec.fit_transform(featureList).toarray()
#print(vec.feature_names_)
#print(dummyX)

#针对class label做向量化
lb = preprocessing.LabelBinarizer()
dummyY = lb.fit_transform(labelList)
#print(dummyY)

#使用决策树算法来分类
clf = tree.DecisionTreeClassifier(criterion="entropy") #分类器 criterion默认选择cart算法的标准来计算结点，现在指定是用id3算法中计算信息熵的方法来选择结点 entropy 信息熵
clf = clf.fit(dummyX, dummyY) #建模
#print(clf)

#生成一个dot文件 以展示决策树
with open(r"C:\Users\Administrator\Desktop\1.dot", "w") as f:
    f = tree.export_graphviz(clf, feature_names=vec.get_feature_names(), out_file=f)
    
#dos命令 打开命令提示符 将dot文件转pdf 能可视化地更直观的展示决策树
#dot -Tpdf C:\Users\Administrator\Desktop\1.dot -o output.pdf

#应用决策树来预测，先取原来数据集的第一行，然后改一改弄个新的
oneRowX = dummyX[0, :]
print(oneRowX)

newRowX = oneRowX
newRowX[0] = 1
newRowX[2] = 0
print(newRowX)
#使用模型来做预测
predictedY = clf.predict([newRowX]) #一维数据不加[]会报错：Expected 2D array, got 1D array instead:
print(predictedY)

#




