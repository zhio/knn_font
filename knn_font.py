import numpy as np
import operator


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

    # 因为 dataSet 的维度是30 所以 将传入的数据 inX 扩展成训练集的长度
    # 接着将他们的数据进行相减
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
    # print(diffMat)
    # print(diffMat.shape)
    # print("====================================")

    # 将结果进行平方
    sqDiffMat = diffMat**2
    # print(sqDiffMat)
    # print("===============================")

    # 将结果求和
    # a = [1, 2, 3, 4, 5]
    # data = np.tile(a, (2, 1))
    # data --> array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
    # b = data.sum(axis=1)
    # b --> array([15, 15])
    sqDistances = sqDiffMat.sum(axis=1)
    # print(sqDistances)
    # print("===========================")

    # 对结果进行开方
    distances = sqDistances**0.5

    # 对其进行排序
    # x = np.array([9, 5, 6, 1, 4])
    # y = x.argsort()
    # array([3, 4, 1, 2, 0], dtype=int64)
    # 很好理解 按小到大排序 (排序结果是索引)
    sortedDistIndices = distances.argsort()
    # print(sortedDistIndices)
    # print("=========================")
    classCount = {}
    # 这里的 k 的值是1 实际上 i 循环时值要小于k 所以 循环只执行一次
    for i in range(k):
        # 这里 sortedDistIndices[i] 实际取的是 sortedDistIndices[0]
        # 因为 上边 argsort() 所以 sortedDistIndices[0] 存放的是差值最小的索引
        # labels 中差值最小的索引所对应的值 就是我们想要的值
        voteIlabel = labels[sortedDistIndices[i]]
        # print("i: " + str(i))
        # print(labels)
        # print(sortedDistIndices[i])
        # print(voteIlabel)
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
        print(classCount.get(voteIlabel, 0))
    # print(classCount)
    # print("======================================")
    # 将数据表进行一个排序 最大的值就是最可能的值
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    # 返回第一个 即为程序计算出最相似的那个
    # print(sortedClassCount)
    # print("===========================")
    return sortedClassCount[0][0]


def file2matrix():
    # 构造训练集
    # 从外部导入
    with open('fontdata.txt') as file:
        arrayOlines = file.readlines()
    numberOfLines = len(arrayOlines)
    # 和 classifyPerson 中一样 生成一个200大小的矩阵
    returnMat = np.zeros((numberOfLines, 200))
    classLabelVector = []
    index = 0
    # 下边这段就是对 fontdata.txt 中的数据进行还原
    # 还原成训练集
    for line in arrayOlines:
        line = line.strip()
        listFromLine = line.split('->')
        other = listFromLine[1]
        a = other.replace('(', '').replace(')', "").replace('[', '').replace(']', '')[:-1].split(',')
        returnMat[index, :len(a)] = a
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
    # 返回
    return returnMat, classLabelVector


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
