# Jin Hee Choe
# 011249069
# WGUPS

import csv
import datetime
import Truck
from Packages import Package
from createHash import createHash

#Reading the csv files for address, distance, and package information
with open("csv/addresses.csv") as address:
    addressCSV = csv.reader(address)
    addressCSV = list(addressCSV)

with open("csv/distances.csv") as distance:
    distanceCSV = csv.reader(distance)
    distanceCSV = list(distanceCSV)

with open("csv/package.csv") as package:
    packagesCSV = csv.reader(package)
    packagesCSV = list(packagesCSV)

#Creating and loading package objects from the package CSV file and placing them into a hash table
def load_packages(filename, packageHash):
    with open(filename) as packageInfo:
        packageInfo = csv.reader(packageInfo)
        for package in packageInfo:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipCode = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pStatus = "At the hub"

            p = Package(pID, pAddress, pCity, pState, pZipCode, pDeadline, pWeight, pStatus)
        
            packageHash.insert(pID, p)

#Locates the distances between two address using the distance CSV file 
def distance_between(address1, address2):
    distance = distanceCSV[address1][address2]
    if distance == '':
        distance = distanceCSV[address2][address1]

    return float(distance)

#Extracts the address number from the address CSV file
def address(address):
    for row in addressCSV:
        if address in row[2]:
            return int(row[0])
        
#Loading the truck objects
truck1 =Truck.Truck(0.0, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 18, 16, datetime.timedelta(hours=8), "4001 South 700 East")
truck2 = Truck.Truck(0.0,[2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 18, 25, 28, 32, 36, 38], 18, 16, datetime.timedelta(hours=9, minutes=5), "4001 South 700 East")
truck3 = Truck.Truck(0.0, [9, 17, 19, 21, 22, 23, 24, 26, 27, 33, 35, 39], 18, 16, datetime.timedelta(hours=10, minutes=30), "4001 South 700 East")

#Creating the package hash table
packageHash = createHash()

#Loading the packages into the hash table
load_packages("csv/package.csv", packageHash)

#Method for delivering packages that utlizes the nearest neighbor algorithm
def package_delivery(truck):

    #Creating an array and populating it with the packages that have not been delivered.
    notDelivered = []
    for packageID in truck.packages:
        package = packageHash.search(packageID)
        notDelivered.append(package)

    #Clearing the packages within the truck to rearrange it from closest to farthest
    truck.packages.clear()

    #"Delivers" the packages one by one until there is none and appends the package list 
    while len(notDelivered) > 0:
        nextAddress = 2000
        nextPackage = None 
        for package in notDelivered:
            if distance_between(address(truck.location), address(package.address)) <= nextAddress:
                nextAddress = distance_between(address(truck.location), address(package.address))
                nextPackage = package
    
        #Adds the next package to the package list
        truck.packages.append(nextPackage.ID)

        #Removes the package from the not delivered list
        notDelivered.remove(nextPackage)

        #Adds the milege from the package delivery to the mile count
        truck.miles += nextAddress

        #Updates the address to the next package's address. "Driving to the next address"
        truck.location = nextPackage.address

        #Updates the time for the truck to "drive"
        truck.time += datetime.timedelta(hours=nextAddress / 18)
        nextPackage.deliverytime = truck.time
        nextPackage.departuretime = truck.departuretime

#Truck 1 going out for delivery
package_delivery(truck1)

#Truck 2 going out for delivery
package_delivery(truck2)

#Ensuring that truck 3 does not leave before one of the truck drivers returns
truck3.departuretime = min(truck1.time, truck2.time)

#Truck 3 is out for delivery
package_delivery(truck3)

#Creating the user interface in the Main class

class Main:
    print("======================================")
    print("\tWelcome to WGUPS!")

    #Takes the user input for their desired action
    userAction = input("What would you like to do? (package status, truck mileage, or quit) ")

    #While loop to go through all the user's actions until they decide to quit
    while userAction.lower() != "quit":

        
        if userAction.lower() == "package status":
            userTime = input("Please enter the time: ")
            (h,m) = userTime.split(":")
            packageTime = datetime.timedelta(hours=int(h), minutes=int(m))
            userSelection = input("Would you like to see one or all packages? ")
            if userSelection.lower() == "one":
                userPackage = input("Please enter the package ID : ")
                package = packageHash.search(int(userPackage))
                package.status_update(packageTime)
                print(package.package_info())
                userAction = input("Is there anything else you would like to do?(package status, truck mileage, or quit) ")
            elif userSelection.lower() == "all":
                for packageID in range(1, 41):
                    package = packageHash.search(packageID)
                    package.status_update(packageTime)
                    print(package.package_info())
                userAction = input("Is there anything else you would like to do?(package status, truck mileage, or quit) ")
            else:
                print("Error: Invalid entry")
                userAction = input("What would you like to do? (package status, truck mileage, or quit) ")
        

        elif userAction.lower() == "truck mileage":
            totalMileage = (round(truck1.miles + truck2.miles + truck3.miles))
            print(f"The trucks travelled a total of {totalMileage} miles. ")
            userAction = input("What would you like to do? (package status or quit) ")
        
        else:
            print("Error! Invalid entry")
            userAction = input("What would you like to do? (package status, truck mileage, or quit) ")
    
    print("Thank you for using WGUPS!")
        
    

