import math
from abc import ABC, abstractmethod

class Shape(ABC):
    """Абстрактные фундаментальные классы: отцы всех форм"""
    
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    def compare_area(self, other: 'Shape') -> str:
        if self.area() > other.area():
            return 'larger'
        elif self.area() < other.area():
            return 'smaller'
        else:
            return 'equal'
    
    def compare_perimeter(self, other: 'Shape') -> str:
        if self.perimeter() > other.perimeter():
            return 'larger'
        elif self.perimeter() < other.perimeter():
            return 'smaller'
        else:
            return 'equal'


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive.")
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Square(Rectangle):
    """Квадрат-это специальный прямоугольник"""
    def __init__(self, side: float):
        super().__init__(side, side)  
        self.side = side 


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Sides must be positive.")
        # Проверяем, соответствует ли треугольное неравенство
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Invalid triangle sides.")
        self.a, self.b, self.c = a, b, c
    
    def area(self) -> float:
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def perimeter(self) -> float:
        return self.a + self.b + self.c


class Circle(Shape):
    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("Radius must be positive.")
        self.radius = radius
    
    def area(self) -> float:
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


# ===== Пример использования =====
if __name__ == "__main__":
    rect = Rectangle(4, 5)
    sq = Square(4)
    tri = Triangle(3, 4, 5)
    circ = Circle(3)

    print("Rectangle area:", rect.area())          # 20
    print("Square perimeter:", sq.perimeter())     # 16
    print("Triangle area:", tri.area())            # 6.0
    print("Circle perimeter:", circ.perimeter())   # ~18.85

    print("\nComparisons:")
    print("Square vs Rectangle area:", sq.compare_area(rect))  # 'smaller'
    print("Circle vs Triangle perimeter:", circ.compare_perimeter(tri))  # 'larger'