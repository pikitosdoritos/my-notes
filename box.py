l = 4
b = 1
c = 3
class Box:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.color = "white"

    def calc_volume(self):
        return self.length * self.width * self.height
    
    def paint(self, color):
        self.color = color
    
    def __str__(self):
        return f"{self.color} box with lenght {self.length}, width {self.width}, and height {self.height}."
    
    
    
    

    
box = Box(length=l, width=b, height=c)
#print("\n", box.calc_volume())
#print(box)
#box.paint("orange")
#print(box)

import math


class Engine:

    def __init__(self, piston_radius, number_of_cylinders, wsh, rpm): #wsh -высота рабочего хода, rpm = revolution_per_minute
        self.refueling_volume = "59"
        self.mileage = "450"
        self.piston_radius = piston_radius
        self.number_of_cylinders = number_of_cylinders
        self.wsh = wsh
        self.rpm = rpm


    def fuel_consumption(self):
        return round((float(self.refueling_volume)/float(self.mileage))*100, 2)
    
    def engine_volume(self):
        return round((math.pi*(float(self.piston_radius)**2)*float(self.wsh)*float(self.number_of_cylinders))/1000, 2)
    
    def engine_nm(self):
        return round((float(1840900)*self.engine_volume())/(2*math.pi), 2) #1840900 -среднее давление в цилиндрах 
    
    def power_engine_kw(self):
        return round((self.engine_nm() *float(self.rpm))/9550, 2)
            
    def power_engine_hp(self):
        return  round(self.power_engine_kw()*1.3596, 2)
    
    def __str__(self):
        return f"\nОб'єм двигуна: {self.engine_volume()} л., \nОберальний момент: {self.engine_nm()} Нм., \nПотужність двигуна в кВт: {self.power_engine_kw()} кВт, \nПотужність двигуна в кінських силах: {self.power_engine_hp()} кс, \nВитрата палива: {self.fuel_consumption()} л., \nЗаправлений об'єм топлива: {self.refueling_volume} л., \nРадіус поршня: {self.piston_radius} мм., \nКількість циліндрів: {self.number_of_cylinders}, \nВисота робочого ходу: {self.wsh} мм., \nМаксимальна кількість обертів на хвилну: {self.rpm} об/хв."
    
engine = Engine(piston_radius=49, number_of_cylinders=8, wsh=90.5, rpm=5550)
print(engine)