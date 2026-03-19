import os
import codecs

def go():
    base_dir = r"d:\1\AI"
    pages_dir = os.path.join(base_dir, "pages")
    
    app_py_path = os.path.join(base_dir, "App.py")
    
    files = [
        "1_Chẩn_Đoán.py",
        "2_Lịch_Sử.py",
        "3_Thống_Kê.py",
        "4_Phân_Tích_Giấy_Tờ.py",
        "5_Trợ_Lý_AI.py"
    ]
    
    # We already wrote App_part1, 2, 3 manually in previous steps! D'oh!
    # Let's just read them and concatenate them!
    parts = ["App_part1.py", "App_part2.py", "App_part3.py"]
    
    out_lines = []
    for p in parts:
        path = os.path.join(base_dir, p)
        if os.path.exists(path):
            with codecs.open(path, "r", "utf-8") as f:
                out_lines.append(f.read())
                out_lines.append("\n\n")
        else:
            print(f"Missing {p}")
            return
            
    with codecs.open(app_py_path, "w", "utf-8") as f:
        f.write("".join(out_lines))
        
    print("Merged successfully into App.py")

if __name__ == "__main__":
    go()
