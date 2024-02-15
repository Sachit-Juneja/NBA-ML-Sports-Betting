'''
Would recommend reading about this criterion before going through code.
'''

def american_to_decimal(american_odds):
    """
    Converts American odds to decimal odds (European odds).
    
    Args:
        american_odds (float): The odds in American format.

    Returns:
        float: The corresponding decimal odds rounded to two decimal places.
    """
    return round((american_odds / 100) if american_odds >= 100 else (100 / abs(american_odds)), 2)

def calculate_kelly_criterion(american_odds, model_prob):
    """
    Calculates the recommended fraction of the bankroll to wager based on the Kelly Criterion.

    Args:
        american_odds (float): The odds in American format.
        model_prob (float): The predicted probability of a bet being successful.

    Returns:
        float: The calculated bankroll fraction rounded to two decimal places, ensuring it is at least 0.
    """
    decimal_odds = american_to_decimal(american_odds)
    return max(round((decimal_odds * model_prob - (1 - model_prob)) / decimal_odds, 2), 0)