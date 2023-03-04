
"""
Программа игры морской бой.
Автор Кирбасов Петр.
Курс SKILLFACTORY FPW-109 Fullstack разработчик на Python
Задание 8/15  C2.8. Итоговое задание.
Дата 02.03.2023

Техническое задание:

Используя знания, полученные в модуле, напишите следующее приложение:
Суть приложения: игра «Морской бой».
Интерфейс приложения должен представлять собой консольное окно с двумя полями 6х6 вида:
  | 1 | 2 | 3 | 4 | 5 | 6 |
1 | О | О | О | О | О | О |
2 | О | О | О | О | О | О |
3 | О | О | О | О | О | О |
4 | О | О | О | О | О | О |
5 | О | О | О | О | О | О |
6 | О | О | О | О | О | О |
Игрок играет с компьютером. Компьютер делает ходы наугад, но не ходит по тем клеткам, в которые он уже ходил.
Для представления корабля опишите класс Ship с конструктором, принимающим в себя набор точек (координат) на игровой доске.
Опишите класс доски. Доска должна принимать в конструкторе набор кораблей.
Корабли должны находится на расстоянии минимум одной клетки друг от друга.
Корабли на доске должны отображаться следующим образом:
  | 1 | 2 | 3 | 4 | 5 | 6 |
1 | ■ | ■ | ■ | О | О | О |
2 | О | О | О | ■ | ■ | О |
3 | О | О | О | О | О | О |
4 | ■ | О | ■ | О | ■ | О |
5 | О | О | О | О | ■ | О |
6 | ■ | О | ■ | О | О | О |
На каждой доске (у ИИ и у игрока) должно находится следующее количество кораблей:
1 корабль на 3 клетки;
2 корабля на 2 клетки;
4 корабля на одну клетку.
Запретите игроку стрелять в одну и ту же клетку несколько раз. При ошибках хода игрока должно возникать исключение.
  | 1 | 2 | 3 | 4 | 5 | 6 |
1 | X | X | X | О | О | О |
2 | О | О | О | X | X | О |
3 | О | T | О | О | О | О |
4 | ■ | О | ■ | О | ■ | О |
5 | О | О | О | О | ■ | О |
6 | ■ | О | ■ | О | О | О |
Если возникают непредвиденные ситуации, выбрасывать и обрабатывать исключения.
Буквой X помечаются подбитые корабли. Буквой T — промахи.

Побеждает тот, то быстрее всех разгромит корабли противника.
------------------------------------------------------------------------------
конец технического задания.

ВАЖНО: Опишите класс доски. Доска должна принимать в конструкторе набор кораблей.
       Таким образом набор кораблей должен быть сформирован заранее и другим способом чем метод доски.

        Компьютер делает ходы наугад,
        Таким образом, обнаружив корабль, компьютер не должен обстреливать соседние клетки с целью
        потопить корабль.

        Каждый из кораблей занимает одну или несколько клеток, и имеет поле вокруг себя, куда
        нельзя поставить другие корабли. Для разных кораблей разные значения: 1палубный - 9клеток,
        2п - 11 клеток, 3а - 13 клеток. Таким образом 7 кораблей имеют суммарное поле 71 клетку.
        В процессе тестирования выяснилось, что расставляя корабли случайным образом может произойти
        ситуация, при которой бот не может закончить расстановку, потому как не остается свободного места.
        В этом случае производится 16 попыток расставить корабли, в случае неудачи игра заканчивается.


"""
import sys
import numpy
import random


class BoardException(Exception):
    pass

class OutofRangeException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class DoubleShootException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"




class Field:
# класс игровое поле, содержит матрицу точек, список кораблей с координтами точек,
# матрицу строк для вывода поля на печать

    def __init__(self, size, visual, flot, shipmark):
        self.live = sum(shipmark)   # общее количество живых клеток в кораблях
        self.size = size            # размер поля, от 1 до size, в нашем случае 6
        self.visual = visual        # список строк, отображающих поле для перчати
        self.array = self.setarray(size) # одномерная матрица-список точек поля
                                    # 0-пусто,1-корабль,2-мимо,3-ранен или убит
        self.flot = self.setflot(flot) # список объектов-кораблей

    def hod(self,player):   # полифонический метод, запрашивает или генерирует координаты выстрела,
                            # анализирует результат выстрела, печатает поле,
                            # в случае попадания, повторяет все заново.
        while True:
#            print(*self.visual,sep="\n")    # печать поля
            if player=="user":              # запрос или генерация координат выстрела
                print(*self.visual, sep="\n")  # печать поля
                print("приготовьтесь к стрельбе")
                x=(inputint("Ваш выстрел (номер строки)?"))
                y=(inputint("Ваш выстрел (номер столбца)?"))
            else:
                x=random.randint(1,self.size)
                y=random.randint(1,self.size)
#            print("выстрел",player,x,y)     # печать сообщения
            z=self.array[(x-1)+(y-1)*self.size]     # запрос статуса клетки.
            if z==0:                                # клетка чистая.
                self.array[(x - 1) + (y - 1) * self.size] = 2
                self.visual[x] = self.visual[x][0:4 * y - 1] + "T" + self.visual[x][4 * y:]
                print("выстрел",player,x,y,"мимо")
            elif z==2:                              # корабля нет, но сюда уже стреляли
                if player=="bot":                    # боту разрешено повторить выстрел
#                    print("выстрел ")
                    continue
                print("выстрел",player,x,y,"поле уже простреляно, мимо")
                try:
                    raise DoubleShootException      # поднимаем исключние по ТЗ
                except DoubleShootException:
                    print("** обработка исключения")
            elif z==3:
                if player=="bot":                    # боту разрешено повторить выстрел
                    continue
                print("выстрел",player,x,y, "Поле простреляно, было попадание")
            elif z==1:                              #  попадание в корабль
                self.array[(x - 1) + (y - 1) * size] = 3
                self.visual[x] = self.visual[x][0:4 * y - 1] + "X" + self.visual[x][4 * y:]
                kill = False                        # флаг - убит
                for s in self.flot:
                    for dot in s.dots:
                        if [x,y] == dot:
                            s.live -= 1
                            self.live -=1
                            if s.live == 0:         # если корабль убит
                                print("выстрел",player,x,y,"Корабль",s.len,"убит")
                                kill = True
                                break
                            else:
                                print("выстрел",player,x,y,"Корабль ранен")
                    if kill:                        # если корабль убит, отмечаем область вокруг
                                                    # корабля как прострелянную.
                        for dot in s.dots:
                            x1, y1= dot
                            for xn in [x1-1, x1, x1+1]:
                                for yn in [y1-1, y1, y1+1]:
                                    if (0<xn<=self.size) and (0<yn<=self.size):
                                        z1=(xn-1)+(yn-1)*self.size
                                        if self.array[z1] == 0:  # если клетка пустая
                                            self.array[z1] = 2
                                            self.visual[xn] = self.visual[xn][0:4 * yn - 1] + "T" + self.visual[xn][4 * yn:]
                        break
                pass
                if self.live == 0:                  # если все корабли потоплены
                    print(*self.visual, sep="\n")
                    print("Конец игры ====",player,"выиграл !")
                    sys.exit()
                continue # уходим на следующий круг, тк было попадание в корабль
            break
        print(*self.visual,sep="\n")                # печать поля после выстрела
        return

    def setarray(self, fieldsize):
        # генерируем массив точек, в которых хранится информация о попадании ракет и расположении кораблей
        f = [0] * fieldsize ** 2
        return f

    def setflot(self, flot):            # метод проверяет корабли на соприкосновение и вносит в таблицы,
        for ship in flot:               # код возможно устарел и требует модификации.
            free = True
            for dot in ship.dots:
                x, y = dot
                #проверяем точки корабля, есть ли другие корабли в касании
                free = free and checkaround(x,y,size,self.array)
            if free:
                for dot in ship.dots:
                    x, y = dot
                    self.array[(x-1)+(y-1)*self.size]=1
        self.flag = free
        return flot


class Ship:                                 # класс корабль

    def __init__(self, l, live, dots):
        self.len = l                        # длина ( не используется )
        self.live = live                    # количество жизней
        self.dots = dots                    # список координат точек

def inputint(prompt):                       # функция ввода целого числа
    global size                             # size-размер поля, global не обязательно, тк size не меняется.
    while True:
        x = input(prompt)
        try:
            y = int(x)
        except ValueError:
            print('Введите число')
            continue
        if 0<y<=size:
            return y
        else:
            print('Введите число от 1 до',size)
            try:
                raise OutofRangeException               # поднимаем исключение в соответствии с ТЗ
            except OutofRangeException:
                print("** Исключение отработано программой")    # сами его отрабатываем
        pass
 

def checkaround(x,y,size,array):
    # проверяем точку x y на попадание в поле
    # потом проверяем точки вокруг, матрица должна
    # возвращать 0.
    free = (0 < x <= size) and (0 < y <= size)
    for xn in [x - 1, x, x + 1]:
        for yn in [y - 1, y, y + 1]:
            if 0 < xn <= size and 0 < yn <= size:
                z = array[(xn - 1) + (yn - 1) * size]
                if z != 0:
                    free = False
    return free



