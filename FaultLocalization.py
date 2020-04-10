# -*- coding: utf-8 -*-
import os
import copy
import random
import math

"""
    静态方法块
"""
def getParameter(file, readCatalog, saveCatalog, resultOfTC):
    """
    静态方法, 统计计算变异体怀疑度的参数，并计算变异体的怀疑度
    :param file: MutantInfor.txt
    :param readCatalog:
    :param saveCatalog:
    :param resultOfTC: 测试用例执行结果信息
    :param formula: 怀疑度公式
    :return: NULL
    """
    url = os.getcwd()
    #url +=  readCatalog + file
    readCatalog = url + readCatalog + file
    fo = open(readCatalog, "r")
    saveCatalog = url + saveCatalog + "MutantsSus.txt"
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
        """
        try:
            sus = eval(formula)
        except ZeroDivisionError:
            sus = 0
        """
        fi.write(mutant[0] + "Signal" + mutant[1] + "Signal" + str(anp) + "Signal" + str(anf) + "Signal" + str(akp) + "Signal" + str(
            akf) + "Signal" + str("0.00") + "Signal" + mutant[2] + "Signal" + mutant[3] + "Signal" + mutant[4][:-1] + "\n")
    fo.close()
    fi.close()

def killOnlyByFailTest(resultOfTCExec, resultOfMutantExec):
    """
    静态方法， 计算变异体被失败的测试用例杀死的次数
    :param resultOfTCExec: 测试用例执行结果
    :param resultOfMutantExec: 变异体在测试用例上执行的结果
    :return: count 变异体被失败的测试用例杀死的次数
    """
    count = 0
    for index in range(0, len(resultOfTCExec)):
        #print(index)
        # 测试用例执行失败
        if resultOfTCExec[index] == 1:
            # 变异体被该测试用例杀死
            if resultOfMutantExec[index] == '1':
                count += 1
            else:
                pass
        else:
            pass
    return count

def killOnlyByPassTest(resultOfTCExec, resultOfMutantExec):
    """
    静态方法， 计算变异体被通过的测试用例杀死的次数
    :param resultOfTCExec: 测试用例执行结果
    :param resultOfMutantExec: 变异体在测试用例上执行的结果
    :return: count 变异体被失败的测试用例杀死的次数
    """
    count = 0
    for index in range(0, len(resultOfTCExec)):
        # print(index)
        # 测试用例执行失败
        if resultOfTCExec[index] == 0:
            # 变异体被该测试用例杀死
            if resultOfMutantExec[index] == '1':
                count += 1
            else:
                pass
        else:
            pass
    return count

def killRatio(resultOfTCExec, resultOfMutantExec):
    """
    静态方法, 计算通过的测用来杀死该变异体的比例
    :param resultOfTCExec: 测试用例执行结果
    :param resultOfMutantExec:
    :return: 通过的测试用例杀死该变异体的比例
    """
    killCount = killOnlyByPassTest(resultOfTCExec=resultOfTCExec, resultOfMutantExec=resultOfMutantExec)
    total = 0
    for elem in resultOfTCExec:
        if elem == 0:
            total += 1
        else:
            pass
    return killCount/total

def getStatisticsInfor(file, readCatalog, statements):
    """
    静态方法，加载变异体信息
    :param file: MutantsSus.txt
    :param readCatalog:
    :param statements: 程序语句集合
    :return:
    """
    url = os.getcwd()
    readCatalog = url + readCatalog + file
    fo = open(readCatalog, "r")
    Infor = fo.readlines()

    mutants = {}
    # 将 mutants的key设置为语句编号
    mutants = mutants.fromkeys(statements)
    # 将 mutants的value设置为 []
    for key in mutants:
        mutants[key] = []

    for elem in Infor:
        temp = elem.split("Signal")
        Node = []
        Node = temp[1:10]
        mutants[int(temp[0])].append(Node)
    fo.close()
    return mutants

