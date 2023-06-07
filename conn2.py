import pyodbc as db
import pandas as pd

direccion_servidor="10.107.226.241\Reportes"
nombre_bd="150"
nombre_usuario="Angel"
password="Finvarra_92"


argumento= 'DRIVER={SQL Server}; SEVER='+direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD='+password

conexion =db.connect(driver='{SQL Server}', host=direccion_servidor, database=nombre_bd,user=nombre_usuario,password=password)



def get_df2():
    return pd.read_sql_query("SELECT * FROM WMS_STOCK_RESERVA_B150", conexion)

def get_df3():
    return pd.read_sql_query("SELECT * FROM TRASPASOS_100", conexion)

def get_df5():
    return pd.read_sql_query("SELECT * from WMS_REPORTE_PKT_150", conexion)

def get_df6():
    return pd.read_sql_query("SELECT * FROM WMS_STOCK_B150_V01",conexion)

def get_df7():
    return pd.read_sql_query("SELECT * from WMS_REPORTE_DE_JAULA_B150", conexion)