from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, jsonify
from app_2 import app2
from flask import Flask
from clu import appc
from sameday import appsd
from antiguedad import appa
from traspasos import apptr
from pkt import appkt
from stock import appst
from capacidades import appcapa

#unused base app
base_app = Flask(__name__)

app = DispatcherMiddleware(base_app, {
    '/app2':  app2.server,
    '/clu':appc.server,
    '/sameday':appsd.server,
    '/antiguedad':appa.server,
    '/traspasos':apptr.server,
    '/pkt':appkt.server,
    '/stock':appst.server,
    '/capacidades':appcapa.server
})