def setMutantsSuspiciousness(mutants, formula, formulaException):
    """
    静态方法, 计算变异体的怀疑度值
    :param formulaException: 出现异常时的怀疑度计算公式
    :param mutants: key:语句ID, value: [['9', '273.0', '87.0', '0', '0', '0.0', '=', '=0;//', '00000000000000000000000000000000'],[]]
    :param formula: 怀疑度公式
    :return:
    """
    for key in mutants:
        for elem in mutants[key]:
            anp = float(elem[1])
            anf = float(elem[2])
            akp = float(elem[3])
            akf = float(elem[4])

            try:
                sus = eval(formula)
            except ZeroDivisionError:
                sus = eval(formulaException)
            elem[5] = sus

    return copy.deepcopy(mutants)

def getMaxValueOfSuspiciousness(mutant, formula, formulaException):
    """
    静态方法，只执行失败的测试用例，计算变异体怀疑度的最大值
    :param mutant: 变异体信息 [['mutantId', 'anp', 'anf', 'akp', 'akf', '0.0', '=', '=0;//', '00000000000000000000000000000000'],[]]
    :param formula:
    :param formulaException:
    :return: ((index:maxValueOfSus),(),())
    """
    maxValue = {}
    size = len(mutant)
    for index in range(0, size):
        anf = float(mutant[index][2])
        akf = float(mutant[index][4])
        akp = 0.0
        anp = float(mutant[index][1]) + float(mutant[index][3])

        try:
            maxValue[index] = eval(formula)
        except ZeroDivisionError:
            maxValue[index] = eval(formulaException)

    result = sorted(maxValue.items(), key=lambda x: x[1], reverse=True)
    return copy.deepcopy(result)

def threadhold(formula, formulaException, currentMaxSus, anp, anf, akp, akf):
    if currentMaxSus == 0:
        return 0
    else:
        pass
    try:
        result = eval(formula)
    except ZeroDivisionError:
        result = eval(formulaException)
    return result

def getRankTable(suspiciousnessTable):
    """
    静态方法, 计算错误语句定位精度，排名
    :param suspiciousnessTable: 语句怀疑度表(可以无序）
    :return:
    """
    #  结果 0:表示错误定位精度, 1:表示错误语句排名
    tempRank = sorted(suspiciousnessTable.items(), key=lambda x: x[1], reverse=True)
    # key:语句ID, value:该语句在怀疑度表的排名
    rankOfStatements = {}
    # 怀疑度表的长度
    sizeOfRank = len(tempRank)
    # 将怀疑度表赋 初始值
    for index in range(0, sizeOfRank):
        rankOfStatements[tempRank[index][0]] = index + 1
    index = 0
    # 存储 怀疑度值相同的语句
    same = []
    while index < sizeOfRank:

        same.append(tempRank[index])
        # 如后续 语句存在与ID 为 index 语句怀疑度值相同的语句，则将该语句加入same
        for indexNext in range(index + 1, sizeOfRank):
            if tempRank[index][1] == tempRank[indexNext][1]:
                same.append(tempRank[indexNext])
            else:
                break
        # 计算 same中语句的总排名
        total = 0
        for item in same:
            total += rankOfStatements[item[0]]
        # 将怀疑度值相同的语句 赋值为它们排名的平均值
        for item in same:
            rankOfStatements[item[0]] = round(total / len(same), 4)
        same.clear()
        index += 1

    return rankOfStatements

def sampleByRatio(ratio, length):
    """
    静态方法, 按照比例抽取一定数量的变异体
    :param ratio:
    :param length:
    :return:
    """
    sampleSize = length * ratio
    # 抽样集合
    sampleElem = []
    while len(sampleElem) < sampleSize:
        temp = random.randint(0, length-1)
        if temp not in sampleElem:
            sampleElem.append(temp)
        else:
            pass

    return copy.deepcopy(sampleElem)

"""
    类
"""

