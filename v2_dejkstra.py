import heapq

# компоненты
components = [
    {'name': 'Драйверы', 'weight': 1080, 'volume': 5, 'destination': 'Москва'},
    {'name': 'Платы', 'weight': 1.75, 'volume': 2, 'destination': 'Ростов-на-Дону'},
    {'name': 'Шайбы', 'weight': 73.8, 'volume': 3, 'destination': 'Санкт-Петербург'},
    {'name': 'Подшипники', 'weight': 250, 'volume': 2, 'destination': 'Владивосток'},
    {'name': 'Редукторы', 'weight': 1050, 'volume': 3, 'destination': 'Екатеринбург'},
    # Добавьте остальные компоненты
]

# транспортные средства
vehicles = [
    {'name': 'Vehicle1', 'capacity': 1500, 'volume': 18},
    {'name': 'Vehicle2', 'capacity': 3000, 'volume': 25},
    {'name': 'Vehicle3', 'capacity': 5000, 'volume': 36},
    {'name': 'Vehicle4', 'capacity': 10000, 'volume': 50},
    {'name': 'Vehicle5', 'capacity': 20000, 'volume': 86},
    {'name': 'Vehicle6', 'capacity': 700, 'volume': 4},
]

# дороги с ограничениями по весу
roads = [
    {'from': 'Москва', 'to': 'Челябинск', 'distance': 1780, 'weight_limit': 20000},
    {'from': 'Ростов-на-Дону', 'to': 'Челябинск', 'distance': 1700, 'weight_limit': 10000},
    {'from': 'Санкт-Петербург', 'to': 'Челябинск', 'distance': 2500, 'weight_limit': 15000},
    {'from': 'Владивосток', 'to': 'Челябинск', 'distance': 8000, 'weight_limit': 10000},
    {'from': 'Екатеринбург', 'to': 'Челябинск', 'distance': 200, 'weight_limit': 20000},
    # Добавьте остальные дороги
]


# Нахождим кратчайший путь (ну хотя бы пытаемся; алгоритм Дейкстры)
def dijkstra(graph, start, end):
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    return distances[end]


# дороги (расстояние)
graph = {
    'Москва': {'Челябинск': 1780},
    'Ростов-на-Дону': {'Челябинск': 1700},
    'Санкт-Петербург': {'Челябинск': 2500},
    'Владивосток': {'Челябинск': 8000},
    'Екатеринбург': {'Челябинск': 200},
    # Добавьте остальные города
}


# Распределение товаров по машинам и дорогам
def allocate_goods_to_vehicles(components, vehicles, roads):
    allocation = []
    for component in components:
        city = component['destination']
        weight = component['weight']
        volume = component['volume']

        # Найдем возможный маршрут
        route_found = False
        for road in roads:
            if road['from'] == city and road['to'] == 'Челябинск' and road['weight_limit'] >= weight:
                route_found = True

                # Подбираем подходящее транспортное средство
                vehicle_found = False
                for vehicle in vehicles:
                    if vehicle['capacity'] >= weight and vehicle['volume'] >= volume:
                        allocation.append({
                            'component': component['name'],
                            'vehicle': vehicle['name'],
                            'from': city,
                            'to': 'Челябинск',
                            'distance': road['distance'],
                            'cost': (road['distance'] * weight) * 8  # 8 руб. за тонну на км
                        })
                        vehicle_found = True
                        break  # Как только нашли транспорт, выходим из цикла

                if not vehicle_found:
                    print(
                        f"Нет доступного транспорта для товара {component['name']} с весом {weight} т и объемом {volume} м³ из города {city}")

                break  # Как только нашли подходящий маршрут, выходим из цикла

        if not route_found:
            print(f"Нет доступного маршрута для товара {component['name']} с весом {weight} т из города {city}")

    return allocation


# тестим
result = allocate_goods_to_vehicles(components, vehicles, roads)

if not result:
    print("Не удалось отправить ни одного товара.")
else:
    total_cost = 0
    for item in result:
        print(f"Товар {item['component']} отправлен из {item['from']} в {item['to']} "
              f"с использованием {item['vehicle']}, расстояние {item['distance']} км, "
              f"стоимость {item['cost']} руб.")
        total_cost += item['cost']
    print(f"Общая стоимость доставки: {total_cost} руб.")

# ищем кратчайший путь
for city in ['Москва', 'Ростов-на-Дону', 'Санкт-Петербург', 'Владивосток', 'Екатеринбург']:
    print(f"Кратчайший путь от {city} до Челябинска: {dijkstra(graph, city, 'Челябинск')} км")
