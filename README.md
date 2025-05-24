## 🧰 Avvio del Progetto – TripTales Backend (Django + MySQL via XAMPP)

Questa guida ti spiega passo per passo come avviare il backend del progetto **TripTales** in locale usando **Django 4.2** e **MySQL fornito da XAMPP**.


Documentazione API completa [qui](https://protective-helicona-baf.notion.site/Documentazione-TripRoom-API-1fc7eb75f1a38006a26ff410fbc82017?pvs=4).

---

### ✅ **Requisiti**

- Python 3.9+
- XAMPP installato (con MariaDB)
- Git
- pip (gestore pacchetti Python)

---

### ⚙️ **1. Avvia XAMPP**

1. Apri il **pannello di controllo di XAMPP**
2. Avvia **solo il modulo MySQL**
3. (Puoi ignorare Apache)

---

### 🗂️ **2. Clona il repository**

```bash
git clone https://github.com/FantinJacopo/pw-backend-triptales.git
cd pw-backend-triptales
```

---

### 📦 **3. Installa le dipendenze**

Si consiglia l'uso di un virtual environment (facoltativo):

```bash
python -m venv venv
source venv/bin/activate   # Su Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 🔐 **4. Crea un file `.env` nella root**

Contenuto di esempio:

```env
DB_NAME=pwtriptales_db
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
NGROK_AUTH_TOKEN=2xPSuq30Ur...1aYmk
DJANGO_PORT=8000
```

> ⚠️ `DB_PASSWORD` lascia vuoto se in XAMPP non hai impostato una password (default)

---

### 🧱 **5. Crea il database in XAMPP**

Accedi a phpMyAdmin:  
http://localhost/phpmyadmin

Esegui le seguenti query SQL:

```sql
CREATE DATABASE pwtriptales_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON pwtriptales_db.* TO 'root'@'' IDENTIFIED BY '';
FLUSH PRIVILEGES;
```

### 🔄 **6. Applica le migrazioni**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py fix_emoji_support
python manage.py populate_badges
```

---

### 👑 **7. (Opzionale) Crea un superuser per accedere come admin**

```bash
python manage.py createsuperuser
```

---

### 🚀 **8. Avvia il server di sviluppo**

N.B.: così il backend sarà accessibile solo dalla stessa rete
Se hai un server locale, puoi eseguire il server di sviluppo con il comando:
```bash
python manage.py runserver INDIRIZZO_IP_DEL_DISPOSITIVO:8000
```

Per rendere il backend accessibile da reti diverse con ngrok invece eseguire:
```bash
python manage.py runserver 8000

ngrok #solo se non è ancora installato
ngrok config add-authtoken $AUTHTOKEN #solo la prima volta
cmd.exe /c ngrok_start.bat #oppure eseguire il comando: ngrok http --url=shepherd-precious-reliably.ngrok-free.app 8000
```

---

### ✅ Fine! Ora il backend è attivo!