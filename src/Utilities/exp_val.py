'''
expected_value(Pwin, odds):

Takes two parameters: Pwin (probability of winning) and odds (betting odds).
Calculates the expected value by subtracting the expected loss from the expected win.
Uses the get_payout function to determine the payout based on the provided odds.
'''

def expected_value(Pwin, odds):
    return round((Pwin * get_payout(odds)) - ((1 - Pwin) * 100), 2)

'''
get_payout(odds):

Takes a single parameter, odds.
If the odds are positive, it returns the odds directly.
If the odds are negative, it calculates the equivalent payout by using the formula (100 / (-odds)) * 100. This is a common conversion for negative odds.
'''

def get_payout(odds):
    return odds if odds > 0 else (100 / (-odds)) * 100