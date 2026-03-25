-- Activer les clés étrangères (important en SQLite)
PRAGMA foreign_keys = ON;

-- ========================
-- TABLE : players
-- ========================
CREATE TABLE IF NOT EXISTS players (
    player_id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ========================
-- TABLE : games
-- ========================
CREATE TABLE IF NOT EXISTS games (
    game_id TEXT PRIMARY KEY,
    start_time TEXT NOT NULL,
    end_time TEXT,
    duration_seconds INTEGER,
    nb_players INTEGER NOT NULL CHECK (nb_players > 0)
);

-- ========================
-- TABLE : rounds
-- ========================
CREATE TABLE IF NOT EXISTS rounds (
    round_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    round_number INTEGER NOT NULL CHECK (round_number > 0),
    start_time TEXT NOT NULL,
    end_time TEXT,
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- ========================
-- TABLE : initial_deals
-- ========================
CREATE TABLE IF NOT EXISTS initial_deals (
    initial_deal_id TEXT PRIMARY KEY,
    round_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    initial_hand_value INTEGER NOT NULL CHECK (initial_hand_value >= 0),
    dealer_visible_card TEXT NOT NULL,
    FOREIGN KEY (round_id) REFERENCES rounds(round_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- ========================
-- TABLE : player_actions
-- ========================
CREATE TABLE IF NOT EXISTS player_actions (
    action_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    round_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    action_type TEXT NOT NULL CHECK (
        action_type IN ('hit', 'stand', 'double_down', 'split', 'surrender')
    ),
    hand_value_before INTEGER NOT NULL CHECK (hand_value_before >= 0),
    hand_value_after INTEGER CHECK (hand_value_after >= 0),
    drawn_card TEXT,
    action_order INTEGER NOT NULL CHECK (action_order > 0),
    action_timestamp TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (round_id) REFERENCES rounds(round_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- ========================
-- TABLE : round_results
-- ========================
CREATE TABLE IF NOT EXISTS round_results (
    result_id TEXT PRIMARY KEY,
    round_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    final_hand_value INTEGER NOT NULL CHECK (final_hand_value >= 0),
    dealer_final_value INTEGER NOT NULL CHECK (dealer_final_value >= 0),
    result TEXT NOT NULL CHECK (result IN ('win', 'lose', 'push')),
    has_blackjack INTEGER NOT NULL DEFAULT 0 CHECK (has_blackjack IN (0,1)),
    has_bust INTEGER NOT NULL DEFAULT 0 CHECK (has_bust IN (0,1)),
    bet_amount REAL NOT NULL DEFAULT 0 CHECK (bet_amount >= 0),
    gain_loss REAL NOT NULL DEFAULT 0,
    end_time TEXT NOT NULL,
    FOREIGN KEY (round_id) REFERENCES rounds(round_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- ========================
-- INDEX 
-- ========================
CREATE INDEX IF NOT EXISTS idx_rounds_game_id ON rounds(game_id);
CREATE INDEX IF NOT EXISTS idx_actions_round_id ON player_actions(round_id);
CREATE INDEX IF NOT EXISTS idx_actions_player_id ON player_actions(player_id);
CREATE INDEX IF NOT EXISTS idx_results_player_id ON round_results(player_id);

CREATE INDEX IF NOT EXISTS idx_results_round_id ON round_results(round_id);
CREATE INDEX IF NOT EXISTS idx_initial_deals_round_id ON initial_deals(round_id);
CREATE INDEX IF NOT EXISTS idx_initial_deals_player_id ON initial_deals(player_id);