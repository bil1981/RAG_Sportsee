# src/sportsee/database/models.py
from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class PlayerRow(BaseModel):
    model_config = ConfigDict(extra="ignore")

    player_id: int
    player_name: str = Field(min_length=1)
    team: str | None = None
    position: str | None = None


class MatchRow(BaseModel):
    model_config = ConfigDict(extra="ignore")

    match_id: int
    match_date: date
    home_team: str
    away_team: str
    home_score: int | None = Field(default=None, ge=0)
    away_score: int | None = Field(default=None, ge=0)
    season: str | None = None


class StatsRow(BaseModel):
    model_config = ConfigDict(extra="ignore")

    match_id: int
    player_id: int
    team: str
    is_home: bool
    points: int = Field(default=0, ge=0)
    rebounds: int = Field(default=0, ge=0)
    assists: int = Field(default=0, ge=0)
    three_pa: int = Field(default=0, ge=0)
    three_pm: int = Field(default=0, ge=0)