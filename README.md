# Urban-ETA-Prediction-Platform



Voici une version formatée et optimisée pour un fichier **README.md** de ton dépôt GitHub. J'ai ajouté quelques éléments de mise en forme (badges, icônes et blocs de code clairs) pour rendre le guide plus professionnel.

---

# 🚀 Guide de Configuration : WSL, Python & VS Code

Ce guide explique comment configurer un environnement de développement professionnel sous Windows en utilisant **WSL (Ubuntu)**, **Git**, et **Python**, puis comment lier le tout à **VS Code**.

---

## 🖥️ Prérequis

Avant de commencer, assurez-vous d'avoir :
*   **Windows 10 ou 11** (à jour).
*   **VS Code** installé sur Windows.
*   Un compte **GitHub**.
*   Une connexion Internet stable.

---

## 1️⃣ Installation de WSL & Ubuntu

Ouvrez **PowerShell** en mode **Administrateur** et lancez :

```powershell
wsl --install
sudo apt update
sudo apt install openjdk-17-jdk -y

```

> [!IMPORTANT]
> Cette commande installe WSL et la distribution Ubuntu par défaut. **Redémarrez votre PC** après l'exécution pour finaliser l'installation.

---

## 2️⃣ Configuration de Linux (Ubuntu)

1.  Lancez **Ubuntu** depuis le menu Démarrer.
2.  Créez votre **nom d'utilisateur** et votre **mot de passe** (ils sont indépendants de Windows).
3.  Une fois l'invite `username@DESKTOP:~$` affichée, mettez le système à jour :

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 3️⃣ Installation des outils (Git & Python)

### Git
```bash
sudo apt install git -y
# Vérification
git --version
```

### Python & Pip
```bash
sudo apt install python3 python3-pip python3-venv -y
# Vérification
python3 --version
```

### Gitflow (Optionnel)
```bash
sudo apt install git-flow-avh -y
```

---

## 4️⃣ Préparation du projet

### Création de l'espace de travail
Il est fortement recommandé de travailler dans le système de fichiers Linux.

```bash
cd ~
mkdir projects
cd projects
```

### Récupération du dépôt
```bash
git clone https://github.com/VOTRE_NOM_UTILISATEUR/NOM_DU_REPO.git
cd NOM_DU_REPO
```

> [!WARNING]
> **Ne travaillez pas dans `/mnt/c/...`** (disque Windows). Cela ralentit considérablement les performances de Python et Git. Utilisez toujours `/home/votre_nom/...`.

---

## 5️⃣ Environnement Virtuel Python

Configurez un environnement isolé pour votre projet :

```bash
# Créer l'environnement
python3 -m venv .venv

# Activer l'environnement
source .venv/bin/activate
```

Une fois activé, mettez à jour `pip` et installez vos dépendances :
```bash
pip install --upgrade pip
# Si vous avez un fichier requirements.txt :
pip install -r requirements.txt
```

---

## 6️⃣ Intégration avec VS Code

1.  Sur Windows, ouvrez VS Code.
2.  Allez dans les **Extensions** (`Ctrl + Shift + X`).
3.  Cherchez et installez l'extension **"WSL"** (éditée par Microsoft).
4.  Revenez dans votre terminal Ubuntu, à l'intérieur du dossier de votre projet, et tapez :

```bash
code .
```



---


