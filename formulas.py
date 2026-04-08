formulas = [
    {
        "id": "drift_margin",
        "category": "economic",
        "func": lambda scores: (scores.get("revenue", 0) - scores.get("costs", 0)) / max(scores.get("revenue", 1), 1),
        "scale": [(0.05, float('inf'),5), (0.0,0.05,4), (-0.05,0.0,3), (-0.4,-0.05,2), (float('-inf'),-0.4,1)] 
        # min_value < value <= max_value
    },
    {
        "id": "total_margin",
        "category": "economic",
        "func": lambda scores: (scores.get("total_revenue", 0) - scores.get("total_costs", 0)) / max(scores.get("total_revenue", 1), 1),
        "scale": [(0.05, float('inf'),5), (0.0,0.05,4), (-0.05,0.0,3), (-0.4,-0.05,2), (float('-inf'),-0.4,1)]
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
        "scale": [(400, float('inf'),1), (300,400,2), (200,300,3), (150,200,4), (float('-inf'),150,5)]
        # min_value < value <= max_value
    }
]