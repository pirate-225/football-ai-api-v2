from data_api import get_team_xg_stats
from predict_match import predict_match
from data_api import get_odds


def get_top_bets(live_data):

    value_bets = []
    overs = []

    for m in live_data[:1]:

        try:

            fixture_id = m["fixture_id"]

            odds_api = get_odds(fixture_id) or {}

            odd_home = odds_api.get("home", 2.0)
            odd_draw = odds_api.get("draw", 3.2)
            odd_away = odds_api.get("away", 2.0)

            xg_home = get_team_xg_stats(
                m["home_id"],
                m["league_id"],
                m["season"]
            )

            xg_away = get_team_xg_stats(
                m["away_id"],
                m["league_id"],
                m["season"]
            )

            pred = predict_match(

                m["home"],
                m["away"],

                odd_home,
                odd_draw,
                odd_away,

                xg_home,
                xg_away,

                5,
                5,

                50,
                50,

                0,
                0,

                m["home_id"],
                m["away_id"]
            )

            if pred is None:
                continue

            # 💰 VALUE BETS
            if (
                pred.get("value_bet") != "Aucun"
                and pred["confidence"] >= 0.08
            ):

                value_bets.append({

                    "match": f"{m['home']} vs {m['away']}",

                    "bet": pred["prediction"],

                    "value_bet": pred.get("value_bet"),

                    "confidence": round(
                        pred["confidence"],
                        3
                    ),

                    "home_prob": round(
                        pred["prob_home"],
                        3
                    ),

                    "draw_prob": round(
                        pred["prob_draw"],
                        3
                    ),

                    "away_prob": round(
                        pred["prob_away"],
                        3
                    )
                })

            # 🔥 OVERS
            if pred["prob_over"] >= 0.55:

                overs.append({

                    "match": f"{m['home']} vs {m['away']}",

                    "bet": f"OVER 2.5 ({round(pred['prob_over'] * 100)}%)",

                    "value": round(
                        pred["prob_over"],
                        3
                    ),

                    "prob": pred["prob_over"]
                })

        except Exception as e:

            print("TOP BET ERROR:", e)

            continue

    value_bets = sorted(
        value_bets,
        key=lambda x: x["confidence"],
        reverse=True
    )

    overs = sorted(
        overs,
        key=lambda x: x["prob"],
        reverse=True
    )

    return {

        "favorites": value_bets[:1],

        "overs": overs[:1]
    }