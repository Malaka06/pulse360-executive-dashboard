import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker


fake = Faker("fr_FR")

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 6, 30)

N_CUSTOMERS = 1500
N_ORDERS = 10000
N_FEEDBACK = 3000
N_EVENTS = 120

np.random.seed(42)
random.seed(42)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def get_business_config(business_type):
    if business_type == "kultura":
        return {
            "segments": ["Découverte", "Régulier", "Premium", "Corporate", "Créateur"],
            "offers": [
                "Event Ticket",
                "Membership",
                "Creative Studio",
                "Media Package",
                "Workshop",
                "Corporate Package",
                "Partner Offer",
            ],
            "event_types": [
                "Networking",
                "Expo culturelle",
                "Workshop",
                "Conférence",
                "Marché créatif",
                "Concert privé",
            ],
            "cities": ["Paris", "Bruxelles", "Lille", "Lyon", "Anvers", "Kinshasa"],
        }

    if business_type == "ecommerce":
        return {
            "segments": ["Occasionnel", "Standard", "Premium", "VIP", "Ambassadeur"],
            "offers": [
                "Fashion",
                "Beauty",
                "Accessories",
                "Premium Box",
                "Limited Collection",
                "Gift Card",
                "Subscription Box",
            ],
            "event_types": [
                "Pop-up store",
                "Live shopping",
                "Private sale",
                "Product launch",
                "Influencer event",
                "VIP preview",
            ],
            "cities": ["Paris", "Lyon", "Marseille", "Bruxelles", "Lille", "Bordeaux"],
        }

    if business_type == "saas":
        return {
            "segments": ["Freelance", "Startup", "PME", "Enterprise", "Agency"],
            "offers": [
                "Basic Plan",
                "Pro Plan",
                "Business Plan",
                "Enterprise Plan",
                "Add-on",
                "Onboarding",
                "Premium Support",
            ],
            "event_types": [
                "Webinar",
                "Product demo",
                "Customer workshop",
                "Partner session",
                "Training",
                "Community event",
            ],
            "cities": ["Paris", "Berlin", "Amsterdam", "Bruxelles", "Madrid", "Lisbonne"],
        }

    raise ValueError("business_type doit être : kultura, ecommerce ou saas")


# --------------------------------------------------
# MAIN GENERATOR
# --------------------------------------------------

