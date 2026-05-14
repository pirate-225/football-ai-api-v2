from predict_match import predict_match
from data_api import get_odds


def get_top_bets(live_data):

    favorites = []
    overs = []

    for m in live_data[:500]:

        try:

            fixture_id = m["fixture_id"]

            # 🔥 ODDS API
            odds_api = get_odds(fixture_id) or {}

            odd_home = odds_api.get("home", 2.0)
            odd_draw = odds_api.get("draw", 3.2)
            odd_away = odds_api.get("away", 2.0)

            # 🔥 VALEURS LÉGÈRES
            xg_home = {"xg_for": 1.4, "xg_against": 1.0}
            xg_away = {"xg_for": 1.1, "xg_against": 1.2}

            shots_home = 5
            shots_away = 5

            pos_home = 50
            pos_away = 50

            pred = predict_match(

                m["home"],
                m["away"],

                odd_home,
                odd_draw,
                odd_away,

                xg_home,
                xg_away,

                shots_home,
                shots_away,

                pos_home,
                pos_away,

                0,
                0,

                m["home_id"],
                m["away_id"]
            )

            if pred is None:
                continue

            # 🔥 FAVORIS HOME
            if (
                pred["prob_home"] >= 0.60
                and 1.3 <= odd_home <= 2.15
                and abs(pred["xg_home"] - pred["xg_away"]) >= 0.1
            ):

                favorites.append({
                    "match": f"{m['home']} vs {m['away']}",
                    "bet": f"HOME ({round(pred['prob_home'] * 100)}%)",
                    "value": round(pred["prob_home"], 3),
                    "prob": pred["prob_home"]
                })

            # 🔥 FAVORIS AWAY
            if (
                pred["prob_away"] >= 0.60
                and 1.3 <= odd_away <= 2.15
                and abs(pred["xg_home"] - pred["xg_away"]) >= 0.1
            ):

                favorites.append({
                    "match": f"{m['home']} vs {m['away']}",
                    "bet": f"AWAY ({round(pred['prob_away'] * 100)}%)",
                    "value": round(pred["prob_away"], 3),
                    "prob": pred["prob_away"]
                })

            # 🔥 OVERS
            if pred["prob_over"] >= 0.53:

                overs.append({
                    "match": f"{m['home']} vs {m['away']}",
                    "bet": f"OVER 2.5 ({round(pred['prob_over'] * 100)}%)",
                    "value": round(pred["prob_over"], 3),
                    "prob": pred["prob_over"]
                })

        except Exception as e:

            print("TOP BET ERROR:", e)

            continue

    favorites = sorted(
        favorites,
        key=lambda x: x["prob"],
        reverse=True
    )

    overs = sorted(
        overs,
        key=lambda x: x["prob"],
        reverse=True
    )

    return {
        "favorites": favorites[:500],
        "overs": overs[:500]
    }