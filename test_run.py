#!/usr/bin/env python3
import sys
import traceback

try:
    from PyQt5.QtWidgets import QApplication
    from pet_widget import PetWidget
    
    print("✅ 模块导入成功")
    
    app = QApplication(sys.argv)
    print("✅ QApplication 创建成功")
    
    app.setQuitOnLastWindowClosed(False)
    print("✅ setQuitOnLastWindowClosed 设置成功")
    
    pet = PetWidget()
    print("✅ PetWidget 创建成功")
    
    sys.exit(app.exec_())
    
except Exception as e:
    print(f"❌ 错误: {e}")
    traceback.print_exc()
