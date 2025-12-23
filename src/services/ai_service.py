import os
import google.generativeai as genai
import time

class ClasificadorIA:
    def __init__(self):
        # Configuración inicial usando la API KEY del .env
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("❌ Faltan la GOOGLE_API_KEY en el .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash') # Modelo rápido y barato

        # Lista cerrada de sectores para mantener el orden en Metabase
        self.sectores_validos = [
            "Salud", "Educación", "Tecnología", "Hacienda y Crédito Público", 
            "Justicia", "Medio Ambiente", "Transporte", "Defensa y Seguridad",
            "Trabajo y Seguridad Social", "Agricultura", "Comercio e Industria",
            "Cultura y Deporte", "Vivienda", "Relaciones Exteriores", "Otro"
        ]

        # DICCIONARIO DE REGLAS RÁPIDAS (Gratis y Instantáneo)
        self.reglas_keyword = {
            "Hacienda y Crédito Público": ["presupuesto", "tributaria", "impuesto", "financiación", "crédito público"],
            "Salud": ["salud", "hospital", "médico", "vacunación", "eps", "paciente"],
            "Educación": ["educación", "colegio", "universidad", "icetex", "docente"],
            "Justicia": ["código penal", "judicial", "delito", "cárcel", "penitenciario"],
            "Transporte": ["vía", "tránsito", "transporte", "carretera", "infraestructura"],
            "Medio Ambiente": ["ambiente", "sostenible", "animal", "páramo", "agua"],
            "Cultura y Deporte": ["cultura", "deporte", "patrimonio", "artístico"]
        }

    def clasificar_hibrido(self, titulo, resumen):
        texto_completo = (str(titulo) + " " + str(resumen)).lower()

        # 1. INTENTO RÁPIDO: Buscar palabras clave
        for sector, keywords in self.reglas_keyword.items():
            for word in keywords:
                if word in texto_completo:
                    return sector # ¡Éxito! Sin gastar API

        # 2. Si no hay coincidencia obvia, usar IA
        # Aquí es donde llamamos a Gemini
        return self.clasificar(titulo, resumen)

    def clasificar(self, titulo, resumen):
        """
        Recibe título y resumen, devuelve una categoría de la lista.
        """
        prompt = f"""
        Actúa como un analista legislativo experto. 
        Clasifica el siguiente proyecto de ley en EXACTAMENTE UNO de estos sectores:
        {', '.join(self.sectores_validos)}.
        
        Si no encaja claramente, usa "Otro".
        IMPORTANTE: Tu respuesta debe ser SOLO la palabra del sector. Nada más.
        
        Título: {titulo}
        Resumen: {resumen}
        """

        try:
            # Enviamos a Gemini
            response = self.model.generate_content(prompt)
            texto_respuesta = response.text.strip()
            
            # Limpieza básica por si el modelo responde con punto final
            if texto_respuesta.endswith("."):
                texto_respuesta = texto_respuesta[:-1]

            # Validación: Si el modelo alucina una categoría nueva, la marcamos como Otro
            if texto_respuesta not in self.sectores_validos:
                # Intento de corrección flexible (ej: "Salud Pública" -> "Salud")
                for sector in self.sectores_validos:
                    if sector in texto_respuesta:
                        return sector
                return "Otro"
                
            return texto_respuesta

        except Exception as e:
            print(f"⚠️ Error en Gemini: {e}")
            return "Error AI" # Para reintentar luego