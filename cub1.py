from cubiscan.cubiscan import CubiScan
import os
import json
from flask import Flask,jsonify

appcu1 = Flask(__name__)

obj = CubiScan('10.107.230.87', '1050', timeout=50)
a= obj.measure()

@appcu1.route("/cub1")
def cubiscan_1():
    return jsonify(a)

if  __name__=='__main__':
    appcu1.run(debug=True, port=4050)