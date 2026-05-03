import sys
from PyQt6.QtWidgets import QApplication
from logic import Logic


def main() -> None:
    application = QApplication(sys.argv)
    window = Logic()
    window.show()
    sys.exit(application.exec())


if __name__ == '__main__':
    main()