class Mutants:
    """
    类, 变异体及其相关信息；
    DianDian
    date: 2019-07-30
    数据：
        mutantsExec = []  执行的变异体ID
        statement = []    语句ID
        mutants = {}      变异体及其相关信息  key:变异体ID, value: [ 相关信息 ]
        示例 ：[语句ID, 是否执行(1:执行，0:不执行), 变异前语句，变异后语句, 在测试用例上的执行信息]
        [130,9,=,=0;//,00000000000000000000000000000000000000000000000000000]
    方法：
        loadMutantsInfor      加载变异体相关信息；
        statementSet
        isExecMutants      加载变异体执行信息；
        resultOfMutants   加载变异体在测试用例上的执行信息；
    """
    mutants = {}
    statements = []
    mutantsExec = []

    def __init__(self):
        self.mutants.clear()
        self.statements.clear()
        self.mutantsExec.clear()

    def loadMutantsInfor(self, readCatalog, file):
        """
        方法, 加载变异体相关信息
        :param readCatalog:
        :param file: res_record.txt
        :return: 变异体信息 key：变异体编号(从1开始) value: [语句编号, 变异前符号, 变异后符号]
        """
        url = os.getcwd()
        url += readCatalog + file
        fo = open(url, "r")
        Infor = fo.readlines()
        # 变量 变异体ID
        count = 1
        for elem in Infor:
            mutant = elem.split(":")
            # mutant[0] 语句编号; mutant[1] 变异前符号; mutant[2] 变异后符号
            mutant[0] = int(mutant[0])
            # 之后的版本, res_record.txt 中多了一个字段，为了兼容之前的版本，在处理时需要将其删掉
            if len(mutant) == 4:
                del mutant[1]
            else:
                pass
            mutant[2] = mutant[2][:-1]

            self.mutants[count] = mutant
            count += 1
        fo.close()
        return self.mutants

    def statementSet(self, mutants):
        """
        方法, 获取程序语句集合
        :param mutants: mutants key：变异体编号(从1开始) value: [语句编号, 变异前符号, 变异后符号]
        :return: [] 语句编号, 例如 [114, 117.....]
        """
        for key in mutants:
            if mutants[key][1] == 1 and mutants[key][0] not in self.statements :
                self.statements.append(mutants[key][0])
            else:
                pass
        return self.statements

    def isExecMutants(self, file, readCatalog):
        """
        方法， 加载变异体是否执行的信息，并将该信息加载到 mutants中
        此时，mutants 格式为
        :param file:  res_execute.txt
        :param readCatalog:
        :return: mutantsExec 执行的变异体ID, 例如[9,11,.....]
        """
        url = os.getcwd()
        url += readCatalog + file
        fo = open(url, "r")
        Infor = fo.readlines()

        for elem in Infor:
            self.mutantsExec.append(int(elem))
        # 将变异体是否执行信息加载到 mutants中，其他1:执行, 0:不执行
        for key in self.mutants:
            if key in self.mutantsExec:
                self.mutants[key].insert(1, 1)
            else:
                self.mutants[key].insert(1, 0)
        fo.close()
        return self.mutantsExec

    def resultOfMutants(self,file, readCatalog, saveCatalog):
        """
        加载变异体在测试用例上的执行信息，并写入文件中
        :param file: res_vector.txt
        :param readCatalog:
        :param saveCatalog:
        :return: NULL
        """
        url = os.getcwd()
        readCatalog = url + readCatalog + file
        fo = open(readCatalog, "r")
        saveCatalog = url + saveCatalog +"MutantInfor.txt"
        fi = open(saveCatalog, "w")
        Infor = fo.readlines()
        # 遍历被执行的变异体ID
        for index in range(0, len(self.mutantsExec)):
            if self.mutantsExec[index] in self.mutants:
                # 将该变异体在测试用例上的执行信息加入 mutants 中
                self.mutants[self.mutantsExec[index]].append(Infor[index])
                # 将该变异体信息写入文件 MutantInfor.txt 中
                line = str(self.mutants[self.mutantsExec[index]][0]) + "Signal" + str(self.mutantsExec[index]) + "Signal" + str(
                    self.mutants[self.mutantsExec[index]][2]) + "Signal" + str(
                    self.mutants[self.mutantsExec[index]][3]) + "Signal" + self.mutants[self.mutantsExec[index]][4]
                fi.write(line)
            else:
                pass

        fo.close()
        fi.close()

