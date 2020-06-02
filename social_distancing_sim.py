from ball import *
from button import *
from simulation import *
from numberSelector import NumberSelector
import random
import pygame
pygame.init()

# size of screen
screenWidth = 800
screenHeight = 502

# size of box the simulation is in
boxWidth = 500
boxHeight = 500

win = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Social Distancing Simulation")

font1 = pygame.font.SysFont('cambria', 15)
font2 = pygame.font.SysFont('calibri', 14, True)
font3 = pygame.font.SysFont('calibri', 12)

def redrawScreen():

	# update screen
	win.fill((255,255,255))
	pygame.draw.rect(win, (0,0,0), (0,0,500,500), 2)

	pygame.draw.rect(win, (214,214,214), (520, 15, 260, 300), 1)
	label = font1.render('Create a new simulation:', True, (0,0,0))
	win.blit(label, (540, 30))

	label2 = font2.render('Choose the amount of social', True, (50,50,50))
	label3 = font2.render('distancing:', True, (50,50,50))
	win.blit(label2, (550, 195))
	win.blit(label3, (550, 210))

	for button in buttons:
		if button.visible:
			button.draw(win)

	if len(run.simulations) > 0:
		currentSim = run.simulations[len(run.simulations)-1]
		currentSim.draw(win)

	selectNumPeople.draw(win)
	selectPercentInf.draw(win)

	socDistBtnSet.draw(win)

	pygame.display.update()

def reset():
	# gets rid of all past simulations (clears history)
	run.simulations.clear()

	selectNumPeople.val = 100
	selectPercentInf.val = 5
	pauseOrResumeBtn.text = 'Pause'

	selectNumPeople.updateLabel()
	selectPercentInf.updateLabel()
	pauseOrResumeBtn.updateLabel()

	for button in socDistBtnSet.buttons:
		socDistBtnSet.buttonDeselected(button)

	socDistBtnSet.error = False

def newSim():
	if not socDistBtnSet.selected:
		socDistBtnSet.error = True
	else:
		# resetting the  necessary fields
		pauseOrResumeBtn.text = 'Pause'
		pauseOrResumeBtn.updateLabel()
		if len(run.simulations) > 0:
			# clears so that we don't have previous simulations running in the background 
			run.simulations[len(run.simulations)-1].people.clear()

		if not socDistBtnSet.error:
			run.simulations.append(Simulation(selectNumPeople.val, selectPercentInf.val, socDistBtnSet.selectedVal, boxWidth, boxHeight))

		currentSim = run.simulations[len(run.simulations)-1]											
		
		# generating the simulated people
		for i in range(currentSim.num_moving_healthy):
			currentSim.generateDot(GREEN, 5, 3)
		for i in range(currentSim.num_stationary_healthy):
			currentSim.generateDot(GREEN, 5, 3, False)

		for i in range(currentSim.num_moving_inf):
			currentSim.generateDot(RED, 5, 3)
		for i in range(currentSim.num_stationary_inf):
			currentSim.generateDot(RED, 5, 3, False)

def noSocDist():
	socDistBtnSet.selectedVal = 0

def lowSocDist():
	socDistBtnSet.selectedVal = 1

def modSocDist():
	socDistBtnSet.selectedVal = 2

def highSocDist():
	socDistBtnSet.selectedVal = 3
	
def pauseOrResume():
	if len(run.simulations) > 0:
		currentSim = run.simulations[len(run.simulations)-1]
		currentSim.paused = not currentSim.paused
		if pauseOrResumeBtn.text == 'Pause':
			pauseOrResumeBtn.text = 'Resume'
		else:
			pauseOrResumeBtn.text = 'Pause'
		pauseOrResumeBtn.updateLabel()
	
run = Run()

buttons = []
resetBtn = Button(580, 460, 130, 30, 'Reset Simulation', font1, (0,0,0), (211,211,211), (166,166,166), reset)

# would make more sense that it would says "Run Simulation" for the first one, but after that the button says
# "Apply Changes" or something to that effect
newSimBtn = Button(580, 400, 130, 30, 'Run Simulation', font1, (0,0,0), (211,211,211), (166,166,166), newSim)
pauseOrResumeBtn = Button(520, 330, 70, 30, 'Pause', font1, (0,0,0), (211,211,211), (166,166,166), pauseOrResume)
buttons.extend([resetBtn, newSimBtn, pauseOrResumeBtn])

# Number Selectors to allow the user to choose the amount of people present, and the percentage of them who are infected
selectNumPeople = NumberSelector(620, 90, 100, 'Select the number of people:', 0)
selectPercentInf = NumberSelector(620, 150, 5, 'Select the percent of infected people:', 0, 100)

# activating the buttons of the NumberSelectors
buttons.extend(selectNumPeople.buttons)
buttons.extend(selectPercentInf.buttons)

# Button Set for the user to choose the amount of social distancing they want
select_idle_c = (23,227,23)
select_hover_c = (31,194,31)
noSocDistBtn = Button(560, 230, 80, 20, 'None', font2, (0,0,0), (211,211,211), (166,166,166), noSocDist)
lowSocDistBtn = Button(655, 230, 80, 20, 'Low', font2, (0,0,0), (211,211,211), (166,166,166), lowSocDist)
modSocDistBtn = Button(560, 260, 80, 20, 'Moderate', font2, (0,0,0), (211,211,211), (166,166,166), modSocDist)
highSocDistBtn = Button(655, 260, 80, 20, 'High', font2, (0,0,0), (211,211,211), (166,166,166), highSocDist)

errorLbl = font3.render('Please select a level of social distancing', True, (255,0,0))
socDistBtnSet = ButtonSet([noSocDistBtn, lowSocDistBtn, modSocDistBtn, highSocDistBtn], 
	noSocDistBtn.hover_color, noSocDistBtn.idle_color, select_idle_c, select_hover_c, errorLbl, (550, 290))

clock = pygame.time.Clock()
while run.running:

	# update each button with the current mouse pos
	pos = pygame.mouse.get_pos()
	for button in buttons:
		button.updateHover(pos)
	for button in socDistBtnSet.buttons:
		button.updateHover(pos)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run.running = False

		for button in buttons:
			button.get_event(event)

		socDistBtnSet.get_event(event)

	redrawScreen()
	clock.tick(100)

pygame.quit()

