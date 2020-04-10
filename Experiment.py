# -*- coding: utf-8 -*-
import FaultLocalization
import copy
import xlsxwriter
import os
import Reduction
import TestCaseReduction
from shutil import copyfile

# 文件
fileOfMutants = "res_record.txt"
fileOfMutantExec = "res_execute.txt"
fileOfTestExec = "res_vector.txt"
fileOfTestCase = "in_vector.txt"

# 原始MBFL变异体集合
MBFL = "MutantsSus.txt"

formulaSet = {
              "Dstar":["(akf*akf*akf)/(akp+anf)", "(akf*akf*akf)"],
              "Op2":["akf - (akp/(akp+anp+1))", "akf - (akp/(akp+anp+1))"],
              "Jaccard":["akf/(akf+anf+akp)", "akf"],
              "Ochiai":["akf /(math.sqrt((akf+anf)*(akf+akp)))","akf"],
              "Tarantula":["(akf/(akf+akp))/((akf/(akf+anf)) + (akp/(akp+anp)))", "akf"]
              }

# 怀疑度公式 CBFL
# Dstar
CBFL_Dstar = "(aef*aef*aef)/(aep + anf)"
CBFL_Except_Dstar = "(aef*aef*aef)"

# Op2
CBFL_Op2 = "aef - (aep/(aep + anp + 1))"
# Jaccard
CBFL_Jaccard = "aef/(aef + anf + aep)"
CBFL_Except_Jaccard = "aef"
# Ochiai
CBFL_Ochiai = "aef /(math.sqrt((aef+anf)*(aef+aep)))"
CBFL_Except_Ochiai = "aef"
# Tarantula
CBFL_Tarantula = "(aef/(aef+aep))/((aef/(aef+anf)) + (aep/(aep+anp)))"
CBFL_Except_Tarantula = "aef"

# 程序中错误语句位置
# sed    1--9
faultPos_sed = [5920, 988, 2011, 1221, 6042, 2157, 8150, 899, 2060]
# tcars  1--12
faultPos_tcars = [89, 110, 104, 74, 78, 119, 125, 121, 92, 96, 71, 120]
# toc_infor 1--10
faultPos_tot_infor = [117, 177, 200, 231, 248, 198, 170, 166, 201, 221]
# grep  1--10
faultPos_grep = [176, 1795, 2875, 9641, 3118, 2135, 2895, 2454, 3156, 2097]
# printtokens  1--7
faultPos_printtokens = [70, 232, 444, 445, 260, 289, 33]
# schedule   1--11
faultPos_schedule = [206, 210, 232, 108, 171, 299, 148, 199, 225, 247, 253]
# replace    1
faultPos_replace = [79]
# totol_infor
faultPos_totol_infor = [85, 75, 233, 105, 378, 201, 106, 198, 177, 394, 75, 200, 99, 223, 308, 308, 352, 215]
# tcars
faultPos_tcarsPlus = [75, 63, 120, 79, 118, 104, 51, 53, 90, 104, 132, 118,  118, 50, 51, 52, 53, 72, 72, 72, 90, 90,
                      118, 118, 63, 63, 63, 81, 129, 50, 124, 63, 58, 97, 75, 79]
faultLocalization = [5920, 988, 2011, 1221, 6042, 2157, 8150, 899, 2060,
                     89, 110, 104, 74,78, 119, 125, 121, 92, 96, 71, 120,
                     117,177,200,231,248,198,170,166,201,221,
                     176,1795,2875,9641,3118,2135,2895,2454,3156,2097,
                     70,232,444,445,260,289,33,
                     206,210,232,108,171,148,199,225,247,253,
                     79,
                     85, 75, 233, 105, 378, 201, 106, 198, 177, 394, 75, 200, 99, 223, 308, 308, 352, 215,
                     75, 63, 120, 79, 118, 104, 51, 53, 90, 104, 104, 118,  118, 50, 51, 52, 53, 72, 72, 72, 90, 90,
                     118, 118, 63, 63, 63, 76, 129, 53, 124, 63, 58, 97, 126, 79]

