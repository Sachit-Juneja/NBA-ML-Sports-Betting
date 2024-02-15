from colorama import Fore, Style, init, deinit
import numpy as np
import tensorflow as tf
from keras.models import load_model
from src.Utilities import exp_val
from src.Utilities import kelly_crit as kc

init()

# Load models
model = load_model('Models/NN_Models/Trained-Model-ML-1699315388.285516')
ou_model = load_model("Models/NN_Models/Trained-Model-OU-1699315414.2268295")

def print_game_result(home_team, away_team, winner_confidence, bet_type, odds, kelly_criterion):
    winner_color = Fore.GREEN if winner_confidence > 50 else Fore.RED
    bet_type_color = Fore.MAGENTA if bet_type == 'UNDER' else Fore.BLUE
    odds_color = Fore.CYAN
    kelly_color = Fore.YELLOW

    print(f"{winner_color}{home_team}{Style.RESET_ALL} vs {winner_color}{away_team}{Style.RESET_ALL}: "
          f"{bet_type_color}{bet_type} {Style.RESET_ALL}{odds_color}{odds}{Style.RESET_ALL} "
          f"({winner_color}{winner_confidence:.1f}%{Style.RESET_ALL})")

    if kelly_criterion:
        bankroll_descriptor = ' Fraction of Bankroll: '
        kelly_fraction = kc.calculate_kelly_criterion(odds, winner_confidence)
        print(f"{kelly_color}Kelly Criterion:{Style.RESET_ALL}{bankroll_descriptor}{kelly_fraction:.2f}%")

def nn_runner(data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds, kelly_criterion):
    ml_predictions_array = [model.predict(np.array([row])) for row in data]

    frame_uo = tf.keras.utils.normalize(copy.deepcopy(frame_ml.values.astype(float)), axis=1)
    ou_predictions_array = [ou_model.predict(np.array([row])) for row in frame_uo]

    for count, game in enumerate(games):
        home_team, away_team = game
        winner = int(np.argmax(ml_predictions_array[count]))
        under_over = int(np.argmax(ou_predictions_array[count]))
        winner_confidence = ml_predictions_array[count][0][1] if winner == 1 else ml_predictions_array[count][0][0]

        if under_over == 0:
            bet_type = 'UNDER'
            odds = todays_games_uo[count]
        else:
            bet_type = 'OVER'
            odds = todays_games_uo[count]

        print_game_result(home_team, away_team, winner_confidence * 100, bet_type, odds, kelly_criterion)

    deinit()
