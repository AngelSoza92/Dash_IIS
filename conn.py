import pyodbc as db
import pandas as pd

direccion_servidor="10.107.226.241\Reportes"
nombre_bd="100"
nombre_usuario="Angel"
password="Finvarra_92"


argumento= 'DRIVER={SQL Server}; SEVER='+direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD='+password
print(argumento)
#conexion = db.connect(argumento)
conexion =db.connect(driver='{SQL Server}', host=direccion_servidor, database=nombre_bd,user=nombre_usuario,password=password)
#print('okey mackey')
df = pd.read_sql_query("SELECT * from CCT_LITE", conexion)