import duckdb
import pandas as pd

DB_PATH = "data/processed/pulse360.duckdb"


def generate_recommendations():
    con = duckdb.connect(DB_PATH)

    channels = con.execute("SELECT * FROM channel_performance").fetchdf()
    segments = con.execute("SELECT * FROM customer_segments").fetchdf()
    offers = con.execute("SELECT * FROM offer_performance").fetchdf()

    con.close()

    recommendations = []

    # -----------------------------
    # MARKETING — recommandation consolidée
    # -----------------------------

    avg_roas = channels["roas"].mean()
    weak_channels = channels[channels["roas"] < avg_roas].sort_values("roas")

    if not weak_channels.empty:
        weak_names = ", ".join(weak_channels["channel"].head(3).tolist())

        recommendations.append({
            "priority": "P0",
            "title": "Optimiser les investissements marketing",
            "category": "Marketing",
            "description": (
                f"Les canaux {weak_names} présentent un rendement inférieur à la moyenne. "
                "La direction doit analyser ces dépenses et réallouer le budget vers les canaux les plus rentables."
            ),
            "impact": "Élevé"
        })

    # -----------------------------
    # CROISSANCE — offres rentables
    # -----------------------------

    top_offers = offers.sort_values("margin", ascending=False).head(2)
    top_offer_names = ", ".join(top_offers["offer_type"].tolist())

    recommendations.append({
        "priority": "P1",
        "title": "Accélérer les offres les plus rentables",
        "category": "Croissance",
        "description": (
            f"Les offres {top_offer_names} contribuent fortement à la marge. "
            "Elles doivent être priorisées dans les actions commerciales et marketing."
        ),
        "impact": "Élevé"
    })

    # -----------------------------
    # CLIENTS — satisfaction
    # -----------------------------

    avg_satisfaction = segments["avg_satisfaction"].mean()
    weak_segments = segments[segments["avg_satisfaction"] < avg_satisfaction].sort_values("avg_satisfaction")

    if not weak_segments.empty:
        weak_segment_names = ", ".join(weak_segments["segment"].head(2).tolist())

        recommendations.append({
            "priority": "P1",
            "title": "Renforcer l’expérience des segments fragiles",
            "category": "Clients",
            "description": (
                f"Les segments {weak_segment_names} affichent une satisfaction inférieure à la moyenne. "
                "Un plan d’amélioration ciblé peut protéger la fidélisation et la valeur client."
            ),
            "impact": "Moyen"
        })

    return pd.DataFrame(recommendations)