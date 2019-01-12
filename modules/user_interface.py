#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Module responsible for the UI part of the program.'''

import os

from PyQt4 import QtGui

from plagiarism_detection import detect_plagiarism

class InstructionsWindow(QtGui.QWidget):
    '''Window that displays info and instructions of the software.'''

    def __init__(self):
        super(InstructionsWindow, self).__init__()

        self.set_instructions()
        self.set_window_characteristics()

    def set_instructions(self):
        '''Setting the instructions in a text field.'''

        self.le1 = QtGui.QTextEdit(self)
        self.le1.resize(400, 400)
        string = ([u'Инструкции\n\n',
                   u'Изработил: Стевица Божиноски 111025\n',
                   u'Факултет за информатички науки и компјутерско инженерство\n',
                   u'Универзитет „Св. Кирил и Методиј - Скопје“\n\n',
                   u'Влез:\n',
                   u'Два фајла во .txt формат за споредба\n',
                   u'Податоците можат да се внесуваат преку избор на ',
                   u'соодветните патеки на фајовите. За неточна патека се ',
                   u'испишува соодветна порака.\n\n',
                   u'Категории:\n',
                   u'\t-метаподатоци\n',
                   u'\t-референци\n',
                   u'\t-парафразиран текст\n',
                   u'\t-параграфи\n',
                   u'\t-стил на пишување\n',
                   u'Можна е селекција на една или повеќе од горенаведените категории.\n\n',
                   u'Излез:\n',
                   u'Како излез се испишува сличност за секоја од ',
                   u'селектираните категории како и сумарна сличност.\n'])

        self.le1.setText(''.join(string))
        self.le1.setReadOnly(1)

    def set_window_characteristics(self):
        '''Configuring the window characteristics.'''

        self.setWindowTitle(u'Инструкции')
        self.setGeometry(100, 100, 400, 400)
        self.show()

class ValidationWindow(QtGui.QWidget):
    '''Window that pops up when the paths do not exist or are incorrect.'''

    def __init__(self, message):
        super(ValidationWindow, self).__init__()

        self.set_text(message)
        self.set_window_characteristics()

    def set_text(self, message):
        '''Setting the error message.'''

        self.le1 = QtGui.QLineEdit(self)
        self.le1.resize(400, 80)
        self.le1.setText(message)
        self.le1.setReadOnly(1)

    def set_window_characteristics(self):
        '''Configuring the window characteristics.'''

        self.setWindowTitle(u'Погрешна патека')
        self.setGeometry(100, 100, 400, 80)
        self.show()

class DetailsWindow(QtGui.QWidget):
    '''This class contains all of the components related
    to the similarity details window.'''

    def __init__(self, string):
        super(DetailsWindow, self).__init__()

        self.update_details_window(string)
        self.set_window_characteristics()

    def update_details_window(self, string):
        '''Providing more similarity details.'''

        self.le1 = QtGui.QTextEdit(self)
        self.le1.resize(500, 400)
        self.le1.setText(string)
        self.le1.setReadOnly(1)

    def set_window_characteristics(self):
        '''Configuring the window characteristics.'''

        self.setWindowTitle(u'Детали')
        self.setGeometry(200, 200, 500, 400)
        self.show()

