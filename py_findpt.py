# Experimenting with matplotlib

import matplotlib.pyplot as plt
import random
import math
import copy

def move(player_x, player_y, dir_num):
    last_dist = math.dist([copy.deepcopy(player_x), copy.deepcopy(player_y)], [destination_x, destination_y])
    # first move
    if dir_num == 0:
        dir_num = random.choice([-1, 1, -2, 2])
    # last move
    if dir_num == 10:
        if player_x == destination_x:
            chg_y = destination_y - player_y
            player_y += chg_y
        elif player_y == destination_y:
            chg_x = destination_x - player_x
            player_x += chg_x      
    if dir_num == 1:
        player_x += 1
    if dir_num == -1:
        player_x -= 1
    if dir_num == 2:
        player_y += 1
    if dir_num == -2:
        player_y -= 1
    new_dist = math.dist([player_x, player_y], [destination_x, destination_y])
    return player_x, player_y, dir_num, last_dist, new_dist

def determine_reward(last_dist, new_dist):
    if new_dist == 1.0:
        reward_pts = 10
    elif new_dist < last_dist:
        reward_pts = 1
    elif new_dist > last_dist:
        reward_pts = -1
    return reward_pts

# Updating function, to be repeatedly called by the animation
def update(player_x, player_y, reward_pts, dir_num):
    last_dist = 0
    new_dist = 0
    if reward_pts == 10:
        dir_num = 10
        player_x, player_y, dir_num, last_dist, new_dist = move(player_x, player_y, dir_num)
    elif reward_pts >= 0:
        player_x, player_y, dir_num, last_dist, new_dist = move(player_x, player_y, dir_num)
    elif reward_pts < 0:
        dir_list = [-1, 1, -2, 2]
        dir_list.remove(dir_num)
        dir_num = random.choice(dir_list)
        player_x, player_y, dir_num, last_dist, new_dist = move(player_x, player_y, dir_num)
    return player_x, player_y, last_dist, new_dist, dir_num

# Determine x, y coordinates for destination point
destination_x = random.randint(-100, 100)
destination_y = random.randint(-100, 100)
destination_coord = (destination_x, destination_y)
# Set starting position for player
player_x = random.randint(-100, 100)
player_y = random.randint(-100, 100)

reward_pts = 0
dir_num = 0
new_dist = 1
dir_list = [-1, 1, -2, 2]

# create a figure with an axes
fig, ax = plt.subplots()
plt.title('Point Finder')
# set the axes limits
ax.axis([-100,100,-100, 100])
# set equal aspect such that the circle is not shown as ellipse
ax.set_aspect("equal")
# create a point in the axes
player_point, = ax.plot(player_x,player_y, marker="s")
destination_pt = ax.plot(destination_x, destination_y, marker='o', markersize=15, markerfacecolor="green")

while new_dist != 0:
    player_x, player_y, last_dist, new_dist, dir_num = update(player_x, player_y, reward_pts, dir_num)
    reward_pts = determine_reward(last_dist, new_dist)
    ax.plot(player_x, player_y, marker='s', markersize=1, markerfacecolor="red")
    print("new_dist: ", new_dist)


plt.show()
