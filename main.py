import os
import sys
import keyboard
import playsound

from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QSystemTrayIcon, \
    QMenu, QStyle, qApp, QAction, QFileDialog

from pygame import mixer

import disign

mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')


class ExampleApp(QtWidgets.QMainWindow, disign.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.sounds_path = os.path.realpath('sounds')
        self.link_video = 'https://www.youtube.com/'

        # Tray settings
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        show_action = QAction("Развернуть", self)
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
        self.speaker = True
        self.vol = 0.75
        self.show_volume_lable.setText(str(self.vol))
        self.volume_slider.setValue(round(self.vol * 100))
        mixer.music.set_volume(self.vol)

        self.sound_buttons_data = [
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None]
        ]

        self.sound_buttons = [
            self.sound_btn_1,
            self.sound_btn_2,
            self.sound_btn_3,
            self.sound_btn_4,
            self.sound_btn_5,
            self.sound_btn_6,
            self.sound_btn_7,
            self.sound_btn_8,
            self.sound_btn_9
        ]

        self.set_sound_buttons = [
            self.choose_snd_1,
            self.choose_snd_2,
            self.choose_snd_3,
            self.choose_snd_4,
            self.choose_snd_5,
            self.choose_snd_6,
            self.choose_snd_7,
            self.choose_snd_8,
            self.choose_snd_9
        ]

        self.checkBox_speaker.clicked.connect(self.checkbox_play_f)

        # Buttons connect
        self.open_snds_btn.clicked.connect(lambda: os.startfile(self.sounds_path))
        self.video_instr_btn.clicked.connect(lambda: os.system(f'start {self.link_video}'))
        self.pushButton_remove_all_hk.clicked.connect(self.remove_all_hk)
        self.pushButton_remove_all_snds.clicked.connect(self.remove_all_snds)

        self.beep_btn.pressed.connect(lambda: self.play('D:/Projects/SoundBTN/sounds/beep'))

        self.sound_buttons[0].clicked.connect(lambda: self.play(self.sound_buttons_data[0][0]))
        self.sound_buttons[1].clicked.connect(lambda: self.play(self.sound_buttons_data[1][0]))
        self.sound_buttons[2].clicked.connect(lambda: self.play(self.sound_buttons_data[2][0]))
        self.sound_buttons[3].clicked.connect(lambda: self.play(self.sound_buttons_data[3][0]))
        self.sound_buttons[4].clicked.connect(lambda: self.play(self.sound_buttons_data[4][0]))
        self.sound_buttons[5].clicked.connect(lambda: self.play(self.sound_buttons_data[5][0]))
        self.sound_buttons[6].clicked.connect(lambda: self.play(self.sound_buttons_data[6][0]))
        self.sound_buttons[7].clicked.connect(lambda: self.play(self.sound_buttons_data[7][0]))
        self.sound_buttons[8].clicked.connect(lambda: self.play(self.sound_buttons_data[8][0]))

        self.choose_snd_1.clicked.connect(lambda: self.set_sound(0))
        self.choose_snd_2.clicked.connect(lambda: self.set_sound(1))
        self.choose_snd_3.clicked.connect(lambda: self.set_sound(2))
        self.choose_snd_4.clicked.connect(lambda: self.set_sound(3))
        self.choose_snd_5.clicked.connect(lambda: self.set_sound(4))
        self.choose_snd_6.clicked.connect(lambda: self.set_sound(5))
        self.choose_snd_7.clicked.connect(lambda: self.set_sound(6))
        self.choose_snd_8.clicked.connect(lambda: self.set_sound(7))
        self.choose_snd_9.clicked.connect(lambda: self.set_sound(8))

        self.update_buttons()

    def update_buttons(self):
        for btn in range(len(self.sound_buttons)):
            f = self.sound_buttons_data[btn][0]
            s = self.sound_buttons_data[btn][1]

            self.sound_buttons[btn].setDisabled(f is None)

            if f is None:
                f = 'Звук на задан'
            else:
                f = f.split('/')[-1]
            if s is None:
                s = 'Хоткей на задан'

            self.sound_buttons[btn].setText(f'{f}\n{s}')

            print(self.sound_buttons_data)

    def set_sound(self, btn):

        f_name = QFileDialog.getOpenFileName(self, 'Open file', 'D:\Projects\SoundBTN\sounds', "*.mp3")[0][:-4]

        self.sound_buttons_data[btn][0] = f_name
        self.update_buttons()

    def remove_all_snds(self):
        for i in range(len(self.sound_buttons_data)):
            self.sound_buttons_data[i][0] = ''

        self.update_buttons()

    def remove_all_hk(self):
        for i in self.sound_buttons_data:
            hk = i[1]
            if hk is None:
                continue
            keyboard.remove_hotkey(hk)

    def checkbox_play_f(self):
        self.speaker = self.checkBox_speaker.checkState() // 2 == 1
        print(self.speaker)

    def change_hotkey(self, hotkey, button):
        if not (self.sound_buttons_data[button][1] is None):
            keyboard.remove_hotkey(self.sound_buttons_data[button][1])

        self.sound_buttons_data[button][1] = hotkey
        print(f'Set hotkey {hotkey} to sound {self.sound_buttons_data[button][0]}.')

        keyboard.add_hotkey(hotkey, lambda: self.play(self.sound_buttons_data[button][0]))

    def play(self, name):
        if self.speaker:
            playsound.playsound(f'{name}.mp3', False)
            mixer.music.load(f'{name}.mp3')
            mixer.music.play()

        else:
            mixer.music.load(f'{name}.mp3')
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
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
