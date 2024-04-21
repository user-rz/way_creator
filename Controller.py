
from Model import *

# Initial_stop = str(input())
# Final_stop = str(input())

"""
Программа Controller.py: 
Содержит описание класса путей Way и класса построителя путей WayCreator.
Инициализирует список путей Ways.
"""

Ways = list()


class Way:
    number: int
    initial_stop: str
    final_stop: str
    stops: list
    routes: list
    good_way: bool
    time: float

    def __init__(self, new_change, new_route, number, appointed_changes, appointed_routes):
        """
        Путь - непрерывная ломаная из отрезков маршрутов.
        Порядковый номер пути - number.
        Начальная остановка - initial_stop, конечная - final_stop.
        Список stops остановок-пересадок, в которых соединяются отрезки разных маршрутов.
        Список маршрутов routes, из отрезков которых состоит путь. (между любыми соседними пересадками)
        good_way - подтверждение, что на последнем маршруте пути удалось найти конечную остановку final_stop.
        Время проезда time (подсчитывается при good_way == True).

        Из некоторого пути можно создать новый, с помощью добавления новой пересадки new_change,
        и соответствующего пересадочного маршрута new_route.
        appointed_changes и appointed_routes - это списки stops и routes, которые заимствуются у пути-родителя.
        Они затем дополняются элементами new_change и new_route.
        """

        self.stops = appointed_changes.copy()
        self.routes = appointed_routes.copy()
        self.stops.append(new_change)
        self.routes.append(new_route)
        self.number = number
        self.good_way = False
        self.time = -1

    def add_final_stop(self, routes, final_stop):
        """
        Проверяет наличие конечной остановки final_stop в последнем маршруте пути
        (используется routes - список маршрутов Routes из Model.py).
        Если наличие подтверждается, конечная остановка добавляется в путь,
        статус good_way изменяется - путь считается 'хорошим'.
        """

        last_route_name = self.routes[len(self.routes)-1]
        last_route = get_route_by_name(last_route_name, routes)

        if last_route.stop_presence(final_stop) and self.stops[len(self.stops)-1] != final_stop:
            self.stops.append(final_stop)
            self.good_way = True

    def time_calculation(self, routes):
        """
        Для хорошего пути рассчитывает время проезда.
        """

        if self.good_way:
            time = 0
            for i in range(0, len(self.routes)):
                route = get_route_by_name(self.routes[i], routes)
                time = time + abs(route.bus_stops.get(self.stops[i+1]) - route.bus_stops.get(self.stops[i]))
            self.time = time

    def print(self):
        """
        Консольный вывод данных о пути.
        """

        print('number:', self.number)
        print('stops:', self.stops)
        print('routes:', self.routes)
        print('good_way:', self.good_way)
        print('time:', self.time)


class WayCreator:
    initial_stop: str
    final_stop: str
    max_number_of_changes: int

    def __init__(self, initial_stop, final_stop, max_number_of_changes):
        """
        Построитель путей прокладывает пути от остановки initial_stop до остановки final_stop
        с учётом ограничения на максимальное количество пересадок max_number_of_changes.
        Методы класса используют списки маршрутов и путей - routes и ways
        (Routes из Model.py, Ways из Controller.py).
        """

        self.initial_stop = initial_stop
        self.final_stop = final_stop
        self.max_number_of_changes = max_number_of_changes

    def open_ways(self, routes, ways):
        """
        Открывает пути. Каждый новый путь - начальная остановка self.initial_stop
        и некоторый маршрут, которому она принадлежит.
        У открытых путей количество пересадок нулевое.
        """

        for i in routes:
            if i.stop_presence(self.initial_stop):
                way = Way(self.initial_stop, i.name, len(ways), list(), list())
                ways.append(way)

    def create_ways_with_changes(self, routes, ways, number_of_changes):
        """
        Создаёт пути с пересадками.
        Пробегает по списку путей ways, и для путей с числом пересадок len(j.stops)-1 на единицу меньшим
        установленного числа number_of_changes, строит дочерние пути.
        Дочерний путь строится для каждой пересадки в последнем маршруте пути-родителя,
        с добавлением соответствующего пересадочного маршрута.
        Дочерние пути добавляются в список ways.
        """

        for j in ways:
            if len(j.stops) - 1 == number_of_changes - 1:
                last_route_name = j.routes[len(j.routes)-1]
                last_route = get_route_by_name(last_route_name, routes)

                for i in last_route.bus_changes:
                    if i != j.stops[len(j.stops)-1]:
                        way = Way(i, last_route.bus_changes.get(i), len(ways), j.stops, j.routes)
                        ways.append(way)

    def close_ways(self, routes, ways):
        """
        Закрытие путей.
        """

        for way in ways:
            way.add_final_stop(routes, self.final_stop)

    def leave_good_ways(self, ways):
        """
        Плохие пути удаляются из списка ways.
        """

        i = 0
        while 0 <= i < len(ways):
            if ways[i].good_way:
                ways[i].time_calculation(Routes)
                i += 1
            else:
                ways.remove(ways[i])

    def sort_ways_by_time(self, ways):
        """
        Сортировка списка ways по возрастанию значения атрибута time у его элементов.
        """

        for i in range(0, len(ways)-1):
            for j in range(i+1, len(ways)):
                if ways[i].time >= ways[j].time:
                    u = ways[i]
                    ways[i] = ways[j]
                    ways[j] = u


# creator = WayCreator(Initial_stop, Final_stop, 2)
# creator.open_ways(Routes, Ways)
# for i in range(1, creator.max_number_of_changes + 1):
#     creator.create_ways_with_changes(Routes, Ways, i)
# creator.close_ways(Routes, Ways)
# creator.leave_good_ways(Ways)
# creator.sort_ways_by_time(Ways)
#
#
#
# for i in Ways:
#     i.print()
