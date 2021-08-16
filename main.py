from params import *
from build.utils import Pose
from build.player import Player
from Simulation.simulation import *
from Simulation.Scenario import Scenario
from Simulation.keyboard import Keyboard
from Simulation.main_neural import save_neural
import os

for file in os.listdir("Utils/"):
    if ".c" in file:
        os.system('mv Utils/{} build/{}'.format(file, file))

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("./Img/icon.png")
pygame.display.set_caption("Carros autonâmos")
clock = pygame.time.Clock()
pygame.display.set_icon(icon)

players = []
for i in range(N_PLAYERS):
    players.append(Player(i))
    players[i].set_pose(Pose(PIX2M * round(INIT_LINE[0] + i*INIT_MULTIPLICATION/N_PLAYERS), PIX2M * INIT_LINE[1], -pi/2))
    # players[i].set_pose(Pose(POSE[0],POSE[1], -pi/2))
    players[i].init_neural_network()

simulation = Simulation(players)
cars = [pygame.image.load("./Img/carro"+str(i%7)+".png") for i in range(N_PLAYERS)]
# collision array
mapParameters = MAP_PARAMETERS
carsParameters = []
simulation.initScenario(window, mapParameters, cars)

# user = input("Deseja jogar também?(y/n)")
# while user not in ['y', 'Y', 'n', 'N']:
#     user = input("Deseja jogar também?(y/n)")

# remove after

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            mapParameters, carsParameters = Keyboard(event.key, mapParameters, carsParameters)
        else:
            key = None
    if key == None:
        mapParameters, carsParameters = Keyboard(key, mapParameters, carsParameters)

    if mapParameters[2]:
        save_neural(simulation.players)
        mapParameters[2] = False
    if mapParameters[3] != '':
        simulation.load_saved_neural(mapParameters[3])
    clock.tick(FREQUENCY)
    pygame.event.pump()
    simulation.scenario.mapParameters = mapParameters
    draw(simulation)
    simulation.update()

pygame.quit()