def stf(fieldsize):
    # генерируем поле stf(), это список из строк, которые выводятся на
    # печать при печати поля.
    f = []
    y = " !"
    for i in range(fieldsize):      # здесь и далее можно применить строчный цикл, но он менее понятен
        y += str(i + 1) + "  !"     # для новичка в питоне.
    f.append(y)
    for i in range(fieldsize):
        x = str(1 + i) + "!"
        for j in range(fieldsize):
            x += " o !"
        f.append(x)
    return f


# Запрашиваем координаты флота пользователя. Поскольку по ТЗ :
# Опишите класс доски. Доска должна принимать в конструкторе набор кораблей.
# Мы сначала принимаем координаты кораблей, потом инициируем доску,
# А во время инициации доски, одновременно передаем набор кораблей
# И проверяем корабли на соприкосновения друг с другом

def setuserflot(size, len_of_ships):
    f = stf(size)
    array = list([0] * size ** 2)
    flot = []
    for l in len_of_ships:
        print(*f, sep="\n")
        print("\n")
        if l == 1:
            while True:
                print("Корабль длиной 1 клетка. Корабли не должны соприкасаться")
                x = (inputint("Введите номер строки корабля >"))
                y = (inputint("Введите номер столбца корабля>"))
    #            x, y = 1, 6
                c, dots = checkship(x, y, x, y, l, size, array)
                if not c:
                    print("Ошибка, повторите !")  # уходим на повторный запрос второй координаты
                    continue  # необязательный оператор, стоит для наглядности
                dots, array = setship(dots, size, array)
                f[x] = f[x][0:4 * y - 1] + "■" + f[x][4 * y:]
                s = Ship(1, 1, [[x, y]])
                break
        else:
            f1 = []
            while True:
                # Цикл запроса координат, пока не введено
                # Корректное значение
                print("Корабль длинной", l, ". Корабли не должны соприкасаться")
                x = (inputint("Нос корабля.  Номер строки  >"))
                y = (inputint("Нос корабля.  Номер столбца >"))
                x1 = (inputint("Корма корабля. Номер строки >"))
                y1 = (inputint("Корма корабля. Номер столбца>"))
#                x1, y1 = 1, 3
                # Если координаты корректны то расставляем значки на поле и
                # вычисляем список координат.
#                print(x,y,x1,y1)
                if (x == x1) and (abs(y - y1) == l - 1):            # если корабль расположен горизонтально, длина l
                    c, dots = checkship(x, y, x1, y1, l, size, array)
                    if not c:
                        print("Ошибка, повторите !")  # уходим на повторный запрос второй координаты
                        continue  # необязательный оператор, стоит для наглядности
                    dots, array = setship(dots,size,array)
                    for yn in range(y, y1 + numpy.sign(y1 - y), numpy.sign(y1 - y)):    # направление цикла может быть разным
                        f[x] = f[x][0:4 * yn - 1] + "■" + f[x][4 * yn:]
                        f1.append([x, yn])                           # заносим координаты точек в список
                    break
                elif (abs(x - x1) == l - 1) and (y == y1):           # если корабль расположен вертикально, длина l
                    c, dots = checkship(x, y, x1, y1, l, size, array)
                    if not c:
                        print("Ошибка, повторите !")  # уходим на повторный запрос второй координаты
                        continue  # необязательный оператор, стоит для наглядности
                    dots, array = setship(dots,size,array)
                    for xn in range(x, x1 + numpy.sign(x1 - x), numpy.sign(x1 - x)):
                        f[xn] = f[xn][0:4 * y - 1] + "■" + f[xn][4 * y:]
                        f1.append([xn, y])                           # заносим координаты точек в список
                    break
                else:
                    print("Ошибка, повторите !")                     # уходим на повторный запрос второй координаты
                    continue                                         # необязательный оператор, стоит для наглядности
            s = Ship(l, l, f1.copy())
            # s - корабль, длина, жизни, список координат клеток.
        flot.append(s)
        # flot - список из кораблей
    print(*f, sep="\n")
    print()
    return flot, f