# begin 生成对应实验文件
def generateFileOfMutantInfor(version):
    """
    静态方法, 生成文件 MutantInfor.txt
    :param version: 程序版本号
    :return: NULL
    """
    print("version: " + str(version) + "  start create MutantInfor.txt")
    readCatalog = "/resource/" + str(version) + "/"
    saveCatalog = "/result/" + str(version) + "/"
    # 变异体实列
    mutant = FaultLocalization.Mutants()
    mutants = mutant.loadMutantsInfor(readCatalog=readCatalog, file=fileOfMutants)
    # 变异体是否执行信息
    mutantsExecInfor = mutant.isExecMutants(file=fileOfMutantExec, readCatalog=readCatalog)

    mutant.resultOfMutants(file=fileOfTestExec, readCatalog=readCatalog, saveCatalog= saveCatalog)

    print("version: " + str(version) + "  create MutantInfor.txt successful~")

def generateFileOfMutantsSus(version):
    """
    静态方法, 生成文件 MutantsSus.txt
    :param version: 程序版本号
    :return: NULL
    """
    print("version: " + str(version) + " start create MutantsSus.txt")
    readCatalog = "/resource/" + str(version) + "/"
    saveCatalog = "/result/" + str(version) + "/"

    testCase = FaultLocalization.TestCase()
    resultOfTC = testCase.loadTestCaseInfor(file=fileOfTestCase, readCatalog=readCatalog)
    FaultLocalization.getParameter(file="MutantInfor.txt", readCatalog=saveCatalog, saveCatalog=saveCatalog,
                                       resultOfTC=resultOfTC)
    print("version: " + str(version) + "  create MutantsSus.txt successful~")

def generateFileOfmutantsFTMES(version, statements, cover):
    """
    静态方法, 实验FTMES
    :param version:
    :param statements:
    :param cover: 测试用例在语句上的覆盖信息
    :return:
    """
    print("version: " + str(version) + " start create mutantsFTMES.txt")
    readCatalog = "/resource/" + str(version) + "/"
    saveCatalog = "/result/" + str(version) + "/"

    ftmesInstance = FaultLocalization.FTMES()
    ftmesInstance.loadStatisticsInfor(file="MutantsSus.txt", readCatalog=saveCatalog, statements=statements)
    ftmesInstance.methodsOfFTMES(cover=cover, saveCatalog=saveCatalog)
    print("version: " + str(version) + " create mutantsFTMES.txt successful~")

def generateFileOfSampling(version):
    """
    静态方法，变异体约简方法 Sampling
    :param version:
    :return:
    """
    print("version: " + str(version) + " start create Sampling.txt")
    saveCatalog = "/result/" + str(version) + "/"

    sample = FaultLocalization.Sampling()
    size = sample.loadStatisticsInfor(file="MutantsSus.txt", readCatalog=saveCatalog)

    sample.mutantSampling(saveCatalog=saveCatalog, saveFile="Sampling30.txt", ratio= 0.3)
    sample.mutantSampling(saveCatalog=saveCatalog, saveFile="Sampling20.txt", ratio=0.2)
    sample.mutantSampling(saveCatalog=saveCatalog, saveFile="Sampling10.txt", ratio=0.1)

    print("version: " + str(version) + " create Sampling.txt successful~")

