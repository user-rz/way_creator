import sys
from PySide6 import QtWidgets, QtGui

from Controller import *


stops_2d_points = {'a': (204, 337),  'b': (283, 190),  'c': (418, 119),
                   'd': (513, 253),  'e': (502, 364),  'f': (374, 338),
                   'g': (331, 412),  'h': (395, 226)}

"""
Программа View.py:
MyWindow - главное окно.
Дополнительное окно view отображает сцену scene.
View и scene - атрибуты класса MyWindow. 
Координаты остановок на дополнительном окне хранятся в словаре stops_2d_points.
"""

class MyWindow(QtWidgets.QWidget):

    def __init__(self, stops_2d_points, *args, ** kwargs):
        super().__init__(*args, ** kwargs)

        self.stops_2d_points = stops_2d_points

        self.vertical_layout = QtWidgets.QVBoxLayout()

        self.setWindowTitle('Построитель путей')
        self.resize(500, 500)
        self.setGeometry(100, 200, 400, 400)

        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.addWidget(QtWidgets.QLabel('Что Вас интересует?'))

        button_set = ['Карта маршрутов', 'Информация о маршруте', 'Информация об остановке', 'Проложить путь']

        Buttons = list()
        for i in range(0, len(button_set)):
            Buttons.append(QtWidgets.QPushButton(button_set[i]))
            self.vertical_layout.addWidget(Buttons[i])

        btn1 = Buttons[0]
        btn2 = Buttons[1]
        btn3 = Buttons[2]
        btn4 = Buttons[3]

        self.vertical_layout.addWidget(btn1)
        self.vertical_layout.addWidget(btn2)
        self.vertical_layout.addWidget(btn3)
        self.vertical_layout.addWidget(btn4)

        self.setLayout(self.vertical_layout)

        self.pixmap = QtGui.QPixmap('./venv/map.jpg')


        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addPixmap(self.pixmap)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setGeometry(600, 150, self.pixmap.width() + 10, self.pixmap.height() + 10)


        self.view.show()

        btn1.clicked.connect(self.button1)
        btn2.clicked.connect(self.button2)
        btn3.clicked.connect(self.button3)
        btn4.clicked.connect(self.button4)

    def button1(self):
        """
        Освобождает дополнительное окно.
        Размещает на сцене все маршруты, а также метку с их названиями.
        Рисует сцену на дополнительном окне.
        """

        self.set_empty_scene()

        s = ''

        for route in Routes:
            s = s + route.name + '\n'

        label = QtWidgets.QLabel(s)

        self.scene.addWidget(label)

        for route in Routes:
            self.draw_segment_of_route(route, 0, len(route.list_of_bus_stops) - 1)

        self.view.show()

    def button2(self):
        """
        Располагает на главном окне поле для ввода названия маршрута.
        """

        self.label = QtWidgets.QLabel('Введите название маршрута')
        self.edit = QtWidgets.QLineEdit('')
        self.vertical_layout.addWidget(self.label)
        self.vertical_layout.addWidget(self.edit)
        self.setLayout(self.vertical_layout)
        self.submit_btn2 = QtWidgets.QPushButton('Отправить')
        self.vertical_layout.addWidget(self.submit_btn2)
        self.submit_btn2.clicked.connect(self.submit_for_button2)

    def button3(self):
        """
        Располагает на главном окне поле для ввода названия остановки.
        """

        self.label = QtWidgets.QLabel('Введите название остановки:')
        self.edit0 = QtWidgets.QLineEdit('')
        self.vertical_layout.addWidget(self.label)
        self.vertical_layout.addWidget(self.edit0)
        self.setLayout(self.vertical_layout)
        self.submit_btn3 = QtWidgets.QPushButton('Отправить')
        self.vertical_layout.addWidget(self.submit_btn3)
        self.submit_btn3.clicked.connect(self.submit_for_button3)

    def button4(self):
        """
        Располагает на главном окне поле для ввода названий начальной и конечной остановок,
        допустимого количества пересадок.
        """

        self.vertical_layout.addWidget(QtWidgets.QLabel('Начальная остановка:'))
        self.edit1 = QtWidgets.QLineEdit('')
        self.vertical_layout.addWidget(self.edit1)

        self.vertical_layout.addWidget(QtWidgets.QLabel('Конечная остановка:'))
        self.edit2 = QtWidgets.QLineEdit('')
        self.vertical_layout.addWidget(self.edit2)

        self.vertical_layout.addWidget(QtWidgets.QLabel('Допустимое количество пересадок:'))
        self.edit3 = QtWidgets.QLineEdit('')
        self.vertical_layout.addWidget(self.edit3)

        self.setLayout(self.vertical_layout)

        self.submit_btn4 = QtWidgets.QPushButton('Отправить')
        self.vertical_layout.addWidget(self.submit_btn4)
        self.submit_btn4.clicked.connect(self.submit_for_button4)

    def set_empty_scene(self):
        """
        Обновляет сцену, оставляет на дополнительном окне только картинку map с остановками.
        """

        self.scene.addPixmap(self.pixmap)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setGeometry(600, 150, self.pixmap.width() + 15, self.pixmap.height() + 15)


    def draw_segment_of_route(self, route, num_of_first_stop, num_of_last_stop):
        """
        Добавляет на сцену отрезок некоторого маршрута route,
        начиная с остановки номер num_of_first_stop,
        и заканчивая остановкой номер num_of_last_stop.
        """

        pen = QtGui.QPen()
        pen.setWidth(5)

        if route.name == 'Green_route':
            pen.setColor(QtGui.QColor(0, 255, 0))
        if route.name == 'Blue_route':
            pen.setColor(QtGui.QColor(0, 0, 255))
        if route.name == 'Red_route':
            pen.setColor(QtGui.QColor(255, 0, 0))

        for i in range(num_of_first_stop, num_of_last_stop):
            self.line = QtWidgets.QGraphicsLineItem()
            self.line.setPen(pen)
            self.line.setLine(self.stops_2d_points.get(route.list_of_bus_stops[i])[0],
                              self.stops_2d_points.get(route.list_of_bus_stops[i])[1],
                              self.stops_2d_points.get(route.list_of_bus_stops[i+1])[0],
                              self.stops_2d_points.get(route.list_of_bus_stops[i+1])[1])

            self.scene.addItem(self.line)

    def draw_way(self, way):
        """
        Добавляет на сцену путь way. Путь - непрерывная ломаная из отрезков маршрутов.
        """

        for i in range(0, len(way.routes)):
            route = get_route_by_name(way.routes[i], Routes)
            first_edge = route.list_of_bus_stops.index(way.stops[i])
            second_edge = route.list_of_bus_stops.index(way.stops[i+1])

            maximum = max(first_edge, second_edge)
            minimum = min(first_edge, second_edge)

            self.draw_segment_of_route(route, minimum, maximum)

    def submit_for_button2(self):
        """
        Освобождает дополнительное окно.
        Принимает с поля запроса название маршрута,
        добавляет все его звенья на сцену, от первой до последней остановки.
        Рисует сцену на дополнительном окне.
        """

        self.set_empty_scene()

        submitted_route_name = self.edit.text()

        route = get_route_by_name(submitted_route_name, Routes)

        self.draw_segment_of_route(route, 0, len(route.list_of_bus_stops)-1)

        self.view.show()

    def submit_for_button3(self):
        """
        Освобождает дополнительное окно.
        Принимает с поля запроса название остановки,
        добавляет на сцену маршруты, которые включают эту остановку.
        Рисует сцену на дополнительном окне.
        """

        self.set_empty_scene()

        submitted_stop_name = self.edit0.text()

        for route in Routes:
            if route.stop_presence(submitted_stop_name):
                self.draw_segment_of_route(route, 0, len(route.list_of_bus_stops) - 1)

        self.view.show()

    def submit_for_button4(self):
        """
        Освобождает дополнительное окно.
        Освобождает список путей Ways.
        Принимает с поля запроса названия начальной и конечной остановок,
        допустимого количества пересадок.
        Экземпляр creator класса WayCreator строит пути, отбирает хорошие, сортирует их по возрастанию времени.
        На доп. окне добавляются кнопки Вперёд и Назад, рисуется первый путь.
        """

        self.set_empty_scene()
        Ways.clear()

        submitted_first_stop_name = self.edit1.text()
        submitted_last_stop_name = self.edit2.text()
        submitted_num_of_changes = int(self.edit3.text())

        creator = WayCreator(submitted_first_stop_name, submitted_last_stop_name, submitted_num_of_changes)
        creator.open_ways(Routes, Ways)
        for i in range(1, creator.max_number_of_changes + 1):
            creator.create_ways_with_changes(Routes, Ways, i)
        creator.close_ways(Routes, Ways)
        creator.leave_good_ways(Ways)
        creator.sort_ways_by_time(Ways)

        self.num_of_way_for_drawing = 0
        way = Ways[self.num_of_way_for_drawing]

        self.set_forward_and_back_buttons(way.time)
        self.draw_way(way)
        self.view.show()

        self.forward_btn.clicked.connect(self.forward_button)
        self.back_btn.clicked.connect(self.back_button)

    def forward_button(self):
        """
        Освобождает доп. окно.
        Добавляет кнопки Вперёд и Назад.
        Рисует на нём следующий по длительности путь.
        """

        self.set_empty_scene()

        if self.num_of_way_for_drawing < len(Ways)-1:
            self.num_of_way_for_drawing += 1
            way = Ways[self.num_of_way_for_drawing]

            self.set_forward_and_back_buttons(way.time)
            self.draw_way(way)
            self.view.show()
            self.forward_btn.clicked.connect(self.forward_button)
            self.back_btn.clicked.connect(self.back_button)

    def back_button(self):
        """
        Освобождает доп. окно.
        Добавляет кнопки Вперёд и Назад.
        Рисует на нём предшествующий по длительности путь.
        """

        self.set_empty_scene()

        if self.num_of_way_for_drawing > 0:
            self.num_of_way_for_drawing -= 1
            way = Ways[self.num_of_way_for_drawing]

            self.set_forward_and_back_buttons(way.time)
            self.draw_way(way)
            self.view.show()
            self.forward_btn.clicked.connect(self.forward_button)
            self.back_btn.clicked.connect(self.back_button)

    def set_forward_and_back_buttons(self, time):
        """
        Добавляет пометку о времени time, которое занимает путь.
        Размещает на доп. окне кнопки Вперёд и Назад.
        """

        label = QtWidgets.QLabel('Продолжительность поездки: ' + str(time) + ' ед.')
        self.scene.addWidget(label)

        layout = QtWidgets.QVBoxLayout()
        v_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('')
        label.setGeometry(600, 150, self.pixmap.width() + 15, self.pixmap.height() + 15)
        v_layout.addWidget(label)

        h_layout = QtWidgets.QHBoxLayout()
        self.back_btn = QtWidgets.QPushButton('Назад')
        self.forward_btn = QtWidgets.QPushButton('Вперёд')
        h_layout.addWidget(self.back_btn)
        h_layout.addWidget(self.forward_btn)

        layout.addLayout(v_layout)
        layout.addLayout(h_layout)

        self.view.setLayout(layout)


app = QtWidgets.QApplication(sys.argv)


window1 = MyWindow(stops_2d_points)

window1.show()


sys.exit(app.exec())
