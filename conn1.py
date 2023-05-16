import pyodbc as db
import pandas as pd
import urllib
from sqlalchemy import create_engine

direccion_servidor="10.107.226.241\Reportes"
nombre_bd="100"
nombre_usuario="Angel"
password="Finvarra_92"
driver = '{ODBC Driver 17 for SQL Server}'

argumento= 'DRIVER={SQL Server}; SEVER='+direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD='+password

conexion =db.connect(driver='{SQL Server}', host=direccion_servidor, database=nombre_bd,user=nombre_usuario,password=password)

# Creación del objeto de motor SQLAlchemy
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(urllib.parse.quote_plus('DRIVER={};SERVER={};DATABASE={};UID={};PWD={}'.format(driver, direccion_servidor, nombre_bd, nombre_usuario, password))))


def get_df():
    return pd.read_sql_query("SELECT * from IMBECIL_CURRENT_GUIAS_SD ", conexion)

def get_df2():
    return pd.read_sql_query("SELECT * FROM ANTIGUEDAD", conexion)

def get_df3():
    return pd.read_sql_query("SELECT * FROM TRASPASOS_100", conexion)

def get_df5():
    return pd.read_sql_query("SELECT * from PKT_100", conexion)

def get_df6():
    return pd.read_sql_query("SELECT * FROM STOCK100",conexion)

def get_df7():
    return pd.read_sql_query("SELECT * from CCT_LITE", conexion)

def capacidades():
    return pd.read_sql_query("SELECT ZONA,ORIGEN,DIRECTION,FORMAT(SHIP_DATE, 'MM/dd') as SHIP_DATE,JORNADA,DAY_NAME,CAP_TIPO,QTY ,CREATED_DTTM ,CREATED_SOURCE,LAST_MODIFIED_DTTM,LAST_MODIFIED_SOURCE,LANE_ID,TIPO,PARIS,MES ,DIA,UTILIZADO FROM KAPPA2 ORDER BY UTILIZADO DESC", conexion)