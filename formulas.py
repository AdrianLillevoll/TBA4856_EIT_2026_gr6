formulas = [
    {
        "id": "drift_margin",
        "category": "economic",
        "func": lambda scores: (scores.get("costs", 0) - scores.get("revenue", 0)) / max(scores.get("total_area", 1), 1),
        "scale": [(1027.6, float('inf'),1), (717.9,1027.6,2), (520.3,717.9,3), (297.6,520.3,4), (float('-inf'),297.6,5)] 
        # min_value < value <= max_value
    },
    {
        "id": "electricity_balance",
        "category": "environment",
        "func": lambda scores: (
            (scores.get("electricity_usage", 0) - scores.get("electricity_production", 0)) / max(scores.get("total_area", 1), 1)
            if scores.get("electricity_production") is not None 
            else scores.get("electricity_usage", 0) / max(scores.get("total_area", 1), 1)
        ),
        "scale": [(205, float('inf'),1), (141,205,2), (107,141,3), (72,107,4), (float('-inf'),72,5)]
        # min_value < value <= max_value
    }
]