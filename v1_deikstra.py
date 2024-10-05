import heapq
from math import sqrt

# дороги между городами с ограничениями по весу
graph = {
    'Москва': {'Челябинск': {'distance': 1800, 'weight_limit': 20},
               'Санкт-Петербург': {'distance': 700, 'weight_limit': 10},
               'Нижний Новгород': {'distance': 400, 'weight_limit': 5}},
    'Санкт-Петербург': {'Челябинск': {'distance': 2200, 'weight_limit': 20},
                        'Москва': {'distance': 700, 'weight_limit': 10},
                        'Ростов-на-Дону': {'distance': 1500, 'weight_limit': 15}},
    'Ростов-на-Дону': {'Челябинск': {'distance': 1500, 'weight_limit': 10},
                       'Пятигорск': {'distance': 500, 'weight_limit': 5},
                       'Москва': {'distance': 1000, 'weight_limit': 5}},
    'Нижний Новгород': {'Челябинск': {'distance': 1600, 'weight_limit': 5},
                        'Москва': {'distance': 400, 'weight_limit': 5}},
    'Пятигорск': {'Челябинск': {'distance': 2600, 'weight_limit': 20},
                  'Ростов-на-Дону': {'distance': 500, 'weight_limit': 5}},
    'Екатеринбург': {'Челябинск': {'distance': 200, 'weight_limit': 10},
                     'Новосибирск': {'distance': 2000, 'weight_limit': 20}},
    'Новосибирск': {'Челябинск': {'distance': 1800, 'weight_limit': 10},
                    'Владивосток': {'distance': 3500, 'weight_limit': 20}},
    'Владивосток': {'Челябинск': {'distance': 6000, 'weight_limit': 20}},
    'Челябинск': {}
}

# Координаты городов для A*
city_coords = {
    'Москва': (55.7558, 37.6176),
    'Санкт-Петербург': (59.9343, 30.3351),
    'Ростов-на-Дону': (47.2357, 39.7015),
    'Нижний Новгород': (56.3269, 44.0059),
    'Пятигорск': (44.0486, 43.0594),
    'Екатеринбург': (56.8389, 60.6057),
    'Новосибирск': (55.0084, 82.9357),
    'Владивосток': (43.1155, 131.8855),
    'Челябинск': (55.1644, 61.4368)
}

# Транспортные средства: грузоподъемность в тоннах и объем в куб.м
vehicles = [
    {'name': 'Транспорт 1', 'capacity': 1.5, 'volume': 18},  # Малый грузовик
    {'name': 'Транспорт 2', 'capacity': 3.0, 'volume': 25},  # Средний грузовик
    {'name': 'Транспорт 3', 'capacity': 5.0, 'volume': 36},  # Средний грузовик
    {'name': 'Транспорт 4', 'capacity': 10.0, 'volume': 50}, # Большой грузовик
    {'name': 'Транспорт 5', 'capacity': 20.0, 'volume': 86}  # Очень большой грузовик
]

# Пример данных комплектующих: Название, вес в кг, объем в м3
components = [
    {'name': 'Драйверы', 'weight': 1080, 'volume': 600},
    {'name': 'Платы, микросхемы', 'weight': 1.75, 'volume': 500},
    {'name': 'Вставка', 'weight': 35.416, 'volume': 800},
    {'name': 'Манжеты', 'weight': 1.005, 'volume': 300},
    {'name': 'Блоки (контакт, перемычки)', 'weight': 0.23, 'volume': 2300},
    {'name': 'Шайбы', 'weight': 73.8, 'volume': 12300},
    {'name': 'Подшипники', 'weight': 250, 'volume': 1000},
    {'name': 'Проводка', 'weight': 3680.6, 'volume': 13145},
    {'name': 'Ремни', 'weight': 1.5, 'volume': 500},
    {'name': 'Винты', 'weight': 22.25, 'volume': 8900},
    {'name': 'Разъемы', 'weight': 11.04, 'volume': 4800},
    {'name': 'Питание', 'weight': 315, 'volume': 2100},
    {'name': 'Редукторы', 'weight': 1050, 'volume': 500},
    {'name': 'Серво-моторы', 'weight': 60, 'volume': 600},
    {'name': 'Резисторы, конденсаторы', 'weight': 2.166, 'volume': 3800},
    {'name': 'Фитинги', 'weight': 75, 'volume': 1500},
]

# Функция для расчета расстояния по прямой между городами
def heuristic(city1, city2):
    x1, y1 = city_coords[city1]
    x2, y2 = city_coords[city2]
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Алгоритм A* с учетом ограничения по весу транспортного средства
def a_star(graph, start, target, vehicle_capacity):
    queue = [(0, start)]  # Очередь с приоритетом: (стоимость, город)
    g_costs = {node: float('inf') for node in graph}  # Стоимость пути до каждого города
    g_costs[start] = 0
    f_costs = {node: float('inf') for node in graph}  # Общая стоимость пути (включая эвристику)
    f_costs[start] = heuristic(start, target)
    shortest_path = {}  # Для восстановления маршрута

    while queue:
        current_f_cost, current_city = heapq.heappop(queue)

        if current_city == target:
            break

        for neighbor, info in graph[current_city].items():
            if vehicle_capacity <= info['weight_limit']:  # Учитываем ограничения по весу
                tentative_g_cost = g_costs[current_city] + info['distance']

                if tentative_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g_cost
                    f_costs[neighbor] = tentative_g_cost + heuristic(neighbor, target)
                    heapq.heappush(queue, (f_costs[neighbor], neighbor))
                    shortest_path[neighbor] = current_city

    return g_costs, shortest_path

# восстановление пути
def reconstruct_path(shortest_path, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = shortest_path[current]
    path.append(start)
    return path[::-1]

#расчет маршрута   для каждого транспорта
def calculate_route(graph, start_city, end_city, vehicle_capacity):
    g_costs, shortest_path = a_star(graph, start_city, end_city, vehicle_capacity)
    route = reconstruct_path(shortest_path, start_city, end_city)
    return g_costs[end_city], route

# Оптимальное распределение деталей по машинам
def allocate_components_to_vehicles(components, vehicles):
    allocation = {vehicle['name']: [] for vehicle in vehicles}

    for component in components:
        # Поиск машины, в которую можно загрузить комплектующие по весу и объему
        for vehicle in vehicles:
            if component['weight'] <= vehicle['capacity'] * 1000:  # Преобразуем в кг
                allocation[vehicle['name']].append(component)
                break

    return allocation

# тестим
start_city = 'Москва'
end_city = 'Челябинск'

# выбор транспорта
for vehicle in vehicles:
    cost, route = calculate_route(graph, start_city, end_city, vehicle['capacity'])
    print(f"{vehicle['name']}: Кратчайший маршрут: {' -> '.join(route)} (стоимость: {cost} км)")

# распределяем комплектующиие по транспортным средствам
allocation = allocate_components_to_vehicles(components, vehicles)
for vehicle, load in allocation.items():
    print(f"\n{vehicle} загружен комплектующими:")
    for component in load:
        print(f" - {component['name']} (вес: {component['weight']} кг)")
