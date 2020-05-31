import math
import pygame

GREEN = (0,255,0)
RED = (255,0,0)

class Ball():

	def __init__(self, x, y, radius, color, angle, speed, moving):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.angle = angle	# in radians
		self.speed = speed
		self.moving = moving

	def draw(self, win):
		pygame.draw.circle(win, self.color, (int(self.x),int(self.y)), self.radius)

	def updatePos(self, screenSizeX, screenSizeY):

		# checks if we've reached the boundaries of the screen to 
		# determine how to move

		if self.x > screenSizeX - self.radius:	
			self.x = screenSizeX - self.radius
			self.angle = - self.angle
		elif self.x < self.radius:
			self.x = self.radius
			self.angle = - self.angle
		else:
			self.x += self.speed * math.sin(self.angle)

		if self.y > screenSizeY - self.radius:
			self.y = screenSizeY - self.radius
			self.angle = math.pi - self.angle
		elif self.y < self.radius:
			self.y = self.radius
			self.angle = math.pi - self.angle
		else:
			self.y -= self.speed * math.cos(self.angle)
