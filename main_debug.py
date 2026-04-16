#!/usr/bin/env python3
import sys
import os
import logging
import traceback

# 设置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app_debug.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("=" * 50)
        logger.info("程序启动")
        logger.info("=" * 50)
        
        from PyQt5.QtWidgets import QApplication
        logger.info("✅ PyQt5 导入成功")
        
        from pet_widget import PetWidget
        logger.info("✅ PetWidget 导入成功")
        
        app = QApplication(sys.argv)
        logger.info("✅ QApplication 创建成功")
        
        app.setQuitOnLastWindowClosed(False)
        logger.info("✅ setQuitOnLastWindowClosed 设置成功")
        
        pet = PetWidget()
        logger.info("✅ PetWidget 实例化成功")
        
        logger.info("程序进入事件循环")
        exit_code = app.exec_()
        logger.info(f"应用退出，代码: {exit_code}")
        sys.exit(exit_code)
        
    except Exception as e:
        logger.error(f"❌ 发生异常: {e}", exc_info=True)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
