from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from pprint import pprint, pformat
import os
from Controller import *

# _dir = './apis'
# if not os.path.exists(_dir):
#     os.makedirs(_dir)

app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)
filename = os.path.join(app.root_path, 'algorithms', 'args.xlsx')

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



class UploadCSV(Resource):
    def post(self):
        file = request.files['file']
        print(file.filename.split('.')[0])
        l = file.filename.split('.')[0].split('_')
        area = l[0]
        grain = l[1]
        kind = l[2]

        datatype = {'Year': 'S', 'year': 'S','datetime':'S', 'DT':'S'}
        data = pd.read_csv(file, encoding='utf-8', dtype=datatype)
        # print(data)
        uploadData(data, area, grain, kind)
        re = {
            "message": 'success'
        }
        return re

class insertAlgorithmResult(Resource):
    def post(self):
        content = request.json['result']
        tag = request.json['tag']
        print(content)
        re = insertAlgorithmReusltController(content, tag)
        re = {
            "message": 'success'
        }
        return re
class getAlgorithmResult(Resource):
    def post(self):
        tags = request.json['tags'].strip()
        results = getAlgorithmReusltController(tags)
        re = {
            "results": results
        }
        return json.dumps(re)

class GetDataJson(Resource):
    def post(self):
        dataName = request.json['dataName']
        startTime = request.json['startTime'].strip()
        endTime = request.json['endTime'].strip()
        grain = request.json['grain'].strip()
        area = request.json['area'].strip()
        kind = request.json['kind'].strip()
        re = getDatas(area + "_" + grain + "_" + kind, dataName, startTime, endTime)

        # re = dao.getDataTest(area + "_" + grain + "_" + kind, dataName, startTime, endTime)
        return re

    def get(self):
        dataName = request.args.get('dataName')
        startTime = request.args.get('startTime')
        endTime = request.args.get('endTime')
        location = request.args.get('location')
        data = getDatas(location, dataName, startTime, endTime)
        re = {
            "data": data,
            "status": '200'
        }
        return re

