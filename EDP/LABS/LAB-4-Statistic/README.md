# ЛР №4. ОДНОФАКТОРНЫЙ РЕГРЕССИОННЫЙ АНАЛИЗ

---
## Порядок запуска.
1. Скачать и распаковать [архив](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2FArtemKinko%2FSUAI-labs-spring-2023%2Ftree%2Fmain%2FEDP%2FLABS%2FLAB-4-Statistic) в любое доступное место.
2. Открыть новую вкладку терминала в директории с распакованными файлами и проверить версию Python (лабораторная выполнялась на Python 3.10) командой:
> **Windows**: `py --version`

> **MacOS / Linux**: `python3 --version`
3. Установить пакеты с помощью команды:
> **Windows**: `py -m pip install -r requirements.txt`

> **MacOS / Linux**: `python3 -m pip install -r requirements.txt`

4. Запустить скрипт командой:
> **Windows**: `py lab4-statistic.py`

> **MacOS / Linux**: `python3 lab4-statistic.py`
--- 
## Пояснения к содержанию файлов.
* Файл `data.txt` содержит таблицу значений x и y для каждого варианта.
* Файл `f_function.txt` содержит значения функции распределения Фишера для значений от 1 до 30.
* Файл `t_function.txt` содержит значения функции Стьюдента для уровня значимости 0.01.
* Файл `task.txt` содержит номер варианта, строки в файлах выше, которые будут использоваться при расчетах.