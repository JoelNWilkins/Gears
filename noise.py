import numpy
from matplotlib import pyplot as plt

def noise(beta, u, epsilon_alpha, v, W, X):
    L = (((20 * (1 - numpy.tan(beta / 2)) * u**(1/8)) / epsilon_alpha**(1/4))
         * numpy.sqrt((5.56 + numpy.sqrt(v)) / 5.56))
    if W != 0:
        L += 20 * numpy.log10(W / 1000)
    if X != 0:
        L += 20 * numpy.log10(X)
    return L

#z_1 = int(input("Number of teeth on driver: "))
#z_2 = int(input("Number of teeth on driven: "))

plt.figure(1)
plt.suptitle("\nQualative Analysis of Gear Noise", fontsize=16)

beta = 0
u = 1
epsilon_alpha = 1
v = 0.048
W = 0
X = 0

x = numpy.linspace(0.01, 5, 100)
y = []

for epsilon_alpha in x:
    L = noise(beta, u, epsilon_alpha, v, W, X)
    y.append(L)

plt.subplot(221)
plt.plot(x, y)
plt.title("Contact Ratio")
plt.xticks([])
plt.yticks([])

beta = 0
u = 1
epsilon_alpha = 1
v = 0.048
W = 0
X = 0

x = numpy.linspace(0, 10, 100)
y = []

for v in x:
    L = noise(beta, u, epsilon_alpha, v, W, X)
    y.append(L)

plt.subplot(222)
plt.plot(x, y)
plt.title("Reference Velocity")
plt.xticks([])
plt.yticks([])

beta = 0
u = 1
epsilon_alpha = 1
v = 0.048
W = 0
X = 0

x = numpy.linspace(0, 10, 100)
y = []

for u in x:
    L = noise(beta, u, epsilon_alpha, v, W, X)
    y.append(L)

plt.subplot(223)
plt.plot(x, y)
plt.title("Gear Ratio")
plt.xticks([])
plt.yticks([])

beta = 0
u = 1
epsilon_alpha = 1
v = 0.048
W = 0
X = 0

x = numpy.linspace(1, 100, 100)
y = []

for W in x:
    L = noise(beta, u, epsilon_alpha, v, W, X)
    y.append(L)

plt.subplot(224)
plt.plot(x, y)
plt.title("Power Output")
plt.xticks([])
plt.yticks([])

plt.subplots_adjust(top=0.8, bottom=0.08, left=0.1, right=0.9, hspace=0.25,
                    wspace=0.35)

plt.show()
