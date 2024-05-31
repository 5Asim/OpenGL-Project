import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from draw import draw_ball, draw_player, draw_goal
from physics import check_collision, check_goal

class Game:
    def __init__(self, display):
        self.display = display
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -10)
        self.init_game()

    def init_game(self):
        self.ball_pos = np.array([0.0, 0.0, 0.0])
        self.ball_vel = np.array([0.1, 0.0, 0.0])
        self.gravity = np.array([0.0, -0.01, 0.0])
        self.goal_size = 2.0
        self.player1_pos = np.array([-5.0, 0.0, 0.0])
        self.player2_pos = np.array([5.0, 0.0, 0.0])
        self.player_speed = 0.2
        self.player_size = 0.5 

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.handle_input()
            self.update_physics()
            self.render()
            clock.tick(60)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.player1_pos[1] += self.player_speed
        if keys[K_s]:
            self.player1_pos[1] -= self.player_speed
        if keys[K_UP]:
            self.player2_pos[1] += self.player_speed
        if keys[K_DOWN]:
            self.player2_pos[1] -= self.player_speed

    def update_physics(self):
        self.ball_pos += self.ball_vel
        self.ball_vel += self.gravity

        if self.ball_pos[1] <= -3 or self.ball_pos[1] >= 3:
            self.ball_vel[1] = -self.ball_vel[1]

        if check_collision(self.ball_pos, self.player1_pos):
            self.ball_vel = -self.ball_vel
        if check_collision(self.ball_pos, self.player2_pos):
            self.ball_vel = -self.ball_vel

        if check_goal(self.ball_pos, self.goal_size):
            self.ball_pos = np.array([0.0, 0.0, 0.0])
            self.ball_vel = np.array([0.1, 0.0, 0.0])

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_ball(self.ball_pos)
        draw_player(self.player1_pos)
        draw_player(self.player2_pos)
        draw_goal([-6.0, 0.0, 0.0], self.goal_size)
        draw_goal([6.0, 0.0, 0.0], self.goal_size)
        pygame.display.flip()


def main():
    pygame.init()
    display = (1080, 720)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    
    game = Game(display)
    game.run()

if __name__ == "__main__":
    main()
