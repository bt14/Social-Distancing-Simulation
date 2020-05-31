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

def runSim():

	if run.newVals:
		if not socDistBtnSet.selected:
			socDistBtnSet.error = True
			return
		else:
			run.simulations.append(Simulation(selectNumPeople.val, selectPercentInf.val, socDistBtnSet.selectedVal, boxWidth, boxHeight))
			# socDistBtnSet.error = False	
				# if we do this here instead of noSocDist() and the rest, it'll only hide the error message when
				# you click "run simulation" istead of when you choose a level of social distancing
	
	currentSim = run.simulations[len(run.simulations)-1]											
	
	for i in range(currentSim.num_moving_healthy):
		currentSim.generateDot(GREEN, 5, 3)
	for i in range(currentSim.num_stationary_healthy):
		currentSim.generateDot(GREEN, 5, 3, False)

	for i in range(currentSim.num_moving_inf):
		currentSim.generateDot(RED, 5, 3)
	for i in range(currentSim.num_stationary_inf):
		currentSim.generateDot(RED, 5, 3, False)

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
		button.draw(win)

	if len(run.simulations) > 0:
		currentSim = run.simulations[len(run.simulations)-1]
		currentSim.draw(win)

	selectNumPeople.draw(win)
	selectPercentInf.draw(win)

	socDistBtnSet.draw(win)

	pygame.display.update()

def reset():
	run.newVals = False
	# clears the people array of the last simulation in the list
	run.simulations[len(run.simulations)-1].people.clear()
	runSim()

def newSim():
	run.newVals = True
	if len(run.simulations) > 0:
		run.simulations[len(run.simulations)-1].people.clear()
	runSim()

def noSocDist():
	socDistBtnSet.selectedVal = 0
	socDistBtnSet.error = False	

def lowSocDist():
	socDistBtnSet.selectedVal = 1
	socDistBtnSet.error = False

def modSocDist():
	socDistBtnSet.selectedVal = 2
	socDistBtnSet.error = False

def highSocDist():
	socDistBtnSet.selectedVal = 3
	socDistBtnSet.error = False


run = Run()

buttons = []
resetBtn = Button(580, 460, 130, 30, 'Reset Simulation', font1, (0,0,0), (211,211,211), (166,166,166), reset)

# would make more sense that it would says "Run Simulation" for the first one, but after that the button says
# "Apply Changes" or something to that effect
runSimBtn = Button(580, 400, 130, 30, 'Run Simulation', font1, (0,0,0), (211,211,211), (166,166,166), newSim)
buttons.extend([resetBtn, runSimBtn])

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

# add the ability to deselect buttons within a ButtonSet (and check for error accordingly)

'''
--------------------------------------------------------------------------------------------------------------------------------

possible things to add later:

	- maybe if i wanna get really fancy i can have a little timer that stops when everyone has been infected
	  (quantify how much social distancing slows down the spread)

	- could also have a timer for each person thats infected that changes them to a recovered state (dif color)
	  in the recovered state they're now immune (can't get infected)
	  (inspired by that washington post article with a very similar simulation lol)

	- maybe add functionality so that you can pause the simulation at any time, but then you can also resume it
	  this would mean setting all the ball object's moving var to False, but still remembering their previous value so that 
	  it can resume where it left off
	  oh actually can just have a boolean for if the simulation is paused or not and go from there

	- could have something so that you can toggle back an forth to previous simulation runs for easy comparison

	---------------

	** to do next:  pause functionality
					- have a pause button that changes to unpause when paused and vice versa
					- have a "Clear" button to clear screen
					- make sure to pause the ones in the background (the old simulations)

--------------------------------------------------------------------------------------------------------------------------------
'''


# uncomment these if you want it to start running right out of the gate
# sim = Simulation(100, 5, 2, boxWidth, boxHeight)
# run.simulations.append(sim)
# runSim()

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

