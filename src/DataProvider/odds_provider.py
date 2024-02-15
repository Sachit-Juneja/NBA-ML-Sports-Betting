from sbrscrape import Scoreboard

class OddsProvider:
    def __init__(self, sportsbook="fanduel"):
        # Initialize the OddsProvider instance with a specified sportsbook (default is "fanduel")
        self.games = Scoreboard(sport="NBA").games or []  # Fetch NBA games from Sbr
        self.sportsbook = sportsbook  # Set the sportsbook attribute

    def fetch_odds(self):
        odds_data = {}  # Dictionary to store odds data
        for game in self.games:
            # Extract relevant information for each game
            home_team, away_team = game['home_team'], game['away_team']
            home_ml, away_ml, totals = game['home_ml'], game['away_ml'], game['total']

            # Build the odds_data dictionary with a specific structure
            odds_data[f'{home_team}:{away_team}'] = {
                'uo_odds': totals.get(self.sportsbook),
                home_team: {'ml_odds': home_ml.get(self.sportsbook)},
                away_team: {'ml_odds': away_ml.get(self.sportsbook)}
            }
        return odds_data  # Return the collected odds data

def main():
    odds_provider = OddsProvider(sportsbook="draftkings")
    odds_data = odds_provider.fetch_odds()

    if odds_data:
        # Print odds information for each game
        for matchup, odds in odds_data.items():
            home_team, away_team = matchup.split(':')
            print(f"{away_team} ({odds[away_team]['ml_odds']}) @ {home_team} ({odds[home_team]['ml_odds']})")
    else:
        print("No games found.")

if __name__ == "__main__":
    main()