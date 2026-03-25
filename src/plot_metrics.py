from pathlib import Path
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "blackjack.db"
OUTPUT_DIR = BASE_DIR.parent / "charts"


def get_connection():
    return sqlite3.connect(DB_PATH)


def ensure_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def plot_results_distribution(conn):
    query = """
        SELECT result, COUNT(*) AS count
        FROM round_results
        GROUP BY result
        ORDER BY result;
    """
    df = pd.read_sql_query(query, conn)

    if df.empty:
        print("Aucune donnée pour le graphe des résultats.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(df["result"], df["count"])
    plt.title("Répartition des résultats")
    plt.xlabel("Résultat")
    plt.ylabel("Nombre de manches")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "results_distribution.png")
    plt.close()

    print("Graphe enregistré : results_distribution.png")


def plot_actions_frequency(conn):
    query = """
        SELECT action_type, COUNT(*) AS count
        FROM player_actions
        GROUP BY action_type
        ORDER BY action_type;
    """
    df = pd.read_sql_query(query, conn)

    if df.empty:
        print("Aucune donnée pour le graphe des actions.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(df["action_type"], df["count"])
    plt.title("Fréquence des actions du joueur")
    plt.xlabel("Action")
    plt.ylabel("Nombre d'occurrences")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "actions_frequency.png")
    plt.close()

    print("Graphe enregistré : actions_frequency.png")


def plot_bust_rate(conn):
    query = """
        SELECT
            SUM(has_bust) AS bust_count,
            COUNT(*) AS total_count
        FROM round_results;
    """
    df = pd.read_sql_query(query, conn)

    if df.empty or df.loc[0, "total_count"] == 0:
        print("Aucune donnée pour le graphe du bust rate.")
        return

    bust_count = int(df.loc[0, "bust_count"] or 0)
    total_count = int(df.loc[0, "total_count"])
    non_bust_count = total_count - bust_count

    labels = ["Bust", "Non bust"]
    values = [bust_count, non_bust_count]

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Taux de dépassement de 21")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "bust_rate.png")
    plt.close()

    print("Graphe enregistré : bust_rate.png")


def plot_average_game_duration(conn):
    query = """
        SELECT game_id, duration_seconds
        FROM games
        WHERE duration_seconds IS NOT NULL
        ORDER BY start_time;
    """
    df = pd.read_sql_query(query, conn)

    if df.empty:
        print("Aucune donnée pour le graphe de durée des parties.")
        return

    plt.figure(figsize=(10, 5))
    plt.bar(df["game_id"].astype(str), df["duration_seconds"])
    plt.title("Durée des parties")
    plt.xlabel("Game ID")
    plt.ylabel("Durée (secondes)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "game_durations.png")
    plt.close()

    print("Graphe enregistré : game_durations.png")


def main():
    ensure_output_dir()

    if not DB_PATH.exists():
        print(f"Base de données introuvable : {DB_PATH}")
        return

    conn = get_connection()

    try:
        plot_results_distribution(conn)
        plot_actions_frequency(conn)
        plot_bust_rate(conn)
        plot_average_game_duration(conn)
        print(f"Tous les graphes sont enregistrés dans : {OUTPUT_DIR}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()