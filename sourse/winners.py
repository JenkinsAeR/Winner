import sys, os
#импортируем класс с модальным окном из файла
from modal import Ui_Modal
#импортируем графический интерфейс из файла
from winners_ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
 
#Основной массив, в который мы будем собирать другие массивы с участниками 
list_of_lists = []



def generator(file_path=(os.getcwd() + '\\participants.txt'), \
                        list_of_lists=list_of_lists):
    '''Функция генерирующая массив, заполняющая данные из файла.
    Принимает в качестве аргументов: путь к файлу и массив.
    По умолчанию берется файл из текущей директории с именем "participants.txt". '''
    try:
        with open(file_path, 'r') as f:
            for line in f:
                #Из каждой строки в файле генерируем список
                #(Значения должны быть разделены ' , ')
                inner_list = [elt.strip() for elt in line.split(',')]
                #Добавляем сгенерированный массив в list_of_lists
                list_of_lists.append(inner_list)
    except Exception:
        pass

#N = длине list_of_lists

def average(a:list):
    '''Функция вычисления среднего балла по системе:
    Максимальная и минимальная оценка отбрасывается,
    а из остальных формируется средняя.
    В качестве аргументов принимает массив.'''
    for i in range(N):
        #Переменная для минимальной оценки
        min_l = 6
        #Переменная для максимальной оценки
        max_l = 0
        #Переменная для общей суммы 
        s = 0
        #проходим по всем элементам кроме фамилии
        #и организации каждого участника 
        for j in a[i][2:]:
            if int(j) < min_l:
                min_l = int(j)
            if int(j) > max_l:
                max_l = int(j)
            #на каждой итерации цикла суммируем значения
            s += int(j)
        #после выполнения циклов вычитаем мин и макс оценки
        #из общей суммы и делим на 6, т.к. оценок было 8
        #добавляем в массив каждого участника средний балл
        a[i].append((s - min_l - max_l) / 6)


def bubble_sort(array:list):
    '''Алгоритм сортировки пузырьком(простыми обменами)
    В качестве аргументов принимает массив. Сортировка
    производится по среднему баллу каждого участника.'''
    for i in range(N-1):
        for j in range(N-i-1):
            if float(array[j][10]) < float(array[j+1][10]):
                clipboard = array[j]
                array[j] = array[j+1]
                array[j+1] = clipboard
    

class Modality(QtWidgets.QMainWindow):
    '''Класс с модальным окном и его функционалом.
    Все свойства к данному классу находятся в файле:
    modal.py'''
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        #переменная для подсчёта строк таблицы
        self.count = 2
        #создаём объект приложения
        self.modal = Ui_Modal()
        self.modal.setupUi(self)
        #кнопка "ОК", запускает функцию get_data
        self.modal.pushButton.clicked.connect(self.get_data)
        #кнопка "Отмена", закрывает модальное окно
        self.modal.pushButton_2.clicked.connect(self.close)
        #подсказка для кнопки "Отмена"
        self.modal.pushButton_2.setToolTip('Отменить ручной ввод')
        #кнопка "+" (Добавление сроки в таблицу)
        #при нажатии вызывает функцию add_line
        self.modal.pushButton_3.clicked.connect(self.add_line)
        #подсказка к кнопе "+"
        self.modal.pushButton_3.setToolTip('Добавить строку в таблицу')
        #создаём названия для колонок таблицы
        self.modal.tableWidget.setHorizontalHeaderLabels(["Фамилия","Организация", 
                                                        "1","2","3","4","5","6","7","8"])



    def add_line(self):
        '''Метод добавления строк в таблицу.'''
        #установить количество строк таблицы равное self.count
        self.modal.tableWidget.setRowCount(self.count)
        self.modal.tableWidget.visualRow(self.count)
        self.count += 1



    def get_data(self):
        '''Метод сбора данных из таблицы модального
        окна в массив list_of_lists'''
        #количество строк
        rows = self.modal.tableWidget.rowCount()
        #количество столбцов
        cols = self.modal.tableWidget.columnCount()
        for row in range(rows):
            #массив для каждой строки таблицы
            tmp = []
            for col in range(cols):
                try:
                    #пытаемся взять данные из каждой ячейки построчно
                    #предварительно преобразовав в текст, и добавить
                    #во временный массив
                    tmp.append(self.modal.tableWidget.item(row,col).text())
                except:
                    #если произошла ошибка, вместо значения добавить "0"
                    tmp.append('0')
            #добавляем в общий массив с участниками - временный (tmp)
            list_of_lists.append(tmp)
        #перед закрытием модального окна выводим уведомление для пользователя
        QtWidgets.QMessageBox.question(self, 'Внимание!', 
                                            'Для подсчёта нажмите на кнопку "выбрать победителей" ',
                                            QtWidgets.QMessageBox.Ok)
        #закрываем модальное окно
        self.close()
        




