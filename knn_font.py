import numpy as np
import operator
from fontTools.ttLib import TTFont

# inArr 传入的font数据(经过构造)
# datingDataMat 训练集的数据
# datingLabels 训练集的标签
# classify0(inArr, datingDataMat, datingLabels, 1)
def classify0(inX, dataSet, labels, k):
    # KNN
    
    # dataSet 本地的 fontdata.txt 只有30条数据
    # print(dataSet)
    # 所以 shape[0] 为 样本的个数
    dataSetSize = dataSet.shape[0]
    # print(dataSetSize)
    # print("==============================")

    # np.tile()
    # 1.沿X轴复制
    # 2.XY轴都复制，或只沿着Y轴复制的方法

    # 假如
    # inX = [1, 2, 3, 4, 5]
    # data = np.tile(inX, 1)
    # data --> array([1, 2, 3, 4, 5])
    
    # data2 = np.tile(inX, 2)
    # data2 --> array([1, 2, 3, 4, 5, 1, 2, 3, 4, 5])
    
    # data3 = np.tile(inX, (2, 1))
    # data3 --> array([[1, 2, 3, 4, 5],[1, 2, 3, 4, 5]])
    
    # data4 = np.tile(inX, (2, 2))
    # data4 --> array([[1, 2, 3, 4, 5, 1, 2, 3, 4, 5],[1, 2, 3, 4, 5, 1, 2, 3, 4, 5]])
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
    print(diffMat)
    print(diffMat.shape)
    print("====================================")
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndices = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndices[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
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
    # 传进来的font 是字体的坐标信息
    # print("======== font =======")
    # print(font)
    # print("=====================")

    # 生成一个新的 200大小的空间
    returnMats = np.zeros([200])
    
    # 把 font 的内容 存放到上边生成的空间中去
    returnMats[:len(font)] = font
    # print("======= resturnMats =======")
    # print(returnMats)
    # print("===========================")
    
    # datingDataMat数据 和 datingLabels标签
    # file2matrix() 是把数据集导入进来
    datingDataMat, datingLabels = file2matrix()
    inArr = returnMats
    # 调用 classify0 训练数据得出结果
    classifierResult = classify0(inArr, datingDataMat, datingLabels, 1)
    # print(classifierResult)
    return classifierResult
