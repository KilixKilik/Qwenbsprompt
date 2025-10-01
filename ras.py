import os
import shutil

# Создание директории для результатов
os.makedirs("ras", exist_ok=True)

# Определение игнорируемых директорий и файлов
ignore_dirs = {"__pycache__", "ras", "GameAssets", "Assets"}
ignore_files = {"script.py"}

# --- Удаление всех папок с названиями 'obj' и 'bin' ---
def remove_dirs_by_name(root_dir, dir_names_to_remove):
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for dirname in dirnames:
            if dirname in dir_names_to_remove:
                full_path = os.path.join(dirpath, dirname)
                print(f"Удаление папки: {full_path}")
                shutil.rmtree(full_path)

# Выполняем удаление
remove_dirs_by_name(".", {"obj", "bin"})

# --- Обработка корневых файлов ---
with open("ras/Корневая.txt", "w", encoding="utf-8") as root_out:
    for item in os.listdir("."):
        if os.path.isfile(item) and item not in ignore_files:
            root_out.write(f"ПАПКА: .\n")  # Корень — это "."
            root_out.write(f"--------Файл: {item}\n")
            try:
                with open(item, "r", encoding="utf-8") as f:
                    root_out.write(f.read())
            except Exception:
                root_out.write("[BINARY or ERROR]")
            root_out.write("\n\n")

# --- Обработка папок первого уровня ---
for item in os.listdir("."):
    if os.path.isdir(item) and item not in ignore_dirs:
        output_file = f"ras/{item}.txt"
        with open(output_file, "w", encoding="utf-8") as out:
            # Записываем заголовок папки
            out.write(f"ПАПКА: {item}\n")
            
            # Проходим по всем поддиректориям и файлам внутри
            for dirpath, dirnames, files in os.walk(item):
                # Фильтруем игнорируемые директории на лету
                dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
                
                # Для каждого файла в текущей директории
                for f in files:
                    fp = os.path.join(dirpath, f)
                    # Относительный путь от корня папки (для читаемости)
                    rel_path = os.path.relpath(fp, item)
                    
                    out.write(f"--------Файл: {rel_path}\n")
                    try:
                        with open(fp, "r", encoding="utf-8") as infile:
                            out.write(infile.read())
                    except Exception:
                        out.write("[BINARY or ERROR]")
                    out.write("\n\n")