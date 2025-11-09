## Использование

```bash
# Посмотреть доступные параметры
python main.py --help

# Явно перечислить CSV-файлы
python main.py --files examples/products1.csv examples/products2.csv --report average-rating

# Взять все *.csv из каталога
python main.py --path examples --report average-rating

# Сохранить результат в CSV
python main.py --path examples --report average-rating --save reports/avg.csv
```

- `--help` — выводит справку по всем параметрам.
- `--files` — один или несколько путей к CSV с колонками `name,brand,price,rating`.
- `--path` — каталог, из которого автоматически берутся все файлы `*.csv`.
- `--report` — название отчёта (сейчас доступен `average-rating`), который сортирует бренды по среднему рейтингу.
- `--save` — путь к CSV-файлу; в него записывается результат в виде таблицы с заголовками.

## Зависимости и тест

```bash
python -m pip install -r requirements.txt
pytest --cov=brand_rate --cov=main
```

## Примеры работы скрипта:

#### Вывод help:

![help](img\help.png)

#### Вывод по конкретным файлам:

![help](img\fyles.png)

#### Вывод по конкретной папке:

![help](img\path.png)

#### Вывод с ошибкой:

![help](img\error.png)