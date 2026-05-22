import streamlit as st
import altair as alt
import pandas as pd

from src.build_warehouse import build_warehouse
from src.transform_data import run_transformations

from src.metrics import (
    get_executive_kpis,
    get_monthly_revenue,
    get_revenue_by_offer,
    get_channel_performance,
    get_customer_segments,
)

from src.recommendations import generate_recommendations
from src.insights import generate_business_insights


# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="Pulse360 — Intelligence Décisionnelle Exécutive",
    page_icon="◉",
    layout="wide",
)


# ==================================================
# STYLE PREMIUM
# ==================================================

st.markdown(
    """
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(193,18,31,0.24), transparent 28%),
        radial-gradient(circle at bottom right, rgba(212,175,55,0.14), transparent 30%),
        linear-gradient(135deg, #07070A 0%, #101018 48%, #181820 100%);
    color: #F7F3EA;
}

section[data-testid="stSidebar"] {
    background: #08080C;
    border-right: 1px solid rgba(255,255,255,0.08);
}

h1 {
    color: #F7F3EA;
    font-size: 52px !important;
    letter-spacing: -0.055em;
    line-height: 1.05;
}

h2, h3 {
    color: #F7F3EA;
    letter-spacing: -0.035em;
}

p, li, label, span {
    color: #D8D3C8;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 20px;
    border-radius: 22px;
    box-shadow: 0 18px 45px rgba(0,0,0,0.25);
}

[data-testid="stMetricLabel"] {
    color: #A7A7B0;
}

[data-testid="stMetricValue"] {
    color: #F7F3EA;
    font-size: 28px;
}

.pulse-hero {
    padding: 50px;
    border-radius: 34px;
    background:
        radial-gradient(circle at top left, rgba(193,18,31,0.38), transparent 36%),
        linear-gradient(135deg, rgba(255,255,255,0.09), rgba(255,255,255,0.025));
    border: 1px solid rgba(255,255,255,0.13);
    box-shadow: 0 28px 75px rgba(0,0,0,0.38);
    margin-bottom: 32px;
}

.pulse-badge {
    display: inline-block;
    padding: 8px 15px;
    border-radius: 999px;
    background: rgba(193,18,31,0.22);
    color: #F7F3EA;
    border: 1px solid rgba(193,18,31,0.60);
    font-size: 13px;
    margin-bottom: 18px;
}

.pulse-card {
    padding: 25px;
    border-radius: 24px;
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 18px 45px rgba(0,0,0,0.25);
    height: 100%;
}

.pulse-card-strong {
    padding: 30px;
    border-radius: 28px;
    background:
        radial-gradient(circle at top left, rgba(212,175,55,0.18), transparent 32%),
        rgba(255,255,255,0.06);
    border: 1px solid rgba(212,175,55,0.25);
    box-shadow: 0 18px 45px rgba(0,0,0,0.25);
}

.pulse-alert {
    padding: 28px;
    border-radius: 26px;
    background:
        radial-gradient(circle at top left, rgba(193,18,31,0.30), transparent 30%),
        rgba(255,255,255,0.060);
    border: 1px solid rgba(193,18,31,0.38);
    box-shadow: 0 18px 45px rgba(0,0,0,0.25);
}

.pulse-decision {
    padding: 30px;
    border-radius: 28px;
    background:
        radial-gradient(circle at top left, rgba(212,175,55,0.20), transparent 32%),
        linear-gradient(135deg, rgba(255,255,255,0.07), rgba(255,255,255,0.025));
    border: 1px solid rgba(212,175,55,0.32);
    box-shadow: 0 22px 55px rgba(0,0,0,0.32);
}

.pulse-muted {
    color: #A7A7B0;
    font-size: 15px;
}

.pulse-score {
    font-size: 64px;
    font-weight: 850;
    color: #D4AF37;
    line-height: 1;
}

.pulse-red {
    color: #FF4D5A;
    font-weight: 850;
}

.pulse-gold {
    color: #D4AF37;
    font-weight: 850;
}

.pulse-green {
    color: #7DD87D;
    font-weight: 850;
}

div.stButton > button {
    border-radius: 14px;
    padding: 0.75rem 1rem;
    border: 1px solid rgba(255,255,255,0.16);
    background: linear-gradient(135deg, #C1121F, #780000);
    color: white;
    font-weight: 750;
}

div.stDownloadButton > button {
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.16);
}
</style>
""",
    unsafe_allow_html=True,
)