class TestCase:
    """
    类, 测试用例相关信息；
    DianDian
    date: 2019-07-30
    数据：
        ResultOfTestCaseExec = []    测试用例执行信息  0：pass; 1:fail
        cover = {} 测试用例在语句上的覆盖信息 0表示没有覆盖，1表示覆盖了，2表示不计入覆盖信息，如空行/宏定义/注释等；
    方法：
        loadTestCaseInfor      加载测试用例执行信息
    """
    resultOfTestCase = []
    cover = {}

    def __init__(self):
        self.resultOfTestCase.clear()
        self.cover.clear()

    def loadTestCaseInfor(self,file, readCatalog):
        """
        方法, 加载测试用例的执行结果
        :param file: in_vector.txt
        :param readCatalog:
        :return: 测试用例执行信息 [1,0,0,0,1] 0：pass; 1:fail
        """
        url = os.getcwd()
        readCatalog = url + readCatalog + file
        fo = open(readCatalog, "r")
        Infor = fo.readlines()
        for elem in Infor:
            self.resultOfTestCase.append(int(elem))
        fo.close()
        return self.resultOfTestCase

    def loadTestCaseCoverInfor(self, file, readCatalog):
        """
        方法, 加载测试用例的语句覆盖信息
        :param file: covMatrix.in 格式[[测试用例1在所有语句上的覆盖信息],[测试用例2在所有语句上的覆盖信息]]
        :param readCatalog:
        :return: key: 语句编号, value:[0,1,2.....] 0表示没有覆盖，1表示覆盖了，2表示不计入覆盖信息，如空行/宏定义/注释等；
        """
        url = os.getcwd()
        readCatalog = url + readCatalog + file
        fo = open(readCatalog, "r")
        infor = fo.readlines()
        # 变量 covMatrix每一行的行数, 代表语句数
        rows = len(infor[0])

        for index in range(0, rows-1):
            result = []
            # 变量所测试用例的覆盖结果，查找语句index 的覆盖信息
            for elem in infor:
                result.append(elem[index])
            # 存储 index 语句在所有测试用例上的覆盖信息
            self.cover[index + 1] = result
        fo.close()
        return self.cover

    def statementsCoverByTC(self, flag):
        """
        方法， 返回被测试用例覆盖的语句集合
        :param flag: 标志，1:表示失败的测试用例，0：表示通过的测试用例
        :return:
        """
        result = []
        for index in range(0, len(resultOfTestCase)):
            if self.resultOfTestCase[index] == flag:
                for key in self.cover:
                    if self.cover[key][index] == '1':
                        if key not in result:
                            result.append(key)
                        else:
                            pass
                    else:
                        pass
        return result

    def selectTestCase(self, flag):
        """
        方法, 依据 flag 选择测试用例
        :param flag: 1:表示失败的测试用例，0：表示通过的测试用例
        :return: 选择的测试用例 ID
        """
        result = []
        size = len(self.resultOfTestCase)
        for index in range(0, size):
            if self.resultOfTestCase[index] == flag:
                result.append(index)
            else:
                pass
        return copy.deepcopy(result)

class FTMES:

    mutants = {}

    def __init__(self):
        self.mutants.clear()

    def loadStatisticsInfor(self,file, readCatalog, statements):
        """
        方法，加载变异体信息
        :param statements: 程序语句集合
        :param file: MutantsSus.txt
        :param readCatalog:
        :return: mutants key:语句ID, value: [['9', '273.0', '87.0', '0', '0', '0.0', '=', '=0;//', '00000000000000000000000000000000'],[]]
        """
        self.mutants = copy.deepcopy(getStatisticsInfor(file=file, readCatalog=readCatalog, statements=statements))
        return self.mutants

    def methodsOfFTMES(self, cover, saveCatalog):
        """
        方法，生成FTMES 变异体文件
        :param cover: 测试用例在语句上的覆盖信息
        :param saveCatalog: 存储路径
        :return: NULL, 将结果写入文件 mutantsFTMES.txt
        """
        url = os.getcwd()
        saveCatalog = url + saveCatalog + "mutantsFTMES.txt"
        fi = open(saveCatalog, "w")

        for key in self.mutants:
            # 变量 编号为key的语句覆盖的通过的测试用例个数
            covp = 0.0
            # 变量 编号为key的语句覆盖的失败的测试用例个数
            covn = 0.0
            for elem in cover[int(key)+1]:
                if elem == '1':
                    covp += 1.0
                else:
                    covn += 1.0
            # 替换 用 covp,covn 替换变异体中的参数信息，并保存
            for item in self.mutants[key]:
                fi.write(str(key)+"Signal"+str(item[0])+"Signal"+str(covn)+"Signal"+str(item[2])+"Signal"+str(covp)+"Signal"+str(item[4])
                        +"Signal"+"0.0"+"Signal"+str(item[6])+"Signal"+str(item[7])+"Signal"+str(item[8][:-1])+"\n")
        fi.close()

