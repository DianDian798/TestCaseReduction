# -*- coding: utf-8 -*-
import os
import copy
import random
import math
import FaultLocalization

# 信息熵相关
def getSusTable(coverInfor, resultOfTestCase, formula, formula_Except):
    """
    静态方法, CBFL方法获得程序怀疑度表
    :param formula_Except: 异常时的计算公式
    :param formula: 怀疑度公式
    :param coverInfor:  key: 语句编号, value:[0,1,2.....] 0表示没有覆盖，1表示覆盖了，2表示不计入覆盖信息，如空行/宏定义/注释等；
    :param resultOfTestCase: 测试用例执行信息 [1,0,0,0,1] 0：pass; 1:fail
    :return: table 程序怀疑度表
    """
    table = {}
    # 程序语句集合
    statements = copy.deepcopy(list(coverInfor.keys()))
    # 初始化 程序语句怀疑度表 table
    for elem in statements:
        table[elem] = 0.0

    for key in coverInfor:
        size = len(coverInfor[key])
        aef = anf = aep = anp = 0
        for index in range(0, size):
            # 覆盖
            if coverInfor[key][index] == '1':
                # 执行失败
                if resultOfTestCase[index] == 1:
                    aef += 1
                # 执行通过
                else:
                    aep += 1
            else:
                if resultOfTestCase[index] == 1:
                    anf += 1
                else:
                    anp += 1
        try:
            # 移位, 使得怀疑度值不为负数
            sus = round(eval(formula), 4) + 100000.00
        except ZeroDivisionError:
            sus = round(eval(formula_Except), 4) + 100000.00
        table[key] = sus
    return copy.deepcopy(table)

def getProbabilityOfBeFault(statement, table):
    """
    静态方法, 语句成为错误语句的概率
    :param statement:
    :param table:
    :return:
    """
    totalSus = 0.0
    for key in table:
        totalSus += table[key]
    try:
        result = table[statement] / totalSus
    except ZeroDivisionError:
        result = 0.0
    return result

def getEntropyOfStatement(coverInfor, resultOfTestCase, formula, formula_Except):
    """
    静态方法, 计算语句的熵
    :param coverInfor:
    :param resultOfTestCase:
    :param formula:
    :param formula_Except:
    :return: 语句的熵
    """
    # 程序怀疑度表
    table = getSusTable(coverInfor=coverInfor, resultOfTestCase=resultOfTestCase, formula=formula, formula_Except=formula_Except)
    # 程序语句集合
    statementSet = copy.deepcopy(list(table.keys()))

    entropy = 0.0
    for elem in statementSet:
        probability = getProbabilityOfBeFault(statement=elem, table=table)
        if probability == 0.0:
            probability = 0.1e-301
        else:
            pass
        entropy += -(probability * math.log2(probability))
    return entropy
# 信息熵相关

# 测试用例集, 语句覆盖信息相关操作
def removeTestCase(resultOfTestCase, removeId):
    """
    静态方法, 从测试用例执行结果中移除指定Id的测试用例
    :param removeId:
    :param resultOfTestCase: 测试用例执行结果
    :return: 移除后的测试用例执行结果
    """
    # 移除后的测试用例执行结果
    result = []
    for index in range(0, len(resultOfTestCase)):
        if index not in removeId:
            result.append(resultOfTestCase[index])
        else:
            pass
    return result

def removeTestCaseById(resultOfTestCase, removeId):
    result = []
    size = len(resultOfTestCase)
    for index in range(0, size):
        if index != removeId:
            result.append(index)
        else:
            pass
    return copy.deepcopy(result)

def removeTestCaseCoverInfor(coverInfor, removeId):
    """
    静态方法, 从测试用例的语句覆盖信息中移除指定测试用例覆盖语句的信息
    :param removeId: 需要移除的测试用例 ID
    :param coverInfor:测试用例的语句覆盖信息
    :return:
    """
    result = {}
    statementSet = copy.deepcopy(list(coverInfor.keys()))
    for item in statementSet:
        result[item] = []

    for key in coverInfor:
        tempData = []
        for index in range(0, len(coverInfor[key])):
            if index not in removeId:
                tempData.append(coverInfor[key][index])
            else:
                pass
        result[key] = tempData

    return result