def mutantSampling(ratio, times,  begin, end, resultFile):
    """
    静态方法，变异体约简测试Sampling
    :param ratio: 约简比例
    :param times: 重复执行次数
    :param begin: 开始版本
    :param end: 结束版本
    :param resultFile: 生成结果文件名称
    :return:
    """
    methodMBFL = ["Jaccard", "Ochiai", "Op2", "Tarantula", "Dstar"]
    for susMethod in methodMBFL:
        # 排名
        rank = []
        # 定位精度
        precision = []
        # 遍历每一个版本
        for index in range(begin, end):
            saveCatalog = "/result/" + str(index) + "/"
            tempRank = 0
            tempPrecision = 0.0
            # 对每个版本，重复执行 times 次，结果取平均值
            # 创建 Sampling 方法对象，加载对应的变异体文件 MutantsSus.txt
            sample = FaultLocalization.Sampling()
            size = sample.loadStatisticsInfor(file="MutantsSus.txt", readCatalog=saveCatalog)
            for time in range(0, times):
                sample.mutantSampling(saveCatalog=saveCatalog, saveFile="Sampling_" + str(ratio) + ".txt", ratio= ratio)
                # 计算错误定位精度及排名
                result = getPrecision(file="Sampling_" + str(ratio) + ".txt", version=index, formula=formulaSet[susMethod][0],
                                      formulaException=formulaSet[susMethod][1])
                tempPrecision += result[0]
                tempRank += result[1]

            rank.append(round(tempRank / times, 4))
            precision.append(round(tempPrecision / times, 4))
            print("formula:" + susMethod + "  version: " + str(index) + "  " + str(round(tempPrecision / times, 4)) + "  " + str(round(tempRank / times, 4)))
        saveToExcel(saveFile=resultFile + susMethod + "_" + str(ratio) + ".xlsx", data1Head="错误定位精度", data1=precision, data2Head="排名", data2=rank)

# end 生成对应实验文件

# begin 获取对应方法执行的MTP次数
def getMTP(version, readFileBefore, readFileAfter):
    """
    静态方法，获取指定方法执行的MTP次数
    :param version: 程序版本
    :param readFileBefore: 约简前文件
    :param readFileAfter: 约简后文件
    :return: result, 0：约简前执行MTP次数，1:约简后执行MTP次数
    """
    readCatalog = "/result/" + str(version) + "/"
    tempData = Reduction.mutantChange(readCatalog=readCatalog, readFileBefor=readFileBefore, readFileAfter=readFileAfter)
    return [tempData[0] * tempData[2], tempData[1] * tempData[2]]
    #return [tempData[2], tempData[1]]
def saveMethodReduction(begin, end, readFileBefore, readFileAfter, saveFile):
    """
    静态方法, 计算方法的约简率
    :param begin: 开始版本
    :param end: 结束版本
    :param readFileBefore: 约简前文件
    :param readFileAfter: 约简后文件
    :param saveFile: 存储文件名称
    :return: NULL
    """
    result = []
    for index in range(begin, end):
        print(str(index) + ":   start")
        temp = getMTP(version= index, readFileBefore=readFileBefore, readFileAfter=readFileAfter)
        result.append(temp)
        print(str(index) + ":   end")
    before = []
    after = []
    for elem in result:
        before.append(elem[0])
        after.append(elem[1])
    saveToExcel(saveFile=saveFile, data1=before, data2=after, data1Head=readFileBefore[:-4], data2Head=readFileAfter[:-4])
def getFTMESMTP(version):
    """
    静态方法,获取方法 FTMES执行的MTP次数
    :param version: 程序版本
    :return: result 0:约简前执行的MTP次数 1:约简后执行的MTP次数
    """
    readCatalog = "/resource/" + str(version) + "/"
    tempData = Reduction.caculateMTPOfFTMES(readCatalog=readCatalog, readFileOfTestCase="in_vector.txt", readFileOfMutants="res_vector.txt")
    return copy.deepcopy(tempData)
# end 获取对应方法执行的MTP次数

def saveFTMESReduction(begin, end, saveFile):
    """
    静态方法, 计算FTMES 方法的约简率
    :param begin: 开始版本
    :param end: 结束版本
    :param saveFile: 存储文件名
    :return: NULL
    """
    result = []
    for index in range(begin, end):
        print(str(index) + ":   start")
        tempData = getFTMESMTP(version=index)
        result.append(tempData)
        print(str(index) + ":   end")
    before = []
    after = []
    for elem in result:
        before.append(elem[0])
        after.append(elem[1])
    saveToExcel(saveFile=saveFile, data1=before, data2=after, data1Head="MBFL", data2Head="FTMES")

