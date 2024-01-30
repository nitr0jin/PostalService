#Package class

class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.deliverytime = None
        self.departuretime = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zipcode, self.deadline, self.weight, self.address, self.status, self.deliverytime)
    
    def package_info(self):
        if self.status == "At the hub" or self.status == "On the way":
            return "Package ID: %s \t Status: %s \t Delivery Time: NOT DELIVERED" % (self.ID, self.status)
        else:
            return "Package ID: %s \t Status: %s \t Delivery Time: %s" % (self.ID, self.status, self.deliverytime)

    #Changes the package's status
    def status_update(self, time_timedelta):
        if self.deliverytime < time_timedelta:
            self.status = "Delivered"
        elif self.departuretime > time_timedelta:
            self.status = "On the way"
        else:
            self.status = "At the hub"