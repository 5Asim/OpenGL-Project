import numpy as np

def check_goal(ball_position, goal_size):
    if ball_position[0] <= -6.0 and abs(ball_position[1]) <= goal_size / 2:
        print("Player 2 scores!")
        return True
    elif ball_position[0] >= 6.0 and abs(ball_position[1]) <= goal_size / 2:
        print("Player 1 scores!")
        return True
    return False

def check_collision(ball_position, player_position):
    if np.linalg.norm(ball_position - player_position) < 0.75:
        return True
    return False
