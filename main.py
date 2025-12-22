import requests
import pandas as pd

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
'''
response = requests.post(php_url, data=php_payload, headers=headers)
if response.status_code == 200:
    with open('proyectos_de_ley_colombia.xlsx', 'wb') as f:
        f.write(response.content)
    print("Archivo descargado exitosamente.")
'''

proyectos_de_ley_colombia = pd.read_excel('proyectos_de_ley_colombia.xlsx')
print(proyectos_de_ley_colombia.head())