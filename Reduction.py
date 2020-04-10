import os

import xlsxwriter

def loadFile(readCatalog, readFile):
    """
    静态方法, 加载文件
    :param readCatalog:
    :param readFile:
    :return: [] 文件内容
    """
    url = os.getcwd()
    url = url + readCatalog + readFile
    fo = open(url, "r")
    infor = fo.readlines()
    fo.close()
    return infor

def mutantChange(readCatalog, readFileBefor, readFileAfter):
    """
    静态方法，统计约简变异体的数目
    :param readCatalog:
    :param readFileBefor: 约简前的变异体文件
    :param readFileAfter: 约简后的变异体文件
    :return: result 0:约简前的变异体个数 1：约简后的变异体个数 2：测试用例个数
    """
    result = []
    # 约简前的变异体集合
    mutantsBefore = loadFile(readCatalog=readCatalog, readFile=readFileBefor)
    before = len(mutantsBefore)
    result.append(before)
    # 约简后的变异体集合
    after = len(loadFile(readCatalog=readCatalog, readFile=readFileAfter))
    result.append(after)
    # 测试用例个数
    numberOfTestCase = len(mutantsBefore[9])
    result.append(numberOfTestCase)
    return result

def caculateMTP(numberOfTestCase, numberOfMutant):
    """
    静态方法, 计算变异体执行MTP次数
    :param numberOfTestCase: 测试用例个数
    :param numberOfMutant: 变异体个数
    :return: MTP次数
    """
    return numberOfTestCase*numberOfMutant

def getCountOfTestCase(testCaseInfor):
    """
    静态方法, 获取测试用例个数
    :param testCaseInfor: 测试用例执行信息
    :return: 测试用例个数
    """
    return len(testCaseInfor)

def getCountOfFailTestCase(testCaseInfor):
    """
    静态方法,获取执行失败的测试用例个数
    :param testCaseInfor: 测试用例执行信息
    :return: 失败的测试用例个数
    """
    count = 0
    for item in testCaseInfor:
        if item[:-1] == '1':
            count += 1
        else:
            pass
    return count

def getCountOfMutants(mutantsInfor):
    """
    静态方法, 获取变异体个数
    :param mutantsInfor:
    :return:
    """
    return len(mutantsInfor)

def caculateMTPOfFTMES(readCatalog, readFileOfTestCase, readFileOfMutants):
    """
    静态方法，获取 FTMES 方法约简前后执行的MTP次数
    :param readCatalog:
    :param readFileOfTestCase: in_vector.txt
    :param readFileOfMutants: res_vector.txt
    :return: result 0:约简前执行的MTP次数 1:约简后执行的MTP次数
    """
    # 测试用例执行信息
    testCaseInfor = loadFile(readCatalog=readCatalog, readFile=readFileOfTestCase)
    # 变异体执行信息
    mutantsInfor = loadFile(readCatalog=readCatalog, readFile=readFileOfMutants)
    # 测试用例个数
    testCase = getCountOfTestCase(testCaseInfor=testCaseInfor)
    # 失败的测试用例个数
    testCaseFail = getCountOfFailTestCase(testCaseInfor=testCaseInfor)
    # 变异体个数
    mutants = getCountOfMutants(mutantsInfor=mutantsInfor)

    return [testCase*mutants, testCaseFail*mutants]