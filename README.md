📘 CodeCraftHub — Plataforma Simple para Aprender APIs REST con Flask
CodeCraftHub es una aplicación educativa diseñada para ayudar a desarrolladores principiantes a aprender cómo construir una API REST usando Python y Flask, almacenando datos en un archivo JSON en lugar de una base de datos.

El proyecto es pequeño, fácil de entender y perfecto para quienes están dando sus primeros pasos en el desarrollo backend.

🚀 Características principales
API REST completa (CRUD) para gestionar cursos.

Datos almacenados en un archivo courses.json (sin base de datos).

Validación de datos (campos requeridos, formatos, estados válidos).

Manejo de errores para entradas inválidas.

Código simple, modular y bien comentado.

Ideal para aprender:

Rutas REST

Métodos HTTP (GET, POST, PUT, DELETE)

Manejo de JSON

Estructura básica de un proyecto Flask

📁 Estructura del proyecto
Código
codecrafthub/
│
├── app.py                 # Aplicación principal Flask
├── courses.json           # Archivo donde se guardan los cursos
│
├── services/
│   └── storage.py         # Funciones para leer/escribir JSON
│
└── routes/
    └── courses.py         # Endpoints de la API
¿Por qué esta estructura?
app.py mantiene la aplicación limpia.

routes/ separa las rutas de la lógica.

services/ maneja la lectura/escritura del archivo JSON.

Es una estructura realista pero simple para principiantes.

🛠️ Instalación (paso a paso)
1. Clonar el repositorio
bash
git clone https://github.com/tuusuario/codecrafthub.git
cd codecrafthub
2. Crear un entorno virtual (opcional pero recomendado)
bash
python -m venv venv
Activar:

Windows

bash
venv\Scripts\activate
macOS/Linux

bash
source venv/bin/activate
3. Instalar dependencias
bash
pip install flask
4. Crear el archivo JSON (si no existe)
El programa lo creará automáticamente, pero puedes hacerlo manualmente:

bash
echo [] > courses.json
▶️ Cómo ejecutar la aplicación
bash
python app.py
La API estará disponible en:

Código
http://127.0.0.1:5000
📚 Documentación de la API
Todos los endpoints comienzan con:

Código
/api/courses
➕ Crear un curso
POST /api/courses

Ejemplo de cuerpo JSON:
json
{
  "name": "Flask Básico",
  "description": "Aprender a crear APIs REST",
  "target_date": "2026-06-01",
  "status": "Not Started"
}
Respuesta esperada (201):
json
{
  "id": 1,
  "name": "Flask Básico",
  "description": "Aprender a crear APIs REST",
  "target_date": "2026-06-01",
  "status": "Not Started",
  "created_at": "2026-05-08T06:12:34.123456"
}
📄 Obtener todos los cursos
GET /api/courses

Respuesta:
json
[
  {
    "id": 1,
    "name": "Flask Básico",
    "description": "Aprender a crear APIs REST",
    "target_date": "2026-06-01",
    "status": "Not Started",
    "created_at": "2026-05-08T06:12:34.123456"
  }
]
🔍 Obtener un curso por ID
GET /api/courses/<id>

Ejemplo:

Código
GET /api/courses/1
✏️ Actualizar un curso
PUT /api/courses/<id>

Ejemplo JSON:
json
{
  "name": "Flask Básico (Actualizado)",
  "description": "Descripción actualizada",
  "target_date": "2026-06-15",
  "status": "In Progress"
}
🗑️ Eliminar un curso
DELETE /api/courses/<id>

Respuesta:

json
{
  "message": "Course deleted successfully"
}
🧪 Pruebas (PowerShell)
Crear un curso
powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/courses" -Method POST -ContentType "application/json" -Body '{
    "name": "Flask Básico",
    "description": "Aprender APIs REST",
    "target_date": "2026-06-01",
    "status": "Not Started"
}'
Obtener todos los cursos
powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/courses"
Actualizar un curso
powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/courses/1" -Method PUT -ContentType "application/json" -Body '{
    "name": "Flask Básico (Actualizado)",
    "description": "Descripción actualizada",
    "target_date": "2026-06-15",
    "status": "In Progress"
}'
Eliminar un curso
powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/courses/1" -Method DELETE
🛑 Manejo de errores
La API devuelve mensajes claros cuando:

❌ Faltan campos requeridos
json
{
  "error": "Missing required fields: description, target_date, status"
}
❌ Estado inválido
json
{
  "error": "Invalid status value. Must be one of: Not Started, In Progress, Completed"
}
❌ Fecha inválida
json
{
  "error": "Invalid target_date format. Use YYYY-MM-DD."
}
❌ Curso no encontrado
json
{
  "error": "Course not found"
}
🛠️ Problemas comunes y soluciones
⚠️ “El archivo courses.json no existe”
La app lo crea automáticamente.
Si falla, crea uno manualmente:

bash
echo [] > courses.json
⚠️ PowerShell no reconoce -d o -X
PowerShell no usa la sintaxis de curl de Linux.
Usa siempre:

Código
Invoke-RestMethod
⚠️ Cambios no se guardan
Verifica permisos del archivo:

En Windows:
Asegúrate de que courses.json no esté en modo solo lectura.

🎯 Conclusión
CodeCraftHub es un proyecto perfecto para aprender:

Cómo funciona una API REST

Cómo manejar JSON en Flask

Cómo estructurar un proyecto backend simple

Cómo validar datos y manejar errores