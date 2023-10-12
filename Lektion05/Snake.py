# -*- truncate-lines:t -*-
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 05 16:12:49 2020
@author: Sila
"""

import pygame
import time

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the width and height of each snake segment
segment_width = 15
segment_height = 15
# Margin between each segment
segment_margin = 3

# Set initial speed
x_change = segment_width + segment_margin
y_change = 0


class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """

    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Call this function so the Pygame library can initialize itself
pygame.init()

dis_width = 800
dis_height  = 600

firstfood_placex = round(dis_width / 4)
firstfood_placey = round(dis_height / 3)

secondfood_placex = round(dis_width / 2)
secondfood_placey = round(dis_height / 4)


# Create an 800x600 sized screen
screen = pygame.display.set_mode([dis_width, dis_height])

# Set the title of the window
pygame.display.set_caption('Programmeringssprog - Eksempel')

allspriteslist = pygame.sprite.Group()

font_style = pygame.font.SysFont(None, 50)

dis = pygame.display.set_mode((dis_width, dis_height))

def message(msg,color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/2, dis_height/2])

# Create an initial snake
snake_segments = []
for i in range(8):
    x = 250 - (segment_width + segment_margin) * i
    y = 30
    segment = Segment(x, y)
    snake_segments.append(segment)
    allspriteslist.add(segment)

foodx = firstfood_placex
foody = firstfood_placey

clock = pygame.time.Clock()
game_over = False
game_step = 0
yummy_points = 0

while not game_over:

    game_step = game_step + 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = (segment_width + segment_margin) * -1
                y_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = (segment_width + segment_margin)
                y_change = 0
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = (segment_height + segment_margin) * -1
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = (segment_height + segment_margin)

    if snake_segments[0].rect.x >= dis_width or snake_segments[0].rect.x < 0 or snake_segments[0].rect.y >= dis_height or snake_segments[0].rect.y < 0:
        game_over = True

    # Get rid of last segment of the snake
    # .pop() command removes last item in list
    old_segment = snake_segments.pop()
    allspriteslist.remove(old_segment)

    # Figure out where new segment will be
    x = snake_segments[0].rect.x + x_change
    y = snake_segments[0].rect.y + y_change
    segment = Segment(x, y)

    if abs(x-foodx)<10 and abs(y-foody)<10:
        print("Yummy!!")
        if foodx == firstfood_placex:
           foodx = secondfood_placex
           foody = secondfood_placey
        else:
           foodx = firstfood_placex
           foody = firstfood_placey
        yummy_points = yummy_points + 100

    # Insert new segment into the list
    snake_segments.insert(0, segment)
    allspriteslist.add(segment)

    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)

    allspriteslist.draw(screen)
    pygame.draw.rect(dis, BLUE, [foodx, foody, 10, 10])

    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(10)

    if (game_step)>499:
       game_over = True

message("You lost",RED)
pygame.display.update()
time.sleep(2)

your_points = game_step + yummy_points
print("Your points are", your_points)

pygame.quit()