def generate_demo_data(business_type):
    config = get_business_config(business_type)

    output_path = f"data/demo/{business_type}"
    os.makedirs(output_path, exist_ok=True)

    segments = config["segments"]
    offer_types = config["offers"]
    event_types = config["event_types"]
    event_cities = config["cities"]

    channels = [
        "Instagram",
        "TikTok",
        "LinkedIn",
        "Google Search",
        "Referral",
        "Event Walk-in",
        "Partnership",
    ]

    # --------------------------------------------------
    # REALISTIC BUSINESS DISTRIBUTIONS
    # --------------------------------------------------

    segment_weights = {
        "kultura": [0.08, 0.40, 0.20, 0.25, 0.07],
        "ecommerce": [0.45, 0.25, 0.15, 0.10, 0.05],
        "saas": [0.40, 0.25, 0.20, 0.10, 0.05],
    }

    channel_weights = {
        "kultura": [0.28, 0.18, 0.08, 0.10, 0.05, 0.20, 0.11],
        "ecommerce": [0.30, 0.22, 0.05, 0.25, 0.03, 0.08, 0.07],
        "saas": [0.10, 0.05, 0.35, 0.30, 0.03, 0.02, 0.15],
    }

    offer_weights = {
        "kultura": [0.18, 0.12, 0.15, 0.28, 0.10, 0.07, 0.10],
        "ecommerce": [0.35, 0.22, 0.15, 0.10, 0.05, 0.08, 0.05],
        "saas": [0.35, 0.25, 0.18, 0.08, 0.05, 0.06, 0.03],
    }

    score_weights = [0.08, 0.12, 0.18, 0.34, 0.28]

    channel_spend_multiplier = {
        "LinkedIn": 1.3,
        "Instagram": 1.2,
        "Google Search": 1.1,
        "TikTok": 1.0,
        "Referral": 1.4,
        "Event Walk-in": 0.7,
        "Partnership": 0.8,
    }

    conversion_modifier = {
        "LinkedIn": 1.4,
        "Instagram": 1.2,
        "Google Search": 1.3,
        "TikTok": 1.1,
        "Referral": 0.5,
        "Event Walk-in": 1.6,
        "Partnership": 1.3,
    }

    # --------------------------------------------------
    # CUSTOMERS
    # --------------------------------------------------

    customers = []

    for i in range(N_CUSTOMERS):
        customers.append({
            "customer_id": f"CUST_{i+1}",
            "customer_name": fake.name(),
            "city": fake.city(),
            "country": fake.country(),
            "age_group": random.choice(["18-25", "26-35", "36-45", "46-60"]),
            "segment": random.choices(
                segments,
                weights=segment_weights[business_type],
                k=1
            )[0],
            "signup_date": random_date(START_DATE, END_DATE),
            "acquisition_channel": random.choices(
                channels,
                weights=channel_weights[business_type],
                k=1
            )[0],
            "is_member": random.choices([0, 1], weights=[0.55, 0.45], k=1)[0],
        })

    customers_df = pd.DataFrame(customers)

    # --------------------------------------------------
    # ORDERS
    # --------------------------------------------------

    statuses = ["Completed", "Refunded", "Cancelled"]
    orders = []

    for i in range(N_ORDERS):
        customer = customers_df.sample(1).iloc[0]

        if business_type == "saas":
            revenue = round(np.random.uniform(20, 1200), 2)
            cost_ratio = np.random.uniform(0.15, 0.45)
        elif business_type == "ecommerce":
            revenue = round(np.random.uniform(15, 700), 2)
            cost_ratio = np.random.uniform(0.35, 0.75)
        else:
            revenue = round(np.random.uniform(20, 500), 2)
            cost_ratio = np.random.uniform(0.30, 0.70)

        cost = round(revenue * cost_ratio, 2)

        orders.append({
            "order_id": f"ORD_{i+1}",
            "customer_id": customer["customer_id"],
            "order_date": random_date(START_DATE, END_DATE),
            "offer_type": random.choices(
                offer_types,
                weights=offer_weights[business_type],
                k=1
            )[0],
            "channel": customer["acquisition_channel"],
            "revenue": revenue,
            "cost": cost,
            "status": random.choices(statuses, weights=[85, 10, 5], k=1)[0],
        })

    orders_df = pd.DataFrame(orders)

    # --------------------------------------------------
    # MARKETING SPEND
    # --------------------------------------------------

    months = pd.date_range(START_DATE, END_DATE, freq="MS")
    marketing_rows = []

    for month in months:
        for channel in channels:
            if business_type == "saas":
                base_spend = np.random.uniform(1000, 9000)
            elif business_type == "ecommerce":
                base_spend = np.random.uniform(800, 7000)
            else:
                base_spend = np.random.uniform(500, 6000)

            spend = round(
                base_spend * channel_spend_multiplier[channel],
                2
            )

            impressions = int(np.random.uniform(10000, 150000))
            clicks = int(impressions * np.random.uniform(0.01, 0.08))

            base_conversion = np.random.uniform(0.02, 0.12)
            conversions = int(
                clicks * base_conversion * conversion_modifier[channel]
            )

            marketing_rows.append({
                "month": month.strftime("%Y-%m-%d"),
                "channel": channel,
                "spend": spend,
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
            })

    marketing_df = pd.DataFrame(marketing_rows)

    # --------------------------------------------------
    # SATISFACTION
    # --------------------------------------------------

    complaints = [
        "Aucune plainte",
        "Prix",
        "Réservation",
        "Communication",
        "Organisation",
        "Qualité service",
        "Support client",
    ]

    comments_by_type = {
        "kultura": [
            "Très bonne expérience globale.",
            "Le prix est un peu élevé.",
            "Le processus de réservation est compliqué.",
            "Excellent service client.",
            "Je reviendrai pour un prochain événement.",
            "Le support a mis du temps à répondre.",
            "Très satisfait de l’ambiance.",
            "Le studio créatif est top.",
            "Organisation moyenne.",
            "Expérience premium.",
        ],
        "ecommerce": [
            "Livraison rapide et produit conforme.",
            "Le prix est intéressant mais le retour est compliqué.",
            "Très bonne qualité.",
            "Le site est fluide et simple.",
            "J’ai eu un problème avec ma commande.",
            "Service client réactif.",
            "Packaging premium.",
            "Taille indisponible trop souvent.",
            "Expérience d’achat agréable.",
            "Produit reçu en retard.",
        ],
        "saas": [
            "L’outil est simple à utiliser.",
            "Le support a répondu rapidement.",
            "La configuration initiale est un peu longue.",
            "Les fonctionnalités sont utiles.",
            "Le prix est élevé pour une petite équipe.",
            "Très bon accompagnement client.",
            "La documentation pourrait être plus claire.",
            "La plateforme aide vraiment au pilotage.",
            "Interface claire.",
            "Quelques lenteurs observées.",
        ],
    }

    feedback_rows = []

    for i in range(N_FEEDBACK):
        customer = customers_df.sample(1).iloc[0]

        feedback_rows.append({
            "feedback_id": f"FB_{i+1}",
            "customer_id": customer["customer_id"],
            "date": random_date(START_DATE, END_DATE),
            "score": random.choices(
                [1, 2, 3, 4, 5],
                weights=score_weights,
                k=1
            )[0],
            "complaint_category": random.choice(complaints),
            "comment": random.choice(comments_by_type[business_type]),
        })

    feedback_df = pd.DataFrame(feedback_rows)

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    event_rows = []

    for i in range(N_EVENTS):
        capacity = random.randint(50, 400)
        tickets_sold = random.randint(20, capacity)

        revenue = round(tickets_sold * np.random.uniform(15, 80), 2)
        cost = round(revenue * np.random.uniform(0.35, 0.75), 2)

        event_rows.append({
            "event_id": f"EVT_{i+1}",
            "event_date": random_date(START_DATE, END_DATE),
            "event_type": random.choice(event_types),
            "city": random.choice(event_cities),
            "capacity": capacity,
            "tickets_sold": tickets_sold,
            "revenue": revenue,
            "cost": cost,
        })

    events_df = pd.DataFrame(event_rows)

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    customers_df.to_csv(f"{output_path}/customers.csv", index=False)
    orders_df.to_csv(f"{output_path}/orders.csv", index=False)
    marketing_df.to_csv(f"{output_path}/marketing_spend.csv", index=False)
    feedback_df.to_csv(f"{output_path}/satisfaction.csv", index=False)
    events_df.to_csv(f"{output_path}/events.csv", index=False)

    print(f"Demo generated successfully: {business_type}")


# --------------------------------------------------
# RUN ALL DEMOS
# --------------------------------------------------

if __name__ == "__main__":
    generate_demo_data("kultura")
    generate_demo_data("ecommerce")
    generate_demo_data("saas")