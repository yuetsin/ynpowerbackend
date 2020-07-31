from flask import Flask, request
from flask_restful import Resource, Api
from Controller import uploadData
from algorithms import *
from dao import *
import numpy as np

app = Flask(__name__)
api = Api(app)


class UploadCSV(Resource):
    def post(self):
        file = request.files['file']
        l = file.filename.split('_')
        area = l[0]
        grain = l[1]

        datatype = {'Year': 'S'}
        data = pd.read_csv(file, dtype=datatype)
        header = [i for i in data.columns]
        x, y = data.shape
        allData = []
        for i in range(x):
            t = data.iloc[i][0].strip()
            for j in range(1, y):
                temp = [t, header[j], data.iloc[i][j], grain, area]
                allData.append(temp)

        allData = pd.DataFrame(allData)
        allData.columns = ['datatime', 'dataname', 'datavalue', 'grain', 'area']
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
        re = getData(dataName, startTime, endTime, grain, area)
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


class ESQRM(Resource):
    def post(self):
        PreLoad = request.json['PreLoad'].strip()
        MAPE = request.json['MAPE'].strip()
        RMSE = request.json['RMSE'].strip()

        re = ""
        return re


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


api.add_resource(UploadCSV, "/api/upload")
api.add_resource(GetDataJson, '/getDataJson')
api.add_resource(TestAlgorithm, "/interface.py")
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
api.add_resource(ESQRM, "/api/ESQRM")
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




if __name__ == '__main__':
    app.run()