class MainWindow(QtGui.QWidget):
    '''This class contains all of the components and events related to the first window.'''

    def __init__(self):
        super(MainWindow, self).__init__()

        self.components = {}
        self.init_components1()
        self.init_components2()

        self.dialog = None
        self.kombinacii = None
        self.informacii = None
        self.new_app = None

        self.set_window_characteristics()

    def init_components1(self):
        '''Function that initializes some of the UI components
        (combobox, button, label).'''

        self.components['combo1'] = QtGui.QComboBox(self)
        self.components['combo1'].addItems([u'изберете категорија'])
        self.components['combo1'].move(660, 500)
        self.components['combo1'].currentIndexChanged.connect(self.click5)
        self.components['combo1'].hide()

        self.components['btn1'] = QtGui.QPushButton(self)
        self.components['btn1'].setText(u'Одбери документ')
        self.components['btn1'].move(20, 60)
        self.components['btn1'].resize(150, 20)
        self.components['btn1'].clicked.connect(self.click1)

        self.components['btn2'] = QtGui.QPushButton(self)
        self.components['btn2'].setText(u'Одбери документ')
        self.components['btn2'].move(20, 90)
        self.components['btn2'].resize(150, 20)
        self.components['btn2'].clicked.connect(self.click2)

        self.components['btn3'] = QtGui.QPushButton(self)
        self.components['btn3'].setText(u'Прикажи сличности')
        self.components['btn3'].move(20, 120)
        self.components['btn3'].resize(160, 20)
        self.components['btn3'].clicked.connect(self.click3)

        self.components['btn4'] = QtGui.QPushButton(self)
        self.components['btn4'].setText(u'Инструкции')
        self.components['btn4'].move(800, 30)
        self.components['btn4'].resize(120, 20)
        self.components['btn4'].clicked.connect(self.click4)

        self.components['label1'] = QtGui.QLabel(self)
        self.components['label1'].setText(u'Патека 1:')
        self.components['label1'].move(180, 65)

        self.components['label2'] = QtGui.QLabel(self)
        self.components['label2'].setText(u'Патека 2:')
        self.components['label2'].move(180, 95)

        self.components['label3'] = QtGui.QLabel(self)
        self.components['label3'].setText(u'Текст 1')
        self.components['label3'].move(150, 180)

        self.components['label4'] = QtGui.QLabel(self)
        self.components['label4'].setText(u'Текст 2')
        self.components['label4'].move(450, 180)

        self.components['label5'] = QtGui.QLabel(self)
        self.components['label5'].setText(u'Сличност меѓу документи')
        self.components['label5'].move(740, 180)

        self.components['label6'] = QtGui.QLabel(self)
        self.components['label6'].setText(u'Детали по категорија')
        self.components['label6'].move(660, 470)
        self.components['label6'].hide()

        self.components['label7'] = QtGui.QLabel(self)
        self.components['label7'].setText(u'Категории')
        self.components['label7'].move(520, 40)

    def init_components2(self):
        '''Function that initializes some of the UI components
        (line edit, text edit, check boxes).'''

        self.components['le1'] = QtGui.QLineEdit(self)
        self.components['le1'].move(250, 60)
        self.components['le1'].resize(250, 20)

        self.components['le2'] = QtGui.QLineEdit(self)
        self.components['le2'].move(250, 90)
        self.components['le2'].resize(250, 20)

        self.components['te1'] = QtGui.QTextEdit(self)
        self.components['te1'].resize(300, 350)
        self.components['te1'].move(20, 200)
        self.components['te1'].setReadOnly(1)

        self.components['te2'] = QtGui.QTextEdit(self)
        self.components['te2'].resize(300, 350)
        self.components['te2'].move(340, 200)
        self.components['te2'].setReadOnly(1)

        self.components['te3'] = QtGui.QTextEdit(self)
        self.components['te3'].resize(300, 200)
        self.components['te3'].move(660, 200)
        self.components['te3'].setReadOnly(1)

        self.components['cb1'] = QtGui.QCheckBox(self)
        self.components['cb1'].move(520, 60)
        self.components['cb1'].setText(u'референци')

        self.components['cb2'] = QtGui.QCheckBox(self)
        self.components['cb2'].move(520, 80)
        self.components['cb2'].setText(u'парафразиран текст')

        self.components['cb3'] = QtGui.QCheckBox(self)
        self.components['cb3'].move(520, 100)
        self.components['cb3'].setText(u'параграфи')

        self.components['cb4'] = QtGui.QCheckBox(self)
        self.components['cb4'].move(520, 120)
        self.components['cb4'].setText(u'стил на пишување')

    def set_window_characteristics(self):
        '''Configuring the window characteristics.'''

        self.setWindowTitle(u'Систем за проверка на плагијати')
        self.setGeometry(50, 50, 980, 600)
        self.show()

    def click1(self):
        '''Chooses document 1.'''

        pateka = QtGui.QFileDialog.getOpenFileName(self, u'Одбери документ', './')
        self.components['le1'].setText(pateka)

    def click2(self):
        '''Chooses document 2.'''

        pateka = QtGui.QFileDialog.getOpenFileName(self, u'Одбери документ', './')
        self.components['le2'].setText(pateka)

    def click3(self):
        '''Function triggered when the plagiarism detection is initialized.'''

        path1 = self.components['le1'].text()
        path2 = self.components['le2'].text()

        if path1 == '' or path2 == '':
            self.dialog = ValidationWindow(u'\nВнесете текст за проверка')
            self.components['te1'].setText('')
            self.components['te2'].setText('')
            self.components['te3'].setText('')
            self.components['label7'].hide()
            self.components['combo1'].hide()
        elif not os.path.exists(path1) or not os.path.exists(path2):
            self.dialog = ValidationWindow(u'\nВнесовте погрешна патека!')
            self.components['te1'].setText('')
            self.components['te2'].setText('')
            self.components['te3'].setText('')
            self.components['label7'].hide()
            self.components['combo1'].hide()
        else:
            kategorii = [self.components['cb1'].isChecked(), self.components['cb2'].isChecked(),
                         self.components['cb3'].isChecked(), self.components['cb4'].isChecked()]

            self.kombinacii, summary = detect_plagiarism(unicode(path1), unicode(path2), kategorii)

            file_text = open(path1, 'r')
            text1 = file_text.read().decode("utf-8")
            file_text.close()

            file_text = open(path2, 'r')
            text2 = file_text.read().decode("utf-8")
            file_text.close()

            self.components['te1'].setText(text1)
            self.components['te2'].setText(text2)
            self.components['te3'].setText(summary)
            self.components['combo1'].clear()
            self.components['combo1'].addItems([u'изберете категорија'])

            if self.components['cb1'].isChecked():
                self.components['combo1'].addItem(u'референци')
            if self.components['cb2'].isChecked():
                self.components['combo1'].addItem(u'парафразиран текст')
            if self.components['cb3'].isChecked():
                self.components['combo1'].addItem(u'параграфи')
            if self.components['cb4'].isChecked():
                self.components['combo1'].addItem(u'стил на пишување')
            self.components['label7'].show()
            self.components['combo1'].show()

    def click4(self):
        '''Displays information and instructions.'''

        self.informacii = InstructionsWindow()

    def click5(self):
        '''Function triggered when different details should be displayed.'''

        idx = self.components['combo1'].currentIndex()
        if idx > 0:
            details_view_content = self.kombinacii[idx - 1]
            self.new_app = DetailsWindow(details_view_content)
