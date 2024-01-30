#Truck class

class Truck:
    def __init__(self, miles, packages, speed, capacity, departuretime, location):
        self.miles = miles
        self.packages = packages
        self.speed = speed
        self.capacity = capacity
        self.departuretime = departuretime
        self.location = location
        self.time = departuretime
    
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.miles, self.packages, self.speed, self.capacity, self.departuretime, self.location)
    