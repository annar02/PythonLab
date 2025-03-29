# Вариант 5. Rectangle, Pentagon, move, is_include 
import math

# Oбщие свойства и методы для всех фигур
class Shape:
    def __init__(self, shape_id):
        self.id = shape_id
    
    def move(self, dx, dy):
        for point in self.points:
            point[0] += dx
            point[1] += dy
    
    def is_include(self, other):
        pass

# Класс Rectangle (прямоугольник)
class Rectangle(Shape):
    def __init__(self, shape_id, x, y, width, height):
        super().__init__(shape_id)
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


rect1 = Rectangle("rect1", 0, 0, 10, 10)
rect2 = Rectangle("rect2", 2, 2, 4, 4)
pentagon1 = Pentagon("pent1", 5, 5, 3)
pentagon2 = Pentagon("pent2", 15, 15, 2)

print("Фигуры созданы:")
print(rect1)
print(rect2)
print(pentagon1)
print(pentagon2)

print("\nПроверка включения:")
print(f"rect1 включает rect2: {rect1.is_include(rect2)}")
print(f"rect1 включает pentagon1: {rect1.is_include(pentagon1)}")
print(f"pentagon1 включает rect2: {pentagon1.is_include(rect2)}")

print("\nПеремещаем rect2 на (5, 5):")
rect2.move(5, 5)
print(rect2)
print(f"rect1 включает rect2 после перемещения: {rect1.is_include(rect2)}")

print("\nПеремещаем pentagon1 на (1, 1):")
pentagon1.move(1, 1)
print(pentagon1)