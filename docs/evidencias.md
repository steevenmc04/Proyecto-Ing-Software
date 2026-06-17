# Evidencias De Funcionamiento

## Repositorio

https://github.com/steevenmc04/Proyecto-Ing-Software

## Servicios Documentados

Swagger:

http://127.0.0.1:8000/docs

Redoc:

http://127.0.0.1:8000/redoc

## Pagina Funcional

http://127.0.0.1:8000

Usuarios de prueba:

- `admin` / `Admin123`
- `socio` / `Socio123`

## Comandos De Ejecucion

```powershell
cd C:\Users\steeven\Documents\ProyectoIngSoftware
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python seed.py
uvicorn app.main:app --reload
```

## Pruebas

```powershell
pytest -q
```

Resultado esperado:

```text
9 passed
```

