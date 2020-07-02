import sys
from PyQt5.QtWidgets import *
import googletrans


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.translator = googletrans.Translator()

        self.beforeLang = ''
        self.afterLang = 'af'
        self.LANGUAGES = googletrans.LANGUAGES
        self.LANGCODES = dict(map(reversed, self.LANGUAGES.items()))

        self.lblBefore = QLabel('자동 언어 인식', self)
        self.cbLAfter = QComboBox(self)
        self.teBefore = QTextEdit(self)
        self.teAfter = QTextEdit(self)
        self.trans_btn = QPushButton('번역', self)

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.lblBefore)
        for lang in self.LANGCODES:
            self.cbLAfter.addItem(lang)
        vbox.addWidget(self.teBefore)
        vbox.addWidget(self.cbLAfter)
        vbox.addWidget(self.teAfter)
        vbox.addWidget(self.trans_btn)
        self.setLayout(vbox)
        
        self.teBefore.textChanged.connect(self.detectBeforeLanguage)
        self.cbLAfter.activated[str].connect(self.setAfterLanguage)
        self.trans_btn.clicked.connect(self.translate)

        self.setWindowTitle('Google Translator')
        self.setGeometry(200, 200, 400, 300)
        self.center()
        self.show()

    # 프로그램을 화면 중앙으로 배치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # beforeQTextEdit에 변경이 일어나면, 번역 될 언어 detect
    def detectBeforeLanguage(self):
        text = self.teBefore.toPlainText()
        if len(text) == 0:
            self.beforeLang = ''
        elif len(text) % 5 == 1: # 계속 detect하면 너무 느려져서 5글자 마다 언어 detect
            self.beforeLang = self.translator.detect(text).lang

        if self.beforeLang == '':
            self.lblBefore.setText('자동 언어 인식')
        else:
            self.lblBefore.setText(self.LANGUAGES[self.beforeLang.lower()])

    # QComboBox에 변경이 일어나면 번역할 언어 설정
    def setAfterLanguage(self, text):
        self.afterLang = self.LANGCODES[text]

    # 번역
    def translate(self):
        text_before = self.teBefore.toPlainText()
        text_after = self.translator.translate(text_before, dest=self.afterLang, src=self.beforeLang).text
        self.teAfter.setPlainText(text_after)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())