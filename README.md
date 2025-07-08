# NOTAM - Sistema de Avisos a Navegantes

[![NOTAM Version](https://img.shields.io/badge/NOTAM-v2.0-blue.svg)](https://github.com/isidororeyes/NOTAM)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Status](https://img.shields.io/badge/status-en%20desarrollo-orange.svg)](https://github.com/isidororeyes/NOTAM)

## ?? Descripci¨®n

NOTAM (Notice to Airmen) es un sistema para la gesti¨®n y procesamiento de avisos a navegantes a¨¦reos. Este proyecto proporciona herramientas para el manejo, an¨¢lisis y distribuci¨®n de informaci¨®n NOTAM cr¨ªtica para la aviaci¨®n civil.

## ? Caracter¨ªsticas Principales

- ? **Procesamiento de mensajes NOTAM** - Analiza NOTAMs en formato ICAO est¨¢ndar
- ? **Validaci¨®n de formato** - Verifica sintaxis y estructura seg¨²n normas internacionales
- ? **An¨¢lisis de datos aeron¨¢uticos** - Extrae informaci¨®n de aeropuertos, pistas y servicios
- ? **Interfaz de usuario intuitiva** - F¨¢cil de usar para profesionales de aviaci¨®n
- ? **Exportaci¨®n de reportes** - Genera reportes en PDF, Excel y JSON
- ? **API REST** - Integraci¨®n con sistemas externos
- ? **B¨²squeda avanzada** - Filtros por fecha, aeropuerto, tipo de NOTAM

## ?? Instalaci¨®n R¨¢pida

### Requisitos del Sistema
- **Python 3.8 o superior**
- **Windows 10/11, macOS 10.14+, o Linux Ubuntu 18.04+**
- **4 GB RAM** (recomendado 8 GB)
- **2 GB espacio libre en disco**

### Instalaci¨®n Paso a Paso

1. **Clonar el repositorio:**
```bash
git clone https://github.com/isidororeyes/NOTAM.git
cd NOTAM
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
```

3. **Activar entorno virtual:**
```bash
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

4. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

5. **Configurar variables de entorno:**
```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus configuraciones
notepad .env
```

6. **Ejecutar la aplicaci¨®n:**
```bash
python src/main/app.py
```

## ??? C¨®mo Usar el Programa

### Uso B¨¢sico - L¨ªnea de Comandos

#### 1. Procesar un archivo NOTAM individual

```bash
# Analizar un archivo NOTAM
python src/main/app.py --file "ruta/al/archivo.notam"

# Ejemplo:
python src/main/app.py --file "data/samples/example_notam.txt"
```

#### 2. Procesar m¨²ltiples archivos

```bash
# Procesar todos los archivos de un directorio
python src/main/app.py --directory "ruta/al/directorio"

# Ejemplo:
python src/main/app.py --directory "data/samples/"
```

#### 3. Generar reporte completo

```bash
# Generar reporte en PDF
python src/main/app.py --file "archivo.notam" --report --format pdf

# Generar reporte en Excel
python src/main/app.py --file "archivo.notam" --report --format xlsx

# Generar reporte en JSON
python src/main/app.py --file "archivo.notam" --report --format json
```

#### 4. Validar formato NOTAM

```bash
# Solo validar sin procesar
python src/validators/notam_validator.py --file "archivo.notam"

# Validar con reporte detallado
python src/validators/notam_validator.py --file "archivo.notam" --verbose
```

#### 5. Opciones avanzadas

```bash
# Procesar con filtros espec¨ªficos
python src/main/app.py --file "archivo.notam" --airport LEMD --date-from 2024-01-01

# Procesar en modo estricto
python src/main/app.py --file "archivo.notam" --strict-mode

# Procesar con salida personalizada
python src/main/app.py --file "archivo.notam" --output "mi_reporte.json"
```

### Uso Avanzado - Interfaz Gr¨¢fica

#### 1. Iniciar la interfaz gr¨¢fica

```bash
python src/ui/main_window.py
```

#### 2. Pasos en la interfaz:

1. **Cargar archivo NOTAM:**
   - Clic en "Abrir Archivo"
   - Seleccionar archivo .notam o .txt
   - El contenido se mostrar¨¢ en el panel principal

2. **Configurar opciones:**
   - Seleccionar modo de validaci¨®n (estricto/flexible)
   - Elegir formato de salida
   - Configurar filtros si es necesario

3. **Procesar:**
   - Clic en "Procesar NOTAM"
   - Ver resultados en tiempo real
   - Revisar errores y advertencias

4. **Exportar resultados:**
   - Clic en "Exportar Reporte"
   - Elegir ubicaci¨®n y formato
   - Guardar el archivo

### Uso como API REST

#### 1. Iniciar el servidor API

```bash
python src/api/routes.py
```

El servidor estar¨¢ disponible en `http://localhost:5000`

#### 2. Endpoints principales

**Procesar NOTAM:**
```bash
curl -X POST http://localhost:5000/api/notam/process \
  -H "Content-Type: application/json" \
  -d '{"notam_text": "A1234/24 NOTAM..."}'
```

**Validar NOTAM:**
```bash
curl -X POST http://localhost:5000/api/notam/validate \
  -H "Content-Type: application/json" \
  -d '{"notam_text": "A1234/24 NOTAM..."}'
```

**Obtener historial:**
```bash
curl http://localhost:5000/api/notam/history
```

### Ejemplos Pr¨¢cticos

#### Ejemplo 1: Procesar NOTAM de aeropuerto espec¨ªfico

```bash
# Archivo: madrid_notam.txt
# Contenido: A1234/24 NOTAM LEMD...

python src/main/app.py --file "madrid_notam.txt" --airport LEMD --format json
```

#### Ejemplo 2: An¨¢lisis de NOTAMs por fecha

```bash
python src/main/app.py \
  --directory "notams_enero/" \
  --date-from 2024-01-01 \
  --date-to 2024-01-31 \
  --report \
  --format pdf
```

#### Ejemplo 3: Validaci¨®n masiva

```bash
python src/validators/notam_validator.py \
  --directory "notams_to_validate/" \
  --output "validation_report.json" \
  --strict-mode
```

## ?? Formatos de Salida

### JSON (Predeterminado)
```json
{
  "notam_id": "A1234/24",
  "airport": "LEMD",
  "effective_date": "2024-01-15T00:00:00Z",
  "expiry_date": "2024-01-20T23:59:59Z",
  "content": "...",
  "classification": "A",
  "status": "ACTIVE"
}
```

### Excel (.xlsx)
- Hoja "Resumen": Estad¨ªsticas generales
- Hoja "NOTAMs": Listado detallado
- Hoja "Errores": Problemas encontrados

### PDF
- Portada con resumen ejecutivo
- ¨ªndice de contenidos
- An¨¢lisis detallado por aeropuerto
- Anexos con NOTAMs originales

## ?? Configuraci¨®n Avanzada

### Archivo de configuraci¨®n (config/config.json)

```json
{
  "parser": {
    "strict_mode": true,
    "validate_dates": true,
    "max_retries": 3
  },
  "database": {
    "type": "sqlite",
    "path": "./data/notam.db"
  },
  "output": {
    "format": "json",
    "pretty_print": true,
    "include_raw": false
  }
}
```

### Variables de entorno importantes

```bash
# Configuraci¨®n b¨¢sica
NOTAM_LOG_LEVEL=INFO
NOTAM_DB_PATH=./data/notam.db
NOTAM_STRICT_MODE=true

# APIs externas (opcional)
ICAO_API_KEY=tu-clave-api
FAA_API_KEY=tu-clave-api
```

## ?? Pruebas y Validaci¨®n

### Ejecutar pruebas

```bash
# Todas las pruebas
pytest tests/

# Pruebas espec¨ªficas
pytest tests/unit/test_parser.py

# Con cobertura
pytest --cov=src tests/
```

### Datos de prueba

El proyecto incluye datos de ejemplo en `data/samples/`:
- `example_notam.txt` - NOTAM b¨¢sico de ejemplo
- `complex_notam.txt` - NOTAM con m¨²ltiples elementos
- `invalid_notam.txt` - Ejemplo de NOTAM inv¨¢lido

## ?? Estructura del Proyecto

```
NOTAM/
©À©¤©¤ src/                    # C¨®digo fuente
©¦   ©À©¤©¤ main/              # Aplicaci¨®n principal
©¦   ©À©¤©¤ parsers/           # Analizadores NOTAM
©¦   ©À©¤©¤ validators/        # Validadores
©¦   ©¸©¤©¤ utils/             # Utilidades
©À©¤©¤ tests/                 # Pruebas
©À©¤©¤ docs/                  # Documentaci¨®n
©À©¤©¤ data/                  # Datos y ejemplos
©À©¤©¤ config/                # Configuraciones
©¸©¤©¤ scripts/               # Scripts de automatizaci¨®n
```

## ?? Soluci¨®n de Problemas

### Errores Comunes

**Error: "No se puede encontrar el archivo"**
```bash
# Verificar que el archivo existe
ls -la archivo.notam
# o en Windows:
dir archivo.notam
```

**Error: "Formato NOTAM inv¨¢lido"**
```bash
# Usar validador para diagn¨®stico
python src/validators/notam_validator.py --file archivo.notam --verbose
```

**Error: "Dependencias faltantes"**
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Logs y Depuraci¨®n

```bash
# Ejecutar con logs detallados
python src/main/app.py --file archivo.notam --log-level DEBUG

# Ver logs en archivo
tail -f logs/notam.log
```

## ?? Contribuir

?Quieres contribuir al proyecto? ?Genial!

1. Lee la [Gu¨ªa de Contribuci¨®n](CONTRIBUTING.md)
2. Fork el repositorio
3. Crea una rama para tu feature
4. Env¨ªa un Pull Request

## ?? Licencia

Este proyecto est¨¢ bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para m¨¢s detalles.

## ?? Autor

**Isidoro Reyes** - [@isidororeyes](https://github.com/isidororeyes)

## ?? Reconocimientos

- Organizaci¨®n de Aviaci¨®n Civil Internacional (ICAO)
- Administraci¨®n Federal de Aviaci¨®n (FAA)
- Comunidad de desarrolladores de aviaci¨®n

## ?? Soporte

?Necesitas ayuda?
- ?? [Reportar un bug](https://github.com/isidororeyes/NOTAM/issues)
- ?? [Solicitar una caracter¨ªstica](https://github.com/isidororeyes/NOTAM/issues)
- ?? Contacto: [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)

---

? **?Si este proyecto te ayuda, dale una estrella en GitHub!** ?