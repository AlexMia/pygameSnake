import pygame, sys
from pygame.locals import *
from random import randint as rnd

pygame.init()
pygame.display.set_caption('Snake')


# Constants =====================================

WIN_SIZE = (400, 400)
CELL_SIZE = 20
GRID_SIZE = tuple(int(x/CELL_SIZE) for x in WIN_SIZE)
FPS = 10


# Pygame Variables ==============================

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WIN_SIZE)


# Classes =======================================

class bodyPart:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Snake:
	def __init__(self, x, y, length):
		self.headX = x
		self.headY = y
		self.length = length
		self.body = []
		self.direction = 1
		for i in range(self.length):
			self.body.append(bodyPart(x-i, y))

	def move(self):
		global apple
		global snake
		for i in range(len(self.body)):
			if i > 0:
				self.body[-i].x = self.body[-i-1].x
				self.body[-i].y = self.body[-i-1].y

		if self.direction == 0:
			self.body[0].y -= 1
		elif self.direction == 1:
			self.body[0].x += 1
		elif self.direction == 2:
			self.body[0].y += 1
		elif self.direction == 3:
			self.body[0].x -= 1

		# Pacman effect implementation ==========
		for part in self.body:
			if part.x < 0:
				part.x = GRID_SIZE[0]-1
			if part.y < 0:
				part.y = GRID_SIZE[1]-1
			if part.x >= GRID_SIZE[0]:
				part.x = 0
			if part.y >= GRID_SIZE[1]:
				part.y = 0

		# Collisions with body and apple ========
		for i in range(len(self.body)):
			for j in range(len(self.body)):
				if i != j:
					if self.body[i].x == self.body[j].x and self.body[i].y == self.body[j].y:
						snake = Snake(10, 10, 3)
						apple = Apple()
		for i in range(len(self.body)):
			if self.body[i].x == apple.x and self.body[i].y == apple.y:
				apple = Apple()
				self.body.append(bodyPart(self.body[-1].x, self.body[-1].y))


class Apple:
	def __init__(self):
		self.x = rnd(0, GRID_SIZE[0]-1)
		self.y = rnd(0, GRID_SIZE[1]-1)

# Variables =====================================

snake = Snake(10, 10, 3)
apple = Apple()


# Functions =====================================

def redrawWindow(screen, snake):
	screen.fill((0, 0, 0))
	pygame.draw.lines(screen, (255, 255, 255), True, ((0, 0), (WIN_SIZE[0]-1, 0), (WIN_SIZE[0]-1, WIN_SIZE[1]-1), (0, WIN_SIZE[1]-1)))

	# Draw the snake ============================
	for part in snake.body:
		pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(part.x*CELL_SIZE, part.y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

	# Draw the apple ============================
	pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(apple.x*CELL_SIZE, apple.y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

	# Draw the grid =============================
	for i in range(GRID_SIZE[0]):
		pygame.draw.line(screen, (255, 255, 255), (i*CELL_SIZE, 0), (i*CELL_SIZE, WIN_SIZE[1]))
		pygame.draw.line(screen, (255, 255, 255), (0, i*CELL_SIZE), (WIN_SIZE[0], i*CELL_SIZE))
	

	pygame.display.update()

# Main loop =====================================

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == K_UP:
				snake.direction = 0
			if event.key == K_RIGHT:
				snake.direction = 1
			if event.key == K_DOWN:
				snake.direction = 2
			if event.key == K_LEFT:
				snake.direction = 3
	snake.move()
	redrawWindow(screen, snake)
	clock.tick(FPS)