import logging
import sys

import selenium
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, \
    QFileDialog, QLabel, QPlainTextEdit, QProgressBar, QComboBox
from selenium import webdriver
from multiprocessing import Process

from core import send_message, read_dataframe, autenticate

logger = logging.getLogger(__name__)

FORMAT = '%(asctime)s %(message)'

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):

    def __init__(self, driver: selenium.webdriver):
        super(MainWindow, self).__init__()
        self.webdriver = driver
        self.setWindowTitle("Simple Messenger")

        self.contact_df = None

        layout = QVBoxLayout()

        self.file_path_label = QLabel(f"Selecione o arquivo .csv contendo o número do whatsapp dos destinatários")
        layout.addWidget(self.file_path_label)


        layout1= QHBoxLayout()

        self.file_path_selected = QLineEdit()
        self.file_path_selected.textChanged.connect(self.load_data_frame)
        layout1.addWidget(self.file_path_selected)

        file_path_selector = QPushButton()
        file_path_selector.setText("...")
        file_path_selector.clicked.connect(self.open_file_selector_dialog)
        layout1.addWidget(file_path_selector)

        layout.addLayout(layout1)

        layout2 = QVBoxLayout()
        self.num_contacts_label = QLabel(f"Número de contatos encontrados: {0}")
        layout.addWidget(self.num_contacts_label)

        self.variables_label = QLabel(f"Variáveis: Nenhuma variável")
        layout.addWidget(self.variables_label)

        layout.addLayout(layout2)

        self.template_editor = QPlainTextEdit()
        self.template_editor.setDisabled(True)
        self.template_editor.setPlaceholderText("Digite a mensagem a ser enviada\nAs variáveis serão substituidas "
                                                "quando o texto for enviado.")
        layout.addWidget(self.template_editor)

        self.phone_number_column_name = QComboBox()
        self.phone_number_column_name.setDisabled(True)
        self.phone_number_column_name.setPlaceholderText("Indique a coluna com o número de telefone")
        self.phone_number_column_name.currentIndexChanged.connect(self.phone_number_selected)
        layout.addWidget(self.phone_number_column_name)

        self.send_button = QPushButton()
        self.send_button.setText("Enviar")
        self.send_button.setDisabled(True)
        self.send_button.clicked.connect(self.send)
        layout.addWidget(self.send_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_file_selector_dialog(self):
        dialog = QFileDialog()
        dialog.setNameFilters(["CSV File (*.csv)", "Excel (*.xlsx)"])
        if dialog.exec():
            self.file_path_selected.setText(dialog.selectedFiles()[0])

    def load_data_frame(self, text):
        self.contact_df = read_dataframe(text)
        self.num_contacts_label.setText(f"Número de contatos: {self.contact_df.shape[0]}")
        self.variables_label.setText("Variáveis: " + ", ".join(map(lambda x: f"${x}", self.contact_df.columns)))
        self.progress_bar.setMaximum(self.contact_df.shape[0])
        self.phone_number_column_name.addItems(self.contact_df.columns.to_list())
        self.template_editor.setDisabled(False)
        self.progress_bar.setDisabled(False)
        self.phone_number_column_name.setDisabled(False)

    def phone_number_selected(self):
        self.send_button.setDisabled(False)

    def send(self):
        text = self.template_editor.toPlainText()
        this.process = Process(target=send_message,
                        args=(
                            self.webdriver,
                            text,
                            self.contact_df,
                            self.phone_number_column_name.currentText(),
                            lambda i: self.progress_bar.setValue(i + 1),
                            True,
                            self.file_path_selected.text()),
                        deamon=True)

        this.process.run()
        
        # send_message(self.webdriver, text, contacts_df=self.contact_df,
        #              counter_callback=lambda i: self.progress_bar.setValue(i + 1),
        #              phone_number_column=self.phone_number_column_name.currentText(),
        #              save_progress=True,
        #              progress_entry_id=self.file_path_selected.text())

    def closeEvent(self, event):
        logger.info('application closed')
        self.webdriver.quit()
        if this.process.is_alive():
            this.process.terminate()
        

if __name__ == "__main__":
    driver = None
    logging.basicConfig(filename='simple-messager.log', filemode="a", level=logging.INFO)
    logger.info('application initialized')

    app = QApplication(sys.argv)

    options = webdriver.ChromeOptions()

    if sys.platform == 'linux':
        options.add_argument(f'--user-data-dir=./session/')
    else:
        options.add_argument(r'--user-data-dir=\session')
    driver = webdriver.Chrome(options=options)
    autenticate(driver)

    window = MainWindow(driver)

    window.setMinimumSize(400, 400)

    window.show()

    app.exec()
    driver.quit()
