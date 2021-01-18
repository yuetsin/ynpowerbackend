import sqlalchemy
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from pprint import pprint, pformat
from Controller import uploadData
from Controller.login import login
from Controller.program import *
from algorithms import *
import dao
import json
import numpy as np

# import os
# _dir = './apis'
# if not os.path.exists(_dir):
#     os.makedirs(_dir)

app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)


def try_print_args():
    try:
        pprint(request.args)
    except RuntimeError:
        pass

def try_print_json():
    try:
        pprint(request.json)
    except RuntimeError:
        pass

def try_print_files():
    try:
        pprint(request.files)
    except RuntimeError:
        pass

class GetProgramName(Resource):
    def post(self):
        name = getProgramNameController()
        re = {
            "name": name
        }
        return re


class GetProgramLastInfo(Resource):
    def post(self):
        con = getProgramLastInfo()
        re = {

        }
        return re

class UploadCSV(Resource):
    def post(self):
        file = request.files['file']
        print(file.filename.split('.')[0])
        l = file.filename.split('.')[0].split('_')
        area = l[0]
        grain = l[1]
        kind = l[2]
        datatype = {'Year': 'S', 'year': 'S'}
        #dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
        #data = pd.read_csv(file, encoding='utf-8',  parse_dates=['year'], date_parser=pd.to_datetime)
        data = pd.read_csv(file, encoding='utf-8', dtype=datatype)
        header = [i for i in data.columns]
        x, y = data.shape
        allData = []
        for i in range(x):
            t = data.iloc[i][0]
            for j in range(1, y):
                temp = [t, header[j], data.iloc[i][j], grain, area, kind]
                allData.append(temp)

        allData = pd.DataFrame(allData)
        allData.columns = ['datatime', 'dataname', 'datavalue', 'grain', 'area', 'kind']
        print(allData)
        uploadData(allData)
        re = {
            "message": 'success'
        }
        return re


class GetDataJson(Resource):
    def post(self):
        dataName = request.json['dataName'].strip()
        startTime = request.json['startTime'].strip()
        endTime = request.json['endTime'].strip()
        grain = request.json['grain'].strip()
        area = request.json['area'].strip()
        kind = request.json['kind'].strip()
        re = dao.getData(area + "_" + grain + "_" + kind, dataName, startTime, endTime)
        return re

    def get(self):
        dataName = request.args.get('dataName')
        startTime = request.args.get('startTime')
        endTime = request.args.get('endTime')
        location = request.args.get('location')
        data = dao.getData(location, dataName, startTime, endTime)
        re = {
            "data": data,
            "status": '200'
        }
        return re

class Compute(Resource):
    def post(self):

        SelectYear = request.json['SelectYear'].strip()
        SelectMonth = request.json['SelectMonth'].strip()
        SelectDay = request.json['SelectDay'].strip()

        re = ""
        return re