def getProgramStatements(version):
    """
    静态方法，获取程序语句ID集合
    :param version: 程序版本
    :return:
    """
    readCatalog = "/resource/" + str(version) + "/"

    mutantInstance = FaultLocalization.Mutants()
    mutants = mutantInstance.loadMutantsInfor(readCatalog=readCatalog, file=fileOfMutants)
    # 变异体是否执行信息
    mutantsExecInfor = mutantInstance.isExecMutants(file=fileOfMutantExec, readCatalog=readCatalog)
    # 语句信息
    statements = mutantInstance.statementSet(mutants=mutants)
    return copy.deepcopy(statements)

def getResultOfTestCase(version):
    """
    静态方法, 获取该版本测试用例执行结果
    :param version: 程序版本
    :return: 测试用例执行结果
    """
    readCatalog = "/resource/" + str(version) + "/"

    testCaseInstance = FaultLocalization.TestCase()
    resultOfTC = testCaseInstance.loadTestCaseInfor(file="in_vector.txt", readCatalog=readCatalog)
    return copy.deepcopy(resultOfTC)

def getCoverInforOfTestCase(version):
    """
    静态方法，获取该版本测试用例在语句上的覆盖信息
    :param version: 程序版本
    :return: key: 语句编号, value:[0,1,2.....] 0表示没有覆盖，1表示覆盖了，2表示不计入覆盖信息，如空行/宏定义/注释等；
    """
    readCatalog = "/resource/" + str(version) + "/"

    testCaseInstance = FaultLocalization.TestCase()
    coverInfor = testCaseInstance.loadTestCaseCoverInfor(file="covMatrix.in", readCatalog=readCatalog)
    return copy.deepcopy(coverInfor)

def generateRelativeFiles(begin, end):
    """
    静态方法, 生成相关文件, mutantInfor.txt, mutantsSus.txt, RelationshipOnlyFail.txt, mutantsFTMES.txt
    :param begin: 起始版本
    :param end: 终止版本
    :return:
    """
    for index in range(begin, end):
        #mutex.acquire()
        # 程序语句ID集合
        statements = getProgramStatements(version=index)
        # 测试用例执行结果
        resultOfTC = getResultOfTestCase(version=index)
        # 测试用例在语句上的覆盖信息
        coverInfor = getCoverInforOfTestCase(version=index)
        # 生成 MutantInfor.txt
        generateFileOfMutantInfor(version=index)
        # 生成 MutantsSus.txt
        generateFileOfMutantsSus(version=index)
        # 生成 mutantsFTMES.txt
        generateFileOfmutantsFTMES(version=index,statements=statements,cover=coverInfor)
        # 生成 Sampling.txt
        generateFileOfSampling(version=index)

    print("All tesk finished~")

def getPrecision(file, version, formula, formulaException):
    """
    静态方法，计算错误定位精度，排名
    :param formulaException:
    :param file: 加载的文件
    :param version: 程序版本号
    :param formula: 错误定位公式
    :return: 0:错误定位精度 1:排名
    """
    # windows or linux
    readCatalog = "/result/" + str(version) + "/"

    statementSet = getProgramStatements(version= version)

    mbflInstance = FaultLocalization.MBFL()
    mbflInstance.loadStatisticsInfor(file=file, readCatalog=readCatalog,statements=statementSet ,formula=formula, formulaException=formulaException)
    mbflInstance.createSuspiciousnessTable()
    """
    for key in mbflInstance.suspiciousnessTable:
        print(str(key) + ":" + str(mbflInstance.suspiciousnessTable[key]))
    """
    result = mbflInstance.rankTable(faultPosition=faultLocalization[version-1])
    return copy.deepcopy(result)

