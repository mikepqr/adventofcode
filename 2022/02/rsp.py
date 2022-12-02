SHAPE_SCORE = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
}

OUTCOME_SCORE = {
    "win": 6,
    "tie": 3,
    "loss": 0,
}

PLAYER1 = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
}

PLAYER2 = {
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}

DESIRED_OUTCOME = {
    "X": "loss",
    "Y": "tie",
    "Z": "win",
}


def score_game(player1, player2):
    player1 = PLAYER1[player1]
    player2 = PLAYER2[player2]
    if player1 == player2:
        outcome = "tie"
    elif player1 == "rock":
        outcome = "win" if player2 == "paper" else "loss"
    elif player1 == "scissors":
        outcome = "win" if player2 == "rock" else "loss"
    else:  # player2 == "paper"
        outcome = "win" if player2 == "scissors" else "loss"
    return OUTCOME_SCORE[outcome] + SHAPE_SCORE[player2]


def compute1(fname):
    score = 0
    with open(fname) as f:
        for line in f:
            player1, player2 = line.strip().split()
            score += score_game(player1, player2)
    return score


def infer_player2(player1, outcome):
    player1 = PLAYER1[player1]
    if outcome == "tie":
        return player1
    elif outcome == "win":
        if player1 == "scissors":
            return "rock"
        elif player1 == "rock":
            return "paper"
        else:
            return "scissors"
    else:  # loss
        if player1 == "scissors":
            return "paper"
        elif player1 == "rock":
            return "scissors"
        else:
            return "rock"


def compute2(fname):
    score = 0
    with open(fname) as f:
        for line in f:
            player1, outcome = line.strip().split()
            outcome = DESIRED_OUTCOME[outcome]
            player2 = infer_player2(player1, outcome)
            score += SHAPE_SCORE[player2] + OUTCOME_SCORE[outcome]
    return score


def test_compute1():
    assert compute1("test.txt") == 15


def test_compute2():
    assert compute2("test.txt") == 12


if __name__ == "__main__":
    print(compute1("input.txt"))
    print(compute2("input.txt"))
