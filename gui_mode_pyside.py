# gui_mode.py

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QComboBox, QTextEdit,
    QMessageBox, QStackedLayout
)
from PySide6.QtCore import Qt
from currency_api import get_exchange_rate


class SmartCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Calculator - sur4jkum4r")
        self.setGeometry(100, 100, 450, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-family: Arial;
                font-size: 16px;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #2e2e2e;
                color: white;
                border: 1px solid #555;
                padding: 6px;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border: 1px solid #666;
                padding: 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QLabel {
                padding: 6px;
            }
        """)

        self.history = []
        self.current_expression = ""

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        self.create_nav(main_layout)
        self.create_display(main_layout)

        # Stacked layout for pages
        self.stack = QStackedLayout()
        main_layout.addLayout(self.stack)

        self.basic_widget = self.build_basic()
        self.currency_widget = self.build_currency()
        self.unit_widget = self.build_unit()
        self.history_widget = self.build_history()

        self.stack.addWidget(self.basic_widget)
        self.stack.addWidget(self.currency_widget)
        self.stack.addWidget(self.unit_widget)
        self.stack.addWidget(self.history_widget)

        self.stack.setCurrentWidget(self.basic_widget)

    def create_nav(self, parent_layout):
        nav = QHBoxLayout()
        for name, handler in [
            ("Basic", self.show_basic),
            ("Currency", self.show_currency),
            ("Unit", self.show_unit),
            ("History", self.show_history),
            ("Exit", self.close)
        ]:
            btn = QPushButton(name)
            btn.clicked.connect(handler)
            nav.addWidget(btn)
        parent_layout.addLayout(nav)

    def create_display(self, parent_layout):
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFixedHeight(50)
        parent_layout.addWidget(self.display)

    def build_basic(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        btn_rows = [
            ["AC", "DEL", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="],
        ]

        for row in btn_rows:
            row_layout = QHBoxLayout()
            for char in row:
                btn = QPushButton(char)
                btn.setFixedHeight(50)
                btn.clicked.connect(lambda _, ch=char: self.basic_input(ch))
                row_layout.addWidget(btn)
            layout.addLayout(row_layout)

        return page

    def basic_input(self, char):
        if char == 'AC':
            self.current_expression = ""
            self.display.clear()
        elif char == 'DEL':
            self.current_expression = self.current_expression[:-1]
            self.display.setText(self.current_expression)
        elif char == '=':
            try:
                result = eval(self.current_expression)
                self.history.append(f"{self.current_expression} = {result}")
                self.display.setText(str(result))
                self.current_expression = str(result)
            except:
                QMessageBox.critical(self, "Error", "Invalid Expression")
        else:
            self.current_expression += char
            self.display.setText(self.current_expression)

    def build_currency(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        self.from_currency = QComboBox()
        self.to_currency = QComboBox()
        currencies = ['INR', 'USD', 'EUR', 'GBP', 'AUD', 'CAD', 'SGD', 'JPY', 'CNY', 'AED',
                       'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AWG', 'AZN', 'BAM', 'BBD',
                       'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN',
                       'BWP', 'BYN', 'BZD', 'CDF', 'CHF', 'CLP', 'COP', 'CRC', 'CUP', 'CVE',
                       'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'FJD', 'FKP',
                       'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK',
                       'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD',
                       'JOD', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT',
                       'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD',
                       'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN',
                       'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK',
                       'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR',
                       'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'SSP',
                       'STD', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD',
                       'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST',
                       'XAF', 'XCD', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWL']
        self.from_currency.addItems(currencies)
        self.to_currency.addItems(currencies)
        self.from_currency.setCurrentText("USD")
        self.to_currency.setCurrentText("INR")

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")

        btn = QPushButton("Convert")
        btn.clicked.connect(self.convert_currency)

        self.currency_result = QLabel("")

        layout.addWidget(self.from_currency)
        layout.addWidget(self.to_currency)
        layout.addWidget(self.amount_input)
        layout.addWidget(btn)
        layout.addWidget(self.currency_result)

        return page

    def convert_currency(self):
        try:
            amount = float(self.amount_input.text())
            from_cur = self.from_currency.currentText()
            to_cur = self.to_currency.currentText()
            rate = get_exchange_rate(from_cur, to_cur)
            if rate:
                result = round(amount * rate, 2)
                self.currency_result.setText(f"{amount} {from_cur} = {result} {to_cur}")
                self.history.append(f"{amount} {from_cur} = {result} {to_cur}")
            else:
                raise Exception
        except:
            QMessageBox.critical(self, "Error", "Conversion Failed")

    def build_unit(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        self.unit_type = QComboBox()
        self.unit_type.addItems(["Length", "Weight", "Temperature", "Time", "Area", "Volume", "Speed"])
        self.unit_type.currentTextChanged.connect(self.update_units)

        self.from_unit = QComboBox()
        self.to_unit = QComboBox()

        self.unit_input = QLineEdit()
        self.unit_input.setPlaceholderText("Value")

        btn = QPushButton("Convert")
        btn.clicked.connect(self.convert_unit)

        self.unit_result = QLabel("")

        layout.addWidget(self.unit_type)
        layout.addWidget(self.from_unit)
        layout.addWidget(self.to_unit)
        layout.addWidget(self.unit_input)
        layout.addWidget(btn)
        layout.addWidget(self.unit_result)

        self.update_units("Length")

        return page

    def update_units(self, category):
        options = {
            "Length": ['km', 'm', 'cm', 'mm', 'inch', 'ft', 'mile'],
            "Weight": ['kg', 'g', 'lb', 'oz'],
            "Temperature": ['C', 'F', 'K'],
            "Time": ['sec', 'min', 'hour', 'day'],
            "Area": ['sqm', 'sqft', 'acre', 'hectare'],
            "Volume": ['litre', 'ml', 'gal', 'm³', 'cm³'],
            "Speed": ['km/h', 'm/s', 'mph', 'knot'],
        }
        self.from_unit.clear()
        self.to_unit.clear()
        self.from_unit.addItems(options[category])
        self.to_unit.addItems(options[category])

    def convert_unit(self):
        try:
            v = float(self.unit_input.text())
            t = self.unit_type.currentText()
            f = self.from_unit.currentText()
            to = self.to_unit.currentText()

            units = {
                'Length': {'km': 1000, 'm': 1, 'cm': 0.01, 'mm': 0.001, 'inch': 0.0254, 'ft': 0.3048, 'mile': 1609.34},
                'Weight': {'kg': 1000, 'g': 1, 'lb': 453.592, 'oz': 28.3495},
                'Time': {'sec': 1, 'min': 60, 'hour': 3600, 'day': 86400},
            	'Area': {'sqm': 1, 'sqft': 0.092903, 'acre': 4046.86, 'hectare': 10_000},
            	'Volume': {'litre': 1, 'ml': 0.001, 'gal': 3.78541, 'm³': 1000, 'cm³': 0.001},
            	'Speed': {'km/h': 0.277778, 'm/s': 1, 'mph': 0.44704, 'knot': 0.514444},
            }

            if t == "Temperature":
                if f == "C" and to == "F": result = v * 9/5 + 32
                elif f == "F" and to == "C": result = (v - 32) * 5/9
                elif f == "C" and to == "K": result = v + 273.15
                elif f == "K" and to == "C": result = v - 273.15
                elif f == "F" and to == "K": result = (v - 32) * 5/9 + 273.15
                elif f == "K" and to == "F": result = (v - 273.15) * 9/5 + 32
                else: result = v
            else:
                result = v * units[t][f] / units[t][to]

            self.unit_result.setText(f"{v} {f} = {result:.2f} {to}")
            self.history.append(f"{v} {f} = {result:.2f} {to}")

        except:
            QMessageBox.critical(self, "Error", "Conversion Failed")

    def build_history(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.history_view = QTextEdit()
        self.history_view.setReadOnly(True)
        layout.addWidget(self.history_view)
        return page

    def show_basic(self):
        self.stack.setCurrentWidget(self.basic_widget)

    def show_currency(self):
        self.stack.setCurrentWidget(self.currency_widget)

    def show_unit(self):
        self.stack.setCurrentWidget(self.unit_widget)

    def show_history(self):
        self.history_view.setText('\n'.join(self.history[-20:]) if self.history else "No history yet.")
        self.stack.setCurrentWidget(self.history_widget)


def run_gui_mode():
    app = QApplication(sys.argv)
    win = SmartCalculator()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui_mode()
