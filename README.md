# 🔧 GreenSpots – Backend

Backend Django servant d’API pour le projet **GreenSpots**.  
👉 Cette version est un **prototype** : l’API retourne des **données statiques** afin de tester l’intégration avec le frontend Next.js, sauf pour les bornes de recharge électrique récupérées via [data.gouv](https://data.gouv.fr)

---

## 🚀 Installation & lancement du backend en local

### 1. Cloner le projet
```bash
git clone https://github.com/aulemarouille/green-spots-back.git
cd green-spots-back
```
### 2. Créer et activer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
### 3. Installer les dépendences
```bash
pip install -r requirements.txt
```
### 4. Lancer le serveur
```bash
python manage.py runserver
```

Le backend est disponible sur http://localhost:8000.

---

## ✨ Déploiement de l'app

Le back utilise [Render](https://render.com/) pour le déploiement et la liste des spots est disponible à cet endpoint : https://green-spots-back.onrender.com/api/spots