import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def A_matrix(theta, d, a, alpha):
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

def get_transformation_matrices(dh_params):
    T = np.eye(4)
    transformations = []
    for param in dh_params:
        theta, d, a, alpha = param
        T = np.matmul(T, A_matrix(theta, d, a, alpha))
        transformations.append(T)
    return transformations

def update_angles(thetas):
    dh_params = [
        (thetas[0], 333, 185, -np.pi/2),
        (thetas[1], 0, 534, -np.pi),
        (thetas[2], 0, 0, np.pi/2),
        (thetas[3], 594, 0, np.pi/2),
        (thetas[4], 0, 0, -np.pi/2),
        (np.pi, 160, 0, 0),
    ]
    transformations = get_transformation_matrices(dh_params)
    return transformations

def plot_manipulator(ax, thetas):
    transformations = update_angles(thetas)
    
    ax.cla()
    
    x = [0, 0]
    y = [0, 0]
    z = [0, 333]
    
    for i, T in enumerate(transformations):
        x.append(T[0, 3])
        y.append(T[1, 3])
        z.append(T[2, 3])
        print(T[2, 3])
    
    ax.plot(x, y, z, marker='o')
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
    ax.set_xlim([-1000, 1000])
    ax.set_ylim([-1000, 1000])
    ax.set_zlim([0, 1000])

    plt.draw()

def d_to_r(angle):
    return np.pi / 180 * angle

def r_to_g(x):
    return 180 * x / np.pi

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.35)

theta_init = [0, -np.pi/2, 0, 0, -np.pi, np.pi]                 
 
plot_manipulator(ax, theta_init)                                  

ax_theta = []
sliders = []

for i in range(5):
    ax_theta.append(plt.axes([0.1, 0.25 - 0.05*i, 0.8, 0.03]))
    sliders.append(Slider(ax_theta[i], f'Theta {i+1}', -180,180, valinit=r_to_g(theta_init[i])))

def update(val):                                                       
    thetas = [d_to_r(slider.val) for slider in sliders]                        
    plot_manipulator(ax, thetas)

for slider in sliders:
    slider.on_changed(update)

plt.show()
