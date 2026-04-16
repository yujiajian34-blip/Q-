import sys
import logging
import traceback
from PyQt5.QtWidgets import QApplication
from pet_widget import PetWidget

# 设置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8')
    ]
)

def main():
    try:
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)  # 只有关闭宠物窗口时才退出
        
        pet = PetWidget()
        
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"程序崩溃: {e}", exc_info=True)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
