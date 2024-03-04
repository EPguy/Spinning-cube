import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy as np
from math import *

pygame.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100

circle_pos = [WIDTH/2, HEIGHT/2]

angle = 0
movement = 0

vertices = [np.matrix([-1, -1, 1])]

vertices.append(np.matrix([1, -1, 1]))
vertices.append(np.matrix([1,  1, 1]))
vertices.append(np.matrix([-1, 1, 1]))
vertices.append(np.matrix([-1, -1, -1]))
vertices.append(np.matrix([1, -1, -1]))
vertices.append(np.matrix([1, 1, -1]))
vertices.append(np.matrix([-1, 1, -1]))


projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])


projected_vertices = [
    [n, n] for n in range(len(vertices))
]

myFont = pygame.font.SysFont("arialblack", 12)

def rotaion_matrix(vertex, angle):
    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ]) 

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ]) 

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])

    vertex = np.dot(rotation_z, vertex)
    vertex = np.dot(rotation_y, vertex)
    vertex = np.dot(rotation_x, vertex)
    return vertex

def connect_line(i, j, vertices):
    pygame.draw.line(
        screen, WHITE, 
        (vertices[i][0], vertices[i][1]),
        (vertices[j][0], vertices[j][1]))
        
def display_cube(vertices):
    for i in range(4):
        connect_line(i, (i+1) % 4, vertices)
        connect_line(i+4, ((i+1) % 4) + 4, vertices)
        connect_line(i, (i+4), vertices)

clock = pygame.time.Clock()

while True:
    
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_DOWN:
                movement = -0.01
            if event.key == pygame.K_UP:
                movement = 0.01
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                movement = 0
            if event.key == pygame.K_UP:
                movement = 0

    angle += movement
    screen.fill(BLACK)

    for i, vertex in enumerate(vertices):
        vertex = rotaion_matrix(vertex.reshape((3,1)), angle)
        vertex = np.dot(projection_matrix, vertex)

        x = int(vertex[0][0] * scale) + circle_pos[0]
        y = int(vertex[1][0] * scale) + circle_pos[1]

        projected_vertices[i] = [x, y]
        pygame.draw.circle(screen, RED, (x, y), 4)

        coord = myFont.render("x: {} y: {}".format(x,y), True, WHITE)
        screen.blit(coord, [x + 10, y + 10])

    display_cube(projected_vertices)

    pygame.display.update()