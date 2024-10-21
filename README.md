# Snapture

## English

### Description
The **Snapture** script is for taking snapshots of a file structure into a single file (snap-file). It is similar to archiving but without any compression or transformation.

Key features:
  - Create a snap file from a specified directory.
  - Restore file structure from a snap file to a chosen directory.
  - Preserve information about the owner and access rights in UNIX-like systems.
  - List the files and directories stored in the snap file.
  - Verify file integrity using hash checks.
  - *Strict mode* in which recovery is aborted in the event of a hash error.

### Usage
options:
```
  -h, --help    show help message and exit
  -m            сreate a snap-structure in a file
  -u            restore from a snap-structure
  -s            disable strict mode (try to continue restoring on file hash mismatch)
  -l snap_file  list files and directories stored in snap file
  -d directory  path to the directory
  -f snap_file  path to the snap file
```

#### Examples
- Snapshot whole file structure inside the `./folder/a` directory to the `file.snap` file:
```
python3 snapture.py -m -d ./folder/a -f file.snap
```

- Restore the file structure from the `file.snap` file to the `./folder/b` directory:
```
python3 snapture.py -u -d ./folder/b -f file.snap
```

- Display all files and directories saved within the `file.snap` file:
```
python3 snapture.py -l file.snap
```

## Солов'їна

### Опис
Скрипт **Snapture** призначений для створення знімків файлової структури в один файл-*знімок*. Це схоже на архівування, але без стиснення чи перетворення.

Основні можливості:
  - Створення *знімка* вказаної директорії.
  - Відновлення структури файлів зі *знімка* в обрану директорію.
  - Збереження інформації про власника і права доступу в UNIX-подібних системах.
  - Виведення списку файлів і директорій, що зберігаються у *знімку*.
  - Перевірка цілісності файлів у *знімку* за допомогою хешів.
  - *Суворий режим* при якому відновлення переривається при помилці хешу.

### Використання
параметри:
```
  -h, --help    показати повідомлення довідки та вийти
  -m            зробити знімок файлової структури у snap-файл
  -u            відновити файлову структуру зі snap-файлу
  -s            вимкнути строгий режим (намагатись продовжувати розпаковку при невідповідності хешу файлу)
  -l snap_file  вивести список файлів і директорій, що зберігаються у snap-файлі
  -d директорія шлях до директорії
  -f snap_file  шлях до snap-файлі
```

#### Приклади
- Зробіти знімок усієї файлової структури директорії `./folder/a` у файл `file.snap`:
```
python3 snapture.py -m -d ./folder/a -f file.snap
```

- Відновити файлову структуру з файлу `file.snap` до директорії `./folder/b`:
```
python3 snapture.py -u -d ./folder/b -f file.snap
```

- Відображення всіх файлів і директорій, збережених у файлі `file.snap`:
```
python3 snapture.py -l file.snap
```