def saveToExcel(saveFile, data1, data2, data1Head, data2Head):
    """
    静态方法，将数据保存到excel中
    :param data2Head: data2 表头
    :param data1Head: data1 表头
    :param saveFile: 存储文件名
    :param data1: 第一列数据
    :param data2: 第二列数据
    :return:
    """
    # 创建一个新的 Excel 文件，并添加一个工作表
    workbook = xlsxwriter.Workbook(saveFile)
    worksheet = workbook.add_worksheet()

    # 设置第一列(A) 单元格宽度为 20
    worksheet.set_column('A:A', 10)
    worksheet.set_column('A:B', 10)
    worksheet.write(0,0, data1Head)
    worksheet.write(0, 1, data2Head)
    size = len(data1)
    for index in range(0, size):
        worksheet.write(index + 1, 0, data1[index])
        worksheet.write(index + 1, 1, data2[index])

    workbook.close()

def saveResultToFile(begin, end, method, saveFile, formula, formulaException):
    """
    静态方法, 将对应方法的错误定位精度,排名保存到文件中
    :param begin: 开始版本
    :param end: 终止版本
    :param method: 方法类型, 填写对应文件名称
    :param saveFile: 存储文件名
    :param formula: 错误定位公式
    :param formulaException: 出现异常时的计算公式
    :return: NULL
    """
    precision = []
    rank = []
    for index in range(begin, end):
        print(str(index) + ":  begin")
        temp = getPrecision(file=method, version=index, formula=formula, formulaException=formulaException)
        precision.append(temp[0])
        rank.append(temp[1])
        print(str(index) + ":  end")

    """
    for index in range(0, len(precision)):
        print(str(precision[index]) + ":" + str(rank[index]))
    """

    saveToExcel(saveFile=saveFile, data1=precision, data2=rank, data1Head="错误定位精度", data2Head="排名")

def translate(begin, end):
    for index in range(begin, end):
        url = os.getcwd()
        readCatalog = url + "/resource/" + str(index) + "/in_vector.txt"
        saveCatalog = url + "/resource/" + str(index) + "/in_vector1.txt"
        fo = open(readCatalog, "r")
        fi = open(saveCatalog, "w")
        infor = fo.readlines()
        for elem in range(0, len(infor[0])):
            fi.write(str(infor[0][elem]) + "\n")

def saveEntropyOfAllTestCase(begin, end, formula, formulaExcept, saveFile):
    """
    静态方法, 计算指定版本中测试用例的信息熵，并将结果保存到文件 entropyOfTestCase.txt 中
    :param saveFile: 结果文件
    :param formulaExcept:
    :param formula:
    :param begin: 开始版本
    :param end: 结束版本
    :return:
    """
    for index in range(begin,end):
        readCatalog = "/resource/" + str(index) + "/"
        saveCatalog = "/result/" + str(index) + "/"
        case = TestCaseReduction.EntropyOfTestCase()
        case.loadInfor(readCatalog=readCatalog)
        result = case.getMapOfEntropy(formula=formula, formula_Except=formulaExcept)
        case.saveEntropyOfTestCase(saveCatalog=saveCatalog, saveFile=saveFile)
        print("version  " + str(index) + "finished" )
    print("all version finished")

def getEntropyOfTestCase(catalog, file):
    """
    静态方法, 获取指定程序版本测试用例的信息熵
    :param file: 加载文件
    :param catalog: 读取目录
    :return: entropy key:测试用例ID, value: 信息熵
    """
    url = os.getcwd()
    path = url + catalog + file
    fo = open(path, "r")
    infor = fo.readlines()
    entropy = {}
    for elem in infor:
        temp = elem.split("Signal")
        entropy[int(temp[0])] = float(temp[1])
    return copy.deepcopy(entropy)

