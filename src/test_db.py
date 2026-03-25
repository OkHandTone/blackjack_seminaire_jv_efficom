from datetime import datetime
import uuid

from src.database.db_manager import (
    init_db,
    insert_player,
    log_game_started,
    log_game_ended,
    log_round_started,
    log_round_ended,
    log_initial_deal,
    log_player_action,
    log_round_result,
)


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def main():
    # 1. Initialiser la base
    init_db()
    print("Base initialisée.")

    # 2. Générer des UID
    player_id = str(uuid.uuid4())
    game_id = str(uuid.uuid4())
    round_id = str(uuid.uuid4())
    initial_deal_id = str(uuid.uuid4())
    action_id_1 = str(uuid.uuid4())
    action_id_2 = str(uuid.uuid4())
    result_id = str(uuid.uuid4())

    # 3. Insérer un joueur
    insert_player(player_id, f"Jacques_Test_{player_id[:8]}")
    print("Joueur inséré.")

    # 4. Démarrer une partie
    game_start = now_iso()
    log_game_started(game_id, game_start, nb_players=1)
    print("Partie démarrée.")

    # 5. Démarrer une manche
    round_start = now_iso()
    log_round_started(round_id, game_id, round_number=1, start_time=round_start)
    print("Manche démarrée.")

    # 6. Enregistrer la distribution initiale
    # Exemple : joueur a 16, croupier montre un 9
    log_initial_deal(
        deal_id=initial_deal_id,
        round_id=round_id,
        player_id=player_id,
        initial_hand_value=16,
        dealer_card="9"
    )
    print("Distribution initiale enregistrée.")

    # 7. Action 1 : hit
    log_player_action(
        action_id=action_id_1,
        game_id=game_id,
        round_id=round_id,
        player_id=player_id,
        action_type="hit",
        hand_value_before=16,
        hand_value_after=20,
        drawn_card="4",
        action_order=1,
        timestamp=now_iso()
    )
    print("Action 1 enregistrée : hit.")

    # 8. Action 2 : stand
    log_player_action(
        action_id=action_id_2,
        game_id=game_id,
        round_id=round_id,
        player_id=player_id,
        action_type="stand",
        hand_value_before=20,
        hand_value_after=20,
        drawn_card=None,
        action_order=2,
        timestamp=now_iso()
    )
    print("Action 2 enregistrée : stand.")

    # 9. Résultat final de la manche
    # Exemple : joueur 20, dealer 18 => win
    round_end = now_iso()
    log_round_result(
        result_id=result_id,
        round_id=round_id,
        player_id=player_id,
        final_hand_value=20,
        dealer_final_value=18,
        result="win",
        has_blackjack=0,
        has_bust=0,
        bet_amount=10.0,
        gain_loss=10.0,
        end_time=round_end
    )
    print("Résultat de manche enregistré.")

    # 10. Clôturer la manche
    log_round_ended(round_id, round_end)
    print("Manche terminée.")

    # 11. Clôturer la partie
    game_end = now_iso()
    duration_seconds = 60
    log_game_ended(game_id, game_end, duration_seconds)
    print("Partie terminée.")

    print("Test terminé avec succès.")


if __name__ == "__main__":
    main()