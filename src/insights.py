import duckdb
import pandas as pd

DB_PATH = "data/processed/pulse360.duckdb"


def get_connection():
    return duckdb.connect(DB_PATH)


def generate_business_insights():
    con = get_connection()

    kpis = con.execute("""
        SELECT
            SUM(revenue) AS total_revenue,
            SUM(margin) AS total_margin,
            COUNT(DISTINCT customer_id) AS active_customers,
            SUM(is_refunded) * 1.0 / COUNT(*) AS refund_rate
        FROM orders_clean
    """).fetchdf()

    offers = con.execute("""
        SELECT offer_type, revenue, margin, avg_margin_rate
        FROM offer_performance
        ORDER BY margin DESC
    """).fetchdf()

    channels = con.execute("""
        SELECT channel, revenue, margin, roas, cac
        FROM channel_performance
        ORDER BY revenue DESC
    """).fetchdf()

    segments = con.execute("""
        SELECT segment, customers_count, revenue, margin, avg_satisfaction
        FROM customer_segments
        ORDER BY revenue DESC
    """).fetchdf()

    con.close()

    total_revenue = float(kpis.loc[0, "total_revenue"])
    total_margin = float(kpis.loc[0, "total_margin"])
    active_customers = int(kpis.loc[0, "active_customers"])
    refund_rate = float(kpis.loc[0, "refund_rate"])

    margin_rate = total_margin / total_revenue if total_revenue else 0

    top_offer = offers.iloc[0]["offer_type"]
    top_channel = channels.iloc[0]["channel"]
    top_segment = segments.iloc[0]["segment"]

    weakest_channel = channels.sort_values("roas", ascending=True).iloc[0]["channel"]

    revenue_per_customer = total_revenue / active_customers if active_customers else 0

    executive_summary = (
    f"Pulse360 détecte une activité rentable avec {total_revenue:,.0f} € de chiffre d’affaires "
    f"et un taux de marge de {margin_rate:.1%}. "
    f"La performance est portée par le segment {top_segment} et l’offre {top_offer}. "
    f"Cependant, l’efficacité marketing reste hétérogène : le canal {weakest_channel} doit être analysé avant d’augmenter les budgets."
)

    top_findings = [
        f"L’offre {top_offer} est le principal moteur de rentabilité.",
        f"Le canal {top_channel} génère le plus fort volume de chiffre d’affaires.",
        f"Le revenu moyen par client est de {revenue_per_customer:,.0f} €.",
        f"Le taux de remboursement reste à {refund_rate:.1%}, ce qui permet de surveiller la qualité commerciale.",
    ]

    business_signals = pd.DataFrame([
        {
            "Signal": "Rentabilité",
            "Statut": "Solide" if margin_rate >= 0.35 else "À surveiller",
            "Lecture business": "La marge permet de soutenir la croissance." if margin_rate >= 0.35 else "La marge doit être renforcée."
        },
        {
            "Signal": "Efficacité marketing",
            "Statut": "À surveiller",
            "Lecture business": f"Le canal {weakest_channel} présente un rendement plus faible."
        },
        {
            "Signal": "Base client",
            "Statut": "Solide" if active_customers >= 1000 else "Fragile",
            "Lecture business": f"{active_customers:,} clients actifs observés sur la période."
        },
        {
            "Signal": "Qualité commerciale",
            "Statut": "Stable" if refund_rate < 0.12 else "Risque",
            "Lecture business": "Le taux de remboursement reste maîtrisé." if refund_rate < 0.12 else "Les remboursements doivent être analysés."
        },
    ])

    return {
        "executive_summary": executive_summary,
        "top_findings": top_findings,
        "business_signals": business_signals,
        "top_offer": top_offer,
        "top_channel": top_channel,
        "weakest_channel": weakest_channel,
        "top_segment": top_segment,
        "revenue_per_customer": revenue_per_customer,
    }