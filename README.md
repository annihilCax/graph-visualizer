# Визуализация графа зависимостей
## 1. Общее описание
Зависимости определяются для git-репозитория. Для описания графа зависимостей используется представление **Mermaid**. Визуализатор должен выводить результат на экран в виде графического изображения графа.

Построить граф зависимостей для коммитов, в узлах которого содержатся дата, время и автор коммита. Граф необходимо строить только для тех коммитов, где фигурирует файл с заданным хеш-значением. Ключами командной строки задаются:\
• Путь к программе для визуализации графов.\
• Путь к анализируемому репозиторию.\
• Файл с заданным хеш-значением в репозитории.

## 2. Описание всех функций и настроек


## 3. Описание команд для сборки проекта

Клонировать репозиторий
```
git clone https://github.com/git/git.git
```

Сборка проекта осуществляется в командной строке с ключами --visualizer, --repo, --file-hash для пути к программе для визуализации графов, репозитория и файлы с хэш-значением соответственно.
```
python main.py --visualizer /path/to/mmdc --repo /path/to/git --file-hash <hash>
```

## 4. Примеры использования
![alt text](image.png)
![alt text](image-1.png)
## 5. Результаты прогона тестов

python main.py --visualizer mermaid/mmdc --repo /path/to/git --file-hash <hash>