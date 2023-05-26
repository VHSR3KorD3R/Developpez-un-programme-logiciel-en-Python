# Développez un programme logiciel en Python
Ce projet vise à coder un outil permettant de gérer des tournois d'échecs en étant hors ligne. Développé en Python en utilisant le pattern MVC, modèle vue controlleur.

## Installation

# Créer un répertoire local dans lequel on installera l'application
```bash
cd /home/<nom d'utilisateur>/<nouveau repertoire>
```

# Creer l'environnement virtuel
```bash
python -m venv env
source env/bin/activate
```

# Cloner le projet
```bash
git clone https://github.com/VHSR3KorD3R/Developpez-un-programme-logiciel-en-Python.git
cd Developpez-un-programme-logiciel-en-Python
```

# Installer les dépendances
```bash
pip install -r requirements.txt
```

# Executer le programme
```bash
python main.py
```

# Générer le rapport flake8 html
```bash
flake8 --exclude venv --max-line-length 119 --format=html --htmldir=flake-report
```

