import pyodbc as db
import pandas as pd

direccion_servidor="10.107.226.241\Reportes"
nombre_bd="M"
nombre_usuario="Angel"
password="Finvarra_92"


argumento= 'DRIVER={SQL Server}; SEVER='+direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD='+password

conexion =db.connect(driver='{SQL Server}', host=direccion_servidor, database=nombre_bd,user=nombre_usuario,password=password)



def get_df2():
    return pd.read_sql_query("SELECT * FROM WMS_STOCK_RESERVA", conexion)

def get_df5():
    return pd.read_sql_query("SELECT * from WMS_REPORTE_PKT_MHT", conexion)

def get_df6():
    return pd.read_sql_query("SELECT * FROM WMS_STOCK_MHT",conexion)

def get_df7():
    return pd.read_sql_query("SELECT * from WMS_REPORTE_DE_JAULA_MHT", conexion)

def capacidades():
    return pd.read_sql_query("SELECT * from CAPACIDADES ORDER BY UTILIZADO DESC ", conexion)

def get_df():
    return pd.read_sql_query("SELECT * from SAMEDAY", conexion)

def get_despachos():
    return pd.read_sql_query("SELECT * from DESPACHOS_BODEGAS", conexion)