# ==================================================
# SESSION STATE
# ==================================================

PAGES = ["Accueil", "Dashboard", "Salle de Décision"]

DEMO_MAPPING = {
    "Démo KULTURA Hub": "kultura",
    "Démo E-commerce": "ecommerce",
    "Démo SaaS": "saas",
}

SOURCE_OPTIONS = [
    "Démo KULTURA Hub",
    "Démo E-commerce",
    "Démo SaaS",
    "Importer mes CSV",
]

if "page" not in st.session_state:
    st.session_state.page = "Accueil"

if "data_mode" not in st.session_state:
    st.session_state.data_mode = "Démo KULTURA Hub"

if "active_demo" not in st.session_state:
    st.session_state.active_demo = "kultura"


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("Pulse360")
st.sidebar.caption("Intelligence Décisionnelle Exécutive")

selected_page = st.sidebar.radio(
    "Navigation",
    PAGES,
    index=PAGES.index(st.session_state.page),
)
st.session_state.page = selected_page

st.sidebar.divider()
st.sidebar.caption("Source des données")

data_choice = st.sidebar.radio(
    "Choisir la source",
    SOURCE_OPTIONS,
    index=SOURCE_OPTIONS.index(st.session_state.data_mode),
)
st.session_state.data_mode = data_choice

if st.session_state.data_mode in DEMO_MAPPING:
    st.sidebar.success(f"{st.session_state.data_mode} sélectionnée")
else:
    st.sidebar.warning("Mode import activé")

st.sidebar.divider()
st.sidebar.caption("Modèles CSV")

template_files = {
    "Clients": "data/templates/customers_template.csv",
    "Commandes": "data/templates/orders_template.csv",
    "Marketing": "data/templates/marketing_spend_template.csv",
    "Satisfaction": "data/templates/satisfaction_template.csv",
    "Événements": "data/templates/events_template.csv",
}

for label, path in template_files.items():
    try:
        with open(path, "rb") as file:
            st.sidebar.download_button(
                label=f"Télécharger {label}",
                data=file,
                file_name=path.split("/")[-1],
                mime="text/csv",
                use_container_width=True,
            )
    except FileNotFoundError:
        pass


# ==================================================
# DEMO LAUNCH
# ==================================================

def launch_selected_demo():
    selected_demo = DEMO_MAPPING.get(st.session_state.data_mode)

    if selected_demo:
        build_warehouse(selected_demo)
        run_transformations()
        st.session_state.active_demo = selected_demo
        st.session_state.page = "Dashboard"
        st.rerun()


# ==================================================
# DATA LOADING
# ==================================================

kpis = get_executive_kpis()
monthly = get_monthly_revenue()
offers = get_revenue_by_offer()
channels = get_channel_performance()
segments = get_customer_segments()
recommendations = generate_recommendations()
insights = generate_business_insights()

total_revenue = float(kpis.loc[0, "total_revenue"])
total_margin = float(kpis.loc[0, "total_margin"])
active_customers = int(kpis.loc[0, "active_customers"])
refund_rate = float(kpis.loc[0, "refund_rate"])
margin_rate = total_margin / total_revenue if total_revenue else 0
total_cost = total_revenue - total_margin

revenue_per_customer = insights["revenue_per_customer"]

business_health_score = round(
    (margin_rate * 100 * 0.45)
    + ((1 - refund_rate) * 100 * 0.25)
    + (min(active_customers / 1500, 1) * 100 * 0.30),
    0,
)

max_value = max(
    float(offers["revenue"].max()),
    float(channels["revenue"].max()),
)

top_offer = insights["top_offer"]
top_segment = insights["top_segment"]
weakest_channel = insights["weakest_channel"]


# ==================================================
# ACCUEIL
# ==================================================