class TestAlgorithm(Resource):
    def post(self):
        return ""

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
            if login(username, password):
                re = {
                    "msg": "success",
                    "code": 200
                }
            else:
                re = {
                    "msg": "fail",
                    "code": -1
                }
            return re
        except RuntimeError:
            return {
                    "msg": "fail",
                    "code": -1
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

# 简化起见，value 就是 label，label 就是 value，不作区分。N16_15


#  N14_30
#  N21_15
_metadata = [
                {
                    "value": "电力电量类-测试1",
                    "label": "电力电量类-测试1",
                    "children": [
                        {
                            "value": "N16_15",
                            "label": "N16_15",
                        },
                        {
                            "value": "N14_30",
                            "label": "N14_30",
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
        startTime = request.json['beginYear']
        endTime = request.json['endYear']
        grain = request.json['grain'].strip()
        area = request.json['region'].strip()
        category = request.json['category']
        data = getDataByCondition(grain = grain, startTime = str(startTime), endTime = str(endTime), kind = category[0], dataName = category[1], area = area)
        datalist = []
        if data is not None:
            for d in data:
                temp = {}
                temp["key"] = d[0]
                temp["category"] = [d[5], d[1]]
                temp['region'] = d[4]
                temp['grain'] = d[3]
                temp['value'] = d[2]
                datalist.append(temp)
        re = {
            "msg": "success",
            "code": 200,
            "data":datalist
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": [
        #         {
        #             "key": "2021-1-8",
        #             "value": "陈瑞球"
        #         },
        #         {
        #             "key": "2021-1-7",
        #             "value": "杨咏曼"
        #         },
        #         {
        #             "key": "2021-1-5",
        #             "value": "蔡翠菊"
        #         },
        #         {
        #             "key": "2021-1-3",
        #             "value": "包玉刚"
        #         }
        #     ]
        # }

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
        # try_print_json()
        originData = request.json['originData']
        modifiedData = request.json['modifiedData']
        re = modifyDataByCondition(modifiedData['value'], grain=originData['grain'], startTime=originData['key'],
                                   endTime=originData['key'], kind=originData['category'][0],
                                   dataName=originData['category'][1], area=originData['region'])

        return re


@register('db', 'delete')
class PerformDelete(Resource):
    def post(self):
        # try_print_json()
        originData = request.json['originData']
        re = deleteDataByCondition(grain=originData['grain'], startTime=originData['key'],
                                   endTime=originData['key'], kind=originData['category'][0], dataName=originData['category'][1], area=originData['region'])

        return re
        #         {
        #     "msg": "success",
        #     "code": 200
        # }



@register('db', 'except', 'query')
class ExceptionQuery(Resource):
    def post(self):
        # try_print_json()
        category = request.json['category']
        startTime = request.json['beginYear']
        endTime = request.json['endYear']
        grain = request.json['grain'].strip()
        area = request.json['region'].strip()
        result = exceptQuery(category, str(startTime), str(endTime), grain, area)
        re = {
            "msg": "success",
            "code": 200,
            "data": result
        }
        return re

    # {
    #     "key": "2021-1-8",
    #     "category": ['三', '1', 'iv'],
    #     "grain": "天",
    #     "value": 10,
    #     "suggest": 42
    # },
    # {
    #     "key": "2021-1-7",
    #     "category": ['三', '1', 'i'],
    #     "grain": "年",
    #     "value": "杨咏曼",
    #     "suggest": "蔡翠菊"
    # },
    # {
    #     "key": "2021-1-5",
    #     "category": ['三', '2', 'iii'],
    #     "grain": "秒",
    #     "value": 3.141592653589,
    #     "suggest": 2.718281828
    # },
    # {
    #     "key": "2021-1-3",
    #     "category": ['四', '2', 'ii'],
    #     "grain": "年",
    #     "value": True,
    #     "suggest": False
    # }

@register('db', 'except', 'resolve')
class ExceptionResolve(Resource):

    def post(self):
        # try_print_json()
        originData = request.json['originData']
        modifiedData = request.json['modifiedData']
        result = exceptResolve(originData, modifiedData)
        return result

@register('db', 'except', 'accept')
class ExceptionAccept(Resource):
    def post(self):
        # try_print_json()
        acceptData = request.json['acceptData']
        result = exceptAccept(acceptData)
        return result

_versions = ['v1.0', 'v1.1', 'v1.2', 'v2.0', 'v2.1a', 'v2.1b']

_categories = ['MINING', 'STATIC_REGIONAL', 'DYNAMIC_INDUSTRIAL', 'MIX', 'LONGTERM', 'BIGUSER', 'SOKU', 'CLAMP', 'INTERP', 'YEARCONT']
_categories_count = len(_categories)

@register('tags', 'query')
class TagsQuery(Resource):
    def get(self):
        try:
            tagType = request.args['tagType']
            result = tagsQuery(tagType)
        except:
            result = tagsQuery()
        re = {
            "msg": "success",
            "code": 200,
            "data": result
        }
        return re

        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": [
        # #         {
        #             'id': tag,
        #             'tagType': _categories[randint(0, _categories_count - 1)]
        #         } for tag in sorted(_versions)
        #     ]
        # }

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
        # try_print_json()
        try:
            current_name = request.json['tag'].strip()
            new_name = request.json['newTag'].strip()
            re = tagsRename(current_name, new_name)
            return re
        except RuntimeError:
            return {
                "msg": "fail",
                "code": -1
            }


@register('tags', 'delete')
class TagsDelete(Resource):
    def post(self):
        # try_print_json()
        try:
            current_name = request.json['tag'].strip()
            re = tagDelete(current_name)
            return re
        except RuntimeError:
            return {
                "msg": "fail",
                "code": -1,
            }


@register('mining', 'request')
class MiningRequest(Resource):
    def post(self):
        # try_print_json()
        args = request.json
        tag = request.json['tag']
        # tagType: 'MINING'
        tagType = request.json['tagType']
        region = request.json['region']
        # factors: list[str]
        factors = request.json['factors']
        # method: str  # Pearson / KMeans / PCA / ARL
        method = request.json['method']
        beginYear = request.json['beginYear']
        endYear = request.json['endYear']
        if method == "Pearson":
           pearson = request.json['pearson']
           re = miningRequest(tag, tagType, region, factors, method, pearson, beginYear, endYear, args)

        elif method == "KMeans":
            kMeans = request.json['kMeans']
            re = miningRequest(tag, tagType, region, factors, method, kMeans, beginYear, endYear, args)

        elif method == "PCA":
            PCA = request.json['PCA']
            re = miningRequest(tag, tagType, region, factors, method, PCA, beginYear, endYear, args)

        elif method == "ARL":
            ARL = request.json['ARL']
            re = miningRequest(tag, tagType, region, factors, method, ARL, beginYear, endYear, args)

        return {
            "msg": "success",
            "code": 200,
            "data": ['阳光', '空气', '水']
        }

@register('mining', 'factor', 'kmeans', 'suggest')
class MiningKMeansSuggestCategoryCount(Resource):
    def get(self):
        try_print_args()
        factors = request.args['factors']
        factorslist = factors.split(",")
        re = {
            "msg": "success",
            "code": 200,
            "data": {
                "count": len(factorslist)
            }
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": {
        #         "count": 2
        #     }
        # }

@register('mining', 'results')
class MiningResults(Resource):
    def get(self):

        # tagType = request.args["tagType"]
        result = miningResults("MINING")
        re = {
            "msg": "success",
            "code":200,
            "data": result
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": [
        #         {
        #             'plan': '某个挖掘计划',
        #             'results': ['阳光', '空气', '水']
        #         },
        #         {
        #             'plan': '另一个挖掘计划',
        #             'results': ['光风', '霁月']
        #         },
        #         {
        #             'plan': '最后一个挖掘计划',
        #             'results': ['阴雨', '晦冥']
        #         },
        #     ]
        # }


_regions = ['仰光', '丽江市', '红河州', '内比都']

@register('region', 'query')
class RegionQuery(Resource):
    def get(self):
        region = regionQueryCon()
        re = {
            "msg": "success",
            "code": 200,
            "data": region
        }
        return re



_industries = ['工业', '农业', '医疗业', '餐饮业']

@register('industry', 'query')
class IndustryQuery(Resource):
    def get(self):
        re = industryQuery()
        # re = {
        #     "msg": "success",
        #     "code": 200,
        #     "data": industry
        # }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": _industries
        # }

_industrial_methods = ['基于ARIMA季节分解的行业电量预测', '基于EEMD的行业用电量预测', '基于主成分因子的行业用电量预测', '基于随机森林的行业用电量预测', '基于神经网络的行业用电量预测']

@register('method', 'industry', 'query')
class IndustrialMethodQuery(Resource):
    def get(self):
        filename = os.path.join(app.root_path, 'algorithms', 'args.xlsx')
        a, b = getAlgorithmName(filename)
        return {
            "msg": "success",
            "code": 200,
            "data": a
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
        filename = os.path.join(app.root_path, 'algorithms', 'args.xlsx')
        a, b = getAlgorithmName(filename)
        return {
            "msg": "success",
            "code": 200,
            "data": a
        }

@register('grain', 'query')
class GrainQuery(Resource):
    def get(self):
        re = grainQuery()
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": ['年', '月', '日', '时', '分', '秒']
        # }

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
        # try_print_json()
        re = regionSinglePredict(request.json)

        
        # payload = {
        #     'graphData': [
        #         {
        #             'xName': str(i),
        #             'yValue': randint(0, 1000)
        #         } for i in range(1, 18)
        #     ],
        #     'tableOneData': [
        #         {
        #             'index': '评价指标 %d' % i,
        #             'r2': random(),
        #             'mape': random(),
        #             'rmse': random()
        #         } for i in range(1, 18)
        #     ],
        #     'tableTwoData': [
        #         {
        #             'year': i + 2010,
        #             'predict': random() * randint(300, 500)
        #         } for i in range(17)
        #     ]
        # }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('predict', 'region', 'mix', 'validate')
class RegionMixModelValidate(Resource):
    def post(self):
        # try_print_json()
        methods = request.json['methods']
        re = regionMixModelValidate(methods)
        # ok = (randint(0, 1) == 0)
        return {
            "msg": "success",
            "code": 200,
            "data": {
                "ok": re
            }
        }


@register('predict', 'region', 'mix')
class RegionMixPredict(Resource):
    def post(self):
        # try_print_json()
        re = regionMixPredict(request.json)

        # payload = {
        #     'graphData': [
        #         {
        #             'xName': str(i),
        #             'yValue': randint(0, 1000)
        #         } for i in range(1, 18)
        #     ],
        #     'tableOneData': [
        #         {
        #             'index': '评价指标 %d' % i,
        #             'r2': random(),
        #             'mape': random(),
        #             'rmse': random()
        #         } for i in range(1, 18)
        #     ],
        #     'tableTwoData': [
        #         {
        #             'year': i + 2010,
        #             'predict': random() * randint(300, 500)
        #         } for i in range(17)
        #     ]
        # }
        return re

        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('predict', 'industry', 'single')
class IndustrySinglePredict(Resource):
    def post(self):
        # try_print_json()
        re = industrySinglePredict(request.json)



        # payload = {
        #     'graphData': [
        #         {
        #             'xName': str(i),
        #             'yValue': randint(0, 1000)
        #         } for i in range(1, 18)
        #     ],
        #     'tableOneData': [
        #         {
        #             'index': '评价指标 %d' % i,
        #             'r2': random(),
        #             'mape': random(),
        #             'rmse': random()
        #         } for i in range(1, 18)
        #     ],
        #     'tableTwoData': [
        #         {
        #             'year': i + 2010,
        #             'predict': random() * randint(300, 500)
        #         } for i in range(17)
        #     ]
        # }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('predict', 'industry', 'mix', 'validate')
class IndustryMixModelValidate(Resource):
    def post(self):
        # try_print_json()
        methods = request.json['methods']
        re = industryMixModelValidate(methods)
        # ok = (randint(0, 1) == 0)
        return {
            "msg": "success",
            "code": 200,
            "data": {
                "ok": re
            }
        }


@register('predict', 'industry', 'mix')
class IndustryMixPredict(Resource):
    def post(self):
        # try_print_json()
        re = industryMixPredict(request.json)

        # payload = {
        #     'graphData': [
        #         {
        #             'xName': str(i),
        #             'yValue': randint(0, 1000)
        #         } for i in range(1, 18)
        #     ],
        #     'tableOneData': [
        #         {
        #             'index': '评价指标 %d' % i,
        #             'r2': random(),
        #             'mape': random(),
        #             'rmse': random()
        #         } for i in range(1, 18)
        #     ],
        #     'tableTwoData': [
        #         {
        #             'year': i + 2010,
        #             'predict': random() * randint(300, 500)
        #         } for i in range(17)
        #     ]
        # }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('predict', 'saturation')
class SaturationCurvePredict(Resource):
    def post(self):
        # try_print_json()
        result = saturationCurvePredict(request.json)
        re = {
            "msg": "success",
            "code": 200,
            "data": result
        }

        # payload = {
        #     'graphData': [
        #         {
        #             'xName': str(i),
        #             'yValue': randint(0, 1000)
        #         } for i in range(1, 18)
        #     ],
        #     'tableOneData': [
        #         {
        #             'index': '评价指标 %d' % i,
        #             'r2': random(),
        #             'mape': random(),
        #             'rmse': random()
        #         } for i in range(1, 18)
        #     ],
        #     'tableTwoData': [
        #         {
        #             'year': i + 2010,
        #             'predict': random() * randint(300, 500)
        #         } for i in range(17)
        #     ]
        # }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('predict', 'payload')
class PayloadDensityPredict(Resource):
    def post(self):
        # try_print_json()
        re = payloadDensityPredict(request.json)

        # payload = {
        #     'graphData': [
        #         {
        #             'xName': str(i),
        #             'yValue': randint(0, 1000)
        #         } for i in range(1, 18)
        #     ],
        #     'tableOneData': [
        #         {
        #             'index': '评价指标 %d' % i,
        #             'r2': random(),
        #             'mape': random(),
        #             'rmse': random()
        #         } for i in range(1, 18)
        #     ],
        #     'tableTwoData': [
        #         {
        #             'year': i + 2010,
        #             'predict': random() * randint(300, 500)
        #         } for i in range(17)
        #     ]
        # }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

_files = ['红河州.csv', '迪庆州.json', '仰光.txt', '...']

@register('predict', 'munidata', 'upload')
class MunicipalDataUpload(Resource):
    def post(self):
        try_print_files()

        _files.append(request.files.get('file').filename)
        return {
            "msg": "success",
            "code": 200
        }

@register('predict', 'munidata', 'files')
class MunicipalDataQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": _files
        }

@register('predict', 'provmuni')
class ProvincialAndMunicipalPredict(Resource):
    def post(self):
        # try_print_json()
        result = provincialAndMunicipalPredict(request.json)

        re = {
            "msg": "success",
            "code": 200,
            "data": result
        }
        # payload = {
        #     'tableThreeData': [
        #         {
        #             'year': i + 2010,
        #             'region': '某个地方',
        #             'predictValueBefore': random() * randint(300, 500),
        #             'predictErrorBefore': random() * randint(30, 50),
        #             'predictValueAfter': random() * randint(300, 500),
        #             'predictErrorAfter': random() * randint(20, 80)
        #         } for i in range(1, 18)
        #     ],
        #     'tableFourData': [
        #         {
        #             'year': i + 2010,
        #             'region': '地方 %d' % i,
        #             'predictBefore': random() * randint(300, 500),
        #             'predictAfter': random() * randint(300, 500),
        #         } for i in range(17)
        #     ]
        # }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }


#大用户预测
@register('predict', 'bigdata')
class BigDataPredict(Resource):
    def post(self):
        # try_print_json()
        result = bigDataPredict(request.json)
        re = {
            "msg": "success",
            "code": 200,
            "data": result
        }
        # payload = {
        #     'graphData': [
        #         {
        #             'xName': str(i),
        #             'yValue': randint(0, 1000)
        #         } for i in range(1, 18)
        #     ],
        #     'tableOneData': [
        #         {
        #             'index': '评价指标 %d' % i,
        #             'r2': random(),
        #             'mape': random(),
        #             'rmse': random()
        #         } for i in range(1, 18)
        #     ],
        #     'tableTwoData': [
        #         {
        #             'year': i + 2010,
        #             'predict': random() * randint(300, 500)
        #         } for i in range(17)
        #     ]
        # }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

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
        # try_print_args()
        result = dailyPayloadTraits(request.args)
        re = {
            "msg": "success",
            "code": 200,
            "data": result
        }
        # payload = [
        #         {
        #             'day': '2020 年 %d 月 %d 日' % (i, i * 2),
        #             'dayMaxPayload': randint(0, 1000),
        #             'dayAveragePayload': random() * 500,
        #             'dayPayloadRate': random() * 500,
        #             'dayMinPayloadRate': random() * 500,
        #             'dayPeekValleyDiff': random() * 500,
        #             'dayPeekValleyDiffRate': random() * 500
        #         } for i in range(1, 13)
        #     ]
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('payload', 'traits', 'monthly')
class MonthlyPayloadTraits(Resource):
    def get(self):
        # try_print_args()
        result = monthlyPayloadTraits(request.args)
        re = {
            "msg":"success",
            "code": 200,
            "data" : result
        }
        # payload = [
        #         {
        #             'month': '2020 年 %d 月' % i,
        #             'monthAverageDailyPayload': randint(0, 1000),
        #             'monthMaxPeekValleyDiff': random() * 500,
        #             'monthAverageDailyPayloadRate': random() * 500,
        #             'monthImbaRate': random() * 500,
        #             'monthMinPayloadRate': random() * 500,
        #             'monthMaxPeekValleyDiffRate': random() * 500
        #         } for i in range(1, 13)
        #     ]
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('payload', 'traits', 'yearly')
class YearlyPayloadTraits(Resource):
    def get(self):
        # try_print_args()
        result = yearlyPayloadTraits(request.args)

        re = {
            "msg": "success",
            "code": 200,
            "data": result
        }
        # payload = [
        #         {
        #             'year
        #             ': '%d 年' % (2010 + i),
        #             'yearMaxPayload': randint(10000, 1000000),
        #             'yearAverageDailyPayloadRate': random() * 500,
        #             'seasonImbaRate': random() * 500,
        #             'yearMaxPeekValleyDiff': random() * 500,
        #             'yearMaxPeekValleyDiffRate': random() * 500,
        #             'yearMaxPayloadUsageHours': 20
        #         } for i in range(1, 13)
        #     ]
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('payload', 'predict', 'dbquery')
class SokuPayloadPredict(Resource):
    def post(self):
        # try_print_json()
        result = sokuPayloadPredict(request.json)
        payload = {
            'xName': '小时',
            'xData': list(range(0, 24, 2)),
            'yName': '单位：MW',
            'yData': [
                {
                    'tag': '预测负荷',
                    'data': result["result"]
                }
            ]
        }
        re = {
            "msg": "success",
            "code": 200,
            "data": payload
        }
        # payload = [
        #         {
        #             'time': '%d:%d' % (randint(10, 20), randint(10, 50)),
        #             'actualPayload': randint(10000, 1000000),
        #             'predictPayload': randint(10000, 1000000)
        #         } for _ in range(1, 13)
        #     ]
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('payload', 'predict', 'clamping')
class ClampingPayloadPredict(Resource):
    def post(self):
        # try_print_json()
        result = clampingPayloadPredict(request.json)
        print(result)
        payload = {
            'xName': '小时',
            'xData': list(range(0, 24, 2)),
            'yName': '单位：MW',
            'yData': [
                {
                    'tag': '预测负荷',
                    'data': result["result"]
                }
            ]
        }
        re = {
            "msg": "success",
            "code": 200,
            "data": payload
        }


        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('payload', 'predict', 'interp')
class InterpolatingPayloadPredict(Resource):
    def post(self):
        # try_print_json()
        result = interpolatingPayloadPredict(request.json)
        payload = {
            'xName': "小时",
            'xData': list(range(0, 24, 2)),
            'yName': '单位：MW',
            'yData': [
                {
                    'tag': '预测负荷',
                    'data': result["result"]
                }
            ]
        }
        re = {
            "msg": "success",
            "code": 200,
            "data": payload
        }

        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('payload', 'predict', 'yearly')
class YearlyContinuousPayloadPredict(Resource):
    def post(self):
        # try_print_json()
        result = yearlyContinuousPayloadPredict(request.json)
        payload = {
            'xName': "时刻",
            'xData': list(range(0, 8760)),
            'yName': '单位：MW',
            'yData': [
                {
                    'tag': '预测负荷',
                    'data': result["result"]
                }
            ]
        }
        re = {
            "msg": "success",
            "code": 200,
            "data": payload
        }
        # payload = [
        #         {
        #             'time': '%d:%d' % (randint(10, 20), randint(10, 50)),
        #             'payload': randint(10000, 1000000)
        #         } for _ in range(1, 13)
        #     ]
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('params', 'mining')
class DataMiningParameters(Resource):
    def get(self):
        tag = request.args['tag']
        result = getAlgorithmContentByTag(tag)
        contentstr = result[0]["content"]
        content = json.loads(contentstr)
        arg = content["arg"]
        re = {
            "msg": "success",
            "code": 200,
            "data": arg
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": {
        #         "region": '地域',
        #         "factors": ['factor 1', 'factor 2', 'factor 3'],
        #         "method": '方法',
        #         "pearson": {
        #             "threshold": 0.77777
        #         },
        #         "kMeans": {
        #             "categoryCount": 2
        #         },
        #         "PCA": {
        #             "absThreshold": 0.77777
        #         },
        #         "ARL": {
        #             "minSupport": 0.11111,
        #             "minConfidence": 0.11111
        #         },
        #         "beginYear": 2024,
        #         "endYear": 2029,
        #         "tag": request.args['tag']
        #     }
        # }

@register('params', 'predict', 'static', 'region')
class StaticRegionalPredictionParameters(Resource):
    def get(self):
        tag = request.args['tag']
        result = getAlgorithmContentByTag(tag)
        contentstr = result[0]["content"]
        content = json.loads(contentstr)
        arg = content["arg"]
        re = {
            "msg": "success",
            "code": 200,
            "data": arg
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": {
        #         "historyBeginYear": 1999,
        #         "historyEndYear": 2009,
        #         'beginYear': 2023,
        #         'endYear': 2033,
        #         'region': '地域',
        #         'industry': '行业',
        #         'method': '方法',
        #         'factor1': {
        #             'name': 'MINGZI',
        #             'hasValue': True,
        #             'value': 0.1
        #         },
        #         'factor2': {
        #             'name': 'MINGZI2',
        #             'hasValue': True,
        #             'value': 0.9
        #         },
        #         'tag': request.args['tag']
        #     }
        # }

@register('params', 'predict', 'dynamic', 'industry')
class DynamicIndustrialPredictionParameters(Resource):
    def get(self):
        tag = request.args['tag']
        result = getAlgorithmContentByTag(tag)
        contentstr = result[0]["content"]
        content = json.loads(contentstr)
        arg = content["arg"]
        re = {
            "msg": "success",
            "code": 200,
            "data": arg
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": {
        #         'industry': '行业',
        #         'method': '方法',
        #         'parameters': ['paramA', 'paramB', '...'],
        #         'beginYear': 1995,
        #         'endYear': 2006,
        #         'historyBeginYear': 2012,
        #         'historyEndYear': 2055,
        #         'tag': request.args['tag']
        #     }
        # }

@register('params', 'predict', 'mix')
class MixPredictionParameters(Resource):
    def get(self):
        tag = request.args['tag']
        result = getAlgorithmContentByTag(tag)
        if result is not None:
            contentstr = result[0]["content"]
            content = json.loads(contentstr)
            arg = content["arg"]
        else:
            arg = None
        re = {
            "msg": "success",
            "code": 200,
            "data": arg
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": {
        #         'historyBeginYear': 2012,
        #         'historyEndYear': 2066,
        #         'beginYear': 2012,
        #         'endYear': 2022,
        #         'region': '地域',
        #         'industry': '工业',
        #         'selectedMethods': ['methodA', 'methodB', '...'],
        #         'tag': request.args['tag']
        #     }
        # }

@register('params', 'predict', 'dynamic', 'region')
class LongTermPredictionParameters(Resource):
    def get(self):
        tag = request.args['tag']
        result = getAlgorithmContentByTag(tag)
        contentstr = result[0]["content"]
        content = json.loads(contentstr)
        arg = content["arg"]
        re = {
            "msg": "success",
            "code": 200,
            "data": arg
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": {
        #         'region': '地域',
        #         'method': '行业',
        #         'parameters': ['1', '2', '...'],
        #         'beginYear': 1993,
        #         'endYear': 2013,
        #         'historyBeginYear': 2012,
        #         'historyEndYear': 2022,
        #         'tag': request.args['tag']
        #     }
        # }


@register('params', 'predict', 'biguser')
class BigUserPredictionParameters(Resource):
    def get(self):
        tag = request.args['tag']
        result = getAlgorithmContentByTag(tag)
        contentstr = result[0]["content"]
        content = json.loads(contentstr)
        arg = content["arg"]
        re = {
            "msg": "success",
            "code": 200,
            "data": arg
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": {
        #         'historyBeginYear': 1966,
        #         'historyEndYear': 1997,
        #         'beginYear': 1994,
        #         'endYear': 2004,
        #         'method': '测试方法',
        #         'region': '测试地域',
        #         'patches': [
        #             {
        #                 'metaData': ['a', 'b', 'c'],
        #                 'grain': '粒度（总是「年」）',
        #                 'year': '年份',
        #                 'value': '42',
        #             }, '...'
        #         ],
        #         'tag': request.args['tag']
        #     }
        # }

@register('params', 'predict', 'soku')
class SokuPayloadPredictionParameters(Resource):
    def get(self):
        tag = request.args['tag']
        result = getAlgorithmContentByTag(tag)
        contentstr = result[0]["content"]
        content = json.loads(contentstr)
        arg = content["arg"]
        re = {
            "msg": "success",
            "code": 200,
            "data": arg
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": {
        #         'beginYear': 1955,
        #         'endYear': 2055,
        #         'season': 3,
        #         'maxPayload': 2033,
        #         'dailyAmount': 1000,
        #         'gamma': 0.555,
        #         'beta': 0.777,
        #         'tag': request.args['tag']
        #     }
        # }


@register('params', 'predict', 'clamping')
class ClampingPayloadPredictionParameters(Resource):
    def get(self):
        tag = request.args['tag']
        result = getAlgorithmContentByTag(tag)
        contentstr = result[0]["content"]
        content = json.loads(contentstr)
        arg = content["arg"]
        re = {
            "msg": "success",
            "code": 200,
            "data": arg
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": {
        #         'beginYear': 2021,
        #         'endYear': 2022,
        #         'season': 3,
        #         'maxPayload': 2013,
        #         'dailyAmount': 155,
        #         'tag': request.args['tag']
        #     }
        # }


@register('params', 'predict', 'interp')
class InterpolatingPayloadPredictionParameters(Resource):
    def get(self):
        tag = request.args['tag']
        result = getAlgorithmContentByTag(tag)
        contentstr = result[0]["content"]
        content = json.loads(contentstr)
        arg = content["arg"]
        re = {
            "msg": "success",
            "code": 200,
            "data": arg
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": {
        #         'beginYear': 2012,
        #         'endYear': 2022,
        #         'season': 3,
        #         'maxPayload': 14444,
        #         'dailyAmount': 28888,
        #         'tag': request.args['tag']
        #     }
        # }


@register('params', 'predict', 'yearcont')
class YearlyContinuousPayloadPredictionParameters(Resource):
    def get(self):
        tag = request.args['tag']
        result = getAlgorithmContentByTag(tag)
        contentstr = result[0]["content"]
        content = json.loads(contentstr)
        arg = content["arg"]
        re = {
            "msg": "success",
            "code": 200,
            "data": arg
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": {
        #         'beginYear': 2023,
        #         'endYear': 2033,
        #         'maxPayload': 98768,
        #         'tag': request.args['tag']
        #     }
        # }

@register('predict', 'results', 'query')
class PredictionResultsQuery(Resource):
    def get(self):
        re = {
            "msg": "success",
            "code": 200,
            "data": []
        }
        re1 = getTagByKind("STATIC_REGIONAL")
        if re1 is not None:
            for t in re1:
                re["data"].append(t)
        re2 = getTagByKind("MIX")
        if re2 is not None:
            for t in re2:
                re["data"].append(t)
        re3 = getTagByKind("LONGTERM")
        if re3 is not None:
            for t in re3:
                re["data"].append(t)
        re4 = getTagByKind("BIGUSER")
        if re4 is not None:
            for t in re4:
                re["data"].append(t)
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": [
        #         {
        #             'id': tag,
        #             'tagType': _categories[randint(0, _categories_count - 1)]
        #         } for tag in sorted(_versions)
        #     ]
        # }

@register('predict', 'results', 'detail')
class PredictionResultDetail(Resource):
    def get(self):
        # try_print_args()
        tag = request.args['tag']
        result = getAlgorithmContentByTag(tag)
        contentstr = result[0]["content"]
        content = json.loads(contentstr)
        arg = content["arg"]
        re = {
            "msg": "success",
            "code": 200,
            "data": {
                "parameters": arg

            }
        }
        # payload = {
        #     'parameters': [
        #         {
        #             'key': '方案名称',
        #             'value': request.args['tag']
        #         },
        #         {
        #             'key': '预测类型',
        #             'value': '远期预测'
        #         },
        #         {
        #             'key': '预测年份',
        #             'value': '2015 到 2020'
        #         },
        #         {
        #             'key': '预测方法',
        #             'value': '猜测法'
        #         },
        #         {
        #             'key': '预测时间',
        #             'value': '2021 年 1 月 21 日 11:04:33'
        #         }
        #     ],
        #     'graphData': [
        #         {
        #             'xName': str(i),
        #             'yValue': randint(0, 1000)
        #         } for i in range(1, 18)
        #     ],
        #     'tableOneData': [
        #         {
        #             'index': '评价指标 %d' % i,
        #             'r2': random(),
        #             'mape': random(),
        #             'rmse': random()
        #         } for i in range(1, 18)
        #     ],
        #     'tableTwoData': [
        #         {
        #             'year': i + 2010,
        #             'predict': random() * randint(300, 500)
        #         } for i in range(17)
        #     ]
        # }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('predict', 'results', 'compare')
class PredictionResultComparison(Resource):
    def post(self):
        # try_print_json()
        tags = request.json['tags']
        trait = request.json['trait']
        result = getAlgorithmContentByTag(tags)
        re = {}
        re['msg'] = "success"
        re['code'] = 200
        re["data"] = result['content']
        re["data"]['tag'] = result['tag']
        # payload = [
        #     {
        #         'tag': tag,
        #         'data': [random() for _ in range(40)]
        #     } for tag in tags
        # ]
        return re
        #     {
        #     "msg": "success",
        #     "code": 200,
        #     "data": {
        #         'xName': '年份',
        #         'xData': ['%i 年' % (i + 2000) for i in range(40)],
        #         'yName': 'RMSE 值',
        #         'yData': payload
        #     }
        # }

@register('payload', 'charts', 'daily')
class PayloadChartsDaily(Resource):
    def get(self):
        # try_print_args()
        day = request.args['day']
        result = payloadChartsDaily(day)
        payload = {
            'xName': '小时',
            'xData': list(range(0, 24, 2)),
            'yName': '单位：MW',
            'yData': [
                {
                    'tag': '负荷',
                    'data': result
                }
            ]
        }
        re = {
            "msg": "success",
            "code": 200,
            "data": payload
        }
        # payload = {
        #     'metaData': [
        #         {
        #             'key': '日最大负载',
        #             'value': 42.4
        #         },
        #         {
        #             'key': '日平均负载',
        #             'value': 11.6
        #         },
        #         {
        #             'key': '日负载率',
        #             'value': '50.5%'
        #         },
        #         {
        #             'key': '日峰谷差',
        #             'value': 3000
        #         },
        #         {
        #             'key': '日峰谷差率',
        #             'value': '50%'
        #         }
        #     ],
        #     'xName': '小时',
        #     'xData': list(range(0, 24, 2)),
        #     'yName': '单位：MW',
        #     'yData': [
        #         {
        #             'tag': '原始负荷',
        #             'data': [random() for _ in range(12)]
        #         },
        #         {
        #             'tag': '预测负荷',
        #             'data': [random() for _ in range(12)]
        #         }
        #     ]
        # }
        return re


@register('payload', 'charts', 'daily', 'typical')
class PayloadChartsDailyTypical(Resource):
    def get(self):
        # try_print_args()
        year = request.args['year']
        period = request.args['period']  # 丰水期、汛前枯期、汛后枯期
        category = request.args['category'] # 最大负荷、最小负荷、中位负荷
        if period == "丰水期":
            periodnum = 1
        elif period == "汛前枯期":
            periodnum = 0
        else:
            periodnum = 2
        result = DailyTypicalOp(year,periodnum,category)
        payload = {
            'xName': '小时',
            'xData': list(range(0, 24, 2)),
            'yName': '单位：MW',
            'yData': [
                {
                    'tag': '典型负荷',
                    'data': result["re"]
                }
            ]
        }
        re = {
            "msg": "success",
            "code": 200,
            "data": payload
        }
        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('payload', 'charts', 'monthly')
class PayloadChartsMonthly(Resource):
    def get(self):
        # try_print_args()
        year = request.args['year']
        category = request.args['category']
        result = ChartMonthlyOp(year, category)
        payload = {
                'xName': '月份',
                'xData': list(range(1, 13)),
                'yName': '单位：MW',
                'yData': [
                    {
                        'tag': category,
                        'data': result
                    }
                ]
            }
        re = {
            "msg": "success",
            "code": 200,
            "data": payload
        }

        return re
        # {
        #     "msg": "success",
        #     "code": 200,
        #     "data": payload
        # }

@register('payload', 'charts', 'yearly')
class PayloadChartsYearly(Resource):
    def get(self):
        # try_print_args()
        result = payloadChartsYearly(request.args)

        payload = {
            # 'xName': '年份',
            # 'xData': list(range(2000, 2012)),
            'yName': '单位：MW',
            'yData': [
                {
                    'tag': '负荷',
                    'data': result
                }
            ]
        }
        re = {
            "msg": "success",
            "code": 200,
            "data": payload
        }
        return re


"""
fore-end related http apis
END
"""

class getAlgorithmArg(Resource):
    def get(self):
        method = request.args["method"]
        filename = os.path.join(app.root_path, 'algorithms', 'args.xlsx')

        args = getAlgorithmArgs(method= method, filename=filename)
        re = {
            "msg":"success",
            "code":200,
            "data":args
        }
        return re
class testExecuteAlgorithm(Resource):
    def post(self):
        method = request.json['method']
        result = executeAlgorithm(method, request.json)
        return result
class addData(Resource):
    def post(self):
        data = request.json['data']
        area = request.json['area']
        grain = request.json['grain']
        kind = request.json['kind']
        # print(data)
        data = pd.read_json(data, orient='split')
        # print(data)

        uploadData(data, area, grain, kind)
        re = {
            "msg": "success",
            "code":200
        }
        return re



api.add_resource(UploadCSV, "/api/upload")
api.add_resource(GetDataJson, '/getDataJson')
api.add_resource(TestAlgorithm, "/interface")
api.add_resource(insertAlgorithmResult, "/api/insert/result")
api.add_resource(getAlgorithmResult, "/api/get/result")
api.add_resource(getAlgorithmArg, "/api/get/args")
api.add_resource(testExecuteAlgorithm, "/api/test")

api.add_resource(addData, "/api/add/data")

if __name__ == '__main__':
    app.run()