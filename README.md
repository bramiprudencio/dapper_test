# 🏛️ Legislación AI Monitor - Colombia

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql)
![Gemini AI](https://img.shields.io/badge/AI-Gemini_1.5-8E75B2?style=for-the-badge&logo=google)

Este proyecto es un pipeline de datos automatizado que monitorea, descarga y clasifica los proyectos de ley del Congreso de la República de Colombia utilizando Inteligencia Artificial.

El sistema resuelve el problema de la estructuración de datos gubernamentales mediante un proceso ETL (Extract, Transform, Load) moderno y contenerizado.

## 🚀 Arquitectura

El sistema está orquestado con **Docker Compose** y consta de tres servicios interconectados:

1.  **Scraper (Python 3.11):**
    * **Extracción:** Se conecta al servidor del Congreso manejando cookies y sesiones para evitar bloqueos.
    * **Procesamiento:** Descarga y procesa archivos Excel masivos (60k+ registros) utilizando **Streams en memoria RAM** (evitando escritura en disco).
    * **Inteligencia:** Utiliza un sistema híbrido (Palabras Clave + **Google Gemini AI**) para clasificar cada ley en sectores económicos (Salud, Hacienda, Justicia, etc.).
2.  **Base de Datos (PostgreSQL):** Data Warehouse que almacena el histórico, evita duplicados y gestiona el estado de los proyectos.
3.  **Visualización (Metabase):** Plataforma de Business Intelligence para explorar los datos mediante Dashboards interactivos.

## 🏃‍♂️ Cómo ejecutar este proyecto localmente

Sigue estos pasos para levantar todo el entorno (Base de datos + Scraper + Visualizador) en tu propia máquina en menos de 5 minutos.

### 1. Prerrequisitos
Asegúrate de tener instalado lo siguiente:
* **Docker Desktop:** [Descargar aquí](https://www.docker.com/products/docker-desktop/) (Windows/Mac) o Docker Engine (Linux).
* **Git:** Para clonar el repositorio.
* **API Key de Gemini:** Obtén una clave gratuita en [Google AI Studio](https://aistudio.google.com/).

### 2. Instalación Paso a Paso

**Paso 1: Clonar el repositorio**
Abre tu terminal y ejecuta (esto descargará el proyecto en una carpeta llamada `legislacion-ai-colombia`):

```bash
git clone [https://github.com/bramiprudencio/dapper_test.git](https://github.com/bramiprudencio/dapper_test.git)
cd dapper_test
```

**Paso 2: Configurar Credenciales**
El proyecto necesita claves privadas. Crea un archivo .env basado en el ejemplo incluido:

```bash
# En Mac/Linux:
cp .env.example .env

# En Windows (PowerShell):
Copy-Item .env.example .env
```

**Paso 3: Encender los motores 🐳**
Ejecuta el siguiente comando para que Docker descargue, construya y conecte todo automáticamente:

```bash
docker compose up -d --build
```