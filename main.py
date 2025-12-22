import requests
import pandas as pd
from openpyxl import load_workbook
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from google import genai

url_proyectos_colombia  = "https://www.camara.gov.co/proyectos-de-ley/#menu"

php_url = "https://www.camara.gov.co/wp-admin/admin-ajax.php"
php_payload = {
    'action': 'download_proyectos_ley_xlsx',
    '_ajax_nonce': '376dd2bad5',
    'tipo': 'All',
    'estado': 'All',
    'origen': 'All',
    'legislatura': 'All',
    'comision_adv': 'All'
}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

DATABASE_URL = "postgresql://admin:Pass123@localhost:5432/legislacion_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
metadata = MetaData()

'''
response = requests.post(php_url, data=php_payload, headers=headers)
if response.status_code == 200:
    with open('proyectos_de_ley_colombia.xlsx', 'wb') as f:
        f.write(response.content)
    print("Archivo descargado exitosamente.")
'''

wb = load_workbook('proyectos_de_ley_colombia.xlsx').active
df = pd.read_excel('proyectos_de_ley_colombia.xlsx')

df['Fecha Cámara'] = pd.to_datetime(df['Fecha Cámara'], errors='coerce')

links = []

for cell in wb['P'][1:]:

    if cell.hyperlink:
        links.append(cell.hyperlink.target)
    else:
        links.append(None)
df['Link'] = links if len(links) == len(df) else None
print(df.head())

class ProyectoLey(Base):
    __tablename__ = 'proyectos_ley'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String)
    fecha_radicacion = Column(DateTime)
    resumen = Column(Text)
    enlace = Column(String)
    estado = Column(String)
    pais = Column(String)
    sector_economico = Column(String)

Base.metadata.create_all(engine)

for index, row in df.iterrows():
    titulo = row['Título'] if not pd.isna(row['Título']) else None
    fecha_radicacion = row['Fecha Cámara'] if not pd.isna(row['Fecha Cámara']) else None
    resumen = row['Objeto del proyecto'] if not pd.isna(row['Objeto del proyecto']) else None
    estado = row['Estado de Ley'] if not pd.isna(row['Estado de Ley']) else None

    proyecto = ProyectoLey(
        titulo=titulo,
        fecha_radicacion=fecha_radicacion,
        resumen=resumen,
        enlace=row['Link'],
        estado=estado,
        pais='Colombia',
        sector_economico='N/A'
    )
    session.add(proyecto)
try:
    session.commit()
    print("✅ Datos insertados exitosamente.")
except Exception as e:
    session.rollback()
    print(f"❌ Error al guardar en BD: {e}")
finally:
    session.close()