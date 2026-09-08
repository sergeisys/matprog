import numpy as np

def modified_jordan_step(a, k, s):
    # Создаем копию таблицы, чтобы не изменять оригинал
    b = np.array(a, dtype=float)
    rows, cols = b.shape
    
    # Разрешающий элемент
    pivot_element = b[k, s]
    
    if abs(pivot_element) < 1e-10:
        raise ValueError("Разрешающий элемент близок к нулю!")
    
    # 1) Остальные элементы разрешающей строки делятся на разрешающий элемент
    for j in range(cols):
        if j != s:
            b[k, j] = a[k, j] / pivot_element
    
    # 2) Элементы разрешающего столбца (кроме разрешающего) меняют знак и делятся на разрешающий элемент
    for i in range(rows):
        if i != k:
            b[i, s] = -a[i, s] / pivot_element
    
    # Разрешающий элемент становится 1 (или 1/pivot_element * pivot_element)
    b[k, s] = 1 / pivot_element
    
    # 3) Остальные элементы пересчитываются по правилу прямоугольника
    for i in range(rows):
        if i != k:
            for j in range(cols):
                if j != s:
                    b[i, j] = a[i, j] - (a[i, s] * a[k, j]) / pivot_element
    
    return b


def print_table(table, row_names=None, col_names=None):
    """Выводит таблицу в удобочитаемом виде"""
    rows, cols = table.shape
    
    # Заголовки столбцов
    if col_names is None:
        col_names = [f"-X{i+1}" for i in range(cols)]
    
    # Заголовки строк
    if row_names is None:
        row_names = [f"y{i+1}" for i in range(rows)]
    
    # Выводим заголовки
    print("   ", end=" ")
    for name in col_names:
        print(f"{name:>8}", end=" ")
    print()
    
    # Выводим строки
    for i, row_name in enumerate(row_names):
        print(f"{row_name:2}", end=" ")
        for val in table[i]:
            print(f"{val:>8.2f}", end=" ")
        print()


# ============== ДЕМОНСТРАЦИЯ НА ПРИМЕРЕ ==============

print("=" * 60)
print("МОДИФИЦИРОВАННОЕ ЖОРДАНОВО ИСКЛЮЧЕНИЕ - ОДИН ШАГ")
print("=" * 60)

# Исходная система:
# y1 = 2*x1 - x2 + 3*x3
# y2 = -x1 + 4*x2 - 2*x3
# y3 = 5*x1 + 2*x2 - 4*x3

# Таблица коэффициентов (строки: y1, y2, y3; столбцы: -X1, -X2, -X3)
# Для y1: 2*x1 - x2 + 3*x3  -> коэффициенты при -X1, -X2, -X3: -2, 1, -3
# Для y2: -x1 + 4*x2 - 2*x3 -> коэффициенты: 1, -4, 2
# Для y3: 5*x1 + 2*x2 - 4*x3 -> коэффициенты: -5, -2, 4

a = np.array([
    [-2,  1, -3],   # y1
    [ 1, -4,  2],   # y2
    [-5, -2,  4]    # y3
])

row_names = ["y1", "y2", "y3"]
col_names = ["-X1", "-X2", "-X3"]

print("\nИсходная таблица:")
print_table(a, row_names, col_names)

# Выполняем один шаг с разрешающим элементом: строка 1 (y2), столбец 2 (-X3)
# (в Python индексы: строка 1, столбец 2)
k = 1  # y2
s = 2  # -X3

print(f"\nРазрешающий элемент: строка '{row_names[k]}', столбец '{col_names[s]}'")
print(f"Разрешающий элемент = {a[k, s]}")

b = modified_jordan_step(a, k, s)

print("\nТаблица после одного шага модифицированного жорданова исключения:")
print_table(b, row_names, col_names)

print("\n" + "=" * 60)
print("ПОЛУЧЕННАЯ СИСТЕМА УРАВНЕНИЙ:")
print("=" * 60)

# Интерпретация результатов:
# После исключения переменная X3 становится базисной (выраженной через остальные)
# В строке y2 теперь стоит 1 в столбце -X3, что означает: -X3 = ... -> X3 = ...

print(f"\n{row_names[0]} = {b[0, 0]:.1f}*X1 + {-b[0, 1]:.1f}*X2 + {-b[0, 2]:.1f}*{row_names[1]}")
print(f"{col_names[2][1:]} = {b[1, 0]:.1f}*X1 + {-b[1, 1]:.1f}*X2 + {b[1, 2]:.1f}*{row_names[1]}")
print(f"{row_names[2]} = {b[2, 0]:.1f}*X1 + {-b[2, 1]:.1f}*X2 + {-b[2, 2]:.1f}*{row_names[1]}")