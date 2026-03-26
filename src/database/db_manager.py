from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent.parent / "blackjack.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_connection()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()


def insert_player(player_id: str, username: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO players (player_id, username)
        VALUES (?, ?)
    """, (player_id, username))

    conn.commit()
    conn.close()


def log_game_started(game_id: str, start_time: str, nb_players: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO games (game_id, start_time, nb_players)
        VALUES (?, ?, ?)
    """, (game_id, start_time, nb_players))

    conn.commit()
    conn.close()

def log_game_ended(game_id: str, end_time: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE games
        SET
            end_time = ?,
            duration_seconds = (
                strftime('%s', replace(?, 'T', ' ')) -
                strftime('%s', replace(start_time, 'T', ' '))
            )
        WHERE game_id = ?
    """, (end_time, end_time, game_id))

    conn.commit()
    conn.close()


def log_round_started(round_id: str, game_id: str, round_number: int, start_time: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO rounds (round_id, game_id, round_number, start_time)
        VALUES (?, ?, ?, ?)
    """, (round_id, game_id, round_number, start_time))

    conn.commit()
    conn.close()


def log_round_ended(round_id: str, end_time: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE rounds
        SET end_time = ?
        WHERE round_id = ?
    """, (end_time, round_id))

    conn.commit()
    conn.close()


def log_initial_deal(
    deal_id: str,
    round_id: str,
    player_id: str,
    initial_hand_value: int,
    dealer_card: str
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO initial_deals (
            initial_deal_id, round_id, player_id,
            initial_hand_value, dealer_visible_card
        )
        VALUES (?, ?, ?, ?, ?)
    """, (deal_id, round_id, player_id, initial_hand_value, dealer_card))

    conn.commit()
    conn.close()


def log_player_action(
    action_id: str,
    game_id: str,
    round_id: str,
    player_id: str,
    action_type: str,
    hand_value_before: int,
    hand_value_after: int | None,
    drawn_card: str | None,
    action_order: int,
    timestamp: str
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO player_actions (
            action_id, game_id, round_id, player_id,
            action_type, hand_value_before, hand_value_after,
            drawn_card, action_order, action_timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        action_id, game_id, round_id, player_id,
        action_type, hand_value_before, hand_value_after,
        drawn_card, action_order, timestamp
    ))

    conn.commit()
    conn.close()


def log_round_result(
    result_id: str,
    round_id: str,
    player_id: str,
    final_hand_value: int,
    dealer_final_value: int,
    result: str,
    has_blackjack: int,
    has_bust: int,
    bet_amount: float,
    gain_loss: float,
    end_time: str
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO round_results (
            result_id, round_id, player_id,
            final_hand_value, dealer_final_value,
            result, has_blackjack, has_bust,
            bet_amount, gain_loss, end_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        result_id, round_id, player_id,
        final_hand_value, dealer_final_value,
        result, has_blackjack, has_bust,
        bet_amount, gain_loss, end_time
    ))

    conn.commit()
    conn.close()