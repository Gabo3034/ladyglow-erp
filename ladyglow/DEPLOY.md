# 🚀 Guía de Deploy — LadyGlow ERP en la Nube

Stack gratuito: **Supabase** (base de datos) + **Streamlit Community Cloud** (hosting)

---

## PASO 1 — Crear la base de datos en Supabase (5 minutos)

1. Ve a **https://supabase.com** → *Start your project*
2. Crea cuenta con Google o GitHub
3. Haz clic en **New Project**
   - Name: `ladyglow`
   - Database Password: anota una contraseña segura (la vas a necesitar)
   - Region: South America (São Paulo) → la más cercana a Chile
4. Espera ~2 minutos a que se cree el proyecto
5. Ve a **Project Settings → Database → Connection Pooling**
6. Activa **Transaction Mode** (si no está activo)
7. Copia la **Connection String** de esa sección → se ve así:
   `postgresql://postgres.XXXX:[YOUR-PASSWORD]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres`
   - ⚠️ Usa **esta URL del pooler** (puerto 6543), NO la directa (puerto 5432)
   - Reemplaza `[YOUR-PASSWORD]` por la contraseña que pusiste en el paso 3
   - Guarda esta URL, la necesitas en el Paso 3

---

## PASO 2 — Subir el código a GitHub (3 minutos)

1. Ve a **https://github.com** e inicia sesión
2. Haz clic en **+** → *New repository*
   - Nombre: `ladyglow-erp`
   - Visibilidad: **Private** ✅ (importante para no exponer el código)
   - Haz clic en *Create repository*
3. Sube los archivos a ese repositorio:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/secrets.toml.example` (el `.example` no tiene credenciales reales, es seguro subirlo)
4. **NO subas** el archivo `.streamlit/secrets.toml` (con la URL real de Supabase)

> Si no sabes subir archivos a GitHub, puedes usar la interfaz web:
> En tu repositorio → *Add file* → *Upload files*

---

## PASO 3 — Deploy en Streamlit Community Cloud (5 minutos)

1. Ve a **https://share.streamlit.io** e inicia sesión con tu cuenta de GitHub
2. Haz clic en **New app**
3. Configura:
   - Repository: `tu-usuario/ladyglow-erp`
   - Branch: `main`
   - Main file path: `app.py`
4. Antes de hacer deploy, haz clic en **Advanced settings**
5. En el campo **Secrets**, pega esto (con tu URL real de Supabase):

```toml
DATABASE_URL = "postgresql://postgres:TU-PASSWORD@db.TUPROYECTO.supabase.co:5432/postgres"
```

6. Haz clic en **Deploy!**
7. Espera ~2 minutos → tu app estará en una URL del tipo:
   `https://ladyglow-erp-tuusuario.streamlit.app`

---

## RESULTADO FINAL

- ✅ App disponible desde cualquier dispositivo con internet
- ✅ Base de datos en la nube (Supabase), no se borra
- ✅ Tú y Anny pueden entrar simultáneamente sin problemas
- ✅ Todo gratis (Supabase: 500MB gratis / Streamlit Cloud: ilimitado gratis)

---

## ⚠️ Seguridad importante

Las contraseñas actuales son `admin/1234` y `anny/anny123`.
Se recomienda cambiarlas en el código fuente antes de subir a producción.
Busca la función `login()` en `app.py` y modifica los valores.

---

## 🆘 Si algo falla

- **Error de conexión a DB**: Verifica que la URL de Supabase esté correctamente pegada en los Secrets de Streamlit (sin espacios, sin comillas de más)
- **ModuleNotFoundError**: Asegúrate de que `requirements.txt` esté en la raíz del repositorio
- **La app se demora al abrir**: Normal la primera vez, Streamlit "despierta" la app si lleva tiempo inactiva (gratis = puede dormir)

Para soporte técnico adicional: https://discuss.streamlit.io
