from ball import *
import pygame
import random
import math

# this file contains the Simulation and Run classes

# percentage of people that are stationary based on
# the amount of social distancing
stationary_percent = [0, 0.2, 0.7, 0.9]

# amt_distancing : 	0 - none
# 					1 - low
# 					2 - moderate
# 					3 - high

class Simulation():

	def __init__(self, num_people, percent_infected, amt_distancing, width, height):

		self.people = []
		self.width = width
		self.height = height
		self.paused = False

		self.num_infected = num_people * percent_infected / 100
		self.num_healthy = num_people - self.num_infected

		total_stationary = num_people * stationary_percent[amt_distancing]

		# randomizes the percent of the infected that are stationary
		percent_stationary_inf = random.randint(0,100) / 100		

		self.num_stationary_inf = int(self.num_infected * percent_stationary_inf)
		if self.num_stationary_inf > total_stationary:
			self.num_stationary_inf = int(total_stationary)

		self.num_stationary_healthy = int(total_stationary - self.num_stationary_inf)
		if self.num_stationary_healthy > self.num_healthy:
			self.num_stationary_inf += int(self.num_stationary_healthy - self.num_healthy)
			self.num_stationary_healthy = int(self.num_healthy)

		self.num_moving_inf = int(self.num_infected - self.num_stationary_inf)
		self.num_moving_healthy = int(self.num_healthy - self.num_stationary_healthy)

	def draw(self, win):

		for person1 in self.people:
			if person1.moving:
				person1.updatePos(self.width, self.height)
				for person2 in self.people:
					if person1 != person2:
						self.collide(person1, person2)
			person1.draw(win)

	def generateDot(self, color, radius=None, speed=None, moving=True):

		if not radius:
			radius = random.randint(15,25)
		if not speed:
			speed = random.randint(3,8)

		x = random.randint(radius + 2, self.width - radius - 2)
		y = random.randint(radius + 2, self.height - radius - 2)
		angle = random.uniform(0, math.pi*2)

		self.people.append(Ball(x, y, radius, color, angle, speed, moving))

	def collide(self, ball1, ball2):

		# checks for collision, and performs it if they have collided
		dx = ball1.x - ball2.x
		dy = ball1.y - ball2.y
		dist = math.hypot(dx, dy)
		if dist < (ball1.radius + ball2.radius):
			# has collided
			ball1.speed, ball2.speed = ball2.speed, ball1.speed

			# tangent that the ball will bounce off of
			tangent = math.atan2(dy, dx)	
			ball1.angle = (2 * tangent) - ball1.angle
			ball2.angle = (2 * tangent) - ball2.angle

			# prevents the balls from getting stuck together 
			# by moving them apart slightly so that they dont overlap while trying to collide
			angle = 0.5 * math.pi + tangent
			ball1.x += math.sin(angle)
			ball1.y -= math.cos(angle)
			ball2.x -= math.sin(angle)
			ball2.y += math.cos(angle)

			if ball1.color is RED and ball2.color is GREEN:
				ball2.color = RED
			elif ball2.color is RED and ball1.color is GREEN:
				ball1.color = RED

class Run():
	def __init__(self):
		self.simulations = []
		self.running = True
