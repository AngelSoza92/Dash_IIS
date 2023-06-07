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
from clu100 import appc100
from pkt100 import appkt100
from tracking100 import apptra100
from stock100 import appst100
from samedaytodes import appsdt
from traspasos100 import apptr100
from antiguedad100 import appa100
from clu150 import appc150
from antiguedad150 import appa150
from pkt150 import appkt150
from antiguedad12 import appa12
from clu12 import appc12
from pkt12 import appkt12
from stock12 import appst12
from despachoswhse import despachito
from ultimamilla import applm
from params import apppa

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
    '/capacidades':appcapa.server,
    '/asdf':appc100.server,
    '/pkt100':appkt100.server,
    '/tracking100':apptra100.server,
    '/stock100':appst100.server,
    '/samedaytodes':appsdt.server,
    '/traspasos100':apptr100.server,
    '/antiguedad100':appa100.server,
    '/clu150':appc150.server,
    '/antiguedad150':appa150.server,
    '/pkt150':appkt150.server,
    '/antiguedad12':appa12.server,
    '/clu12':appc12.server,
    '/pkt12': appkt12.server,
    '/stock12':appst12.server,
    '/despachosbodegas':despachito.server,
    '/ultimamilla':applm.server,
    '/params':apppa.server
})