def getInitialTestCaseSetId(resultOfTestCase):
    """
    静态方法, 获得最初的测试用例集合ID（保证至少包含一个失败的测试用例）
    :param resultOfTestCase:
    :return:
    """
    result = [0]
    size = len(resultOfTestCase)
    for index in range(1, size):
        if resultOfTestCase[index] == 1:
            result.append(index)
            break
        else:
            result.append(index)

    return copy.deepcopy(result)

def getTestCaseSetById(resultOfTestCase, testCaseId):
    """
    静态方法, 获取初始测试用例中测试用例的执行结果
    :param testCaseId:
    :param resultOfTestCase:
    :return:
    """
    result = []
    size = len(resultOfTestCase)
    for index in range(0,size):
        if index in testCaseId:
            result.append(resultOfTestCase[index])
        else:
            pass
    return copy.deepcopy(result)

def addTestCase(initialTestCaseSetId, addId):
    initialTestCaseSetId.append(addId)
    return copy.deepcopy(initialTestCaseSetId)

def getCoverInforByTestCaseId(testCaseSetId, coverInfor):
    """
    静态方法, 获得最初的测试用例集合语句覆盖信息
    :param testCaseSetId: 测试用例Id 集合
    :param coverInfor: 测试用例的语句覆盖信息
    :return: 最初的测试用例集语句覆盖信息
    """
    result = {}

    for key in coverInfor:
        result[key] = []

    for key in coverInfor:
        for elem in testCaseSetId:
            result[key].append(coverInfor[key][elem])
    return copy.deepcopy(result)

def addCoverInfor(initialCoverInfor, coverInfor, testCaseId):
    """
    静态方法, 在 initialCoverInfor 中添加指定ID的测试用例语句覆盖信息
    :param initialCoverInfor:
    :param coverInfor:
    :param testCaseId:
    :return:
    """
    for key in initialCoverInfor:
        initialCoverInfor[key].append(coverInfor[key][testCaseId])
    return copy.deepcopy(initialCoverInfor)

def getNextTestCaseSetId(initialTestCaseSetId, resultOftestCase):
    result = []
    size = len(resultOftestCase)
    for index in range(0, size):
        if index not in initialTestCaseSetId:
            result.append(index)
        else:
            pass
    return result

def getNextTestCaseSet(initialTestCaseSetId, resultOfTestCase):
    """
    静态方法, 获得需要约简的测试用例集合
    :param initialTestCaseSetId: base 测试用例集合ID
    :param resultOfTestCase: 测试用例集合
    :return:
    """
    result = []
    size = len(resultOfTestCase)
    for index in range(0, size):
        if index not in initialTestCaseSetId:
            result.append(resultOfTestCase[index])
        else:
            pass
    return result
# 测试用例集, 语句覆盖信息相关操作

# 变异体 及其相关操作
def selectMutantExecResultByTestCaseId(resultOfMutantExec, testCaseId):
    """
    静态方法，依据测试用例Id 选择变异体在测试用例上的执行信息
    :param resultOfMutantExec: 变异体在测试用例上的执行信息
    :param testCaseId:
    :return: 变异体在集合 testCaseId 中测试用例上的执行信息
    """
    result = ''
    size = len(resultOfMutantExec)
    for index in range(0, size):
        if index in testCaseId:
            result = result + resultOfMutantExec[index]
        else:
            pass
    return copy.deepcopy(result)

def createMutantsInfor(catalog, testCaseId, readFile, saveFile):
    """
    静态方法, 依据测试用例ID, 创建变异体相关信息文件
    :param saveFile: 存储的文件
    :param readFile: 需要读取的文件 MutantInfor.txt or RelationshipOnlyFail.txt
    :param catalog: 存取目录
    :param testCaseId: 执行的测试用例ID
    :return:
    """
    url = os.getcwd()
    readCatalog = url + catalog + readFile
    saveCatalog = url + catalog + saveFile
    fo = open(readCatalog, "r")
    infor = fo.readlines()
    fi = open(saveCatalog, "w")
    for elem in infor:
        # MutantInfor.txt 文件 tempData 格式 "130Signal9Signal=Signal=0;//Signal000000000000000000000"
        # RelationshipOnlyFail.txt文件 tempData 格式  "130Signal11Signal4.0Signal0Signal269.0Signal87.0Signal0.00Signal=Signal=!Signal110011111111100111111111111111111"
        tempData = elem.split("Signal")
        # 变异体在测试用例上的执行结果
        resultOfMutantOnTC = ""
        if readFile == "MutantInfor.txt":
            resultOfMutantOnTC = selectMutantExecResultByTestCaseId(resultOfMutantExec=tempData[4], testCaseId=testCaseId)
        elif readFile == "RelationshipOnlyFail.txt":
            resultOfMutantOnTC = selectMutantExecResultByTestCaseId(resultOfMutantExec=tempData[9], testCaseId=testCaseId)

        fi.write(str(tempData[0]) + "Signal" + str(tempData[1]) + "Signal" + str(tempData[2]) + "Signal" + str(tempData[3]) + "Signal" + str(resultOfMutantOnTC) + "\n")

    fo.close()
    fi.close()

