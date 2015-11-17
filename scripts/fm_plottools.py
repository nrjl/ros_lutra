import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random

def init_fig():
    fign=plt.figure()
    axn=fign.add_subplot(111)
    axn.set_aspect('equal', 'datalim')
    axn.tick_params(labelbottom='on',labeltop='off')
    axn.set_xlabel('x')
    axn.set_ylabel('y') 
    axn.autoscale(tight=True)
    return fign, axn

def generate_obstacles(width, height, num_obstacles, max_size=None):
    if max_size==None:
        max_size = width/4
    obs_list = []
    for ii in range(num_obstacles):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        sx = random.randint(1, min(max_size, width-x))
        sy = random.randint(1, min(max_size, height-y))
        obs_list.extend([(a, b) for a in range(x, x+sx) for b in range(y, y+sy)])
    return obs_list
            
def draw_grid(axes, grid, path=[], max_cost = 0):
    if axes.images:
        axes.images.pop()
    grid_mat = np.zeros((grid.width, grid.height))
    for x in range(grid.width):
        for y in range(grid.height):
            grid_mat[x,y] = grid.node_cost((x,y))
    for x,y in grid.obstacles:
        grid_mat[x,y] = -1
    grid_mat = np.ma.masked_where(grid_mat == -1, grid_mat)
    max_cost = max(max_cost, grid_mat.max())
    cmap = plt.cm.terrain
    cmap.set_bad(color='black')
    axes.set_xlim([0, grid.width]); axes.set_ylim([0, grid.height])
    mat_out =  [axes.matshow(grid_mat.transpose(), interpolation='none', cmap=cmap, vmax=max_cost)]
    if len(path) > 0:
        x, y = zip(*path)
        mat_out.append(axes.plot(x, y, 'w-', linewidth=2.0 )[0])
    axes.tick_params(labelbottom='on',labeltop='off')
    return mat_out, [grid_mat.min(), grid_mat.max()]
    
def draw_costmap(axes, grid, cost_to_come, path=[]):
    if axes.images:
        axes.images.pop()
    cost_mat = -1*np.ones((grid.width, grid.height))
    for node in cost_to_come:
        cost_mat[node[0],node[1]] = cost_to_come[node]
    for x,y in grid.obstacles:
        cost_mat[x,y] = -2
    cost_mat = np.ma.masked_where(cost_mat == -2, cost_mat)
    cmap = plt.cm.jet
    cmap.set_bad(color='black')
    cmap.set_over(color='#C2A366')
    cmap.set_under(color='0.8')

    axes.set_xlim([0, grid.width]); axes.set_ylim([0, grid.height])
    mat_out = [axes.matshow(cost_mat.transpose(), 
        norm = matplotlib.colors.Normalize(vmin=0, vmax=cost_mat.max(), clip=False))]
    if len(path) > 0:
        x, y = zip(*path)
        mat_out.append(axes.plot(x, y, 'w-', linewidth=2.0 )[0])
    axes.tick_params(labelbottom='on',labeltop='off')
    return mat_out


def draw_corridor(axes, grid, cost_to_come, corridor, interface=[], path=[]):
    if axes.images:
        axes.images.pop()
    cost_mat = -1*np.ones((grid.width, grid.height))
    for node in corridor:
        cost_mat[node[0],node[1]] = cost_to_come[node]
    for x,y in grid.obstacles:
        cost_mat[x,y] = -2
    max_cost = cost_mat.max()
    for node in interface:
        cost_mat[node[0],node[1]] = max_cost+1
    cost_mat = np.ma.masked_where(cost_mat == -2, cost_mat)
    cmap = plt.cm.jet
    cmap.set_bad(color='black')
    cmap.set_over(color='#C2A366')
    cmap.set_under(color='0.8')

    axes.set_xlim([0, grid.width]); axes.set_ylim([0, grid.height])
    mat_out = [axes.matshow(cost_mat.transpose(),
        norm = matplotlib.colors.Normalize(vmin=0, vmax=max_cost, clip=False))]
    if len(path) > 0:
        x, y = zip(*path)
        mat_out.append(axes.plot(x, y, 'w-', linewidth=2.0 )[0])
    axes.tick_params(labelbottom='on',labeltop='off')

    return mat_out


def draw_fbfmcost(axes, grid, path_cost, path=[], min_cost = 1e7, max_cost = 0):
    if axes.images:
        axes.images.pop()
    grid_mat = np.zeros((grid.width, grid.height))
    for x in range(grid.width):
        for y in range(grid.height):
            if (x,y) in path_cost:
                grid_mat[x,y] = path_cost[(x,y)]
    for x,y in grid.obstacles:
        grid_mat[x,y] = -1
    grid_mat = np.ma.masked_where(grid_mat == -1, grid_mat)
    cmap = plt.cm.jet
    cmap.set_bad(color='black')
    axes.set_xlim([0, grid.width]); axes.set_ylim([0, grid.height])
    max_cost = max(max_cost, grid_mat.max())
    min_cost = min(min_cost, min(path_cost.values()))
    mat_out =  [axes.matshow(grid_mat.transpose(), interpolation='none', cmap=cmap, vmax=max_cost, vmin=min_cost)]
    if len(path) > 0:
        x, y = zip(*path)
        mat_out.append(axes.plot(x, y, 'w-', linewidth=2.0 )[0])
    axes.tick_params(labelbottom='on',labeltop='off')
    #axes.figure.colorbar(mat_out[0])
    return mat_out, [grid_mat.min(), grid_mat.max()]