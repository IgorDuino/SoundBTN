import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon, \
    QSpacerItem, QSizePolicy, QMenu, QAction, QStyle, qApp
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSound, QSoundEffect
import disign  # Это наш конвертированный файл дизайна
from pygame._sdl2 import get_num_audio_devices, get_audio_device_name
from PyQt5 import QtCore
from pygame import mixer
import keyboard


mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')


class ExampleApp(QtWidgets.QMainWindow, disign.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        # Tray settings
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        show_action = QAction("Разверуть", self)
        hide_action = QAction("Спрятать", self)
        quit_action = QAction("Закрыть", self)

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Volume settings
        self.volume_slider.valueChanged.connect(self.change_volume)

        self.vol = 0.5
        self.show_volume_lable.setText(str(self.vol))
        self.volume_slider.setValue(50)
        mixer.music.set_volume(self.vol)

        self.bs = [
            ['29-bruh', None],
            ['', None],
            ['', None],
            ['', None],
            ['', None],
            ['', None],
            ['', None],
            ['', None],
            ['', None]
        ]

        # Buttons connect
        self.sound_btn_1.clicked.connect(lambda: self.play(self.bs[0][0]))
        self.sound_btn_2.clicked.connect(lambda: self.play(self.bs[1][0]))
        self.sound_btn_3.clicked.connect(lambda: self.play(self.bs[2][0]))
        self.sound_btn_4.clicked.connect(lambda: self.play(self.bs[3][0]))
        self.sound_btn_5.clicked.connect(lambda: self.play(self.bs[4][0]))
        self.sound_btn_6.clicked.connect(lambda: self.play(self.bs[5][0]))
        self.sound_btn_7.clicked.connect(lambda: self.play(self.bs[6][0]))
        self.sound_btn_8.clicked.connect(lambda: self.play(self.bs[7][0]))
        self.sound_btn_9.clicked.connect(lambda: self.play(self.bs[8][0]))

        # keySequenceEdit settings
        self.keySequenceEdit_1.keySequenceChanged.connect(lambda : self.change_hotkey(
            (self.keySequenceEdit_1.keySequence().toString(QtGui.QKeySequence.NativeText)).lower(), 0))
        self.keySequenceEdit_2.keySequenceChanged.connect(lambda: self.change_hotkey(
            (self.keySequenceEdit_2.keySequence().toString(QtGui.QKeySequence.NativeText)).lower(), 1))
        self.keySequenceEdit_3.keySequenceChanged.connect(lambda: self.change_hotkey(
            (self.keySequenceEdit_3.keySequence().toString(QtGui.QKeySequence.NativeText)).lower(), 2))
        self.keySequenceEdit_4.keySequenceChanged.connect(lambda: self.change_hotkey(
            (self.keySequenceEdit_4.keySequence().toString(QtGui.QKeySequence.NativeText)).lower(), 3))
        self.keySequenceEdit_5.keySequenceChanged.connect(lambda: self.change_hotkey(
            (self.keySequenceEdit_5.keySequence().toString(QtGui.QKeySequence.NativeText)).lower(), 4))
        self.keySequenceEdit_6.keySequenceChanged.connect(lambda: self.change_hotkey(
            (self.keySequenceEdit_6.keySequence().toString(QtGui.QKeySequence.NativeText)).lower(), 5))
        self.keySequenceEdit_7.keySequenceChanged.connect(lambda: self.change_hotkey(
            (self.keySequenceEdit_7.keySequence().toString(QtGui.QKeySequence.NativeText)).lower(), 6))
        self.keySequenceEdit_8.keySequenceChanged.connect(lambda: self.change_hotkey(
            (self.keySequenceEdit_8.keySequence().toString(QtGui.QKeySequence.NativeText)).lower(), 7))
        self.keySequenceEdit_9.keySequenceChanged.connect(lambda: self.change_hotkey(
            (self.keySequenceEdit_9.keySequence().toString(QtGui.QKeySequence.NativeText)).lower(), 8))

    def change_hotkey(self, hotkey, button):
        if not (self.bs[button][1] is None):
            keyboard.remove_hotkey(self.bs[button][1])

        self.bs[button][1] = hotkey
        print(f'Set hotkey {hotkey} to sound {self.bs[button][0]}.')

        keyboard.add_hotkey("ctrl+alt+p", lambda: self.play(''))

    def play(self, name):
        mixer.music.load(f'sounds/{name}.mp3')
        mixer.music.play()

    def change_volume(self):
        self.vol = self.volume_slider.value() / 100
        self.show_volume_lable.setText(str(self.vol))
        mixer.music.set_volume(self.vol)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