def caculateMutantsParameter(readFile, saveFile, readCatalog, saveCatalog, resultOfTC):
    """
    静态方法, 依据执行的测试用例, 统计错误定位相关参数
    :param readFile: 读取文件
    :param saveFile: 存储文件
    :param readCatalog: 读取目录
    :param saveCatalog: 存储目录
    :param resultOfTC: 测试用例执行结果
    :return:
    """
    url = os.getcwd()
    readCatalog = url + readCatalog + readFile
    fo = open(readCatalog, "r")
    saveCatalog = url + saveCatalog + saveFile
    fi = open(saveCatalog, "w")

    Infor = fo.readlines()
    # 遍历变异体
    for elem in Infor:
        mutant = elem.split("Signal")
        anp = anf = akp = akf = 0
        for index in range(0, len(resultOfTC)):
            # 测试用例执行通过
            if resultOfTC[index] == 0:
                # not kill
                #print(mutant[4])
                if mutant[4][index] == '0':
                    anp += float(1)
                # kill
                else:
                    akp += float(1)
            # 测试用例执行失败
            else:
                if mutant[4][index] == '0':
                    anf += float(1)
                else:
                    akf += float(1)
        fi.write(mutant[0] + "Signal" + mutant[1] + "Signal" + str(anp) + "Signal" + str(anf) + "Signal" + str(
            akp) + "Signal" + str(
            akf) + "Signal" + str("0.00") + "Signal" + mutant[2] + "Signal" + mutant[3] + "Signal" + mutant[4][
                                                                                                     :-1] + "\n")
    fo.close()
    fi.close()
# 变异体 及其相关操作