class MyWin(QtWidgets.QMainWindow):
    '''Класс с главным окном приложения и его функционалом.
    Все свойства к данному классу находятся в файле:
    winners_ui.py'''
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #кнопка выбора файла
        self.ui.pushButton.clicked.connect(self.browse_file)
        self.ui.pushButton.setToolTip('Выбор файла для загрузки данных')
        #кнопка 'выбрать победителей'
        self.ui.pushButton_2.clicked.connect(self.winer_table)
        self.ui.pushButton_2.setToolTip('Показать результат')
        #кнопка для закрытия окна, ввиде крестика
        self.ui.pushButton_3.clicked.connect(self.exit)
        self.ui.pushButton_3.setToolTip('Закрыть приложение')
        #кнопка '+', создающая модальное окно
        self.ui.pushButton_4.clicked.connect(self.showChildWindow)
        self.ui.pushButton_4.setToolTip('Добавить участников вручную')

    def exit(self):
        '''Метод закрытия главного окна программы и уведомление'''
        message = 'Вы уверены, что хотите выйти?'
        #спрашиваем пользователя "уверен ли он, что хочет выйти из программы"
        reply = QtWidgets.QMessageBox.question(self, 'Уведомление', message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        #если ответ "да/yes" - закрыть.
        if reply == QtWidgets.QMessageBox.Yes:
            self.close()
        #иначе пропустить и скрыть уведомление
        else:
            pass

    def showChildWindow(self):
        '''Метод создания модального окна с таблицами для ручного ввода'''
        global modal_table
        modal_table = Modality()
        modal_table.show()


    def browse_file(self):
        # открыть диалог выбора файла и установить значение переменной
        # равной пути к выбранного файла
        try:
            file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл")[0]
            #передать в функцию generator путь к файлу
            generator(file_path)
        #если будет вызвано исключение - проигнорировать
        except Exception:
            pass



    def winer_table(self):
        '''Метод для выбора победителей из каждого общества'''
        #объявление глобальной переменной N
        global N
        #если основной массив пуст -
        #запускаем фенкцию генератор
        #по умолчанию из файла participants.txt
        if list_of_lists == []:
            generator()
        N = len(list_of_lists) #присваиваем N значение равное длинне list_of_lists
        average(list_of_lists) #вычисляем средний балл
        #сортируем списки по среднему баллу
        #от большего к меньшему
        bubble_sort(list_of_lists)
        self.ui.tableWidget.clear() #очищаем таблицу главного окна
        self.ui.tableWidget.setColumnCount(3) #Устанавливаем три колонки
        #устанавливаем ширину колонок таблицы
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        x = list_of_lists #делаем ссылку на основной массив для удобства

        old_list = [] #массив для уникальных участников из каждого общества
        row_count = 0 #переменная для кол-ва строк таблицы
        for i in range(N): 
            if (x[i][1].lower()) not in old_list: #если организация не в массиве old_list
                old_list.append(x[i][1].lower()) #добавляем в массив old_list эту организацию
                self.ui.tableWidget.setRowCount(row_count+1) #создаём новую строку таблицы
                #выводим в таблицу фамилию
                self.ui.tableWidget.setItem(row_count,0,QtWidgets.QTableWidgetItem(x[i][0]))
                #выводим в таблицу итоговую оценку (только 3 знака, например 4.1) 
                self.ui.tableWidget.setItem(row_count,1,QtWidgets.QTableWidgetItem(str(x[i][10])[:3]))
                #выводим в таблицу организацию участника 
                self.ui.tableWidget.setItem(row_count,2,QtWidgets.QTableWidgetItem(x[i][1]))
                #прибавляем 1 к переменной строк
                row_count+=1
            #иначе пропускаем (если уже есть организация в old_list)
            else:pass
        #перед выходом стираем наш основной массив      
        list_of_lists[:] = []
         # Устанавливаем заголовки таблицы
        self.ui.tableWidget.setHorizontalHeaderLabels(["Фамилия", "Оценка", "Организация"])
        
        

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())