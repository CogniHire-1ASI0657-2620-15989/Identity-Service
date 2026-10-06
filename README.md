# Identity Service

Microservicio horientado a la autenticación y gestión del perfil profesional, desarrollado con FastAPI, SQLAlchemy y PostgreSQL.

## Requisitos

- Python 3.12 o superior
- PostgreSQL ejecutándose en `localhost:5432`
- Base de datos `identity_db`
- Usuario de PostgreSQL con permisos sobre `identity_db`

## Configuración

Crea o revisa el archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql+psycopg://postgres:<tu_contraseña>@localhost:5432/identity_db
JWT_SECRET_KEY=una-clave-secreta-para-desarrollo
JWT_ISSUER=identity-service
JWT_AUDIENCE=job-platform-services
JWT_EXPIRATION_MINUTES=60
```

Instala las dependencias:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si todavía no existe la base de datos:

```sql
CREATE DATABASE identity_db;
```

## Ejecutar el servicio

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

La API estará disponible en:

- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

Al iniciar, el servicio crea las tablas necesarias si no existen.

## Flujo básico

### 1. Registrar un usuario

`POST /api/v1/auth/register`

```json
{
  "name": "Ana García",
  "email": "ana.garcia@example.com",
  "password": "secreto123",
  "segment": "trabajador",
  "city": "Madrid",
  "country": "España"
}
```

La respuesta incluye un `access_token`. Para los siguientes endpoints protegidos, en Swagger pulsa **Authorize** y usa:

```text
Bearer <access_token>
```

Los segmentos válidos son `trabajador` y `practicante`.

### 2. Iniciar sesión

`POST /api/v1/auth/login`

```json
{
  "email": "ana.garcia@example.com",
  "password": "secreto123"
}
```

También devuelve un `access_token`.

### 3. Consultar el perfil

`GET /api/v1/profile/me`

Requiere autenticación Bearer.

### 4. Actualizar el perfil profesional

`PUT /api/v1/profile/me`

Los campos son opcionales, por lo que se pueden actualizar solo los datos necesarios:

```json
{
  "target_position": "Backend Developer",
  "expected_city": "Madrid",
  "expected_country": "España",
  "work_modality": "hibrido",
  "professional_summary": "Desarrollador especializado en APIs REST.",
  "education": [
    {
      "degree": "Ingeniería de Sistemas",
      "institution": "Universidad Nacional",
      "field_of_study": "Software",
      "start_year": 2020,
      "end_year": 2024
    }
  ],
  "experience": [
    {
      "position": "Backend Developer",
      "company": "Empresa X",
      "description": "Desarrollo de APIs REST.",
      "start_date": "2022-01",
      "end_date": "2024-06",
      "current": false
    }
  ],
  "languages": [
    {
      "name": "Inglés",
      "level": "B2"
    }
  ]
}
```

Los valores válidos para `work_modality` son `remoto`, `hibrido` y `presencial`.

### 5. Gestionar habilidades

Todas estas rutas requieren autenticación Bearer.

Añadir una habilidad hard:

`POST /api/v1/profile/me/skills/hard`

```json
{
  "name": "Python",
  "level": "avanzado"
}
```

Añadir una habilidad soft:

`POST /api/v1/profile/me/skills/soft`

```json
{
  "name": "Comunicación",
  "level": "alto"
}
```

Actualizar una habilidad:

`PUT /api/v1/profile/me/skills/hard/Python`

```json
{
  "name": "Python",
  "level": "experto"
}
```

Eliminar una habilidad:

`DELETE /api/v1/profile/me/skills/hard/Python`

### 6. Cambiar la contraseña autenticado

`PUT /api/v1/profile/me/password`

```json
{
  "current_password": "secreto123",
  "new_password": "nuevoSecreto456"
}
```

### 7. Recuperar la contraseña

Solicitar recuperación:

`POST /api/v1/auth/password-recovery`

```json
{
  "email": "ana.garcia@example.com"
}
```

En este proyecto universitario, la respuesta devuelve temporalmente el token para poder probar el flujo:

```json
{
  "message": "Si el correo existe, se ha generado un token de recuperación.",
  "token": "token-generado"
}
```

Restablecer la contraseña:

`POST /api/v1/auth/password-reset`

```json
{
  "token": "token-generado",
  "new_password": "otraClave789"
}
```

### 8. Consultar el perfil para otros servicios

`GET /api/v1/internal/users/{id}/job-profile`

Ejemplo:

```text
GET /api/v1/internal/users/1/job-profile
```

Devuelve únicamente datos profesionales útiles para búsqueda o recomendación:

```json
{
  "id": 1,
  "target_position": "Backend Developer",
  "expected_city": "Madrid",
  "expected_country": "España",
  "work_modality": "hibrido",
  "hard_skills": [],
  "soft_skills": [],
  "education": [],
  "experience": [],
  "languages": [],
  "professional_summary": "Desarrollador especializado en APIs REST."
}
```

## Estructura principal

- `app/domain`: entidades, comandos, consultas y repositorios.
- `app/application`: servicios de aplicación y puertos.
- `app/infrastructure`: PostgreSQL, SQLAlchemy, JWT y bcrypt.
- `app/interfaces/rest`: controladores, recursos y ensambladores.
