from flask import Flask, jsonify, request
from flask_restful import Api,Resource
from flask_cors import CORS
# from datetime import date,datetime

app = Flask(__name__)
api = Api(app)
# CORS(app)
# cors = CORS(app)




class simple(Resource):
    def funcx(self):
        return "Python Stocks API"

class datet(Resource):
    def get(self):
        with open('Stock_data.txt','r') as sfile:
            sfile.read()
            

       

        # return jsonify({"start_date":s_date,"end_date":e_date,"current_date":c_date,"dtime":dt})
        return "sdsd"

api.add_resource(datet,"/")
api.add_resource(simple,"/g")


if __name__ == "__main__":
    app.run(debug=True)


# Income and Expenses will be saved in server as json,csv,pdf at the end of the month