def checkship(x,y,x1,y1,l, size,array):
    # получаем координаты двух концов корабля, проверяем на длину l и
    # проверяем по полям массива array, составляем список координат
    free = True
    dotlist = []
    if (x==x1) and (y==y1) and (l==1):              # если корабль длиной 1, проверяем одну точку и окрестности
        dotlist = [[x, y]]
        free = checkaround(x,y,size, array)
    elif (x == x1) and (abs(y - y1) == l - 1):      # если корабль расположен горизонтально
        for yn in range(y, y1 + numpy.sign(y1 - y), numpy.sign(y1 - y)):
            dotlist.append([x, yn])
            free = free and checkaround(x, yn, size, array)
    elif (abs(x - x1) == l - 1) and (y == y1):      # если корабль расположен вертикально
        for xn in range(x, x1 + numpy.sign(x1 - x), numpy.sign(x1 - x)):
            dotlist.append([xn, y])
            free = free and checkaround(xn, y, size, array)
    else:
        free = False                                # если точки расположены иным способом и корабль не вписывается
                                                    # в координаты
    return free, dotlist


def setship(dots,size,array):                       # ставим 1 в массив, в координаты точек корабля.
    for d in dots:
        x, y = d
        array[(x-1)+(y-1)*size] = 1
    return dots, array

#------------------------------------------------------------------------
# Небольшое пояснение, при инициализации поля требуется сразу в конструктор
# передать весь список кораблей, поэтому проверку координат происходит
# на временном поле array[]
#------------------------------------------------------------------------
def setmyships(size, shipmask):     # генерируем и проверяем на совместимость координаты кораблей бота.
    for j in range(16):     # цикл, на случай если все корабли не поместятся на поле.
        array = None
        array = list([0] * size ** 2)
#        print(array)
        flot = []
        new_attempt = False

        for i in shipmask:          # создаем несколько кораблей, в нашем случае 7шт.
                                    # i - берем длину корабля из списка длин.
            start = random.randint(0, size**2 - 1)  # нос корабля
#            print("start",start)
            a = start
            while True:                 # за начало поиска берем точку start.
                                        # цикл, если не удастся создать корабль с
                                        # с первого раза.
                x = a%size+1
                y = a//size+1
                if checkaround(x,y,size,array):                      # проверяем точку
                    b, bdots = checkship(x,y,x,y+i-1,i,size,array)   # можно ли
                    c, cdots = checkship(x,y,x+i-1,y,i,size,array)
                    d = bool(random.randint(0,1))
                    if (b and d) or (b and not(c)):                 # логика - какой корабль установить, в зависимости от 3х булей
                        dots, array = setship(bdots,size,array)
                        break
                    elif (c and (not d)) or (c and not(b)):
                        dots, array = setship(cdots,size,array)
                        break
                    else:
                        pass
#                print(a,end="")
                a += 1      # если корабль не встал, то проверяем следующую клетку
                if a == size**2:
                    a = 0   # если дошли до последней, то продолжаем с нуля
                if a == start:
#                    print("Попытка", j)  # если перебрали все клетки без успеха.
                    new_attempt = True
#                    sys.exit()
                    break
            if new_attempt:
                break
            s = Ship(i,i,dots)      # инициируем корабль
            flot.append(s)          # добавляем в список
            pass # выход из цикла перебора a, корабль установлен в массив.
        if new_attempt:
#            print(array)
            continue
#        print(">> выход", array)
        pass # цикл из 16 попыток
        break
    else:
        print("Нет места для размещения кораблей. Попытки исчерпаны", j)  # если перебрали все клетки без успеха.
        sys.exit()
    return flot



#
# Основной код
#

# Запрашиваем у игрока координаты его кораблей

size = 6  # размер игроввого поля.
shipmask = [3,2,2,1,1,1,1]  # какие корабли в игре с каждой стороны.
#shipmask = [1,1,1,1]  # какие корабли в игре с каждой стороны.


# инициация поля игры юзера
while True:
    # запрос координат кораблей юзера
    flot, visualfield = setuserflot(size, shipmask)
    # конструктор поля юзера
    userfield = Field(size, visualfield, flot, shipmask)
    if userfield.flag:
        break
    else:
        print("Установка кораблей не удалась, повторите попытку.")
        _=input("Press any key")

# инициализируем флот бота

flot = setmyships(size, shipmask)
visualfield=stf(size)
botfield = Field(size, visualfield, flot, shipmask)

# основной цикл баталии

print("баталия")

while True:
    botfield.hod("user")
    _ = input("********* ВЫ ПОД ОБСТРЕЛОМ, НЕМЕДЛЕННО ПРОСЛЕДУЙТЕ В УКРЫТИЕ , нажмите ввод")
    userfield.hod("bot")
    _ = input("КОНЕЦ ВОЗДУШНОЙ ТРЕВОГИ, ЗАЙМИТЕ МЕСТО У БОЕВОГО РАДАРА. нажмите ввод")