if st.session_state.page == "Accueil":
    st.markdown(
        """
<div class="pulse-hero">
    <div class="pulse-badge">Pilotage · Performance · Rentabilité · Croissance</div>
    <h1>Pulse360 — Intelligence Décisionnelle Exécutive</h1>
    <p style="font-size:21px; max-width:930px;">
        Transformez vos données business en décisions claires, compréhensibles et directement exploitables.
    </p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.subheader("Choisissez une démonstration")

    demo_col1, demo_col2 = st.columns([1.3, 1])

    with demo_col1:
        st.markdown(
            f"""
<div class="pulse-card">
<h3>Démo sélectionnée</h3>
<p class="pulse-muted">
Source actuelle : <b>{st.session_state.data_mode}</b>
</p>
<p class="pulse-muted">
Sélectionnez une démo dans la barre latérale, puis lancez l’analyse.
Chaque démo simule un modèle économique différent.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with demo_col2:
        if st.session_state.data_mode in DEMO_MAPPING:
            if st.button("Lancer la démo", use_container_width=True):
                launch_selected_demo()
        else:
            st.info("Le mode import est préparé. Sélectionnez une démo pour lancer l’analyse.")

    st.divider()

    st.subheader("Pourquoi Pulse360 ?")

    st.markdown(
        """
<div class="pulse-card">
<p style="font-size:18px; line-height:1.7;">
Les entreprises disposent souvent de données dispersées entre ventes, marketing, clients et satisfaction.
Pulse360 centralise ces informations pour répondre à une question simple :
<b>que doit faire la direction maintenant ?</b>
</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("Ce que Pulse360 détecte automatiquement")

    detect_col1, detect_col2, detect_col3 = st.columns(3)

    with detect_col1:
        st.markdown(
            """
<div class="pulse-card">
<h3>Rentabilité</h3>
<p class="pulse-muted">
Identifie les offres qui créent réellement de la marge et celles qui consomment des ressources.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with detect_col2:
        st.markdown(
            """
<div class="pulse-card">
<h3>Marketing</h3>
<p class="pulse-muted">
Repère les canaux à surveiller pour éviter de financer des investissements peu performants.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with detect_col3:
        st.markdown(
            """
<div class="pulse-card">
<h3>Décisions</h3>
<p class="pulse-muted">
Transforme les signaux business en actions prioritaires pour la direction.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("Aperçu du dataset actif")

    preview_col1, preview_col2, preview_col3, preview_col4 = st.columns(4)

    preview_col1.metric("Clients", "1 500")
    preview_col2.metric("Transactions", "10 000")
    preview_col3.metric("Période", "18 mois")
    preview_col4.metric("Score Business", f"{int(business_health_score)}/100")

    left_preview, right_preview = st.columns([1.35, 1])

    with left_preview:
        st.subheader("Aperçu du chiffre d’affaires")

        preview_chart = (
            alt.Chart(monthly)
            .mark_area(opacity=0.45, color="#C1121F")
            .encode(
                x=alt.X("month:T", title="Mois"),
                y=alt.Y("revenue:Q", title="Chiffre d’affaires"),
                tooltip=["month:T", "revenue:Q", "margin:Q"],
            )
            .properties(height=235)
        )

        st.altair_chart(preview_chart, use_container_width=True)

    with right_preview:
        st.markdown(
            f"""
<div class="pulse-card-strong">
<p class="pulse-muted">Score de Santé Business</p>
<div class="pulse-score">{int(business_health_score)}/100</div>
<p class="pulse-muted">
Performance globale saine. La marge reste solide mais certains investissements marketing doivent être surveillés.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    if st.session_state.data_mode == "Importer mes CSV":
        st.subheader("Importer vos données")

        st.markdown(
            """
<div class="pulse-card">
<p style="font-size:18px; line-height:1.7;">
Importez vos fichiers CSV pour générer automatiquement votre dashboard exécutif.
Les fichiers <b>customers.csv</b>, <b>orders.csv</b> et <b>marketing_spend.csv</b>
sont obligatoires. Les fichiers <b>satisfaction.csv</b> et <b>events.csv</b> sont optionnels.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown("### Téléverser les fichiers CSV")

        uploaded_customers = st.file_uploader(
            "👥 customers.csv — obligatoire",
            type=["csv"],
            key="uploaded_customers",
        )

        uploaded_orders = st.file_uploader(
            "🛒 orders.csv — obligatoire",
            type=["csv"],
            key="uploaded_orders",
        )

        uploaded_marketing = st.file_uploader(
            "📢 marketing_spend.csv — obligatoire",
            type=["csv"],
            key="uploaded_marketing",
        )

        uploaded_satisfaction = st.file_uploader(
            "⭐ satisfaction.csv — optionnel",
            type=["csv"],
            key="uploaded_satisfaction",
        )

        uploaded_events = st.file_uploader(
            "📅 events.csv — optionnel",
            type=["csv"],
            key="uploaded_events",
        )

        detected_files = sum(
            [
                uploaded_customers is not None,
                uploaded_orders is not None,
                uploaded_marketing is not None,
                uploaded_satisfaction is not None,
                uploaded_events is not None,
            ]
        )

        status_df = pd.DataFrame(
            [
                {
                    "Fichier": "customers.csv",
                    "Statut": "Détecté" if uploaded_customers else "Manquant",
                    "Obligatoire": "Oui",
                },
                {
                    "Fichier": "orders.csv",
                    "Statut": "Détecté" if uploaded_orders else "Manquant",
                    "Obligatoire": "Oui",
                },
                {
                    "Fichier": "marketing_spend.csv",
                    "Statut": "Détecté" if uploaded_marketing else "Manquant",
                    "Obligatoire": "Oui",
                },
                {
                    "Fichier": "satisfaction.csv",
                    "Statut": "Détecté" if uploaded_satisfaction else "Manquant",
                    "Obligatoire": "Non",
                },
                {
                    "Fichier": "events.csv",
                    "Statut": "Détecté" if uploaded_events else "Manquant",
                    "Obligatoire": "Non",
                },
            ]
        )

        st.markdown(
            f"""
<div class="pulse-card-strong">
<h3>{detected_files}/5 fichiers détectés</h3>
<p class="pulse-muted">
Le lancement est disponible dès que les 3 fichiers obligatoires sont présents.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

        st.dataframe(status_df, use_container_width=True, hide_index=True)

        required_ready = (
            uploaded_customers is not None
            and uploaded_orders is not None
            and uploaded_marketing is not None
        )

        if required_ready:
            st.success("Fichiers obligatoires détectés. Vous pouvez lancer l’analyse.")

            if st.button("🚀 Importer & Lancer l’analyse", use_container_width=True):
                import os

                upload_dir = "data/uploaded"
                os.makedirs(upload_dir, exist_ok=True)

                with st.spinner("Analyse en cours : import, validation, warehouse et KPI..."):
                    uploaded_customers.seek(0)
                    with open(f"{upload_dir}/customers.csv", "wb") as file:
                        file.write(uploaded_customers.getbuffer())

                    uploaded_orders.seek(0)
                    with open(f"{upload_dir}/orders.csv", "wb") as file:
                        file.write(uploaded_orders.getbuffer())

                    uploaded_marketing.seek(0)
                    with open(f"{upload_dir}/marketing_spend.csv", "wb") as file:
                        file.write(uploaded_marketing.getbuffer())

                    if uploaded_satisfaction is not None:
                        uploaded_satisfaction.seek(0)
                        with open(f"{upload_dir}/satisfaction.csv", "wb") as file:
                            file.write(uploaded_satisfaction.getbuffer())

                    if uploaded_events is not None:
                        uploaded_events.seek(0)
                        with open(f"{upload_dir}/events.csv", "wb") as file:
                            file.write(uploaded_events.getbuffer())

                    build_warehouse("uploaded")
                    run_transformations()

                    st.session_state.active_demo = "uploaded"
                    st.session_state.page = "Dashboard"

                st.success("✅ Analyse terminée. Redirection vers le dashboard.")
                st.rerun()
        else:
            st.warning(
                "Veuillez importer au minimum customers.csv, orders.csv et marketing_spend.csv."
            )
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
<div class="pulse-card">
<h3>1. Organiser</h3>
<p class="pulse-muted">Centraliser les données clients, ventes et marketing dans une vue claire.</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
<div class="pulse-card">
<h3>2. Comprendre</h3>
<p class="pulse-muted">Identifier les moteurs de croissance, de rentabilité et de performance.</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
<div class="pulse-card">
<h3>3. Décider</h3>
<p class="pulse-muted">Prioriser les actions business à partir de signaux fiables.</p>
</div>
""",
            unsafe_allow_html=True,
        )


# ==================================================
# DASHBOARD
# ==================================================

elif st.session_state.page == "Dashboard":
    st.title("Dashboard Exécutif")
    st.caption("Une page longue pour comprendre la performance, la rentabilité et les signaux business.")

    st.subheader("Vue d’ensemble")

    st.markdown(
        f"""
<div class="pulse-card">
<p style="font-size:18px; line-height:1.7;">
{insights["executive_summary"]}
</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("Indicateurs clés")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Chiffre d’affaires", f"{total_revenue:,.0f} €")
    col2.metric("Marge", f"{total_margin:,.0f} €")
    col3.metric("Taux de marge", f"{margin_rate:.1%}")
    col4.metric("Score Business", f"{int(business_health_score)}/100")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Clients actifs", f"{active_customers:,}")
    col6.metric("Remboursements", f"{refund_rate:.1%}")
    col7.metric("Revenu moyen / client", f"{revenue_per_customer:,.0f} €")
    col8.metric("Canal à surveiller", weakest_channel)

    st.divider()

    st.subheader("Signaux prioritaires")

    radar_col1, radar_col2, radar_col3, radar_col4 = st.columns(4)

    with radar_col1:
        st.markdown(
            """
<div class="pulse-card">
<h3>Rentabilité</h3>
<p class="pulse-gold">Solide</p>
<p class="pulse-muted">La marge soutient la croissance.</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with radar_col2:
        st.markdown(
            """
<div class="pulse-card">
<h3>Marketing</h3>
<p class="pulse-red">À surveiller</p>
<p class="pulse-muted">Certains canaux doivent être évalués en fonction de leur coût.</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with radar_col3:
        st.markdown(
            """
<div class="pulse-card">
<h3>Clients</h3>
<p class="pulse-gold">Solide</p>
<p class="pulse-muted">La base active reste élevée.</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with radar_col4:
        st.markdown(
            """
<div class="pulse-card">
<h3>Qualité commerciale</h3>
<p class="pulse-gold">Stable</p>
<p class="pulse-muted">Le remboursement reste maîtrisé.</p>
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("Décision prioritaire")

    st.markdown(
        f"""
<div class="pulse-alert">
<h3><span class="pulse-red">Priorité</span> — Optimiser l’efficacité marketing</h3>
<p class="pulse-muted">
Le canal <b>{weakest_channel}</b> présente un rendement inférieur aux autres canaux.
Avant d’augmenter les budgets, la direction doit comparer le chiffre d’affaires généré avec le coût d’acquisition.
</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("Évolution du chiffre d’affaires et de la marge")

    monthly_chart = (
        alt.Chart(monthly)
        .transform_fold(["revenue", "margin"], as_=["Indicateur", "Valeur"])
        .mark_line(point=True)
        .encode(
            x=alt.X("month:T", title="Mois"),
            y=alt.Y("Valeur:Q", title="Montant"),
            color=alt.Color(
                "Indicateur:N",
                title="Indicateur",
                scale=alt.Scale(range=["#C1121F", "#D4AF37"]),
            ),
            tooltip=["month:T", "Indicateur:N", "Valeur:Q"],
        )
        .properties(height=365)
    )

    st.altair_chart(monthly_chart, use_container_width=True)

    st.markdown(
        """
<div class="pulse-card">
<p class="pulse-muted">
Lecture business : le chiffre d’affaires et la marge évoluent ensemble, ce qui indique une structure économique cohérente.
L’enjeu est maintenant d’identifier les offres et les canaux qui créent réellement de la rentabilité.
</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Rentabilité par offre")

        offer_chart = (
            alt.Chart(offers)
            .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8)
            .encode(
                x=alt.X(
                    "revenue:Q",
                    title="Chiffre d’affaires",
                    scale=alt.Scale(domain=[0, max_value]),
                ),
                y=alt.Y("offer_type:N", sort="-x", title="Offre"),
                color=alt.value("#C1121F"),
                tooltip=["offer_type:N", "revenue:Q", "margin:Q", "orders_count:Q"],
            )
            .properties(height=340)
        )

        st.altair_chart(offer_chart, use_container_width=True)

    with right:
        st.subheader("Chiffre d’affaires par canal")

        channel_revenue_chart = (
            alt.Chart(channels)
            .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8)
            .encode(
                x=alt.X(
                    "revenue:Q",
                    title="Chiffre d’affaires",
                    scale=alt.Scale(domain=[0, max_value]),
                ),
                y=alt.Y("channel:N", sort="-x", title="Canal"),
                color=alt.value("#D4AF37"),
                tooltip=["channel:N", "revenue:Q", "margin:Q", "roas:Q", "cac:Q"],
            )
            .properties(height=340)
        )

        st.altair_chart(channel_revenue_chart, use_container_width=True)

    st.divider()

    st.subheader("Efficacité marketing des canaux")

    efficiency_chart = (
        alt.Chart(channels)
        .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8)
        .encode(
            x=alt.X("roas:Q", title="Rendement marketing"),
            y=alt.Y("channel:N", sort="x", title="Canal"),
            color=alt.value("#D4AF37"),
            tooltip=["channel:N", "revenue:Q", "marketing_spend:Q", "roas:Q", "cac:Q"],
        )
        .properties(height=320)
    )

    st.altair_chart(efficiency_chart, use_container_width=True)

    st.markdown(
        f"""
<div class="pulse-card">
<p class="pulse-muted">
Lecture business : ici, l’analyse ne regarde plus seulement le volume généré, mais le rendement par rapport aux dépenses marketing.
Le canal <b>{weakest_channel}</b> doit être surveillé car son rendement est inférieur aux autres canaux.
</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("Clients & Segments")

    st.dataframe(
        segments,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("À retenir")

    for finding in insights["top_findings"]:
        st.markdown(
            f"""
<div class="pulse-card">
<p>{finding}</p>
</div>
<br>
""",
            unsafe_allow_html=True,
        )

    st.subheader("Signaux de pilotage")

    st.dataframe(
        insights["business_signals"],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Aperçu des recommandations")

    if recommendations.empty:
        st.success("Aucune alerte critique détectée.")
    else:
        for _, row in recommendations.head(3).iterrows():
            st.markdown(
                f"""
<div class="pulse-card">
<h3>{row["priority"]} — {row["title"]}</h3>
<p class="pulse-muted">{row["description"]}</p>
</div>
<br>
""",
                unsafe_allow_html=True,
            )

    if st.button("Ouvrir la Salle de Décision", use_container_width=True):
        st.session_state.page = "Salle de Décision"
        st.rerun()


# ==================================================
# SALLE DE DÉCISION
# ==================================================

elif st.session_state.page == "Salle de Décision":
    st.title("Salle de Décision")
    st.caption("Transformer l’analyse en actions prioritaires.")

    st.markdown(
        f"""
<div class="pulse-decision">
<h3>CEO Mode — Décision de la semaine</h3>
<p class="pulse-muted">
Cette semaine, la priorité est de <b>protéger la rentabilité</b> en surveillant le canal
<b>{weakest_channel}</b> et en renforçant l’offre <b>{top_offer}</b>, qui contribue fortement à la marge.
</p>
<p class="pulse-muted">
Décision proposée : ne pas augmenter les budgets marketing sans arbitrage, et concentrer l’effort commercial
sur les offres les plus rentables.
</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(
            f"""
<div class="pulse-card-strong">
<p class="pulse-muted">Score de Santé Business</p>
<div class="pulse-score">{int(business_health_score)}/100</div>
<p class="pulse-muted">
Performance solide mais dépendance marketing à surveiller.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with col2:
        st.subheader("Résumé exécutif")
        st.markdown(
            f"""
Pulse360 identifie une activité saine soutenue par une base client stable.

Le chiffre d’affaires atteint **{total_revenue:,.0f} €** avec une marge de **{total_margin:,.0f} €**.

Le taux de marge est de **{margin_rate:.1%}**. La priorité est de préserver la rentabilité,
de réduire les canaux peu efficaces et de renforcer les offres les plus rentables.
"""
        )

    st.divider()

    st.subheader("Décisions à prendre")

    decision_1, decision_2, decision_3 = st.columns(3)

    with decision_1:
        st.markdown(
            f"""
<div class="pulse-alert">
<h3><span class="pulse-red">Décision 1</span></h3>
<p><b>Réallouer le budget marketing</b></p>
<p class="pulse-muted">
Réduire l’exposition aux canaux les moins efficaces, notamment <b>{weakest_channel}</b>.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with decision_2:
        st.markdown(
            f"""
<div class="pulse-card-strong">
<h3><span class="pulse-gold">Décision 2</span></h3>
<p><b>Accélérer les offres rentables</b></p>
<p class="pulse-muted">
Renforcer l’offre <b>{top_offer}</b>, qui porte une contribution importante à la marge.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with decision_3:
        st.markdown(
            f"""
<div class="pulse-card">
<h3><span class="pulse-gold">Décision 3</span></h3>
<p><b>Protéger les segments à forte valeur</b></p>
<p class="pulse-muted">
Suivre le segment <b>{top_segment}</b>, qui contribue fortement à la performance.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("Actions prioritaires générées automatiquement")

    if recommendations.empty:
        st.success("Aucune alerte critique détectée. La performance globale est stable.")
    else:
        priority_order = {"Critique": 0, "Haute": 1, "Moyenne": 2, "P0": 0, "P1": 1, "P2": 2}
        recs = recommendations.copy()
        recs["priority_rank"] = recs["priority"].map(priority_order)
        recs = recs.sort_values(["priority_rank", "impact"])

        for _, row in recs.head(6).iterrows():
            badge_class = "pulse-red" if row["priority"] in ["Critique", "P0"] else "pulse-gold"

            st.markdown(
                f"""
<div class="pulse-card">
<h3><span class="{badge_class}">{row["priority"]}</span> — {row["title"]}</h3>
<p class="pulse-muted"><b>Catégorie :</b> {row["category"]} · <b>Impact :</b> {row["impact"]}</p>
<p class="pulse-muted">{row["description"]}</p>
</div>
<br>
""",
                unsafe_allow_html=True,
            )

    st.divider()

    st.subheader("Simulateur d’impact")

    sim_col1, sim_col2, sim_col3 = st.columns(3)

    with sim_col1:
        revenue_uplift = st.slider("Hausse du chiffre d’affaires", 0, 30, 10)

    with sim_col2:
        cost_reduction = st.slider("Réduction des coûts", 0, 30, 5)

    with sim_col3:
        refund_reduction = st.slider("Baisse remboursements", 0, 20, 3)

    simulated_revenue = total_revenue * (1 + revenue_uplift / 100)
    simulated_cost = total_cost * (1 - cost_reduction / 100)
    simulated_margin = simulated_revenue - simulated_cost

    sim1, sim2, sim3 = st.columns(3)

    sim1.metric("CA simulé", f"{simulated_revenue:,.0f} €")
    sim2.metric("Marge simulée", f"{simulated_margin:,.0f} €")
    sim3.metric("Gain estimé", f"{simulated_margin - total_margin:,.0f} €")

    st.markdown(
        f"""
<div class="pulse-card">
<p class="pulse-muted">
Impact business : une hausse de {revenue_uplift}% du chiffre d’affaires combinée à une réduction de coûts de {cost_reduction}%
permettrait d’obtenir une marge simulée de <b>{simulated_margin:,.0f} €</b>.
</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("Risques à surveiller")

    risk_df = pd.DataFrame(
        [
            {
                "Risque": "Dépendance marketing",
                "Niveau": "Moyen",
                "Lecture": f"Le canal {weakest_channel} doit être suivi avant toute hausse de budget.",
            },
            {
                "Risque": "Concentration de la rentabilité",
                "Niveau": "Élevé",
                "Lecture": f"L’offre {top_offer} porte une part importante de la marge.",
            },
            {
                "Risque": "Qualité commerciale",
                "Niveau": "Stable",
                "Lecture": f"Taux de remboursement : {refund_rate:.1%}.",
            },
        ]
    )

    st.dataframe(risk_df, use_container_width=True, hide_index=True)