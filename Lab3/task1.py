# Вариант 5. Rectangle, Pentagon, move, is_include 
import math

# Исключение для недопустимых параметров фигуры
class InvalidShapeParameterError(Exception):
    pass

# Oбщие свойства и методы для всех фигур
class Shape:
    def __init__(self, shape_id):
        if not isinstance(shape_id, str) or not shape_id.strip():
            raise InvalidShapeParameterError("Идентификатор фигуры должен быть непустой строкой")
        self.id = shape_id
    
    def move(self, dx, dy):
        if not isinstance(dx, (int, float)) or not isinstance(dy, (int, float)):
            raise InvalidShapeParameterError("Параметры перемещения должны быть числами")
        
        for point in self.points:
            point[0] += dx
            point[1] += dy
    
    def is_include(self, other):
        pass

# Класс Rectangle (прямоугольник)
class Rectangle(Shape):
    def __init__(self, shape_id, x, y, width, height):
        super().__init__(shape_id)

        if not all(isinstance(param, (int, float)) for param in [x, y, width, height]):
            raise InvalidShapeParameterError("Параметры прямоугольника должны быть числами")
        if width <= 0 or height <= 0:
            raise InvalidShapeParameterError("Ширина и высота прямоугольника должны быть положительными")

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._update_points()
    
    def _update_points(self):
        self.points = [
            [self.x, self.y],
            [self.x + self.width, self.y],
            [self.x + self.width, self.y + self.height],
            [self.x, self.y + self.height]
        ]
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self._update_points()
    
    def is_include(self, other):
        if isinstance(other, Rectangle):
            return (self.x <= other.x and 
                    self.y <= other.y and
                    self.x + self.width >= other.x + other.width and
                    self.y + self.height >= other.y + other.height)
        elif isinstance(other, Pentagon):
            for point in other.points:
                if not (self.x <= point[0] <= self.x + self.width and
                       self.y <= point[1] <= self.y + self.height):
                    return False
            return True
    
    def __str__(self):
        return f"Rectangle(id={self.id}, x={self.x}, y={self.y}, width={self.width}, height={self.height})"

# Класс Pentagon (пятиугольник)
class Pentagon(Shape):
    def __init__(self, shape_id, center_x, center_y, radius):
        super().__init__(shape_id)

        if not all(isinstance(param, (int, float)) for param in [center_x, center_y, radius]):
            raise InvalidShapeParameterError("Параметры пятиугольника должны быть числами")
        if radius <= 0:
            raise InvalidShapeParameterError("Радиус пятиугольника должен быть положительным")

        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self._update_points()
    
    def _update_points(self):
        self.points = []
        for i in range(5):
            angle = 2 * math.pi * i / 5
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            self.points.append([x, y])
    
    def move(self, dx, dy):
        self.center_x += dx
        self.center_y += dy
        self._update_points()
    
    def is_include(self, other):
        if isinstance(other, Rectangle):
            rect_points = [
                [other.x, other.y],
                [other.x + other.width, other.y],
                [other.x + other.width, other.y + other.height],
                [other.x, other.y + other.height]
            ]
            for point in rect_points:
                if not self._point_in_pentagon(point):
                    return False
            return True
        elif isinstance(other, Pentagon):
            for point in other.points:
                if not self._point_in_pentagon(point):
                    return False
            return True
    
    def _point_in_pentagon(self, point):
        x, y = point
        inside = False
        n = len(self.points)
        
        p1x, p1y = self.points[0]
        for i in range(n + 1):
            p2x, p2y = self.points[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def __str__(self):
        return f"Pentagon(id={self.id}, center_x={self.center_x}, center_y={self.center_y}, radius={self.radius})"

def input_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число")

def main():
    shapes = {}
    
    while True:
        print("\nМеню:")
        print("1. Создать прямоугольник")
        print("2. Создать пятиугольник")
        print("3. Переместить фигуру")
        print("4. Проверить включение фигур")
        print("5. Показать все фигуры")
        print("6. Выйти")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            try:
                shape_id = input("Введите идентификатор прямоугольника: ")
                x = input_float("Введите координату x: ")
                y = input_float("Введите координату y: ")
                width = input_float("Введите ширину: ")
                height = input_float("Введите высоту: ")
                
                rect = Rectangle(shape_id, x, y, width, height)
                shapes[shape_id] = rect
                print(f"Создан: {rect}")
            except InvalidShapeParameterError as e:
                print(f"Ошибка: {e}")
        
        elif choice == "2":
            try:
                shape_id = input("Введите идентификатор пятиугольника: ")
                center_x = input_float("Введите координату x центра: ")
                center_y = input_float("Введите координату y центра: ")
                radius = input_float("Введите радиус: ")
                
                pentagon = Pentagon(shape_id, center_x, center_y, radius)
                shapes[shape_id] = pentagon
                print(f"Создан: {pentagon}")
            except InvalidShapeParameterError as e:
                print(f"Ошибка: {e}")
        
        elif choice == "3":
            if not shapes:
                print("Нет созданных фигур")
                continue
                
            shape_id = input("Введите идентификатор фигуры для перемещения: ")
            if shape_id not in shapes:
                print("Фигура не найдена")
                continue
                
            try:
                dx = input_float("Введите смещение по x: ")
                dy = input_float("Введите смещение по y: ")
                shapes[shape_id].move(dx, dy)
                print(f"Фигура {shape_id} перемещена. Новые параметры: {shapes[shape_id]}")
            except InvalidShapeParameterError as e:
                print(f"Ошибка перемещения: {e}")
        
        elif choice == "4":
            if len(shapes) < 2:
                print("Нужно создать хотя бы 2 фигуры")
                continue
                
            id1 = input("Введите идентификатор первой фигуры: ")
            id2 = input("Введите идентификатор второй фигуры: ")
            
            if id1 not in shapes or id2 not in shapes:
                print("Одна из фигур не найдена")
                continue
        
        elif choice == "5":
            if not shapes:
                print("Нет созданных фигур")
            else:
                print("\nСписок фигур:")
                for shape in shapes.values():
                    print(shape)
        
        elif choice == "6":
            print("Выход из программы")
            break
        
        else:
            print("Неверный выбор, попробуйте снова")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")