import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
# Для тестового задания директории созданы руками и прописаны здесь
# Для реального проекта получение APK файлов можно фиксировать в параметрах (путь для получения и вывода)
walk_dir = current_dir + "/APKS"
out_dir = current_dir + "/result"
# Для получения списка методов достаточно apktool, но декомпеляция до Java файлов гораздо удобнее для поиска
apktool = os.path.dirname(os.path.abspath(__file__)) + "/apktool.jar"
# Наименование методов для поиска можно хранить в БД или файлах настроек
methods = [
    "getUnsafeOkHttpClient",
    "addJavascriptInterface",
    "WRITE_EXTERNAL_STORAGE",
    "android:debuggable=\"true\"",
    "android:exported=\"false\""]

# Для удобства тестирования добавил параметр
isDecompile = True
if len(sys.argv) > 1:
    isDecompile = sys.argv[1]


# Декомпиляция APK файлов
def decompile():
    # Собираем список всех файлов в каталоге
    list_files = get_files_directory(walk_dir, ".apk")
    for file_name in list_files:
        os.system("jadx -d result " + file_name)


def search_method(name, files):
    print("Ищем метод с именем: " + name)
    is_fined = False
    for filename in files:
        with open(filename) as f:
            if name in f.read():
                print("Найден в файле: " + f.name)
                is_fined = True
    if is_fined == True:
        print("Метод "+name + " найден")
    else:
        print("Метод " + name + " не найден")


def get_files_directory(directory, type):
    result_list = []

    for r, d, f in os.walk(directory):
        for file in f:
            if type in file:
                path = os.path.join(r, file)
                print(path)
                result_list.append(path)
    return result_list


if isDecompile == True:
    decompile()
list_files = get_files_directory(out_dir, ".java")
list_files + get_files_directory(out_dir, "Manifest.xml")

for method in methods:
    search_method(method, list_files)
