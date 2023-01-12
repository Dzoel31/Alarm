import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from datetime import datetime
from playsound import playsound
from threading import *

class AlarmWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setWindowTitle("Alarm GUI")
        self.resize(400,300)
    
    def setupUI(self):
        self.TargetHour = QLineEdit("00",textEdited = self.UpdateTimeLabel)
        self.TargetHour.setMaxLength(2)
        self.TargetMinute = QLineEdit("00",textEdited = self.UpdateTimeLabel)
        self.TargetMinute.setMaxLength(2)

        self.TimeFormat = QComboBox(activated = self.UpdateTimeLabel)
        self.TimeFormat.addItem("AM")
        self.TimeFormat.addItem("PM")
        self.TimeFormat.setCurrentIndex(0)

        self.ErrorMessages = QLabel()

        self.SetTimerText = QLabel("00:00:00 AM/PM")
        self.SetTimerText.setAlignment(Qt.AlignCenter)
        self.SetTimerText.setStyleSheet("font-size:40px;")
        self.CountdownText = QLabel()
        self.CountdownText.setAlignment(Qt.AlignCenter)
        self.CountdownText.setStyleSheet("font-size:20px;")

        hboxInput = QHBoxLayout()
        hboxInput.addWidget(self.TargetHour)
        hboxInput.addWidget(self.TargetMinute)
        hboxInput.addWidget(self.TimeFormat)

        self.SetTimerButton = QPushButton("Set Alarm",clicked = self.thread)
        self.StopButton = QPushButton("STOP",clicked = self.stopAlarm)
        self.StopButton.setEnabled(False)

        hbutton = QHBoxLayout()
        hbutton.addWidget(self.SetTimerButton)
        hbutton.addWidget(self.StopButton)

        MainWidget = QVBoxLayout()
        MainWidget.addLayout(hboxInput)
        MainWidget.addWidget(self.ErrorMessages)
        MainWidget.addWidget(self.SetTimerText)
        MainWidget.addWidget(self.CountdownText)
        MainWidget.addLayout(hbutton)

        self.setLayout(MainWidget)
        
    def UpdateTimeLabel(self):
        TargetHour = self.TargetHour.text()
        TargetMinute = self.TargetMinute.text()
        TargetFormat = self.TimeFormat.currentText()

        if TargetHour > "12":
            self.ErrorMessages.setText("Invalid HOUR format! Input must be 1 to 12")
            self.SetTimerButton.setEnabled(False)
        
        elif TargetMinute > "59":
            self.ErrorMessages.setText("Invalid MINUTE format! Input must be 1 to 59")
            self.SetTimerButton.setEnabled(False)
        
        else :
            self.ErrorMessages.setText("")
            self.TargetTime = f"{TargetHour}:{TargetMinute}:00 {TargetFormat}"
            self.SetTimerText.setText(self.TargetTime)
            self.SetTimerButton.setEnabled(True)
    
    def thread(self):
        self.Alarm = Thread(target=self.SetAlarm)
        self.Alarm.start()

    def SetAlarm(self):
        target_hour = int(self.TargetTime[0:2]) * 3600
        target_min = int(self.TargetTime[3:5]) * 60
        target_sec = 00
        target_format = self.TargetTime[9:]

        while True:
            CurrentTime = datetime.now().strftime("%I:%M:%S %p")

            current_hour = int(CurrentTime[0:2]) * 3600
            current_min = int(CurrentTime[3:5]) * 60
            current_sec = int(CurrentTime[6:8])
            current_format = CurrentTime[9:]

            
            if target_format != current_format:
                countdown = ((target_hour + target_min + target_sec) + 12 * 3600) - (current_hour + current_min + current_sec)
            else:
                countdown = (target_hour + target_min + target_sec) - (current_hour + current_min + current_sec)

            if countdown < 0:
                countdown += 86400

            HH = (countdown // 3600)
            time_rest = countdown % 3600
            MM = time_rest // 60
            SS = time_rest % 60
            
            self.CountdownText.setText(f"Alarm in {HH:02d} hours {MM:02d} minutes {SS:02d} seconds")

            if self.TargetTime == CurrentTime:
                self.SetTimerText.setText("WAKE UP!!!")
                self.CountdownText.setText("")
                self.StopButton.setEnabled(True)
                playsound("Audio\Latto Latto Sound.mp3") #Masukkan path lagu disini
                break
    
    def stopAlarm(self):
        os._exit(1)

App = QApplication(sys.argv)
Window = AlarmWindow()
Window.show()
App.exec_()