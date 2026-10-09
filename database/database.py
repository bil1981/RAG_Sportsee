# src/sportsee/database/database.py
"""
Utilitaires pour l'accès à la base de données SQLite.
"""
from __future__ import annotations

from pathlib import Path

from sportsee.config import settings


def get_database_path() -> Path:
    """
    Retourne le chemin absolu vers le fichier de base de données SQLite.

    Suppose que DATABASE_URL est de la forme :
      sqlite:///data/processed/sportsee.db
    """
    url = settings.DATABASE_URL

    if not url.startswith("sqlite:///"):
        raise ValueError(
            f"DATABASE_URL doit être de la forme sqlite:///..., reçu : {url}"
        )

    db_relative = url[len("sqlite:///") :]
    db_path = Path(db_relative)

    # Si le chemin n'est pas absolu, on le considère relatif à la racine du projet
    if not db_path.is_absolute():
        # On suppose que le script est lancé depuis la racine du projet
        db_path = Path.cwd() / db_path

    return db_path.resolve()


def is_database_available() -> bool:
    """
    Vérifie si le fichier de base de données existe.
    """
    db_path = get_database_path()
    return db_path.exists()