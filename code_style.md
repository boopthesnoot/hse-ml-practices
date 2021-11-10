# Инструменты

Для форматирования и проверки качества кода были выбраны 3 инструмета:

- форматтер **black**
- линтер **Pylint**
- анализатор **Radon**

## black

**black** был запущен для всех скриптов без специальных ключей следующей командой: 

```
black .
```

**black** форматирует скрипты .py в текущей дирректории рекрсивно согласно стилю. 

```
reformatted ./study/hse-ml-practices/src/rf.py
reformatted ./study/hse-ml-practices/src/preproc.py
All done! ✨ 🍰 ✨
2 files reformatted.
```

В результате получился более читаемый код.

## pylint

В качестве линтера был взят **pylint**. Он используется для анализа логики и стилистики кода. Из-за своей строгости к написанию кода, на больших проектах он может выдавать множество ошибок, поэтому при его запуске лучше выбирать те правила, которые действительно важны. Так как данная часть проекта является незначительным по объему, **pylint** был запущен без указания конкретных правил (по умолчанию все они включены):

```
pylint src/preproc.py
```


```
************* Module preproc
src/preproc.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/preproc.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
src/preproc.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
src/preproc.py:40:20: W0621: Redefining name 'df' from outer scope (line 46) (redefined-outer-name)
src/preproc.py:40:0: C0103: Argument name "df" doesn't conform to snake_case naming style (invalid-name)
src/preproc.py:40:0: C0116: Missing function or method docstring (missing-function-docstring)
src/preproc.py:99:20: W0621: Redefining name 'df' from outer scope (line 46) (redefined-outer-name)
src/preproc.py:106:12: W0621: Redefining name 'pclass' from outer scope (line 60) (redefined-outer-name)
src/preproc.py:99:0: C0103: Argument name "df" doesn't conform to snake_case naming style (invalid-name)
src/preproc.py:99:0: C0116: Missing function or method docstring (missing-function-docstring)
src/preproc.py:123:0: C0116: Missing function or method docstring (missing-function-docstring)
src/preproc.py:202:22: W0621: Redefining name 'df' from outer scope (line 46) (redefined-outer-name)
src/preproc.py:202:0: C0103: Argument name "df" doesn't conform to snake_case naming style (invalid-name)
src/preproc.py:202:0: C0116: Missing function or method docstring (missing-function-docstring)
src/preproc.py:221:0: C0116: Missing function or method docstring (missing-function-docstring)
src/preproc.py:334:8: W0621: Redefining name 'i' from outer scope (line 369) (redefined-outer-name)
src/preproc.py:330:0: C0116: Missing function or method docstring (missing-function-docstring)
src/preproc.py:345:12: C0103: Variable name "c" doesn't conform to snake_case naming style (invalid-name)
src/preproc.py:343:8: W0612: Unused variable 'title' (unused-variable)
src/preproc.py:5:0: C0411: standard import "import string" should be placed before "import pandas as pd" (wrong-import-order)
src/preproc.py:6:0: C0411: standard import "import warnings" should be placed before "import pandas as pd" (wrong-import-order)

------------------------------------------------------------------
Your code has been rated at 9.14/10 (previous run: 8.34/10, +0.80)

```


```bash
pylint preprocessing.py
```

```
************* Module preprocessing
preprocessing.py:1:0: C0114: Missing module docstring (missing-module-docstring)
preprocessing.py:12:0: C0103: Constant name "stock_name" doesn't conform to UPPER_CASE naming style (invalid-name)
preprocessing.py:33:0: C0103: Function name "Future_to_MOEX" doesn't conform to snake_case naming style (invalid-name)
preprocessing.py:33:0: C0103: Argument name "x" doesn't conform to snake_case naming style (invalid-name)
preprocessing.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
preprocessing.py:153:14: E1136: Value 'future_Finam' is unsubscriptable (unsubscriptable-object)
preprocessing.py:7:0: W0611: Unused isfile imported from os.path (unused-import)
preprocessing.py:7:0: W0611: Unused join imported from os.path (unused-import)
preprocessing.py:8:0: W0611: Unused import copy (unused-import)
preprocessing.py:10:0: W0611: Unused matplotlib.pyplot imported as plt (unused-import)
preprocessing.py:3:0: C0411: standard import "import datetime as dt" should be placed before "import numpy as np" (wrong-import-order)
preprocessing.py:4:0: C0411: standard import "import re" should be placed before "import numpy as np" (wrong-import-order)
preprocessing.py:6:0: C0411: standard import "from os import listdir" should be placed before "import numpy as np" (wrong-import-order)
preprocessing.py:7:0: C0411: standard import "from os.path import isfile, join" should be placed before "import numpy as np" (wrong-import-order)
preprocessing.py:8:0: C0411: standard import "import copy" should be placed before "import numpy as np" (wrong-import-order)

-----------------------------------
Your code has been rated at 8.10/10
```

Исправим самые простые ошибки:

```
************* Module rf
src/rf.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/rf.py:48:0: C0103: Constant name "oob" doesn't conform to UPPER_CASE naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 9.62/10 (previous run: 9.43/10, +0.19)
```

### Cтатисика по **pylint**
Самые частые ошибки связаны с отсутствием docstring у функций/модулей (missing-module-docstring и missing-function-docstring).

Все ошибки, связанные с неправильным порядков импорта, были решены.

Так же часть ошибок была связана с неправильными именами функций/переменных/аргументов/констант (invalid-name).

Наименьшими по частоте были ошибки с именами локальных переменных, идентичных глобальным (redefined-outer-name) и (unsubscriptable-object). 

## radon

В качестве анализатора кода я взял **radon**, чтобы посмотреть на разные метрики качества кода.

### Цикломатическая сложность:
```
radon cc .
```

Результат:

```
radon cc -a src 
src/preproc.py
    F 102:0 get_pclass_dist - B
    F 205:0 get_survived_dist - A
    F 333:0 extract_surname - A
    F 43:0 display_missing - A
    F 13:0 concat_df - A
    F 18:0 divide_df - A
    F 126:0 display_pclass_dist - A
    F 224:0 display_surv_dist - A

8 blocks (classes, functions, methods) analyzed.
Average complexity: A (2.625)

```
Так как в коде исползовались несложные функции, их цикломатическая сложность ожидаемо низкая.

### Метрики Холстеда


```
radon hal .
```

Данные метрики описывают сложность программы и количество усилий, предположительно затраченное на написание и понимание кода.

```
src/rf.py:
    h1: 6
    h2: 11
    N1: 11
    N2: 20
    vocabulary: 17
    length: 31
    calculated_length: 53.563522809337215
    volume: 126.71134807876054
    difficulty: 5.454545454545454
    effort: 691.1528077023302
    time: 38.39737820568501
    bugs: 0.04223711602625351
src/preproc.py:
    h1: 8
    h2: 49
    N1: 30
    N2: 59
    vocabulary: 57
    length: 89
    calculated_length: 299.1207823616452
    volume: 519.1272112606621
    difficulty: 4.816326530612245
    effort: 2500.2861603574747
    time: 138.90478668652636
    bugs: 0.17304240375355404
```

Скрипт с препроцессингом оказался значительно сложнее в написании и понимании чем random forest. Это вполне ожидаемо, код длиннее, много обработки и получения новых фичей. 


## Грубые ошибки

В целом ни один из инструментов не нашёл грубых ошибок в коде. Ни одну из ошибок, найденных **pylint** нельзя назвать критической. Возможно это вызвано тем, что был произведён небольшой рефакторинг по результатм **pylint** и **black**. 