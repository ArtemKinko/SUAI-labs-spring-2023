# ЛР №5. МНОГОФАКТОРНЫЙ РЕГРЕССИОННЫЙ АНАЛИЗ

---
## Порядок запуска.
1. Скачать и распаковать [архив](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2FArtemKinko%2FSUAI-labs-spring-2023%2Ftree%2Fmain%2FEDP%2FLABS%2FLAB-5-Statistic) в любое доступное место.
2. Открыть новую вкладку терминала в директории с распакованными файлами и проверить версию Python (для корректной установки пакетов требуется Python версии 3.8 или выше) командой:
> **Windows**: `py --version`

> **MacOS / Linux**: `python3 --version`
3. Обновить `pip` командой:
> **Windows**: `py -m pip install --upgrade pip`
> 
> **MacOS / Linux**: `python3 -m pip install --upgrade pip`

4. Установить пакеты с помощью команды:
> **Windows**: `py -m pip install -r requirements.txt`

> **MacOS / Linux**: `python3 -m pip install -r requirements.txt`
5. Запустить скрипт командой:
> **Windows**: `py lab5-statistic.py`

> **MacOS / Linux**: `python3 lab5-statistic.py`
--- 
## Пояснения к содержанию файлов.
* Файл `data.txt` содержит таблицу значений x1, x2 и y для каждого варианта.
* Файл `f_function.txt` содержит значения функции распределения Фишера для значений от 1 до 30.
* Файл `t_function.txt` содержит значения функции Стьюдента для уровня значимости 0.05.
* Файл `task.txt` содержит номер варианта, строки в файлах выше, которые будут использоваться при расчетах.