def selectTestCaseAndExecute(method, begin, end, ratio, pattern, readMethodFile, createMutantInforFile, createParameterInforFile, resultFile):
    """
    静态方法, 依据信息熵选择测试用例并执行
    :param method:
    :param createParameterInforFile:
    :param createMutantInforFile:
    :param readMethodFile: 变异体约简方法 文件
    :param resultFile: 结果文件
    :param pattern: 选择方式 0: 按比例选择 参数 为 ratio; 1:按数量选择 参数为 count
    :param begin: 开始版本
    :param end: 结束版本
    :param ratio: 抽样比例
    :return:
    """
    entropyFileName = "entropyOfTestCase_" + method + ".txt"

    resultFileName = resultFile + method
    # MBFL阶段怀疑度公式
    methodMBFL = ["Jaccard", "Ochiai", "Op2", "Tarantula", "Dstar"]

    for susMethod in methodMBFL:
        # 排名
        rank = []
        # 定位精度
        precision = []
        # 执行的测试用例个数
        countOfTestCaseExec = []
        for index in range(begin, end):
            # windows 系统 or linux
            readCatalog = "/resource/" + str(index) + "/"
            saveCatalog = "/result/" + str(index) + "/"

            case = TestCaseReduction.EntropyOfTestCase()
            case.loadInfor(readCatalog=readCatalog)
            entropyOfTC = getEntropyOfTestCase(catalog=saveCatalog, file=entropyFileName)
            case.entropy = copy.deepcopy(entropyOfTC)
            # 选择执行的测试用例 ID
            if pattern == 0:
                selectedTestCaseId = case.selectTestCase(ratio=ratio)
            elif pattern == 1:
                selectedTestCaseId = case.selectTestCaseByCount(countOfPassTestCase=len(case.testCaseIdSetOfFail))
            else:
                pass
            # 选择执行的测用来 执行结果
            selectedTestCase = TestCaseReduction.getTestCaseSetById(resultOfTestCase=case.resultOfTestCase, testCaseId=selectedTestCaseId)
            # 存储实际执行的测试用例
            saveTestCaseIdActuallyExecuted(testCaseId=selectedTestCaseId, entropyOfTC=entropyOfTC, savePath=saveCatalog, fileName="testCaseActuallyExectutd" + method+ "_" + str(ratio)+ ".txt")
            # 实际执行的测试用例个数
            countOfTestCaseExec.append(len(selectedTestCase))
            # 创建变异体 执行结果文件
            TestCaseReduction.createMutantsInfor(readFile=readMethodFile, saveFile=createMutantInforFile,
                                                 catalog=saveCatalog, testCaseId=selectedTestCaseId)
            # 写入参数信息
            TestCaseReduction.caculateMutantsParameter(readFile=createMutantInforFile,
                                                       saveFile=createParameterInforFile, readCatalog=saveCatalog,
                                                       saveCatalog=saveCatalog, resultOfTC=selectedTestCase)
            # 计算错误定位精度及排名
            result = getPrecision(file=createParameterInforFile, version=index, formula=formulaSet[susMethod][0],
                                  formulaException=formulaSet[susMethod][1])
            rank.append(result[1])
            precision.append(result[0])
            print("version: " + str(index) + "  " + str(result[0]) + "  " + str(result[1]))
        saveToExcel(saveFile=resultFileName + susMethod + "_"+ str(ratio) + ".xlsx", data1Head="错误定位精度", data1=precision, data2Head="排名", data2=rank)

def getTestCaseCount(begin,end, readFile, resultFile):
    """
    静态方法， 获取测试用例个数
    :param resultFile: 结果文件
    :param readFile: 读取方法文件
    :param begin:开始版本
    :param end: 结束版本
    :return:
    """
    url = os.getcwd()
    result = []
    for index in range(begin, end):
        catalog = url + "/result/" + str(index) + "/"+ readFile

        fo = open(catalog, "r")
        infor = fo.readlines()
        mutant = infor[0].split("Signal")
        testCase = mutant[9]
        result.append(len(testCase) - 1)
    saveToExcel(saveFile= resultFile, data1Head="测试用例个数", data1=result, data2Head="测试用例个数", data2=result)

