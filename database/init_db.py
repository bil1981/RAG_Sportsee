-- Table des équipes (Teams)
CREATE TABLE IF NOT EXISTS teams (
    team_code VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL
);

-- Table des joueurs (Players)
CREATE TABLE IF NOT EXISTS players (
    player_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    team_code VARCHAR(10) REFERENCES teams(team_code) ON DELETE SET NULL
);

-- Table des matchs (Matches)
CREATE TABLE IF NOT EXISTS matches (
    match_id SERIAL PRIMARY KEY,
    match_date DATE,
    home_team_code VARCHAR(10) REFERENCES teams(team_code),
    away_team_code VARCHAR(10) REFERENCES teams(team_code),
    home_score INT,
    away_score INT
);

-- Table des statistiques par joueur / saison ou match (Stats)
CREATE TABLE IF NOT EXISTS stats (
    stat_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id) ON DELETE CASCADE,
    gp INT,              -- Games Played
    w INT,               -- Wins
    l INT,               -- Losses
    min NUMERIC(5,2),    -- Minutes
    pts NUMERIC(5,2),    -- Points
    fgm NUMERIC(5,2),
    fga NUMERIC(5,2),
    fg_pct NUMERIC(5,2),
    fg3m NUMERIC(5,2),
    fg3a NUMERIC(5,2),
    fg3_pct NUMERIC(5,2),
    ftm NUMERIC(5,2),
    fta NUMERIC(5,2),
    ft_pct NUMERIC(5,2),
    oreb NUMERIC(5,2),
    dreb NUMERIC(5,2),
    reb NUMERIC(5,2),
    ast NUMERIC(5,2),
    tov NUMERIC(5,2),
    stl NUMERIC(5,2),
    blk NUMERIC(5,2),
    plus_minus NUMERIC(5,2),
    offrtg NUMERIC(5,2),
    defrtg NUMERIC(5,2),
    netrtg NUMERIC(5,2),
    usg_pct NUMERIC(5,2),
    ts_pct NUMERIC(5,2)
);

-- Table des rapports et analyses textuelles (Reports)
CREATE TABLE IF NOT EXISTS reports (
    report_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id) ON DELETE CASCADE,
    match_id INT REFERENCES matches(match_id) ON DELETE CASCADE,
    report_type VARCHAR(50), -- e.g., 'scouting', 'playoff_summary'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);