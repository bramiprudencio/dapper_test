import requests

url_proyectos_colombia  = "https://www.camara.gov.co/proyectos-de-ley/#menu"
url_proyectos_peru = "https://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2011.nsf/Local%20Por%20Numero%20Inverso?OpenView"

req = requests.get(url_proyectos_colombia)
if req.status_code == 200:
    with open("proyectos_colombia.html", "w", encoding="utf-8") as file:
        file.write(req.text)
    print("Archivo de proyectos de Colombia guardado correctamente.")
else:
    print(f"Error al acceder a la página de proyectos de Colombia: {req.status_code}")