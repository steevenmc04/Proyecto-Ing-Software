# Guia De Despliegue Local

## SQLite

```powershell
cd C:\Users\steeven\Documents\ProyectoIngSoftware
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python seed.py
uvicorn app.main:app --reload
```

## MySQL Workbench

1. Ejecutar `database_mysql.sql` en MySQL Workbench.
2. Configurar `.env`:

```env
DATABASE_URL=mysql+pymysql://usuario_caja:ClaveCaja123@localhost:3306/caja_ahorros
```

3. Ejecutar:

```powershell
python seed.py
uvicorn app.main:app --reload
```

