# src/sql_tool.py
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama


# 1. Chargement des variables d'environnement
load_dotenv()

# 2. Base de données SQLite
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "nba_analytics.db"

db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

# 3. Modèle Ollama (vérifie qu'il est bien téléchargé avec `ollama list`)
llm = ChatOllama(
    model="llama3.1",
    temperature=0
)

# 4. Instructions spécifiques pour forcer la syntaxe SQLite
SQL_PREFIX = """Tu es un expert SQL spécialisé dans l'analyse de données NBA sur SQLite.

Consignes impératives :
1. Examine toujours le schéma de la base de données avec l'outil d'inspection avant d'écrire la requête.
2. N'utilise JAMAIS 'SELECT TOP n'. SQLite ne supporte pas 'TOP'. Utilise TOUJOURS 'ORDER BY ... LIMIT n'.
3. Ne réponds qu'avec des requêtes SQLite valides.
"""

# 5. Création de l'agent SQL réactif adapté à Ollama
sql_agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="zero-shot-react-description",
    prefix=SQL_PREFIX,
    verbose=True,
    handle_parsing_errors=True
)