"""
Centralized Configuration for EV Spare-Parts Import Prioritization.
Defines system paths, candidate vehicle pools, the 10 assigned part categories,
scoring weights, and currency conversion parameters.
"""

from pathlib import Path

# Base Directory Resolution
SRC_DIR = Path(__file__).resolve().parent
REPO_ROOT = SRC_DIR.parent
DATA_DIR = REPO_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RESULTS_DIR = REPO_ROOT / "results"
RANKINGS_DIR = RESULTS_DIR / "rankings"
CHARTS_DIR = RESULTS_DIR / "charts"
REPORTS_DIR = REPO_ROOT / "reports"

# 1. Candidate Vehicles Pool (Slide 4 of Assignment)
CANDIDATE_VEHICLES = {
    "BYD_SEAGULL": {
        "id": "VEH-BYD-SGL",
        "make": "BYD",
        "model": "Seagull",
        "class": "A00 Subcompact Hatchback",
        "platform": "e-Platform 3.0",
        "target_relevance": "Mass-market urban commuter with high visibility on Adey Market & Gezat",
    },
    "BYD_YUAN_UP": {
        "id": "VEH-BYD-YUP",
        "make": "BYD",
        "model": "Yuan Up",
        "class": "A0 Compact Crossover",
        "platform": "e-Platform 3.0",
        "target_relevance": "Compact SUV segment",
    },
    "CHANGAN_BENBEN": {
        "id": "VEH-CHN-BEN",
        "make": "Changan",
        "model": "Benben E-Star",
        "class": "A00 Subcompact Hatchback",
        "platform": "Changan EV",
        "target_relevance": "Budget commercial and ride-share transit entry",
    },
    "TOYOTA_BZ4X": {
        "id": "VEH-TOY-BZ4X",
        "make": "Toyota",
        "model": "bZ4X",
        "class": "Mid-size Crossover SUV",
        "platform": "e-TNGA",
        "target_relevance": "Strong brand-equity legacy automaker EV with global parts interchange",
    },
    "VW_ID4": {
        "id": "VEH-VW-ID4",
        "make": "Volkswagen",
        "model": "ID.4",
        "class": "Compact Crossover SUV",
        "platform": "MEB Platform",
        "target_relevance": "High global aftermarket support and modular MEB platform sharing",
    },
}

# 2. The 10 Mandatory Part Categories (Slide 5 of Assignment)
ASSIGNED_PART_CATEGORIES = {
    "CAT-01-BRKPAD": {
        "name": "Brake pads",
        "description": "Friction wear components replaced periodically",
        "functional_group": "Fast_Moving_Wear",
        "wear_velocity_rating": 95,
        "bulk_factor": 15,  # Low bulk / high shipping compactness
    },
    "CAT-02-BRKDISC": {
        "name": "Brake discs",
        "description": "Braking surfaces paired with brake pads",
        "functional_group": "Fast_Moving_Wear",
        "wear_velocity_rating": 80,
        "bulk_factor": 45,
    },
    "CAT-03-CABFILT": {
        "name": "Cabin-air filters",
        "description": "HVAC dust and pollen filtration elements",
        "functional_group": "Periodic_Maintenance",
        "wear_velocity_rating": 90,
        "bulk_factor": 20,
    },
    "CAT-04-WIPER": {
        "name": "Wiper blades",
        "description": "Windshield clearing rubber consumables",
        "functional_group": "Periodic_Maintenance",
        "wear_velocity_rating": 85,
        "bulk_factor": 10,
    },
    "CAT-05-HEADLIGHT": {
        "name": "Headlights",
        "description": "Front illumination and LED matrix assemblies",
        "functional_group": "Lighting_Assemblies",
        "wear_velocity_rating": 35,
        "bulk_factor": 75,
    },
    "CAT-06-TAILLIGHT": {
        "name": "Tail lights",
        "description": "Rear signaling and brake light assemblies",
        "functional_group": "Lighting_Assemblies",
        "wear_velocity_rating": 35,
        "bulk_factor": 60,
    },
    "CAT-07-MIRROR": {
        "name": "Side mirrors",
        "description": "Exterior visibility and camera/sensor mirrors",
        "functional_group": "Collision_Exterior",
        "wear_velocity_rating": 45,
        "bulk_factor": 40,
    },
    "CAT-08-BUMPER": {
        "name": "Bumpers",
        "description": "Front and rear impact absorbing assemblies",
        "functional_group": "Collision_Exterior",
        "wear_velocity_rating": 50,
        "bulk_factor": 100,  # Extremely bulky freight
    },
    "CAT-09-FENDER": {
        "name": "Fenders/body panels",
        "description": "Exterior sheet metal and composite panels",
        "functional_group": "Collision_Exterior",
        "wear_velocity_rating": 40,
        "bulk_factor": 90,
    },
    "CAT-10-SHOCK": {
        "name": "Shock absorbers",
        "description": "Suspension movement and damping struts",
        "functional_group": "Suspension_Chassis",
        "wear_velocity_rating": 70,
        "bulk_factor": 50,
    },
}

# 3. Baseline Multi-Criteria Scoring Weights (Slide 9 of Assignment)
BASELINE_SCORING_WEIGHTS = {
    "demand_wear_signal": 0.30,       # 30% Demand evidence / wear frequency
    "market_scarcity": 0.25,          # 25% Local market stockout risk & lead time
    "vehicle_compatibility": 0.20,    # 20% Platform sharing & multi-trim fitment
    "sourcing_practicality": 0.15,    # 15% Unit affordability & freight compactness
    "evidence_confidence": 0.10,      # 10% Multi-source catalog verification count
}

# Assert weights sum to 1.0
assert abs(sum(BASELINE_SCORING_WEIGHTS.values()) - 1.0) < 1e-6, "Weights must sum to 1.0"

# 4. Currency Conversion Benchmarks (USD Base)
EXCHANGE_RATES_TO_USD = {
    "USD": 1.000,
    "CNY": 0.138,    # Chinese Yuan
    "AED": 0.272,    # UAE Dirham (Exist.ae)
    "EUR": 1.085,    # Euro
    "ETB": 0.008,    # Ethiopian Birr (Indicative commercial rate)
}

# 5. Missing Data Category Codes
MISSING_DATA_CATEGORIES = [
    "STRUCTURAL_CATALOG_GAP",        # Not listed in public catalog
    "GEOGRAPHIC_BOUNDARY_UNAVAILABLE", # US regulatory data not applicable to China-market models
    "PROPRIETARY_RETAINED",          # OEM restricts part number from public index
]