def saveTestCaseIdActuallyExecuted(testCaseId, entropyOfTC, savePath, fileName):
    """
    静态方法，存储测试用例约简过程中实际执行的测试用例及其信息熵
    :param entropyOfTC: key:测试用例ID, value:信息熵
    :param testCaseId:测试用例Id
    :param savePath:存储路径
    :param fileName:存储文件 testCaseActuallyExectutdDstar.txt
    :return:
    """
    url = os.getcwd()
    savePaths = url + savePath + fileName
    fi = open(savePaths, "w")
    for item in testCaseId:
        fi.write(str(item) +"Signal"+ str(entropyOfTC[item]) +"\n")
    fi.close()

def countOfTestCase(begin, end):
    failTC = []
    passTC = []

    for index in range(begin, end):
        path = "/resource/" + str(index) + "/"
        temp = []
        case = FaultLocalization.TestCase()
        case.loadTestCaseInfor(file="in_vector.txt", readCatalog=path)
        failTC.append(len(case.selectTestCase(flag=1)))
        passTC.append(len(case.selectTestCase(flag=0)))
    saveToExcel(data1Head="fail", data1=failTC, data2Head="pass", data2=passTC, saveFile="countOfTestCase.xlsx")

def countOfMutants(begin, end):
    url = os.getcwd()
    result = []
    version = []
    for index in range(begin, end):
        path = url + "/result/" + str(index) + "/MutantsSus.txt"
        fo = open(path, "r")
        infor = fo.readlines()
        result.append(len(infor))
        version.append(index)
    fo.close()
    saveToExcel(data1Head="version", data1=version, data2Head="mutants", data2=result, saveFile="Mutants.xlsx")

# 文件操作
def removeFile(path, file, begin, end):
    """
    静态方法, 移除目录下某一文件
    :param path: 目录
    :param file: 文件名称
    :param begin: 开始版本
    :param end: 结束版本
    :return:
    """
    for index in range(begin, end):
        removePath = path + str(index) + "/" + file
        os.remove(removePath)

def copyFile(src, dst, srcFile, dstFile, begin, end):
    """
    静态方法， 拷贝文件
    :param src: 源目录
    :param dst: 目标目录
    :param srcFile: 源文件
    :param dstFile: 目标文件
    :param begin: 开始版本
    :param end: 结束版本
    :return:
    """
    for index in range(begin, end):
        srcPath = src + str(index) + "/" + srcFile
        dstPath = dst + str(index) + "/" + dstFile
        copyfile(src=srcPath, dst=dstPath)
        print(str(index) + ":   finished")

def importEntropyFile(method, begin, end):
    """
    静态方法，将测试用例的信息熵文件复制到目录下
    :param method:
    :param begin:
    :param end:
    :return:
    """
    path = os.getcwd()

    src = path + "/save/" + method + "/"
    dst = path + "/result/"
    srcFile = "entropyOfTestCase_" + method + ".txt"
    dstFile = "entropyOfTestCase_" + method + ".txt"
    # 复制执行文件
    copyFile(src=src, dst=dst, srcFile=srcFile, dstFile=dstFile, begin=begin, end=end)

# 文件操作
def main_run():
    methodSet = ["Dstar", "Op2", "Jaccard", "Ochiai", "Tarantula" ]
    # 生成相关文件
    #generateRelativeFiles(begin=108, end=110)
    # 计算测试用例的信息熵
    saveEntropyOfAllTestCase(begin=1, end=114, formula= CBFL_Dstar, formulaExcept= CBFL_Except_Dstar, saveFile="entropyOfTestCase_Dstar.txt")
    #saveResultOfTestCaseReduction(method=methodSet, begin=1, end=114)
    # pattern 0: 按给定比例选择变异体 1：选择和失败的测试用例个数相同的变异体

if __name__ == "__main__":
    main_run()