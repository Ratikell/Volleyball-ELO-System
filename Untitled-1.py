class Player:
    def __init__(self, name, rating=1500):
        self.name = name
        self.rating = rating

    def expected_score(self, opponent_rating):
        return 1 / (1 + 10 ** ((opponent_rating - self.rating) / 400))

    def update_rating(self, opponent_rating, result, K=30):
        expected = self.expected_score(opponent_rating)
        self.rating = round(self.rating + K * (result - expected))


class Team:
    def __init__(self, players):
        self.players = players

    def average_rating(self):
        return sum(player.rating for player in self.players) / len(self.players)


def update_elo_ratings(team_a_names, team_a_ratings, team_b_names, team_b_ratings, score_a, score_b):
    # Create player objects for Team A
    team_a = Team([Player(name, rating) for name, rating in zip(team_a_names, team_a_ratings)])
    
    # Create player objects for Team B
    team_b = Team([Player(name, rating) for name, rating in zip(team_b_names, team_b_ratings)])

    # Calculate average ratings for both teams
    avg_a = team_a.average_rating()
    avg_b = team_b.average_rating()

    # Update ratings based on the match result
    if score_a > score_b:  # Team A wins
        for player in team_a.players:
            player.update_rating(opponent_rating=avg_b, result=1)
        for player in team_b.players:
            player.update_rating(opponent_rating=avg_a, result=0)
    else:  # Team B wins
        for player in team_b.players:
            player.update_rating(opponent_rating=avg_a, result=1)
        for player in team_a.players:
            player.update_rating(opponent_rating=avg_b, result=0)

    # Return updated ratings
    updated_ratings_a = [player.rating for player in team_a.players]
    updated_ratings_b = [player.rating for player in team_b.players]
    
    return updated_ratings_a, updated_ratings_b