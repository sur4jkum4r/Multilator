# ============================
# MULTILATOR - Smart Calculator by sur4jkum4r
# MAIN LAUNCHER
# ============================

import sys
from cli_mode import run_cli_mode
from gui_mode_pyside import run_gui_mode 

def show_about():
    print("\n📖 About MULTILATOR")
    print("=" * 40)
    print("🔹 Project Name : MULTILATOR")
    print("🔹 Type         : AIO Smart Calculator (CLI + GUI)")
    print("🔹 Created By   : Suraj Prajapati (sur4jkum4r)")
    print("🔹 Features     :")
    print("   • Basic Arithmetic Calculator")
    print("   • Worldwide AIO Currency Converter (Live API)")
    print("   • AIO Unit Converter (Length, Weight, Temperature...And Many More)")
    print("   • History Tracking")
    print("   • Dual Modes Supported: CLI and GUI (PySide6)")
    print("=" * 40)

def main():
    print("\n📱 MULTILATOR - Smart Calculator by sur4jkum4r\n")
    print("Select Mode:")
    print("1) CLI Mode")
    print("2) GUI Mode")
    print("3) About MULTILATOR")
    print("0) Exit")

    wrong_input = 0

    while True:
        choice = input("\n👉 Enter choice (1/2/3/0): ").strip()

        if choice == '1':
            run_cli_mode()
            break
        elif choice == '2':
            run_gui_mode()
            break
        elif choice == '3':
            show_about()
        elif choice == '0':
            print("👋 Exiting MULTILATOR. Goodbye!")
            sys.exit()
        else:
            wrong_input += 1
            print("⚠️ Invalid choice! Please enter 1, 2, 3 or 0.")
            if wrong_input >= 3:
                print("🚪 Too many wrong inputs. Exiting...")
                sys.exit()

if __name__ == "__main__":
    main()
