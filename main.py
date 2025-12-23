import schedule
import time
import os
from src.database.connection import init_db, get_db
from src.database.models import ProyectoLey
from src.scrapers.colombia import ColombiaScraper
from src.services.ai_service import ClasificadorIA # <--- IMPORTAR

def procesar_pendientes_con_ai(session):
    """Busca proyectos sin categoría y usa Gemini para clasificarlos"""
    print("🤖 Iniciando clasificación con IA...")
    
    # 1. Buscar filas donde sector_economico sea 'Pendiente AI'
    # Limitamos a 20 por ejecución para no gastar toda la cuota de la API de golpe
    pendientes = session.query(ProyectoLey).filter(
        ProyectoLey.sector_economico == 'Pendiente AI'
    ).order_by(ProyectoLey.fecha_radicacion.desc()).limit(10).all()

    if not pendientes:
        print("✅ No hay proyectos pendientes de clasificación.")
        return

    print(f"🧠 Clasificando {len(pendientes)} proyectos...")
    clasificador = ClasificadorIA()

    for proyecto in pendientes:
        try:
            # Llamada a Gemini
            nuevo_sector = clasificador.clasificar(proyecto.titulo, proyecto.resumen)
            
            # Actualizar BD
            proyecto.sector_economico = nuevo_sector
            print(f"   🔹 [{nuevo_sector}] - {proyecto.titulo[:40]}...")
            
            # Pequeña pausa para no saturar la API (Rate Limits)
            time.sleep(1) 
            
        except Exception as e:
            print(f"   ❌ Fallo en proyecto {proyecto.id}: {e}")

    # Guardar cambios
    session.commit()
    print("✨ Clasificación terminada.")

def job_actualizacion():
    print("\n🕛 Iniciando tarea programada...")
    init_db()
    session = get_db()
    
    # --- FASE 1: SCRAPING ---
    scraper = ColombiaScraper()
    proyectos = scraper.scrape() # Esto trae los 61k diccionarios en memoria
    
    print(f"📡 Procesando {len(proyectos)} registros...")

    # Optimización: Traer todos los títulos existentes a memoria en un SET (mucho más rápido que 61k consultas)
    print("⏳ Cargando caché de títulos existentes...")
    titulos_existentes = {t[0] for t in session.query(ProyectoLey.titulo).all()}
    
    nuevos_para_guardar = []
    lote_tamano = 1000
    contador = 0

    for p in proyectos:
        # Verificación en RAM (Instantánea)
        if p['titulo'] not in titulos_existentes:
            nuevo = ProyectoLey(
                titulo=p['titulo'],
                fecha_radicacion=p['fecha_radicacion'],
                resumen=p['resumen'],
                enlace=p['enlace'],
                estado=p['estado'],
                pais=p['pais'],
                sector_economico="Pendiente AI"
            )
            nuevos_para_guardar.append(nuevo)
            titulos_existentes.add(p['titulo']) # Agregamos al set para evitar duplicados en el mismo excel
        
        # Si llenamos el lote, guardamos
        if len(nuevos_para_guardar) >= lote_tamano:
            try:
                session.bulk_save_objects(nuevos_para_guardar)
                session.commit()
                contador += len(nuevos_para_guardar)
                print(f"💾 Guardados {contador} registros...")
                nuevos_para_guardar = [] # Vaciar lista
            except Exception as e:
                session.rollback()
                print(f"⚠️ Error guardando lote: {e}")
                # Opcional: Aquí podrías intentar guardar 1 a 1 para aislar el error

    # Guardar el remanente final
    if nuevos_para_guardar:
        session.bulk_save_objects(nuevos_para_guardar)
        session.commit()
        contador += len(nuevos_para_guardar)

    print(f"✅ Total insertados: {contador}")
    session.close()

if __name__ == "__main__":
    # Ejecutar una vez al inicio
    job_actualizacion()

    # Programar
    schedule.every().day.at("00:00").do(job_actualizacion)
    
    print("🚀 Sistema Completo (Scraper + AI) Iniciado.")
    while True:
        schedule.run_pending()
        time.sleep(60)