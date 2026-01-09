# Sin Rol Staff — Telegram Auto Sender (Telethon)

Script de Sin Rol Staff que permite:
- Guardar un mensaje (respondiéndolo con `/send`)
- Uso /add -1001234567890 #Para agregar un chat a la lista de envios
- Reenviarlo automáticamente a una lista de grupos/canales guardados
- Eliminar el mensaje anterior reenviado en cada chat (para que siempre quede el último)

- API_ID = 111111111  # TU_API_ID_AQUI
- API_HASH = "TU_API_HASH_AQUI"
- OWNER_ID = 8381560803
- SPAM_INTERVAL = 300  # Tiempo en segundos entre envíos
- DB_PATH = "bot.db"


Python recomendado: **3.11.5**

## Contacto / Comunidad
- Dev (negocios): **@ErzScarlet** (Darwin R)
- Canal: https://t.me/SinRolAlguno
- Grupo: https://t.me/SinRolChat

---

## 1) Requisitos
- **Python 3.11.5**
- Una cuenta de Telegram (se usa sesión de usuario, no bot)
- `API_ID` y `API_HASH` de Telegram:
  - Se obtienen en: https://my.telegram.org/apps

---

## 2) Instalación

### Windows / Linux / Mac
1. Crea una carpeta para el proyecto y guarda tu script como, por ejemplo:
   - `main.py`

2. (Recomendado) Crea un entorno virtual:

**Windows**
```bash
py -3.11 -m venv venv
venv\Scripts\activate


