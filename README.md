# Pulse360 — Executive Decision Intelligence

> Transform business data into executive decisions.

Pulse360 est une plateforme data conçue pour centraliser plusieurs sources de données business et aider les dirigeants à comprendre :

- où se crée la valeur
- où la marge se dégrade
- quels canaux marketing sont rentables
- quels segments clients fidéliser
- quelles décisions prioriser

---

# Project Overview

Pulse360 simule un environnement business réel à partir de données transactionnelles, marketing et clients.

L’objectif n’est pas seulement de visualiser des KPI.

Le projet démontre la construction complète d’un **Data Product** :

- ingestion de données
- validation
- transformation
- mini data warehouse
- couche analytique
- KPI exécutifs
- moteur de recommandations
- interface Streamlit

---

# Business Problem

Les entreprises disposent souvent de données dispersées :

- CRM
- ventes
- marketing
- satisfaction client
- événements

Mais il manque une couche de décision capable de répondre à :

> What should leadership do next?

---

# Solution

Pulse360 construit une couche d’intelligence décisionnelle.

Pipeline :

```text
Raw CSV
↓
Validation Layer
↓
Transformation Layer
↓
DuckDB Warehouse
↓
Analytics Tables
↓
Executive KPIs
↓
Decision Engine
↓
Streamlit Application
```

---

# Dataset

Le projet inclut un dataset démo réaliste :

## KULTURA Hub

Entreprise fictive proposant :

- événements culturels
- memberships
- studio créatif
- workshops
- packages corporate

---

## Tables

### customers.csv

Informations clients.

### orders.csv

Transactions.

### marketing_spend.csv

Investissements marketing.

### satisfaction.csv

Retours clients.

### events.csv

Performance événementielle.

---

# Technical Architecture

## Stack

- Python
- Streamlit
- DuckDB
- Pandas
- Altair
- SQL

---

## Project Structure

```text
pulse360-executive-dashboard/
│
├── app.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── demo/
│   ├── processed/
│   └── templates/
│
├── sql/
│
├── src/
│   ├── generate_demo_data.py
│   ├── validate_inputs.py
│   ├── build_warehouse.py
│   ├── transform_data.py
│   ├── metrics.py
│   ├── recommendations.py
│   └── data_quality.py
│
└── screenshots/
```

---

# Data Pipeline

## 1. Generate demo data

```bash
python src/generate_demo_data.py
```

## 2. Build warehouse

```bash
python src/build_warehouse.py
```

## 3. Transform tables

```bash
python src/transform_data.py
```

## 4. Launch app

```bash
streamlit run app.py
```

---

# Analytics Layer

Tables construites :

- orders_clean
- customers_clean
- marketing_clean
- satisfaction_clean
- events_clean
- monthly_revenue
- offer_performance
- channel_performance
- customer_segments

---

# KPI Layer

Pulse360 calcule :

- Revenue
- Margin
- Margin Rate
- Refund Rate
- Customer Activity
- Segment Performance
- Channel Performance
- Business Health Score

---

# Decision Engine

La plateforme produit :

- recommandations prioritaires
- alertes business
- scénarios What-if
- synthèse exécutive

---

# Product Pages

## Start

- onboarding
- upload CSV
- dataset preview
- architecture

## Dashboard

- KPI
- revenue
- margin
- channels
- segments

## Decision Room

- business score
- recommandations
- simulations

---

# What This Project Demonstrates

Ce projet démontre ma capacité à :

- construire un mini warehouse
- manipuler et transformer des données
- modéliser des KPI
- créer une couche analytique
- penser produit data
- créer une expérience utilisateur
- relier technique et business

---

# Future Improvements

- upload complet connecté au pipeline
- recommandation ML
- anomaly detection
- forecasting
- benchmarking sectoriel
- export PDF executive report

---

# Author

Built by Aimée Malaka.