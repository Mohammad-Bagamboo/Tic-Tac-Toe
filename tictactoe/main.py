""" # Tic-tac-toe game

Made by **Mohammad Bagamboo | MB** with love in *Mukalla*. For any suggestions or reporting any
errors, please get in touch with me using the links below.

X ==> https://x.com/Mohamad_Bagambo

Telegram ==> https://t.me/Mohammad_Bagamboo

Github ==> https://github/Mohammad-Bagamboo

Behance ==> https://MohammadBagamboo

"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase
from ui import *
from helpers import Paths, preprocess_qss_files, settings_dict


app = QApplication(sys.argv)
app.setStyleSheet(preprocess_qss_files(Paths.style("app-style.qss"), settings_dict))

# loading font
font_id = QFontDatabase.addApplicationFont(Paths.font("PAPYRUS.TTF"))
font = QFontDatabase.applicationFontFamilies(font_id)

# applying font
app.setFont(QFont(font))

window = Window()
window.exit_game_button.clicked.connect(app.quit)

window.show()
app.exec()
