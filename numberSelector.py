from button import *
import pygame
pygame.font.init()

font1 = pygame.font.SysFont('cambria', 15)
font2 = pygame.font.SysFont('calibri', 14, True)

class NumberSelector():

	def __init__(self, x, y, initialVal, prompt, minV=None, maxV=None):

		self.x = x
		self.y = y
		self.width = 55
		self.height = 25
		self.rect = pygame.Rect(x, y, self.width, self.height)
		self.val = initialVal
		self.min = minV
		self.max = maxV

		self.prompt = font2.render(prompt, True, (50,50,50))

		self.label = font1.render(str(self.val), True, (0,0,0))
		self.label_rect = self.label.get_rect(center=self.rect.center)

		self.superDownBtn = None
		self.downBtn = None
		self.upBtn = None
		self.superUpBtn = None
		self.createButtons()

		self.buttons = [self.superDownBtn, self.downBtn, self.upBtn, self.superUpBtn]
		
	def draw(self, win):

		pygame.draw.rect(win, (255,255,255), self.rect)
		win.blit(self.prompt, (self.x-70, self.y-20))
		win.blit(self.label, self.label_rect)

		self.superDownBtn.draw(win)
		self.downBtn.draw(win)
		self.upBtn.draw(win)
		self.superUpBtn.draw(win)

	def createButtons(self):
		btnWidth = 30																				
		self.superDownBtn = Button(self.rect.x - (2*btnWidth), self.y, btnWidth, self.height, '<<', font1, (0,0,0), (211,211,211), (166,166,166), self.superDown)
		self.downBtn = Button(self.rect.x - btnWidth, self.y, btnWidth, self.height, '<', font1, (0,0,0), (211,211,211), (166,166,166), self.down)
		self.upBtn = Button(self.rect.right, self.y, btnWidth, self.height, '>', font1, (0,0,0), (211,211,211), (166,166,166), self.up)
		self.superUpBtn = Button(self.rect.right + btnWidth, self.y, btnWidth, self.height, '>>', font1, (0,0,0), (211,211,211), (166,166,166), self.superUp)

	def superDown(self):
		if self.min != None and self.val - 10 < self.min:
			self.val = 0
		else:
			self.val -= 10
		self.updateLabel()

	def down(self):
		if self.min != None and self.val - 1 < self.min:
			self.val = 0
		else:
			self.val -= 1
		self.updateLabel()

	def up(self):
		if self.max != None and self.val + 1 > self.max:
			self.val = self.max
		else:
			self.val += 1
		self.updateLabel()

	def superUp(self):
		if self.max != None and self.val + 10 > self.max:
			self.val = self.max
		else:
			self.val += 10
		self.updateLabel()

	def updateLabel(self):
		self.label = font1.render(str(self.val), True, (0,0,0))
		self.label_rect = self.label.get_rect(center=self.rect.center)