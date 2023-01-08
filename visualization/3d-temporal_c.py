import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

x = [0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9]
y = [16, 14, 12, 10, 8, 6, 4, 2]


X, Y = np.meshgrid(x, y)
fontsize = 10
ax.set_ylabel('capacity', fontsize=fontsize)
ax.set_xlabel('temporal_p', fontsize=fontsize)
ax.set_xticks(x)
ax.set_yticks(y)
x_descr = [0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9]
y_descr = [16, 14, 12, 10, 8, 6, 4, 2]
ax.set_yticklabels(y_descr, fontsize=10)
ax.set_xticklabels(x_descr, fontsize=10)
ax.set_zlabel('cost', rotation='vertical', fontsize=fontsize)
Z = np.array(Y)
print(Z)

z_16 = [32.27, 27.47, 22.66, 17.83, 12.99, 8.13, 3.31]
z_14 = [32.90, 28.01, 23.11, 18.18, 13.25, 8.29, 3.38]
z_12 = [33.63, 28.64, 23.63, 18.61, 13.56, 8.49, 3.46]
z_10 = [34.48, 29.37, 24.25, 19.10, 13.92, 8.72, 3.55]
z_8 = [35.59, 30.33, 25.05, 19.74, 14.40, 9.02, 3.68]
z_6 = [37.15, 31.69, 26.21, 20.67, 15.10, 9.47, 3.85]
z_4 = [39.58, 33.83, 28.04, 22.18, 16.24, 10.22, 4.16]
z_2 = [45.05, 38.76, 32.38, 25.85, 19.15, 12.22, 5.09]

for i in range(0, len(z_16)):
    Z[0][i] = z_16[i]
for i in range(0, len(z_16)):
    Z[1][i] = z_14[i]
for i in range(0, len(z_16)):
    Z[2][i] = z_12[i]
for i in range(0, len(z_16)):
    Z[3][i] = z_10[i]
for i in range(0, len(z_8)):
    Z[4][i] = z_8[i]
for i in range(0, len(z_16)):
    Z[5][i] = z_6[i]
for i in range(0, len(z_16)):
    Z[6][i] = z_4[i]
for i in range(0, len(z_16)):
    Z[7][i] = z_2[i]

print(Z)
print(X)
print(Y)

norm = plt.Normalize(Z.min(), Z.max())
colors = cm.Blues(norm(Z))
rcount, ccount, _ = colors.shape
surf = ax.plot_surface(X, Y, Z, rcount=rcount, ccount=ccount,
                       facecolors=colors, shade=False)
surf.set_facecolor((0.0, 0, 0.0, 0.6))
ax.view_init(15, 40)

plt.savefig("3d_plot_temp.pdf",bbox_inches='tight')
plt.show()