class MBFL:
    suspiciousnessTable = {}
    mutants = {}
    statementRank = {}
    def __init__(self):
        self.suspiciousnessTable.clear()
        self.mutants.clear()
        self.statementRank.clear()

    def loadStatisticsInfor(self, file, readCatalog, statements, formula, formulaException):
        """
        方法，加载变异体信息
        :param formulaException: 出现异常时的怀疑度计算公式
        :param formula: 怀疑度公式
        :param statements: 程序语句集合
        :param file: MutantsSus.txt
        :param readCatalog:
        :return: mutants key:语句ID, value: [['9', '273.0', '87.0', '0', '0', '0.0', '=', '=0;//', '00000000000000000000000000000000'],[]]
        """
        resultTemp = getStatisticsInfor(file= file, readCatalog=readCatalog, statements=statements)
        result = setMutantsSuspiciousness(mutants=resultTemp, formula=formula, formulaException=formulaException)
        self.mutants = copy.deepcopy(result)
        return self.mutants

    def createSuspiciousnessTable(self):
        """
        方法，生成语句怀疑度表
        :return: {} key:语句ID, value: 语句怀疑度值
        """
        # 遍历 所有语句
        for key in self.mutants:
            maxSus = -200000.00
            # 遍历该语句下的所有变异体，并找出变异体怀疑度的最大值
            for elem in self.mutants[key]:
                if float(elem[5]) > maxSus:
                    maxSus = float(elem[5])
                else:
                    pass
            self.suspiciousnessTable[key] = maxSus
        """
        for key in self.suspiciousnessTable:
            print(str(key) + ":" + str(self.suspiciousnessTable[key]))
        """
        return self.suspiciousnessTable

    def rankTable(self, faultPosition):
        """
        :param faultPosition: 错误语句ID
        :return: resutl 0:表示错误定位精度, 1:表示错误语句排名
        """
        #  结果 0:表示错误定位精度, 1:表示错误语句排名
        result = []
        self.statementRank = copy.deepcopy(getRankTable(suspiciousnessTable=self.suspiciousnessTable))
        """
        for key in self.statementRank:
            print(str(key) + ":" + str(self.statementRank[key]))
        """
        result.append(round(self.statementRank[faultPosition]/len(self.statementRank), 4))
        result.append(self.statementRank[faultPosition])
        return result

class Sampling:
    mutants = []
    def __init__(self):
        self.mutants.clear()

    def loadStatisticsInfor(self, file, readCatalog):
        """

        :param file: MutantsSus.txt
        :param readCatalog:
        :return: 变异体数量
        """
        url = os.getcwd()
        readCatalog = url +readCatalog + file
        fo = open(readCatalog, "r")
        infor = fo.readlines()
        self.mutants = copy.deepcopy(infor)
        fo.close()
        return len(infor)

    def mutantSampling(self, saveCatalog, saveFile, ratio):
        """

        :param saveCatalog: 存储路径
        :param saveFile: 存储文件名 Sampling.txt
        :param ratio: 抽样比
        :return:
        """
        url = os.getcwd()
        saveCatalog = url + saveCatalog + saveFile
        fi = open(saveCatalog, "w")
        size = len(self.mutants)
        sampleSet = sampleByRatio(ratio=ratio, length=size)

        for index in range(0, size):
            if index in sampleSet:
                fi.write(self.mutants[index])
            else:
                pass
        fi.close()