# ============================
# Smart Calculator - sur4jkum4r
# CLI MODE
# ============================

import requests
import sys
import time
from colorama import init, Fore, Style
from pyfiglet import Figlet
from currency_api import get_exchange_rate

init(autoreset=True)
fig = Figlet(font='slant')

history = []  # Common history list

def run_cli_mode():
    print(Fore.CYAN + fig.renderText('MULTILATOR'))
    print(Fore.GREEN + "Welcome to CLI Smart Calculator!\n")

    while True:
        print(Fore.YELLOW + "Select Calculator Mode:")
        print("1️⃣  Basic Calculator")
        print("2️⃣  Global Currency Converter")
        print("3️⃣  Unit Converter")
        print("4️⃣  View History")
        print("0️⃣  Exit")

        choice = input(Fore.CYAN + "\n👉 Enter choice (1/2/3/4/0): ").strip()
        if choice == '1':
            run_basic_calculator()
        elif choice == '2':
            run_currency_converter()
        elif choice == '3':
            run_unit_converter()
        elif choice == '4':
            show_history()
        elif choice == '0':
            print(Fore.MAGENTA + "👋 Exiting CLI Mode. Goodbye!")
            sys.exit()
        else:
            print(Fore.RED + "⚠️ Invalid choice! Please enter 1, 2, 3, 4 or 0.")

def run_basic_calculator():
    while True:
        print("\n" + Fore.YELLOW + "📐 Basic Calculator")
        print("1️⃣  Addition (+)")
        print("2️⃣  Subtraction (-)")
        print("3️⃣  Multiplication (*)")
        print("4️⃣  Division (/)")
        print("0️⃣  Back to Main Menu")

        op = input(Fore.CYAN + "👉 Select operation: ").strip()
        if op == '0':
            break

        if op not in ['1', '2', '3', '4']:
            print(Fore.RED + "⚠️ Invalid choice! Try again.")
            continue

        try:
            num1 = float(input(Fore.GREEN + "Enter first number: "))
            num2 = float(input(Fore.GREEN + "Enter second number: "))
        except ValueError:
            print(Fore.RED + "⚠️ Invalid input. Numbers only!")
            continue

        if op == '1':
            result = num1 + num2
            operator = '+'
        elif op == '2':
            result = num1 - num2
            operator = '-'
        elif op == '3':
            result = num1 * num2
            operator = '*'
        elif op == '4':
            if num2 == 0:
                print(Fore.RED + "⚠️ Cannot divide by zero!")
                continue
            result = num1 / num2
            operator = '/'

        print(Fore.MAGENTA + f"✅ Result: {result}")
        history.append(f"Basic Calc: {num1} {operator} {num2} = {result}")

def run_currency_converter():
    currencies = [
        'INR', 'USD', 'EUR', 'GBP', 'AUD', 'CAD', 'SGD', 'JPY', 'CNY', 'AED',
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
        'XAF', 'XCD', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWL'
    ]

    while True:
        print("\n" + Fore.YELLOW + "💱 Currency Converter")
        print(Fore.GREEN + "Available Currencies:")

        for i, cur in enumerate(currencies, 1):
            print(f"{i:3}) {cur}", end='\t')
            if i % 5 == 0:
                print()
        print("\n0) Back to Main Menu")

        try:
            from_choice = int(input(Fore.CYAN + "\n👉 From Currency [Number]: "))
            if from_choice == 0:
                break
            to_choice = int(input(Fore.CYAN + "👉 To Currency [Number]: "))
            if to_choice == 0:
                break

            if from_choice > len(currencies) or to_choice > len(currencies):
                print(Fore.RED + "⚠️ Invalid currency option!")
                continue

            amount = float(input(Fore.GREEN + "Amount: "))

            from_currency = currencies[from_choice - 1]
            to_currency = currencies[to_choice - 1]

            rate = get_exchange_rate(from_currency, to_currency)
            if rate is None:
                print(Fore.RED + "⚠️ Failed to get rate!")
                continue

            converted = round(amount * rate, 2)
            print(Fore.MAGENTA + f"✅ {amount} {from_currency} = {converted} {to_currency}")
            history.append(f"Currency: {amount} {from_currency} ➜ {converted} {to_currency}")

        except ValueError:
            print(Fore.RED + "⚠️ Invalid input. Try again.")
            continue

def run_unit_converter():
    categories = {
        "Length": {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001, "mile": 1609.34, "inch": 0.0254, "ft": 0.3048},
        "Weight": {"kg": 1, "g": 0.001, "mg": 0.000001, "lb": 0.453592, "oz": 0.0283495},
        "Temperature": {"C": "C", "F": "F", "K": "K"},
        "Volume": {"l": 1, "ml": 0.001, "gal": 3.78541},
        "Area": {"sqm": 1, "sqkm": 1_000_000, "sqft": 0.092903, "acre": 4046.86},
        "Speed": {"mps": 1, "kmph": 0.277778, "mph": 0.44704},
        "Time": {"sec": 1, "min": 60, "hr": 3600, "day": 86400},
        "Pressure": {"Pa": 1, "bar": 100000, "atm": 101325, "psi": 6894.76},
        "Energy": {"J": 1, "cal": 4.184, "kWh": 3600000}
    }

    while True:
        print("\n" + Fore.YELLOW + "📏 Unit Converter")
        print("Categories:")
        for i, cat in enumerate(categories.keys(), 1):
            print(f"{i}) {cat}")
        print("0) Back to Main Menu")

        try:
            cat_choice = int(input(Fore.CYAN + "\n👉 Choose category: "))
            if cat_choice == 0:
                break

            cat_keys = list(categories.keys())
            if cat_choice > len(cat_keys):
                print(Fore.RED + "⚠️ Invalid category!")
                continue

            cat_name = cat_keys[cat_choice - 1]
            units = categories[cat_name]

            print(Fore.GREEN + f"Available units for {cat_name}: {', '.join(units.keys())}")

            from_unit = input("From Unit: ").strip()
            to_unit = input("To Unit: ").strip()

            value = float(input("Value: "))

            if cat_name == "Temperature":
                result = convert_temperature(value, from_unit, to_unit)
            else:
                result = value * units[from_unit] / units[to_unit]

            print(Fore.MAGENTA + f"✅ {value} {from_unit} = {result:.4f} {to_unit}")
            history.append(f"Unit: {value} {from_unit} ➜ {result:.4f} {to_unit} [{cat_name}]")

        except Exception as e:
            print(Fore.RED + f"⚠️ Error: {e}")
            continue

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "C":
        if to_unit == "F":
            return value * 9/5 + 32
        elif to_unit == "K":
            return value + 273.15
    if from_unit == "F":
        if to_unit == "C":
            return (value - 32) * 5/9
        elif to_unit == "K":
            return (value - 32) * 5/9 + 273.15
    if from_unit == "K":
        if to_unit == "C":
            return value - 273.15
        elif to_unit == "F":
            return (value - 273.15) * 9/5 + 32
    raise ValueError("Invalid temperature conversion")

def show_history():
    print("\n" + Fore.YELLOW + "📜 Calculation History")
    if not history:
        print(Fore.CYAN + "No history yet!")
    else:
        for entry in history:
            print(Fore.GREEN + f"- {entry}")
