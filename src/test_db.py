import random
import time
import uuid
from datetime import datetime

from database.db_manager import (
    init_db,
    insert_player,
    log_game_ended,
    log_game_started,
    log_initial_deal,
    log_player_action,
    log_round_ended,
    log_round_result,
    log_round_started,
)


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def simulate_round():
    """
    Simule une manche simple de blackjack.
    Retourne un dictionnaire contenant :
    - valeur initiale de la main
    - carte visible du croupier
    - liste des actions
    - score final joueur
    - score final croupier
    - résultat
    - has_blackjack
    - has_bust
    - mise
    - gain/perte
    """

    bet_amount = 10.0

    # Main initiale du joueur et carte visible du croupier
    initial_hand_value = random.randint(12, 20)
    dealer_visible_card = str(random.randint(2, 11))

    actions = []
    current_value = initial_hand_value
    action_order = 1

    # Petite logique de décision simple :
    # si score faible, le joueur a plus de chances de tirer
    # si score élevé, il a plus de chances de rester
    while current_value < 21:
        if current_value <= 14:
            action_type = random.choices(["hit", "stand"], weights=[80, 20])[0]
        elif current_value <= 17:
            action_type = random.choices(["hit", "stand"], weights=[50, 50])[0]
        else:
            action_type = random.choices(["hit", "stand"], weights=[20, 80])[0]

        if action_type == "stand":
            actions.append({
                "action_type": "stand",
                "hand_value_before": current_value,
                "hand_value_after": current_value,
                "drawn_card": None,
                "action_order": action_order,
                "timestamp": now_iso()
            })
            break

        drawn_card_value = random.randint(1, 10)
        new_value = current_value + drawn_card_value

        actions.append({
            "action_type": "hit",
            "hand_value_before": current_value,
            "hand_value_after": new_value,
            "drawn_card": str(drawn_card_value),
            "action_order": action_order,
            "timestamp": now_iso()
        })

        current_value = new_value
        action_order += 1

        if current_value > 21:
            break

    final_hand_value = current_value
    has_blackjack = 1 if initial_hand_value == 21 else 0
    has_bust = 1 if final_hand_value > 21 else 0

    # Logique simplifiée du croupier
    dealer_final_value = random.randint(17, 23)

    # Détermination du résultat
    if has_bust:
        result = "lose"
    elif dealer_final_value > 21:
        result = "win"
    elif final_hand_value > dealer_final_value:
        result = "win"
    elif final_hand_value == dealer_final_value:
        result = "push"
    else:
        result = "lose"

    # Gain / perte
    if result == "win":
        gain_loss = bet_amount
    elif result == "lose":
        gain_loss = -bet_amount
    else:
        gain_loss = 0.0

    return {
        "initial_hand_value": initial_hand_value,
        "dealer_visible_card": dealer_visible_card,
        "actions": actions,
        "final_hand_value": final_hand_value,
        "dealer_final_value": dealer_final_value,
        "result": result,
        "has_blackjack": has_blackjack,
        "has_bust": has_bust,
        "bet_amount": bet_amount,
        "gain_loss": gain_loss,
    }


def main():
    # 1. Initialiser la base
    init_db()
    print("Base initialisée.")

    # 2. Générer des UID principaux
    player_id = str(uuid.uuid4())
    game_id = str(uuid.uuid4())
    round_id = str(uuid.uuid4())
    initial_deal_id = str(uuid.uuid4())
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

    # 6. Simuler une manche réaliste
    simulation = simulate_round()

    # 7. Enregistrer la distribution initiale
    log_initial_deal(
        deal_id=initial_deal_id,
        round_id=round_id,
        player_id=player_id,
        initial_hand_value=simulation["initial_hand_value"],
        dealer_card=simulation["dealer_visible_card"]
    )
    print("Distribution initiale enregistrée.")

    # 8. Enregistrer les actions simulées
    for action in simulation["actions"]:
        log_player_action(
            action_id=str(uuid.uuid4()),
            game_id=game_id,
            round_id=round_id,
            player_id=player_id,
            action_type=action["action_type"],
            hand_value_before=action["hand_value_before"],
            hand_value_after=action["hand_value_after"],
            drawn_card=action["drawn_card"],
            action_order=action["action_order"],
            timestamp=action["timestamp"]
        )
        print(f"Action enregistrée : {action['action_type']}")

    # Petite pause pour éviter une durée nulle
    time.sleep(1)

    # 9. Résultat final de la manche
    round_end = now_iso()
    log_round_result(
        result_id=result_id,
        round_id=round_id,
        player_id=player_id,
        final_hand_value=simulation["final_hand_value"],
        dealer_final_value=simulation["dealer_final_value"],
        result=simulation["result"],
        has_blackjack=simulation["has_blackjack"],
        has_bust=simulation["has_bust"],
        bet_amount=simulation["bet_amount"],
        gain_loss=simulation["gain_loss"],
        end_time=round_end
    )
    print("Résultat de manche enregistré.")

    # 10. Clôturer la manche
    log_round_ended(round_id, round_end)
    print("Manche terminée.")

    # 11. Clôturer la partie
    game_end = now_iso()
    log_game_ended(game_id, game_end)
    print("Partie terminée.")

    print("Test réaliste terminé avec succès.")


if __name__ == "__main__":
    main()