class EntropyOfTestCase:
    entropy = {}
    cover = {}
    resultOfTestCase = []
    testCaseIdSetOfFail = []
    testCaseIdSetOfPass = []
    def __init__(self):
        self.entropy.clear()
        self.resultOfTestCase.clear()
        self.cover.clear()
        self.testCaseIdSetOfFail.clear()
        self.testCaseIdSetOfPass.clear()

    def loadInfor(self, readCatalog):
        """
        方法，加载 cover, resultOfTestCase
        :param readCatalog:
        :return: NULL
        """
        case = FaultLocalization.TestCase()
        self.resultOfTestCase = copy.deepcopy(case.loadTestCaseInfor(file="in_vector.txt", readCatalog=readCatalog))
        self.cover = copy.deepcopy(case.loadTestCaseCoverInfor(file="covMatrix.in", readCatalog=readCatalog))
        self.testCaseIdSetOfFail = copy.deepcopy(case.selectTestCase(flag=1))
        self.testCaseIdSetOfPass = copy.deepcopy(case.selectTestCase(flag=0))

    def getMapOfEntropy(self, formula, formula_Except):
        coverInfor = copy.deepcopy(self.cover)
        resultOfTC = copy.deepcopy(self.resultOfTestCase)

        # 基准测试用例集及其语句覆盖信息
        #baseTestCaseId = getInitialTestCaseSetId(resultOfTestCase=resultOfTC)
        #baseTestCase = getTestCaseSetById(resultOfTestCase=resultOfTC, testCaseId=baseTestCaseId)

        #baseCoverInfor = getCoverInforByTestCaseId(testCaseSetId=baseTestCase, coverInfor=coverInfor)
        # 基准测试用例集 的信息熵
        baseEntropy = getEntropyOfStatement(coverInfor= coverInfor, resultOfTestCase= resultOfTC, formula=formula, formula_Except= formula_Except)

        # 待约简测试用例集及其语句覆盖信息
        #awaitTestCaseId = getNextTestCaseSetId(initialTestCaseSetId=baseTestCaseId, resultOftestCase=resultOfTC)
        size = len(resultOfTC)
        for index in range(0, size):
            print(str(index) + ": begin")
            needTestCaseId = removeTestCaseById(resultOfTestCase=resultOfTC, removeId=index)
            needTestCase = getTestCaseSetById(testCaseId= needTestCaseId, resultOfTestCase=resultOfTC)
            needCoverInfor = getCoverInforByTestCaseId(testCaseSetId=needTestCaseId, coverInfor=coverInfor)
            needEntropy = getEntropyOfStatement(coverInfor=needCoverInfor, resultOfTestCase=needTestCase, formula=formula, formula_Except=formula_Except)
            self.entropy[index] = needEntropy - baseEntropy

        return copy.deepcopy(self.entropy)

    def selectTestCase(self, ratio):
        """
        方法，从按信息熵排好序的通过的测试用例中抽取 ratio 比例的测试用例
        :param ratio: 抽样比例
        :return: 需要执行的测试用例集合 [测试用例ID, 测试用例ID]
        """
        # 将执行失败的测试用例的ID 加入候选集合
        candidateSet = copy.deepcopy(self.testCaseIdSetOfFail)

        # 提取执行通过的测试用例ID 及其对应的信息熵
        temp = {}
        for key in self.entropy:
            if key not in candidateSet:
                temp[key] = self.entropy[key]
            else:
                pass
        # 按信息熵从小到大排序
        tempData = sorted(temp.items(), key=lambda x: x[1], reverse=False)
        # 待约简的测试用例集 大小
        size = len(tempData)
        selectCount = math.ceil(size * ratio)
        # 依次选择要执行的测试用例
        for index in range(0, selectCount):
            candidateSet.append(tempData[index][0])

        candidateSet.sort()
        return copy.deepcopy(candidateSet)

    def getPassedTestCase(self):
        passed = copy.deepcopy(self.testCaseIdSetOfPass)

        # 提取执行通过的测试用例ID 及其对应的信息熵
        temp = {}
        for key in self.entropy:
            if key in passed:
                temp[key] = self.entropy[key]
            else:
                pass
        # 按信息熵从小到大排序
        tempData = sorted(temp.items(), key=lambda x: x[1], reverse=True)
        result = []
        for elem in tempData:
            result.append(elem[0])
        return copy.deepcopy(result)

    def selectTestCaseByCount(self, countOfPassTestCase):
        """
        方法, 从按信息熵排好序的通过的测试用例中抽取 countOfPassTestCase 个测试用例
        :param countOfPassTestCase:
        :return: 需要执行的测试用例集合 [测试用例ID, 测试用例ID]
        """
        # 将执行失败的测试用例的ID 加入候选集合
        candidateSet = copy.deepcopy(self.testCaseIdSetOfFail)

        # 提取执行通过的测试用例ID 及其对应的信息熵
        temp = {}
        for key in self.entropy:
            if key not in candidateSet:
                temp[key] = self.entropy[key]
            else:
                pass
        # 按信息熵从小到大排序
        tempData = sorted(temp.items(), key=lambda x: x[1], reverse=False)
        # 选取测试用例的个数

        if countOfPassTestCase < len(self.testCaseIdSetOfPass):
            selectCount = countOfPassTestCase
        else:
            selectCount = len(self.testCaseIdSetOfPass)

        # 依次选择要执行的测试用例
        for index in range(0, selectCount):
            #candidateSet.append(tempData[index][0])
            candidateSet.append(self.testCaseIdSetOfPass[index])

        candidateSet.sort()
        return copy.deepcopy(candidateSet)

    def saveEntropyOfTestCase(self, saveCatalog, saveFile):
        """
        方法， 将测试用例的信息熵保存到文件 entropyOfTestCase.txt 中
        :param saveCatalog: 保存路径
        :param saveFile: entropyOfTestCase.txt
        :return:
        """
        url = os.getcwd()
        path = url + saveCatalog + saveFile
        fi = open(path, "w")
        for key in self.entropy:
            fi.write(str(key) + "Signal" + str(self.entropy[key]) + "\n")
        fi.close()