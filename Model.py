import sqlite3


"""
Программа Model.py: 
Содержит описание класса маршрутов Route.
Создаёт экземпляры класса Route, используя сведения из базы данных routes.db.
Данные считываются с помощью sqlite3.
Заполняет экземплярами список маршрутов Routes.
"""

class Route:
    name: str
    bus_stops: dict
    list_of_bus_stops: list
    bus_changes: dict

    def __init__(self, name, routes):
        """
        name: имя маршрута.
        bus_stops: ключ - название остановки, значение - время прибытия на остановку.
        list_of_bus_stops: cписок названий остановок маршрута.
        bus_changes: ключ - название остановки-пересадки, значение - название маршрута, на который можно пересесть.
        """

        self.name = name
        cursor.execute('SELECT * FROM ' + self.name)
        result = cursor.fetchall()
        self.bus_stops = {}
        self.list_of_bus_stops = []
        for i in result:
            self.bus_stops[i[0]] = i[1]
            self.list_of_bus_stops.append(i[0])
        self.bus_changes = {}
        routes.append(self)

    def set_bus_change(self, change, another_route):
        """
        Добавляет пересадку в словарь bus_changes маршрута.
        Пересадка - change, маршрут для пересадки - another_route.
        """

        self.bus_changes[change] = another_route

    def stop_presence(self, stop):
        """
        Проверка наличия остановки stop в маршруте.
        """

        if stop in self.bus_stops:
            return True
        else:
            return False

    def print(self):
        """
        Консольный вывод данных о маршруте.
        """

        print(self.name + ':')

        for i in self.bus_stops:
            print(i, self.bus_stops.get(i))

        for i in self.list_of_bus_stops:
            print(i)

        for i in self.bus_changes:
            print(i, self.bus_changes.get(i))


def get_route_by_name(name, routes):
    """
    Получение маршрута по имени name из списка маршрутов routes.
    """

    for i in routes:
        if name == i.name:
            return i


conn = sqlite3.connect('routes.db')

cursor = conn.cursor()

Routes = list()


Green_route = Route('Green_route', Routes)
Blue_route = Route('Blue_route', Routes)
Red_route = Route('Red_route', Routes)

"""
Цикл ниже организует заполнение словаря bus_changes для каждого маршрута.
"""

for i in range(0, len(Routes)-1):
    for j in range(i+1, len(Routes)):
        cursor.execute('SELECT ' + Routes[i].name + '.bus_stop FROM '
                       + Routes[i].name + ' INNER JOIN ' + Routes[j].name +
                       ' ON ' + Routes[i].name + '.bus_stop' + ' = ' + Routes[j].name + '.bus_stop')
        bus_changes = cursor.fetchall()
        for k in bus_changes:
            Routes[i].set_bus_change(k[0], Routes[j].name)
            Routes[j].set_bus_change(k[0], Routes[i].name)



conn.commit()
conn.close()

