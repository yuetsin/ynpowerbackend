import sqlalchemy
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api

from Controller import uploadData
from Controller.login import login
from Controller.program import *
from algorithms import *
import dao
import json
import numpy as np

app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)

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
class Login(Resource):
    def post(self):
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

class Logout(Resource):
    def post(self):
        return {
            "msg": "success",
            "code": 200
        }


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

class GetMetadata(Resource):
    def get(self):
        category_name = request.args['Category'].strip()
        print(category_name)
        return {
            "msg": "success",
            "code": 200,
            "data": [
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
        }

class PerformQuery(Resource):
    def get(self):
        metadata_list = request.args['Metadata']
        category_name = request.args['Category']
        print(metadata_list, category_name)
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

class PerformCreate(Resource):
    def post(self):
        print(request.json)
        return {
            "msg": "success",
            "code": 200
        }

class PerformUpdate(Resource):
    def post(self):
        print(request.json)
        return {
            "msg": "success",
            "code": 200
        }

class PerformDelete(Resource):
    def post(self):
        print(request.json)
        return {
            "msg": "success",
            "code": 200
        }

class DataTypeQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": ['int', 'float', 'string', 'char']
        }

class ExceptionQuery(Resource):
    def get(self):
        print(request.args)
        return {
            "msg": "success",
            "code": 200,
            "data": [
                {
                    "key": "2021-1-8",
                    "type": "int",
                    "value": 10,
                    "suggest": 42
                },
                {
                    "key": "2021-1-7",
                    "type": "string",
                    "value": "杨咏曼",
                    "suggest": "蔡翠菊"
                },
                {
                    "key": "2021-1-5",
                    "type": "float",
                    "value": 3.141592653589,
                    "suggest": 2.718281828
                },
                {
                    "key": "2021-1-3",
                    "type": "bool",
                    "value": True,
                    "suggest": False
                }
            ]
        }

class ExceptionResolve(Resource):
    def post(self):
        print(request.json)
        return {
            "msg": "success",
            "code": 200
        }

class ExceptionAccept(Resource):
    def post(self):
        print(request.json)
        return {
            "msg": "success",
            "code": 200
        }

_versions = ['v1.0', 'v1.1', 'v1.2', 'v2.0', 'v2.1a', 'v2.1b']

class SchemaQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": sorted(_versions)
        }

class SchemaCreate(Resource):
    def post(self):
        print(request.json)
        new_name = request.json['NewSchemaName'].strip()
        if new_name in _versions:
            return {
            "msg": "key existed",
            "code": -1
        }
        _versions.append(new_name)
        return {
            "msg": "success",
            "code": 200
        }

class SchemaRename(Resource):
    def post(self):
        print(request.json)
        current_name = request.json['CurrentSchema'].strip()
        new_name = request.json['NewSchemaName'].strip()
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


class SchemaDelete(Resource):
    def post(self):
        print(request.json)
        current_name = request.json['DeleteSchema'].strip()
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

_regions = ['云南省', '丽江市', '红河州', '内比都']

class RegionQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": _regions
        }

_factors = ['GDP', 'GNP', 'GPPPP', 'GNPPP']

class MiningFactorQuery(Resource):
    def get(self):
        return {
            "msg": "success",
            "code": 200,
            "data": _factors
        }

class MiningRequest(Resource):
    def post(self):
        print(request.json)
        return {
            "msg": "success",
            "code": 200
        }

class MiningKMeansSuggestCategoryCount(Resource):
    def get(self):
        print(request.args)
        return {
            "msg": "success",
            "code": 200,
            "data": {
                "Count": 2
            }
        }

# Account Stuff
api.add_resource(Login, "/api/login")
api.add_resource(Logout, "/api/logout")
api.add_resource(LoadRecent, '/api/recent')

# Database Stuff
api.add_resource(GetMetadata, '/api/db/metadata')
api.add_resource(PerformQuery, '/api/db/query')
api.add_resource(PerformCreate, '/api/db/create')
api.add_resource(PerformUpdate, '/api/db/update')
api.add_resource(PerformDelete, '/api/db/delete')

# Exception Correcting Stuff
api.add_resource(DataTypeQuery, '/api/db/dtypes')
api.add_resource(ExceptionQuery, '/api/db/except/query')
api.add_resource(ExceptionResolve, '/api/db/except/resolve')
api.add_resource(ExceptionAccept, '/api/db/except/accept')

# Schema Stuff
api.add_resource(SchemaQuery, '/api/schema/query')
api.add_resource(SchemaCreate, '/api/schema/create')
api.add_resource(SchemaRename, '/api/schema/rename')
api.add_resource(SchemaDelete, '/api/schema/delete')

# Data Mining Stuff
api.add_resource(MiningRequest, '/api/mining/request')
api.add_resource(MiningFactorQuery, '/api/mining/factor/query')
api.add_resource(MiningKMeansSuggestCategoryCount, '/api/mining/factor/kmeans/suggest')

# Shared Stuff
api.add_resource(RegionQuery, '/api/region/query')

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
