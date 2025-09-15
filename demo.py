# demo.py
import sys
from quick_fix2 import *  # 載入所有修補
import main  # 載入主程式

if __name__ == "__main__":
    print("DEMO MODE ACTIVATED")
    print("Using emergency quick fixes")
    
    # 初始化資料庫
    main.connect_db()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "gui":
            gui = main.TaskGUI()
            gui.run()
        elif sys.argv[1] == "api":
            main.run_flask()
        elif sys.argv[1] == "backup":
            main.backup_database()
    else:
        print("Demo Usage: python demo.py [gui|api|backup]")