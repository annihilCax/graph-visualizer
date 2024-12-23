# Визуализация графа зависимостей
## 1. Общее описание
Зависимости определяются для git-репозитория. Для описания графа зависимостей используется представление **Mermaid**. Визуализатор должен выводить результат на экран в виде графического изображения графа.

Построить граф зависимостей для коммитов, в узлах которого содержатся дата, время и автор коммита. Граф необходимо строить только для тех коммитов, где фигурирует файл с заданным хеш-значением. Ключами командной строки задаются:\
• Путь к программе для визуализации графов.\
• Путь к анализируемому репозиторию.\
• Файл с заданным хеш-значением в репозитории.

## 2. Описание всех функций и настроек
1. Получение всех коммитов
2. Получение информации о каждом коммите
3. Парсинг дерева коммита
4. Проверка наличия хэша файла в дереве
5. Добавление в зависимости

## 3. Описание команд для сборки проекта

Клонировать репозиторий
```
git clone https://github.com/git/git.git
```

В папке репозитория ввести команду,
```
git hash-object <file_path>
```
где <file_path> - путь до необходимого файла.

Скопировать хэш-значение, вставить в файл в корне проекта hash_code.txt

Сборка проекта осуществляется в командной строке с ключами --visualizer, --repo, --file_hash для пути к программе для визуализации графов, репозитория и файла с хэш-значением соответственно.
```
python main.py --visualizer .\mermaid\mmdc.cmd --repo .\repo\learn-to-learn --file_hash hash_code.txt
```

## 4. Примеры использования




