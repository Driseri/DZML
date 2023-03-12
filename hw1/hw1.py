from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance_matrix


def opt_2(points):
    # Вычисляем матрицу расстояний между точками.
    dist_matrix = distance_matrix(points, points)

    # Функция, которая возвращает длину между точками
    def metric(a, b):
        distance = np.sum(np.sqrt((a - b)**2))
        return distance

    #Подсчет расстояния маршрута
    def CalculateEnergy(route):
        E = 0
        for i in range(len(route) - 1):
            E += dist_matrix[route[i]][route[i+1]]
        E += dist_matrix[route[-1]][route[0]]
        return E

    # Функция, которая меняет порядок двух ребер маршрута
    def swap(route, i, j):
        new_route = route[:]
        new_route[i:j+1] = route[i:j+1][::-1]
        return new_route

    # Начальное состояние маршрута
    current_route = list(range(len(points)))
    # print(current_route)
    current_length = CalculateEnergy(current_route)
    init_length = current_length
    print('initial route length: ', init_length)
    # Повторяем процесс до тех пор, пока мы не сможем улучшить маршрут
    improv = True
    while improv:
        improv = False
        for i in range(len(current_route) - 2):
            for j in range(i+2, len(current_route)):
                new_route = swap(current_route, i, j)
                new_length = CalculateEnergy(new_route)
                if new_length < current_length:
                    current_route = new_route[:]
                    current_length = new_length
                    improv = True
                    break
            if improv:
                break
    opt_points = [points[i] for i in current_route]
    return opt_points, current_length, init_length


def SimulatedAnnealing():
    nCities = 100;
    initialTemperature = 100;
    endTemperature = 0;

    cities = np.random.rand(nCities, 2) * 10
    return cities

points = SimulatedAnnealing()



opt_points, opt_length, init_length = opt_2(points)

aert = np.array([list(i) for i in opt_points])

fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)
# Отображение
axs[0].plot(points[:, 0], points[:, 1], "g--o")
axs[0].set_title('initial route')
axs[0].text(-1,-1, 'initial route length: '+ str(init_length), fontsize=11, color='black')

axs[1].plot(aert[:, 0], aert[:, 1], "g--o")
axs[1].set_title('optimized route')
axs[1].text(-1,-1, 'optimized route length: ' + str(opt_length), fontsize=11, color='black')
print('optimized route length: ', opt_length)
plt.show()

