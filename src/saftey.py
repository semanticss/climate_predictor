
r_min = 0
r_max = 1_000_000_000

def risk_level(property_damage: float, injuries: int, casualties: int, volatility: float, air_quality: float, proximity_to_coastlines: float) -> float:
    risk = property_damage + injuries + casualties + volatility + air_quality + proximity_to_coastlines
    return ((risk - r_min) / (r_max-r_min)) * (100)