class Clamp_force(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        SelectYear = request.json['SelectYear'].strip()
        SelectMonth = request.json['SelectMonth'].strip()
        SelectDay = request.json['SelectDay'].strip()
        premaxload = request.json['premaxload'].strip()
        pretotal = request.json['pretotal'].strip()
        re = ""
        return re


class Search(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        SelectYear = request.json['SelectYear'].strip()
        SelectMonth = request.json['SelectMonth'].strip()
        premaxload = request.json['premaxload'].strip()
        SelectDay = request.json['SelectDay'].strip()
        pretotal = request.json['pretotal'].strip()
        pregamma = request.json['pregamma'].strip()
        prebeta = request.json['prebeta'].strip()
        re = ""
        return re



class Fractal(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        SelectYear = request.json['SelectYear'].strip()
        SelectMonth = request.json['SelectMonth'].strip()
        SelectDay = request.json['SelectDay'].strip()
        premaxload = request.json['premaxload'].strip()
        pretotal = request.json['pretotal'].strip()
        re = ""
        return re

class SARIMA_Industry(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class EEMD__Industry(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class PCA__Industry(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()
        Pclist = request.json['Pclist'].strip()

        re = ""
        return re


class RandomForest_Industry(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class ANN__Industry(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class Combination_Industry(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class StepwiseRegression(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class GM(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class FGM(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class GPRM(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class GMR(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class FLR(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class FER(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class Combination(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class GBDT(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class SVM(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class RNN(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class LSTM(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re

#ESQRM 算法
class Esqrm(Resource):
    def post(self):

        StartYear = request.json['StartYear']
        EndYear = request.json['EndYear']
        PreStartYear = request.json['PreStartYear']
        PreEndYear = request.json['PreEndYear']
        result = ESQRM(StartYear, EndYear, PreStartYear, PreEndYear, quatile=0.95, pretype="consumption", econamelist=["GDP1"], city="云南省")
        re = {
            "result": result
        }
        return json.dumps(re, ensure_ascii=False)


class QuantileRegression(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class MultiIndustryDailyProfile(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class MaxUtilizationHourR(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class SARIMA(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class LFconsideringTempHoliday(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


class Unarylinear(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        PreStartYear = request.json['PreStartYear'].strip()
        EndStartYear = request.json['EndStartYear'].strip()
        VariableName = request.json['VariableName'].strip()
        PlanFlag = request.json['PlanFlag'].strip()
        Plan = request.json['Plan'].strip()
        re = ""
        return re


class Squarereg(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        PreStartYear = request.json['PreStartYear'].strip()
        EndStartYear = request.json['EndStartYear'].strip()
        VariableName = request.json['VariableName'].strip()
        PlanFlag = request.json['PlanFlag'].strip()
        Plan = request.json['Plan'].strip()

        re = ""
        return re


class Power(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        PreStartYear = request.json['PreStartYear'].strip()
        EndStartYear = request.json['EndStartYear'].strip()
        VariableName = request.json['VariableName'].strip()
        PlanFlag = request.json['PlanFlag'].strip()
        Plan = request.json['Plan'].strip()

        re = ""
        return re


class Growth(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        PreStartYear = request.json['PreStartYear'].strip()
        EndStartYear = request.json['EndStartYear'].strip()
        VariableName = request.json['VariableName'].strip()
        PlanFlag = request.json['PlanFlag'].strip()
        Plan = request.json['Plan'].strip()

        re = ""
        return re


class Exponent(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        PreStartYear = request.json['PreStartYear'].strip()
        EndStartYear = request.json['EndStartYear'].strip()
        VariableName = request.json['VariableName'].strip()
        PlanFlag = request.json['PlanFlag'].strip()
        Plan = request.json['Plan'].strip()

        re = ""
        return re


class Logarithm(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        PreStartYear = request.json['PreStartYear'].strip()
        EndStartYear = request.json['EndStartYear'].strip()
        VariableName = request.json['VariableName'].strip()
        PlanFlag = request.json['PlanFlag'].strip()
        Plan = request.json['Plan'].strip()

        re = ""
        return re


class Binarylinear(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        PreStartYear = request.json['PreStartYear'].strip()
        EndStartYear = request.json['EndStartYear'].strip()
        VariableName = request.json['VariableName'].strip()
        PlanFlag = request.json['PlanFlag'].strip()
        Plan = request.json['Plan'].strip()
        VariableName2 = request.json['VariableName2'].strip()
        PlanFlag2 = request.json['PlanFlag2'].strip()
        Plan2 = request.json['Plan2'].strip()
        re = ""
        return re

class Kmeans(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        EndStartYear = request.json['EndStartYear'].strip()
        VariableName = request.json['VariableName'].strip()

        re = ""
        return re
class PCA(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        EndStartYear = request.json['EndStartYear'].strip()
        VariableName = request.json['VariableName'].strip()

        re = ""
        return re
class AssociationRule(Resource):
    def post(self):
        StartYear = request.json['StartYear'].strip()
        EndYear = request.json['EndYear'].strip()
        MinConf = request.json['MinConf'].strip()
        EndStartYear = request.json['EndStartYear'].strip()
        VariableName = request.json['VariableName'].strip()

        re = ""
        return re


class TestAlgorithm(Resource):
    def post(self):
        test()

"""
BEGIN
fore-end related http apis
dummy version, not functional yet
"""

from random import randint, random
from uuid import uuid4 as get_uuid

def register(*url):
    def url_param(cls):
        target_url = '/api/' + '/'.join(url)
        print('bind', cls, 'to', target_url)
        api.add_resource(cls, target_url)
        return cls
    return url_param

@register('login')
class Login(Resource):
    def post(self):
        try:
            username = request.json['username'].strip()
            password = request.json['password']
            # dummy judgement
            if username == password:
                re = {
                    "msg": "success",
                    "code": 200
                }
                return re
            else:
                re = {
                    "msg": "fail",
                    "code": -1
                }
                return re
        except RuntimeError:
            return {
                    "msg": "success",
                    "code": 200
                }

@register('logout')
class Logout(Resource):
    def post(self):
        return {
            "msg": "success",
            "code": 200
        }

@register('recent')
class LoadRecent(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": [
                {
                    'name': '预测软件页面初步设计方案',
                    'url': 'https://th.bing.com/th/id/OIP.iLmhNJwXEioFCxt2cisBGgHaES?w=274&h=180&c=7&o=5&dpr=2&pid=1.7'
                },
                {
                    'name': '问题回复',
                    'url': 'https://th.bing.com/th/id/OIP.LE7rdh-q39ceZfXtus1ifAHaE7?w=270&h=180&c=7&o=5&dpr=2&pid=1.7'
                }
            ]
        } 

# 简化起见，value 就是 label，label 就是 value，不作区分。
_metadata = [
                {
                    "value": "行政",
                    "label": "白宫",
                    "children": [
                        {
                            "value": "总统",
                            "label": "唐納·川普",
                        },
                        {
                            "value": "副总统",
                            "label": "麦克·彭斯",
                        }
                    ]
                },
                {
                    "value": "立法",
                    "label": "国会",
                    "children": [
                        {
                            "value": "上院",
                            "label": "参议院",
                            "children": [
                                {
                                    "value": "议长",
                                    "label": "麦克·彭斯"
                                },
                                {
                                    "value": "多数党",
                                    "label": "共和党"
                                }
                            ]
                        },  {
                            "value": "下院",
                            "label": "众议院",
                            "children": [
                                {
                                    "value": "议长",
                                    "label": "南希·佩洛西"
                                },
                                {
                                    "value": "多数党",
                                    "label": "民主党"
                                }
                            ]
                        }
                    ]
                },
                {
                    "value": "司法",
                    "label": "最高法院",
                    "children": [
                        {
                            "value": "首席大法官",
                            "label": "約翰·格洛佛·羅勃茲",
                        }
                    ]
                }
            ]

@register('db', 'metadata')
class GetMetadata(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": _metadata
        }

@register('db', 'metadata', 'create')
class CreateMetadata(Resource):
    def post(self):
        try_print_json()
        return {
            "msg": "success",
            "code": 200
        }

@register('db', 'metadata', 'rename')
class RenameMetadata(Resource):
    def post(self):
        try_print_json()
        return {
            "msg": "success",
            "code": 200
        }

@register('db', 'metadata', 'delete')
class DeleteMetadata(Resource):
    def post(self):
        try_print_json()
        return {
            "msg": "success",
            "code": 200
        }

@register('db', 'metadata', 'upload')
class UploadMetadata(Resource):
    def post(self):
        try_print_files()
        return {
            "msg": "success",
            "code": 200
        }

@register('db', 'query')
class PerformQuery(Resource):
    def post(self):
        try_print_json()
        return {
            "msg": "success",
            "code": 200,
            "data": [
                {
                    "key": "2021-1-8",
                    "value": "陈瑞球"
                },
                {
                    "key": "2021-1-7",
                    "value": "杨咏曼"
                },
                {
                    "key": "2021-1-5",
                    "value": "蔡翠菊"
                },
                {
                    "key": "2021-1-3",
                    "value": "包玉刚"
                }
            ]
        }

@register('db', 'create')
class PerformCreate(Resource):
    def post(self):
        try_print_json()
        return {
            "msg": "success",
            "code": 200
        }

@register('db', 'update')
class PerformUpdate(Resource):
    def post(self):
        try_print_json()
        return {
            "msg": "success",
            "code": 200
        }

@register('db', 'delete')
class PerformDelete(Resource):
    def post(self):
        try_print_json()
        return {
            "msg": "success",
            "code": 200
        }

@register('db', 'except', 'query')
class ExceptionQuery(Resource):
    def post(self):
        try_print_json()
        return {
            "msg": "success",
            "code": 200,
            "data": [
                {
                    "key": "2021-1-8",
                    "category": ['三', '1', 'iv'],
                    "grain": "天",
                    "value": 10,
                    "suggest": 42
                },
                {
                    "key": "2021-1-7",
                    "category": ['三', '1', 'i'],
                    "grain": "年",
                    "value": "杨咏曼",
                    "suggest": "蔡翠菊"
                },
                {
                    "key": "2021-1-5",
                    "category": ['三', '2', 'iii'],
                    "grain": "秒",
                    "value": 3.141592653589,
                    "suggest": 2.718281828
                },
                {
                    "key": "2021-1-3",
                    "category": ['四', '2', 'ii'],
                    "grain": "年",
                    "value": True,
                    "suggest": False
                }
            ]
        }

@register('db', 'except', 'resolve')
class ExceptionResolve(Resource):
    def post(self):
        try_print_json()
        return {
            "msg": "success",
            "code": 200
        }

@register('db', 'except', 'accept')
class ExceptionAccept(Resource):
    def post(self):
        try_print_json()
        return {
            "msg": "success",
            "code": 200
        }

_versions = ['v1.0', 'v1.1', 'v1.2', 'v2.0', 'v2.1a', 'v2.1b']

_categories = ['MINING', 'STATIC_REGIONAL', 'DYNAMIC_INDUSTRIAL', 'MIX', 'LONGTERM', 'BIGUSER', 'SOKU', 'CLAMP', 'INTERP', 'YEARCONT']
_categories_count = len(_categories)

@register('tags', 'query')
class TagsQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": [
                {
                    'id': tag,
                    'tagType': _categories[randint(0, _categories_count - 1)]
                } for tag in sorted(_versions)
            ]
        }

@register('tags', 'detail')
class TagsDetail(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": {
                'tagType': 'MIX',
                'params': {
                    'param1': ...,
                    'param2': ...
                },
                'graphData': [
                    {
                        'xName': '横轴标签',
                        'yValue': '纵轴数字值'
                    }, ...
                ],
                'tableOneData': [
                    {
                        'index': '评价指标',
                        'r2': '就是 R2',
                        'mape': '就是 MAPE',
                        'rmse': '就是 RMSE'
                    }, ...
                ],
                'tableTwoData': [
                    {
                        'year': '年份',
                        'predict': '预测值（MVW）'
                    }, ...
                ]
            }
        }


# @register('tags', 'create')
# class TagsCreate(Resource):
#     def post(self):
#         try_print_json()
#         try:
#             new_name = request.json['newSchemaName'].strip()
#             if new_name in _versions:
#                 return {
#                 "msg": "key existed",
#                 "code": -1
#             }
#             _versions.append(new_name)
#             return {
#                 "msg": "success",
#                 "code": 200
#             }
#         except RuntimeError:
#             return {
#                 "msg": "success",
#                 "code": 200
#             } 

@register('tags', 'rename')
class TagsRename(Resource):
    def post(self):
        try_print_json()
        try:
            current_name = request.json['tag'].strip()
            new_name = request.json['newTag'].strip()
            if not current_name in _versions:
                return {
                "msg": "no key found",
                "code": -1
            }
            if new_name in _versions:
                return {
                "msg": "key existed",
                "code": -1
            }
            _versions.remove(current_name)
            _versions.append(new_name)
            return {
                "msg": "success",
                "code": 200,
            }
        except RuntimeError:
            return {
                "msg": "success",
                "code": 200
            }


@register('tags', 'delete')
class TagsDelete(Resource):
    def post(self):
        try_print_json()
        try:
            current_name = request.json['tag'].strip()
            if not current_name in _versions:
                return {
                "msg": "no key found",
                "code": -1
            }
            _versions.remove(current_name)
            return {
                "msg": "success",
                "code": 200,
            }
        except RuntimeError:
            return {
                "msg": "success",
                "code": 200,
            }

@register('mining', 'request')
class MiningRequest(Resource):
    def post(self):
        try_print_json()
        return {
            "msg": "success",
            "code": 200,
            "data": ['阳光', '空气', '水']
        }

@register('mining', 'factor', 'kmeans', 'suggest')
class MiningKMeansSuggestCategoryCount(Resource):
    def get(self):
        try_print_args()
        return {
            "msg": "success",
            "code": 200,
            "data": {
                "count": 2
            }
        }

@register('mining', 'results')
class MiningResults(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": [
                {
                    'plan': '某个挖掘计划',
                    'results': ['阳光', '空气', '水']
                },
                {
                    'plan': '另一个挖掘计划',
                    'results': ['光风', '霁月']
                },
                {
                    'plan': '最后一个挖掘计划',
                    'results': ['阴雨', '晦冥']
                },
            ]
        } 


_regions = ['云南省', '丽江市', '红河州', '内比都']

@register('region', 'query')
class RegionQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": _regions
        }


_industries = ['工业', '农业', '医疗业', '餐饮业']

@register('industry', 'query')
class IndustryQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": _industries
        }

_industrial_methods = ['基于ARIMA季节分解的行业电量预测', '基于EEMD的行业用电量预测', '基于主成分因子的行业用电量预测', '基于随机森林的行业用电量预测', '基于神经网络的行业用电量预测']

@register('method', 'industry', 'query')
class IndustrialMethodQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": _industrial_methods
        }

_regional_methods = ['逐步回归模型', '灰色滑动平均模型', '分数阶灰色模型',
        '改进的滚动机理灰色预测', '高斯混合回归模型', '模糊线性回归模型',
        '模糊指数平滑模型', '梯度提升模型', '支持向量机模型', '循环神经网络模型',
        '长短期神经网络模型', '扩展索洛模型', '分位数回归模型', '分行业典型日负荷曲线叠加法',
        '负荷最大利用小时数模型', '季节趋势模型', '考虑温度和节假日分布影响的电量预测模型',
        '一元线性函数', '一元二次函数', '幂函数', '生长函数', '指数函数', '对数函数', '二元一次函数']

@register('method', 'region', 'query')
class RegionalMethodQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": _regional_methods
        }

@register('grain', 'query')
class GrainQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": ['年', '月', '日', '时', '分', '秒']
        }

_factors = ['GDP', 'GNP', 'GPPPP', 'GNPPP']

@register('factor', 'query')
class MiningFactorQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": _factors
        }

@register('predict', 'region', 'single')
class RegionSinglePredict(Resource):
    def post(self):
        try_print_json()
        
        payload = {
            'graphData': [
                {
                    'xName': str(i), 
                    'yValue': randint(0, 1000)
                } for i in range(1, 18)
            ],
            'tableOneData': [
                {
                    'index': '评价指标 %d' % i,
                    'r2': random(),
                    'mape': random(),
                    'rmse': random()
                } for i in range(1, 18)
            ],
            'tableTwoData': [
                {
                    'year': i + 2010,
                    'predict': random() * randint(300, 500)
                } for i in range(17)
            ]
        }
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('predict', 'region', 'mix', 'validate')
class RegionMixModelValidate(Resource):
    def post(self):
        try_print_json()
        
        ok = (randint(0, 1) == 0)
        return {
            "msg": "success",
            "code": 200,
            "data": {
                "ok": ok
            }
        }


@register('predict', 'region', 'mix')
class RegionMixPredict(Resource):
    def post(self):
        try_print_json()
        
        payload = {
            'graphData': [
                {
                    'xName': str(i), 
                    'yValue': randint(0, 1000)
                } for i in range(1, 18)
            ],
            'tableOneData': [
                {
                    'index': '评价指标 %d' % i,
                    'r2': random(),
                    'mape': random(),
                    'rmse': random()
                } for i in range(1, 18)
            ],
            'tableTwoData': [
                {
                    'year': i + 2010,
                    'predict': random() * randint(300, 500)
                } for i in range(17)
            ]
        }
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('predict', 'industry', 'single')
class IndustrySinglePredict(Resource):
    def post(self):
        try_print_json()
        
        payload = {
            'graphData': [
                {
                    'xName': str(i), 
                    'yValue': randint(0, 1000)
                } for i in range(1, 18)
            ],
            'tableOneData': [
                {
                    'index': '评价指标 %d' % i,
                    'r2': random(),
                    'mape': random(),
                    'rmse': random()
                } for i in range(1, 18)
            ],
            'tableTwoData': [
                {
                    'year': i + 2010,
                    'predict': random() * randint(300, 500)
                } for i in range(17)
            ]
        }
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('predict', 'industry', 'mix', 'validate')
class IndustryMixModelValidate(Resource):
    def post(self):
        try_print_json()
        
        ok = (randint(0, 1) == 0)
        return {
            "msg": "success",
            "code": 200,
            "data": {
                "ok": ok
            }
        }


@register('predict', 'industry', 'mix')
class IndustryMixPredict(Resource):
    def post(self):
        try_print_json()
        
        payload = {
            'graphData': [
                {
                    'xName': str(i), 
                    'yValue': randint(0, 1000)
                } for i in range(1, 18)
            ],
            'tableOneData': [
                {
                    'index': '评价指标 %d' % i,
                    'r2': random(),
                    'mape': random(),
                    'rmse': random()
                } for i in range(1, 18)
            ],
            'tableTwoData': [
                {
                    'year': i + 2010,
                    'predict': random() * randint(300, 500)
                } for i in range(17)
            ]
        }
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('predict', 'saturation')
class SaturationCurvePredict(Resource):
    def post(self):
        try_print_json()
        
        payload = {
            'graphData': [
                {
                    'xName': str(i), 
                    'yValue': randint(0, 1000)
                } for i in range(1, 18)
            ],
            'tableOneData': [
                {
                    'index': '评价指标 %d' % i,
                    'r2': random(),
                    'mape': random(),
                    'rmse': random()
                } for i in range(1, 18)
            ],
            'tableTwoData': [
                {
                    'year': i + 2010,
                    'predict': random() * randint(300, 500)
                } for i in range(17)
            ]
        }
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('predict', 'payload')
class PayloadDensityPredict(Resource):
    def post(self):
        try_print_json()
        
        payload = {
            'graphData': [
                {
                    'xName': str(i), 
                    'yValue': randint(0, 1000)
                } for i in range(1, 18)
            ],
            'tableOneData': [
                {
                    'index': '评价指标 %d' % i,
                    'r2': random(),
                    'mape': random(),
                    'rmse': random()
                } for i in range(1, 18)
            ],
            'tableTwoData': [
                {
                    'year': i + 2010,
                    'predict': random() * randint(300, 500)
                } for i in range(17)
            ]
        }
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('predict', 'munidata', 'upload')
class MunicipalDataUpload(Resource):
    def post(self):
        try_print_files()
        return {
            "msg": "success",
            "code": 200
        }

@register('predict', 'munidata', 'filess')
class MunicipalDataQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": ['红河州.csv', '迪庆州.json', '仰光.txt', ...]
        }

@register('predict', 'provmuni')
class ProvincialAndMunicipalPredict(Resource):
    def post(self):
        try_print_json()
        
        payload = {
            'tableThreeData': [
                {
                    'year': i + 2010,
                    'region': '某个地方',
                    'predictValueBefore': random() * randint(300, 500),
                    'predictErrorBefore': random() * randint(30, 50),
                    'predictValueAfter': random() * randint(300, 500),
                    'predictErrorAfter': random() * randint(20, 80)
                } for i in range(1, 18)
            ],
            'tableFourData': [
                {
                    'year': i + 2010,
                    'region': '某个地方',
                    'predictBefore': random() * randint(300, 500),
                    'predictAfter': random() * randint(300, 500),
                } for i in range(17)
            ]
        }
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('predict', 'bigdata')
class BigDataPredict(Resource):
    def post(self):
        try_print_json()
        
        payload = {
            'graphData': [
                {
                    'xName': str(i), 
                    'yValue': randint(0, 1000)
                } for i in range(1, 18)
            ],
            'tableOneData': [
                {
                    'index': '评价指标 %d' % i,
                    'r2': random(),
                    'mape': random(),
                    'rmse': random()
                } for i in range(1, 18)
            ],
            'tableTwoData': [
                {
                    'year': i + 2010,
                    'predict': random() * randint(300, 500)
                } for i in range(17)
            ]
        }
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

_bigdata_methods = ['猜测法', '穷举法', '归纳法', '放弃法']

@register('method', 'bigdata', 'query')
class BigDataMethodQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": _bigdata_methods
        }

@register('payload', 'traits', 'daily')
class DailyPayloadTraits(Resource):
    def get(self):
        try_print_args()
        
        payload = [
                {
                    'day': '2020 年 %d 月 %d 日' % (i, i * 2),
                    'dayMaxPayload': randint(0, 1000),
                    'dayAveragePayload': random() * 500,
                    'dayPayloadRate': random() * 500,
                    'dayMinPayloadRate': random() * 500,
                    'dayPeekValleyDiff': random() * 500,
                    'dayPeekValleyDiffRate': random() * 500
                } for i in range(1, 13)
            ]
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('payload', 'traits', 'monthly')
class MonthlyPayloadTraits(Resource):
    def get(self):
        try_print_args()
        
        payload = [
                {
                    'month': '2020 年 %d 月' % i,
                    'monthAverageDailyPayload': randint(0, 1000),
                    'monthMaxPeekValleyDiff': random() * 500,
                    'monthAverageDailyPayloadRate': random() * 500,
                    'monthImbaRate': random() * 500,
                    'monthMinPayloadRate': random() * 500,
                    'monthAveragePayloadRate': random() * 500,
                } for i in range(1, 13)
            ]
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('payload', 'traits', 'yearly')
class YearlyPayloadTraits(Resource):
    def get(self):
        try_print_args()
        
        payload = [
                {
                    'year': '%d 年' % (2010 + i),
                    'yearMaxPayload': randint(10000, 1000000),
                    'yearAverageDailyPayloadRate': random() * 500,
                    'seasonImbaRate': random() * 500,
                    'yearMaxPeekValleyDiff': random() * 500,
                    'yearMaxPeekValleyDiffRate': random() * 500,
                } for i in range(1, 13)
            ]
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('payload', 'predict', 'dbquery')
class SokuPayloadPredict(Resource):
    def post(self):
        try_print_json()
        
        payload = [
                {
                    'time': '%d:%d' % (randint(10, 20), randint(10, 50)),
                    'actualPayload': randint(10000, 1000000),
                    'predictPayload': randint(10000, 1000000)
                } for _ in range(1, 13)
            ]
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('payload', 'predict', 'clamping')
class ClampingPayloadPredict(Resource):
    def post(self):
        try_print_json()
        
        payload = [
                {
                    'time': '%d:%d' % (randint(10, 20), randint(10, 50)),
                    'actualPayload': randint(10000, 1000000),
                    'predictPayload': randint(10000, 1000000)
                } for _ in range(1, 13)
            ]
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('payload', 'predict', 'interp')
class InterpolatingPayloadPredict(Resource):
    def post(self):
        try_print_json()
        
        payload = [
                {
                    'time': '%d:%d' % (randint(10, 20), randint(10, 50)),
                    'actualPayload': randint(10000, 1000000),
                    'predictPayload': randint(10000, 1000000)
                } for _ in range(1, 13)
            ]
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('payload', 'predict', 'yearly')
class YearlyContinuousPayloadPredict(Resource):
    def post(self):
        try_print_json()
        
        payload = [
                {
                    'time': '%d:%d' % (randint(10, 20), randint(10, 50)),
                    'payload': randint(10000, 1000000)
                } for _ in range(1, 13)
            ]
        return {
            "msg": "success",
            "code": 200,
            "data": payload
        }

@register('params', 'mining')
class DataMiningParameters(Resource):
    def get(self):
        print(request.args)
        return {
            "msg": "success",
            "code": 200,
            "data": {
                "region": '地域',
                "factors": ['factor 1', 'factor 2', 'factor 3'],
                "method": '方法',
                "pearson": {
                    "threshold": 0.77777
                },
                "kMeans": {
                    "categoryCount": 2
                },
                "PCA": {
                    "absThreshold": 0.77777
                },
                "ARL": {
                    "minSupport": 0.11111,
                    "minConfidence": 0.11111
                },
                "beginYear": 2024,
                "endYear": 2029,
                "tag": request.args['tag']
            }
        }

@register('params', 'predict', 'static', 'region')
class StaticRegionalPredictionParameters(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": {
                "historyBeginYear": 1999,
                "historyEndYear": 2009,
                'beginYear': 2023,
                'endYear': 2033,
                'region': '地域',
                'industry': '行业',
                'method': '方法',
                'factor1': {
                    'name': 'MINGZI',
                    'hasValue': True,
                    'value': 0.1
                },
                'factor2': {
                    'name': 'MINGZI2',
                    'hasValue': True,
                    'value': 0.9
                },
                'tag': request.args['tag']
            }
        }

@register('params', 'predict', 'dynamic', 'industry')
class DynamicIndustrialPredictionParameters(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": {
                'industry': '行业',
                'method': '方法',
                'parameters': ['paramA', 'paramB', '...'],
                'beginYear': 1995,
                'endYear': 2006,
                'historyBeginYear': 2012,
                'historyEndYear': 2055,
                'tag': request.args['tag']
            }
        }

@register('params', 'predict', 'mix')
class MixPredictionParameters(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": {
                'historyBeginYear': 2012,
                'historyEndYear': 2066,
                'beginYear': 2012,
                'endYear': 2022,
                'region': '地域',
                'industry': '工业',
                'selectedMethods': ['methodA', 'methodB', '...'],
                'tag': request.args['tag']
            }
        }

@register('params', 'predict', 'dynamic', 'region')
class LongTermPredictionParameters(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": {
                'region': '地域',
                'method': '行业',
                'parameters': ['1', '2', '...'],
                'beginYear': 1993,
                'endYear': 2013,
                'historyBeginYear': 2012,
                'historyEndYear': 2022,
                'tag': request.args['tag']
            }
        }


@register('params', 'predict', 'biguser')
class BigUserPredictionParameters(Resource):
    def get(self):
        print(request.args)
        return {
            "msg": "success",
            "code": 200,
            "data": {
                'historyBeginYear': 1966,
                'historyEndYear': 1997,
                'beginYear': 1994,
                'endYear': 2004,
                'method': '测试方法',
                'region': '测试地域',
                'patches': [
                    {
                        'metaData': ['a', 'b', 'c'],
                        'grain': '粒度（总是「年」）',
                        'year': '年份',
                        'value': '42',
                    }, '...'
                ],
                'tag': request.args['tag']
            }
        }

@register('params', 'predict', 'soku')
class SokuPayloadPredictionParameters(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": {
                'beginYear': 1955,
                'endYear': 2055,
                'season': 3,
                'maxPayload': 2033,
                'dailyAmount': 1000,
                'gamma': 0.555,
                'beta': 0.777,
                'tag': request.args['tag']
            }
        }


@register('params', 'predict', 'clamping')
class ClampingPayloadPredictionParameters(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": {
                'beginYear': 2021,
                'endYear': 2022,
                'season': 3,
                'maxPayload': 2013,
                'dailyAmount': 155,
                'tag': request.args['tag']
            }
        }


@register('params', 'predict', 'interp')
class InterpolatingPayloadPredictionParameters(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": {
                'beginYear': 2012,
                'endYear': 2022,
                'season': 3,
                'maxPayload': 14444,
                'dailyAmount': 28888,
                'tag': request.args['tag']
            }
        }


@register('params', 'predict', 'yearcont')
class YearlyContinuousPayloadPredictionParameters(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": {
                'beginYear': 2023,
                'endYear': 2033,
                'maxPayload': 98768,
                'tag': request.args['tag']
            }
        }

@register('predict', 'history', 'query')
class HistoryPredictionQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": [
                {
                    'id': get_uuid(),
                    'type': '电力预测',
                    'time': '2020 年 %d 月 %d 日 %02d:%02d:%02d' % (i, i, i, i, i),
                    'amount': 10
                } for i in range(1, 13)
            ]
        }

@register('predict', 'history', 'detail')
class HistoryPredictionDetail(Resource):
    def get(self):
        try_print_args()
        return {
            "msg": "success",
            "code": 200,
            "data": {
                'type': '电力预测',
                'time': '2020 年 4 月 20 日 14:07:33',
                'dimension': 2,
                'amount': 42,
                'data': [
                    {
                        'x': 42,
                        'y': 84,
                        'y2nd': 88
                    } for _ in range(20)
                ]
            }
        }

"""
fore-end related http apis
END
"""

api.add_resource(UploadCSV, "/api/upload")
api.add_resource(GetDataJson, '/getDataJson')
api.add_resource(TestAlgorithm, "/interface")
api.add_resource(Compute, "/api/compute")
api.add_resource(Clamp_force, "/api/clampforce")
api.add_resource(Search, "/api/search")
api.add_resource(Fractal, "/api/fractal")

api.add_resource(SARIMA_Industry, "/api/SARIMA_Industry")
api.add_resource(EEMD__Industry, "/api/EEMD__Industry")
api.add_resource(PCA__Industry, "/api/PCA__Industry")
api.add_resource(RandomForest_Industry, "/api/RandomForest_Industry")
api.add_resource(ANN__Industry, "/api/ANN__Industry")
api.add_resource(Combination_Industry, "/api/Combination_Industry")
api.add_resource(StepwiseRegression, "/api/StepwiseRegression")
api.add_resource(GM, "/api/GM")
api.add_resource(FGM, "/api/FGM")
api.add_resource(GPRM, "/api/GPRM")
api.add_resource(GMR, "/api/GMR")
api.add_resource(FLR, "/api/FLR")
api.add_resource(FER, "/api/FER")
api.add_resource(Combination, "/api/Combination")
api.add_resource(GBDT, "/api/GBDT")
api.add_resource(SVM, "/api/SVM")
api.add_resource(RNN, "/api/RNN")
api.add_resource(LSTM, "/api/LSTM")
api.add_resource(Esqrm, "/api/Esqrm")
api.add_resource(QuantileRegression, "/api/QuantileRegression")
api.add_resource(MultiIndustryDailyProfile, "/api/MultiIndustryDailyProfile")
api.add_resource(MaxUtilizationHourR, "/api/MaxUtilizationHourR")
api.add_resource(SARIMA, "/api/SARIMA")
api.add_resource(LFconsideringTempHoliday, "/api/LFconsideringTempHoliday")

api.add_resource(Unarylinear, "/api/Unarylinear")
api.add_resource(Squarereg, "/api/Squarereg")
api.add_resource(Power, "/api/Power")
api.add_resource(Growth, "/api/Growth")
api.add_resource(Exponent, "/api/Exponent")
api.add_resource(Logarithm, "/api/Logarithm")
api.add_resource(Binarylinear, "/api/Binarylinear")
api.add_resource(Kmeans, "/api/Kmeans")
api.add_resource(PCA, "/api/PCA")
api.add_resource(AssociationRule, "/api/AssociationRule")
api.add_resource(GetProgramName, "/api/getProgramName")
api.add_resource(GetProgramLastInfo, "/api/getProgramLastInfo")

if __name__ == '__main__':
    app.run()
