import numpy as np
import operator
from fontTools.ttLib import TTFont

def classify0(inX, dataSet, labels, k):
    #numpy函数shape[0]返回dataSet的行数
    dataSetSize = dataSet.shape[0]
    #在列向量方向上重复inX共1次(横向),行向量方向上重复inX共dataSetSize次(纵向)
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
    #二维特征相减后平方
    sqDiffMat = diffMat**2
    #sum()所有元素相加,sum(0)列相加,sum(1)行相加
    sqDistances = sqDiffMat.sum(axis=1)
    #开方,计算出距离
    distances = sqDistances**0.5
    #返回distances中元素从小到大排序后的索引值
    sortedDistIndices = distances.argsort()
    #定一个记录类别次数的字典
    classCount = {}
    for i in range(k):
        #取出前k个元素的类别
        voteIlabel = labels[sortedDistIndices[i]]
        #dict.get(key,default=None),字典的get()方法,返回指定键的值,如果值不在字典中返回默认值。
        #计算类别次数
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    #python3中用items()替换python2中的iteritems()
    #key=operator.itemgetter(1)根据字典的值进行排序
    #key=operator.itemgetter(0)根据字典的键进行排序
    #reverse降序排序字典
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    #返回次数最多的类别,即所要分类的类别
    return sortedClassCount[0][0]
def file2matrix():
    #构造训练集
    with open('fontdata.txt') as file:
        arrayOlines = file.readlines()
    numberOfLines = len(arrayOlines)
    returnMat = np.zeros((numberOfLines,200))
    classLabelVector = []
    index = 0
    for line in arrayOlines:
        line = line.strip()
        listFromLine = line.split('->')
        other = listFromLine[1]
        a = other.replace('(','').replace(')',"").replace('[','').replace(']','')[:-1].split(',')
        returnMat[index,:len(a)] = a
        if listFromLine[0] == '1':
            classLabelVector.append(1)
        elif listFromLine[0] == '2':
            classLabelVector.append(2)
        elif listFromLine[0] == '3':
            classLabelVector.append(3)
        elif listFromLine[0] == '4':
            classLabelVector.append(4)
        elif listFromLine[0] == '5':
            classLabelVector.append(5)
        elif listFromLine[0] == '6':
            classLabelVector.append(6)
        elif listFromLine[0] == '7':
            classLabelVector.append(7)
        elif listFromLine[0] == '8':
            classLabelVector.append(8)
        elif listFromLine[0] == '9':
            classLabelVector.append(9)
        elif listFromLine[0] == '0':
            classLabelVector.append(0)
        index += 1
    return returnMat,classLabelVector

def classifyPerson(font):
    returnMats = np.zeros([200])
    returnMats[:len(font)] = font
    datingDataMat, datingLabels = file2matrix()
    inArr = returnMats
    classifierResult = classify0(inArr, datingDataMat, datingLabels, 1)
    return classifierResult