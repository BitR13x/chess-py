def calculate_elo(player_rating: float, opponent_rating: float, actual_score: float, k_factor: int = 20) -> tuple[float, float]:
  """
    Calculates expected score and new Elo rating after a match.

    Args:
        player_rating: Your current Elo rating.
        opponent_rating: Your opponent's Elo rating.
        actual_score: 1.0 for a win, 0.5 for a draw, 0.0 for a loss.
        k_factor: Volatility factor (default is 20 for standard club players).

    Returns:
        A tuple containing (expected_score, new_rating).
    """
  expected_score = 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))
  new_rating = player_rating + k_factor * (actual_score - expected_score)

  return round(expected_score, 3), round(new_rating, 1)


if __name__ == '__main__':
    my_elo = 1500
    opp_elo = 1700

    # Simulate a win (1.0), draw (0.5), and loss (0.0)
    win_prob, elo_after_win = calculate_elo(my_elo, opp_elo, actual_score=1.0)
    _, elo_after_draw = calculate_elo(my_elo, opp_elo, actual_score=0.5)
    _, elo_after_loss = calculate_elo(my_elo, opp_elo, actual_score=0.0)

    print(f"Expected Win Probability: {win_prob * 100:.1f}%")
    print(f"New Rating on Win:  {elo_after_win}")
    print(f"New Rating on Draw: {elo_after_draw}")
    print(f"New Rating on Loss: {elo_after_loss}")
