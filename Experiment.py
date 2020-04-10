# -*- coding: utf-8 -*-
import FaultLocalization
import copy
import xlsxwriter
import os
import Reduction
import TestCaseReduction
from shutil import copyfile

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