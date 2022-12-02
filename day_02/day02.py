import sys

with open(sys.argv[1], "r") as file:
    strategy_guide = [value for value in file.read().splitlines()]
#print(strategy_guide)

wins = {"A Y": (1, 2), "B Z": (2, 3), "C X": (3, 1)}
losses = {"A Z": (1, 3), "B X": (2, 1), "C Y": (3, 2)}
draws = {"A X": (1, 1), "B Y": (2, 2), "C Z": (3, 3)}


def calc1(x, y, z):
    score = 0
    opponent_score = 0
    
    for i in range(len(strategy_guide)):
        if strategy_guide[i] in wins:
            value = wins[strategy_guide[i]]
            opponent_score += 0 + value[0]
            score += 6 + value[1]
        elif strategy_guide[i] in draws:
            value = draws[strategy_guide[i]]
            opponent_score += 3 + value[0]
            score += 3 + value[1]
        else:
            value = losses[strategy_guide[i]]
            opponent_score += 6 + value[0]
            score += 0 + value[1]
    
    print(f"{x}, {y}, {z}: Score: {score} to {opponent_score} with difference {score-opponent_score}")

def calc2():
    score = 0
    opponent_score = 0
    
    for i in range(len(strategy_guide)):
        opponent_hand = strategy_guide[i][0]
        if "Z" in strategy_guide[i]:
            #we need to win
            value = [val for key, val in wins.items() if opponent_hand in key][0]
            opponent_score += 0 + value[0]
            score += 6 + value[1]
        elif "Y" in strategy_guide[i]:
            #we need a draw
            value = [val for key, val in draws.items() if opponent_hand in key][0]
            opponent_score += 3 + value[0]
            score += 3 + value[1]
        else:
            value = [val for key, val in losses.items() if opponent_hand in key][0]
            opponent_score += 6 + value[0]
            score += 0 + value[1]
    
    print(f"Score: {score} to {opponent_score} with difference {score-opponent_score}")

round_1 = calc1("A", "B", "C")
round_2 = calc2()
