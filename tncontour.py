from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

x = np.arange(-5,5,0.1)
y = np.arange(-5,5,0.1)
X,Y = np.meshgrid(x,y)
Z = X*np.exp(-X**2)

fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.8)#, cmap=cm.ocean)
cset = ax.contour(X, Y, Z, zdir='z', offset=np.min(Z))#, cmap=cm.ocean)
cset = ax.contour(X, Y, Z, zdir='x', offset=-5, cmap=cm.ocean)
cset = ax.contour(X, Y, Z, zdir='y', offset=5)#, cmap=cm.ocean)

#fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

ax.set_xlabel('X')
ax.set_xlim(-5, 5)
ax.set_ylabel('Y')
ax.set_ylim(-5, 5)
ax.set_zlabel('Z')
ax.set_zlim(np.min(Z), np.max(Z))
ax.set_title('3D surface with 2D contour plot projections')

plt.show()
