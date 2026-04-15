formulas = [
    {
        "id": "drift_margin",
        "category": "economic",
        "func": lambda scores: (scores.get("costs", 0) - scores.get("revenue", 0)) / max(scores.get("total_area", 1), 1),
        # "scale": [(0.001, float('inf'),1), (0.0005,0.001,2), (0.0001,0.0005,3), (0.00005,0.0001,2), (float('-inf'),0.00005,1)]
        "scale": [(10000, float('inf'),1), (5000,10000,2), (1000,5000,3), (500,1000,2), (float('-inf'),500,1)] 
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