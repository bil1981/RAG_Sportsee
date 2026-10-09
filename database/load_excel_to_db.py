import pandas as pd
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. SQLAlchemy Engine Setup (SQLite ou PostgreSQL)
DATABASE_URL = "sqlite:///nba_analytics.db"  # Ou postgresql://user:pass@localhost:5432/nbadb
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# 2. Modèles Pydantic pour la validation
class PlayerStatSchema(BaseModel):
    player: str = Field(..., alias="Player")
    team: str = Field(..., alias="Team")
    age: Optional[int] = Field(None, alias="Age")
    gp: Optional[int] = Field(None, alias="GP")
    w: Optional[int] = Field(None, alias="W")
    l: Optional[int] = Field(None, alias="L")
    min: Optional[float] = Field(None, alias="Min")
    pts: Optional[float] = Field(None, alias="PTS")
    fg_pct: Optional[float] = Field(None, alias="FG%")
    fg3_pct: Optional[float] = Field(None, alias="3P%")
    ast: Optional[float] = Field(None, alias="AST")
    reb: Optional[float] = Field(None, alias="REB")
    netrtg: Optional[float] = Field(None, alias="NETRTG")
    ts_pct: Optional[float] = Field(None, alias="TS%")

# 3. Traitement et Ingestion
def load_data_from_excel(file_path: str):
    # Charge le DataFrame
    df_players = pd.read_excel(file_path, sheet_name="Données NBA", header=1)
    
    # 1. Convertit tous les noms de colonnes du DataFrame en str
    df_players.columns = [str(col) for col in df_players.columns]
    
    session = SessionLocal()
    
    for _, row in df_players.iterrows():
        try:
            # 2. Nettoie le dictionnaire en forçant des clés de type str
            record = {str(k): v for k, v in row.dropna().to_dict().items()}
            
            # Validation Pydantic
            validated_data = PlayerStatSchema(**record)
            
            # Insertion en base...
            
        except ValidationError as e:
            print(f"Ligne invalide ignorée ({row.get('Player')}): {e}")

    session.commit()
    session.close()

if __name__ == "__main__":
    load_data_from_excel("./inputs/regular_NBA.xlsx")