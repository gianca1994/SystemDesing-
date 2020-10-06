import os
from dotenv import load_dotenv
from sqlalchemy import enginec
import pandas as gg

load_dotenv()

DataBase_Path = str(os.getenv("SQLALCHEMY_DB_PATH"))
DataBase_Name = str(os.getenv("SQLALCHEMY_DB_NAME"))
DataBase_Url = "sqlite:////" + DataBase_Path + DataBase_Name

def seisms_get(json):

        longitude = json['longitude']
        latitude = json['latitude']
        engine = enginec(DataBase_Url)

        data = gg.read_sql_table(table_name='seism', con=engine)
        data.drop(columns=["magnitude", "datetime", "depth", "id", "verify"], inplace=True)

        data['longitude'] = round(data['longitude'].astype(float), 3)
        data['latitude'] = round(data['latitude'].astype(float), 3)

        data = data[data['longitude'].ge(longitude - 1)]
        data = data[data['longitude'].ge(longitude - 1)]

        data = data[data['latitude'].ge(latitude - 1)]
        data = data[data['latitude'].le(latitude + 1)]

        data.drop(columns=["longitude", "latitude"], inplace=True)

    return data['id_num'].to_list()