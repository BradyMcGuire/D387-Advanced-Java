# Brady McGuire
# Student ID: 010867947
# Data Structures and Algorithms II - C950

import csv
import datetime
from modulefinder import packagePathMap

#------------------DEFINING A PACKAGE------------------#

class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, deliveryStatus, arrivalTime, deliveryTime):
        self.id = int(id)
        self.address = address
        self.city = city
        self.state = state
        self.zip = int(zip)
        self.deadline = deadline
        self.weight = weight
        self.deliveryStatus = deliveryStatus
        self.arrivalTime = arrivalTime
        self.deliveryTime = deliveryTime

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.id, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.deliveryStatus, self.arrivalTime, self.deliveryTime)

    def updateStatus(self, id, updatedStatus):
        packages[id - 1].deliveryStatus = updatedStatus

    def updateAddress(self, id, updatedAddress):
        packages[id - 1].address = updatedAddress


#------------------CREATING PACKAGE OBJECTS------------------#

packages = []

with open('WGUPS_Package_File.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    for row in csv_reader:
        package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], "HUB", "8:00:00", "N/A")
        if (row[7] != "Delayed on flight---will not arrive to depot until 9:05 am"):
            pass
        else:
            package.deliveryStatus = "DELAYED"
            package.arrivalTime = "N/A Currently Delayed"
        packages.append(package)
            

#------------------DEFINING AND CREATING THE HASH TABLE------------------#

class HashTable:
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
      
    # Inserts a new item into the hash table.
    def insert(self, key, item): #  does both insert and update 
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
 
        # update key if it is already in the bucket
        for kv in bucket_list:
          if kv[0] == key:
            kv[1] = item
            return True
        
        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True
 
    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
 
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #print(bucket_list)
 
        # search for the key in the bucket list
        for kv in bucket_list:
          #print (key_value)
          if kv[0] == key:
            return kv[1] # value
        return None

    # Removes an item with matching key from the hash table.
    
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
 
        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
          if kv[0] == key:
              bucket_list.remove([kv[0],kv[1]])


#------------------DEFINING A DISTANCE ARRAY USING THE INFORMATION FROM "WGUPS Distance Table.xlsx"-------------------#
 
distanceArray = [[0.0],
                 [7.2,0.0],
                 [3.8,7.1,0.0],
                 [11.0,6.4,9.2,0.0],
                 [2.2,6.0,4.4,5.6,0.0],
                 [3.5,4.8,2.8,6.9,1.9,0.0],
                 [10.9,1.6,8.6,8.6,7.9,6.3,0.0],
                 [8.6,2.8,6.3,4.0,5.1,4.3,4.0,0.0],
                 [7.6,4.8,5.3,11.1,7.5,4.5,4.2,7.7,0.0],
                 [2.8,6.3,1.6,7.3,2.6,1.5,8.0,9.3,4.8,0.0],
                 [6.4,7.3,10.4,1.0,6.5,8.7,8.6,4.6,11.9,9.4,0.0],
                 [3.2,5.3,3.0,6.4,1.5,0.8,6.9,4.8,4.7,1.1,7.3,0.0],
                 [7.6,4.8,5.3,11.1,7.5,4.5,4.2,7.7,0.6,5.1,12.0,4.7,0.0],
                 [5.2,3.0,6.5,3.9,3.2,3.9,4.2,1.6,7.6,4.6,4.9,3.5,7.3,0.0],
                 [4.4,4.6,5.6,4.3,2.4,3.0,8.0,3.3,7.8,3.7,5.2,2.6,7.8,1.3,0.0],
                 [3.7,4.5,5.8,4.4,2.7,3.8,5.8,3.4,6.6,4.0,5.4,2.9,6.6,1.5,0.6,0.0],
                 [7.6,7.4,5.7,7.2,1.4,5.7,7.2,3.1,7.2,6.7,8.1,6.3,7.2,4.0,6.4,5.6,0.0],
                 [2.0,6.0,4.1,5.3,0.5,1.9,7.7,5.1,5.9,2.3,6.2,1.2,5.9,3.2,2.4,1.6,7.1,0.0],
                 [3.6,5.0,3.6,6.0,1.7,1.1,6.6,4.6,5.4,1.8,6.9,1.0,5.4,3.0,2.2,1.7,6.1,1.6,0.0],
                 [6.5,4.8,4.3,10.6,6.5,3.5,3.2,6.7,1.0,4.1,11.5,3.7,1.0,6.9,6.8,6.4,7.2,4.9,4.4,0.0],
                 [1.9,9.5,3.3,5.9,3.2,4.9,11.2,8.1,8.5,3.8,6.9,4.1,8.5,6.2,5.3,4.9,10.6,3.0,4.6,7.5,0.0],
                 [3.4,10.9,5.0,7.4,5.2,6.9,12.7,10.4,10.3,5.8,8.3,6.2,10.3,8.2,7.4,6.9,12.0,5.0,6.6,9.3,2.0,0.0],
                 [2.4,8.3,6.1,4.7,2.5,4.2,10.0,7.8,7.8,4.3,4.1,3.4,7.8,5.5,4.6,4.2,9.4,2.3,3.9,6.8,2.9,4.4,0.0],
                 [6.4,6.9,9.7,0.6,6.0,9.0,8.2,4.2,11.5,7.8,0.4,6.9,11.5,4.4,4.8,5.6,7.5,5.5,6.5,11.4,6.4,7.9,4.5,0.0],
                 [2.4,10.0,6.1,6.4,4.2,5.9,11.7,9.5,9.5,4.8,4.9,5.2,9.5,7.2,6.3,5.9,11.1,4.0,5.6,8.5,2.8,3.4,1.7,5.4,0.0],
                 [5.0,4.4,2.8,10.1,5.4,3.5,5.1,6.2,2.8,3.2,11.0,3.7,2.8,6.4,6.5,5.7,6.2,5.1,4.3,1.8,6.0,7.9,6.8,10.6,7.0,0.0],
                 [3.6,13.0,7.4,10.1,5.5,7.2,14.2,10.7,14.1,6.0,6.8,6.4,14.1,10.5,8.8,8.4,13.6,5.2,6.9,13.1,4.1,4.7,3.1,7.8,1.3,8.3,0.0],
                 ]


#------------------DEFINING AN ADDRESS & DISTANCE LOOKUP USING DATA FROM THE DISTANCE ARRAY------------------#
def addressLookup(address):
    if (address == "4001 South 700 East"):
        return 0
    elif (address == "1060 Dalton Ave S"):
        return 1
    elif (address == "1330 2100 S"):
        return 2
    elif (address == "1488 4800 S"):
        return 3
    elif (address == "177 W Price Ave"):
        return 4
    elif (address == "195 W Oakland Ave"):
        return 5
    elif (address == "2010 W 500 S"):
        return 6
    elif (address == "2300 Parkway Blvd"):
        return 7
    elif (address == "233 Canyon Rd"):
        return 8
    elif (address == "2530 S 500 E"):
        return 9
    elif (address == "2600 Taylorsville Blvd"):
        return 10
    elif (address == "2835 Main St"):
        return 11
    elif (address == "300 State St"):
        return 12
    elif (address == "3060 Lester St"):
        return 13
    elif (address == "3148 S 1100 W"):
        return 14
    elif (address == "3365 S 900 W"):
        return 15
    elif (address == "3575 W Valley Central Station bus Loop"):
        return 16
    elif (address == "3595 Main St"):
        return 17
    elif (address == "380 W 2880 S"):
        return 18
    elif (address == "410 S State St"):
        return 19
    elif (address == "4300 S 1300 E"):
        return 20
    elif (address == "4580 S 2300 E"):
        return 21
    elif (address == "5025 State St"):
        return 22
    elif (address == "5100 South 2700 West"):
        return 23
    elif (address == "5383 S 900 East #104") or (address == "5383 South 900 East #104"):
        return 24
    elif (address == "600 E 900 South"):
        return 25
    elif (address == "6351 South 900 East"):
        return 26

def distanceLookup(sourceAdd, destinationAdd):
    row = addressLookup(sourceAdd)
    column = addressLookup(destinationAdd)
    if (column > row):
        lookup = distanceArray[(column)] [(row)]
    else:
        lookup = distanceArray[(row)] [(column)]
    return lookup

#------------------DEFINING THE TRUCK------------------#

class Truck:
    def __init__(self, location):
        self.load = []
        self.location = location
        self.loadAmount = 0

    def __str__(self):
            return "%s, %s" %  (self.load, self.location)

    def addLoad(self, package):
        # Add an item to the list attribute
        if (self.loadAmount <= 16):
            self.loadAmount = self.loadAmount + 1
            self.load.append(package)
        else:
            print("Truck is at full capacity")

    def packageDetail(self, id):
        return self.load[id-1]

    def deliveredPackage(self, deliveredPackage):
        self.load.remove(deliveredPackage)
        self.loadAmount = self.loadAmount - 1

#------------------MAIN PROCESSING AND ALGORITHM AREA------------------#

#Needed Variables
totalMiles = 0
# Hash table creation
hashTable = HashTable()

# Filling the Hash Table
for package in packages:
    hashTable.insert(package.id, package)

def timeManaged(time, miles, id):
    delayedArrival = datetime.timedelta(hours=9,minutes=5,seconds=0) # (At 9:05AM the delayed packages arrive at the hub)
    packageCorrection = datetime.timedelta(hours=10,minutes=20,seconds=0) # (At 10:20AM the delayed packages arrive at the hub)
    #capture1 = datetime.timedelta(hours=8,minutes=59,seconds=40)
    #capture2 = datetime.timedelta(hours=10,minutes=2,seconds=0)
    #capture3 = datetime.timedelta(hours=11,minutes=47,seconds=20)
    if time > delayedArrival:
        for i in range(1,41):
            val = hashTable.search(i).arrivalTime
            if val == "N/A Currently Delayed":
                hashTable.search(i).arrivalTime = str(delayedArrival)
            else:
                pass
    if time > packageCorrection:
        hashTable.search(9).address = "410 S State St"
        hashTable.search(9).zip = 84111
    else:
        pass
    timeFloat = miles / 18.0
    addTime = datetime.timedelta(hours = timeFloat)
    time = time + addTime
    if id != None: #marking packages for there delivery time
        hashTable.search(id).deliveryTime = str(time)
        hashTable.search(id).deliveryStatus = "Delivered"
    else: #only when returning to hub
        pass
    # THIS AREA OF CODE IS FOR THE CAPTURE OF SECTION D - 1,2,3
    #if time == capture1:
    #    print("\nstatus of all packages loaded onto each truck at a time between 8:35 a.m. and 9:25 a.m\n")
    #    print("current time captured:",time, "\n")
    #    print("\n" " ID ", "|", "ADDRESS", "|", "CITY", "|", "STATE", "|", "ZIP", "|", "DEADLINE", "|", "WEIGHT", "|", "STATUS", "|", "ARRIVAL TIME", "|", "DELIVERY TIME")
    #    timeCapture()
    #else:
    #    pass
    #if time == capture2:
    #    print("\nstatus of all packages loaded onto each truck at a time between 9:35 a.m. and 10:25 a.m\n")
    #    print("current time captured:",time, "\n")
    #    print("\n" " ID ", "|", "ADDRESS", "|", "CITY", "|", "STATE", "|", "ZIP", "|", "DEADLINE", "|", "WEIGHT", "|", "STATUS", "|", "ARRIVAL TIME", "|", "DELIVERY TIME")
    #    timeCapture()
    #else:
    #    pass
    #if time > capture3:
    #    print("\nstatus of all packages loaded onto each truck at a time between 12:03 p.m. and 1:12 p.m\n")
    #    print("current time captured:",time, "\n")
    #    print("\n" " ID ", "|", "ADDRESS", "|", "CITY", "|", "STATE", "|", "ZIP", "|", "DEADLINE", "|", "WEIGHT", "|", "STATUS", "|", "ARRIVAL TIME", "|", "DELIVERY TIME")
    #    timeCapture()
    #else:
    #    pass
    return time

def timeCapture():
    for i in range(1,41):
        print(hashTable.search(i))

# Truck creation 3x
truck1 = Truck("4001 South 700 East")
truck2 = Truck("4001 South 700 East")
truck3 = Truck("4001 South 700 East")

# Loading the Trucks

#---------TRUCK 1 Load---------# LEAVES AT 8:00
truck1.addLoad(hashTable.search(1))
truck1.addLoad(hashTable.search(2))
truck1.addLoad(hashTable.search(4))
truck1.addLoad(hashTable.search(5))
truck1.addLoad(hashTable.search(13))
truck1.addLoad(hashTable.search(14))
truck1.addLoad(hashTable.search(15))
truck1.addLoad(hashTable.search(16))
truck1.addLoad(hashTable.search(19))
truck1.addLoad(hashTable.search(20))
truck1.addLoad(hashTable.search(29))
truck1.addLoad(hashTable.search(30))
truck1.addLoad(hashTable.search(31))
truck1.addLoad(hashTable.search(34))
truck1.addLoad(hashTable.search(37))
truck1.addLoad(hashTable.search(40))

#---------TRUCK 2 Load---------# LEAVES AT 9:05
truck2.addLoad(hashTable.search(3))
truck2.addLoad(hashTable.search(6))
truck2.addLoad(hashTable.search(7))
truck2.addLoad(hashTable.search(8))
truck2.addLoad(hashTable.search(11))
truck2.addLoad(hashTable.search(17))
truck2.addLoad(hashTable.search(18))
truck2.addLoad(hashTable.search(22))
truck2.addLoad(hashTable.search(23))
truck2.addLoad(hashTable.search(25))
truck2.addLoad(hashTable.search(26))
truck2.addLoad(hashTable.search(28))
truck2.addLoad(hashTable.search(32))
truck2.addLoad(hashTable.search(33))
truck2.addLoad(hashTable.search(36))
truck2.addLoad(hashTable.search(38))



#---------TRUCK 3 Load---------# LEAVES WHEN TRUCK 1 RETURNS
truck3.addLoad(hashTable.search(9))
truck3.addLoad(hashTable.search(10))
truck3.addLoad(hashTable.search(12))
truck3.addLoad(hashTable.search(21))
truck3.addLoad(hashTable.search(24))
truck3.addLoad(hashTable.search(27))
truck3.addLoad(hashTable.search(35))
truck3.addLoad(hashTable.search(39))


#---------ALGORITHM (TRUCK-1)---------#
truck1Time = datetime.timedelta(hours=8,minutes=0,seconds=0) # Time Creation https://docs.python.org/3/library/datetime.html#module-datetime
#print("Truck 1 Depature Time: ", truck1Time)
hashTable.search(1).deliveryStatus = "En route"
hashTable.search(2).deliveryStatus = "En route"
hashTable.search(4).deliveryStatus = "En route"
hashTable.search(5).deliveryStatus = "En route"
hashTable.search(13).deliveryStatus = "En route"
hashTable.search(14).deliveryStatus = "En route"
hashTable.search(15).deliveryStatus = "En route"
hashTable.search(16).deliveryStatus = "En route"
hashTable.search(19).deliveryStatus = "En route"
hashTable.search(20).deliveryStatus = "En route"
hashTable.search(29).deliveryStatus = "En route"
hashTable.search(30).deliveryStatus = "En route"
hashTable.search(31).deliveryStatus = "En route"
hashTable.search(34).deliveryStatus = "En route"
hashTable.search(37).deliveryStatus = "En route"
hashTable.search(40).deliveryStatus = "En route" # updating packages that are loaded on the first truck to "en route" as the first truck has taken off.
while truck1.loadAmount != 0:
    miles = 50.0 # USED IN DETERMINING THE CLOSEST PACKAGE, IT MUST BE RESET EVERYTIME THE ALORITHM IS CALLED
    minPackage = "" # USED IN DETERMINING THE CLOSEST PACKAGE, IT MUST BE RESET EVERYTIME THE ALORITHM IS CALLED
    for i in range(1, truck1.loadAmount+1):
        pack = truck1.packageDetail(i)
        val = distanceLookup(truck1.location,pack.address)       # DISTANCE LOOKUP
        if val <= miles: #TAKES THE VALUE OF DISTANCE LOOKUP AND CHECKS IT AGAINST MILES, MILES COULD BE A LOWER NUMBER AFTER RUNNING THROUGH THE ALGORITHM A FEW TIMES
            miles = val #MILES NEEDS TO BE SET TO THE LOWEST PACKAGE SO FAR IN THE ALGORITHM
            minPackage = pack #minPackage NEEDS TO BE SET TO THE PACKAGE THAT IS THE LOWEST DISTANCE
        else:
            continue
    truck1.location = minPackage.address
    truck1.deliveredPackage(minPackage)
    totalMiles = totalMiles + miles
    truck1Time = timeManaged(truck1Time,miles,minPackage.id)
    #print("Package Delivered:", minPackage.id, "|", "Mile Amount From Previous Stop:", miles, "|", "Total Miles:", totalMiles, "|", "Current Truck Location:", truck1.location, "|", "Time Stamp:", truck1Time) # TESTING PURPOSE ONLY

#---------TRUCK 1 RETURN TO HUB---------#
hubReturnMiles = distanceLookup(truck1.location,"4001 South 700 East")
truck1.location = "4001 South 700 East"
totalMiles = totalMiles + hubReturnMiles
truck1Time = timeManaged(truck1Time,hubReturnMiles,None) 
#print("\nTruck returned to Hub","|", "Miles to Return to Hub:", hubReturnMiles, "|", "Total Miles:", round(totalMiles,2), "|", "Current Truck Location:", truck1.location, "|", "Time Stamp:", truck1Time)
#print("Truck 1 Complete \n") # TESTING PURPOSE ONLY

#---------ALGORITHM (TRUCK-2)---------#
truck2Time = datetime.timedelta(hours=9,minutes=5) # Time Creation https://docs.python.org/3/library/datetime.html#module-datetime
#print("Truck 2 Depature Time: ", truck2Time)
hashTable.search(3).deliveryStatus = "En route"
hashTable.search(6).deliveryStatus = "En route"
hashTable.search(7).deliveryStatus = "En route"
hashTable.search(8).deliveryStatus = "En route"
hashTable.search(11).deliveryStatus = "En route"
hashTable.search(17).deliveryStatus = "En route"
hashTable.search(18).deliveryStatus = "En route"
hashTable.search(22).deliveryStatus = "En route"
hashTable.search(23).deliveryStatus = "En route"
hashTable.search(25).deliveryStatus = "En route"
hashTable.search(26).deliveryStatus = "En route"
hashTable.search(28).deliveryStatus = "En route"
hashTable.search(32).deliveryStatus = "En route"
hashTable.search(33).deliveryStatus = "En route"
hashTable.search(36).deliveryStatus = "En route"
hashTable.search(38).deliveryStatus = "En route" # updating packages that are loaded on the second truck to "en route" as the first truck has taken off.
while truck2.loadAmount != 0:
    miles = 50.0
    minPackage = ""
    for i in range(1, truck2.loadAmount+1):
        pack = truck2.packageDetail(i)
        val = distanceLookup(truck2.location,pack.address)
        if val <= miles:
            miles = val
            minPackage = pack
        else:
            continue
    truck2.location = minPackage.address
    truck2.deliveredPackage(minPackage)
    totalMiles = totalMiles + miles
    truck2Time = timeManaged(truck2Time,miles,minPackage.id)
    #print("Package Delivered:", minPackage.id, "|", "Mile Amount From Previous Stop:", miles, "|", "Total Miles:", totalMiles, "|", "Current Truck Location:", truck2.location, "|", "Time Stamp:", truck2Time) # TESTING PURPOSE ONLY

#---------TRUCK 2 RETURN TO HUB---------#
hubReturnMiles = distanceLookup(truck2.location,"4001 South 700 East")
truck2.location = "4001 South 700 East"
totalMiles = totalMiles + hubReturnMiles
truck2Time = timeManaged(truck2Time,hubReturnMiles,None)
#print("\nTruck returned to Hub","|", "Miles to Return to Hub:", hubReturnMiles, "|", "Total Miles:", round(totalMiles,2), "|", "Current Truck Location:", truck2.location, "|", "Time Stamp:", truck2Time)
#print("Truck 2 Complete \n") # TESTING PURPOSE ONLY

#---------ALGORITHM (TRUCK-3)---------#
truck3Time = datetime.timedelta(seconds=truck1Time.seconds) # Time Creation https://docs.python.org/3/library/datetime.html#module-datetime
#print("Truck 3 Depature Time: ", truck3Time)
hashTable.search(9).deliveryStatus = "En route"
hashTable.search(10).deliveryStatus = "En route"
hashTable.search(12).deliveryStatus = "En route"
hashTable.search(21).deliveryStatus = "En route"
hashTable.search(24).deliveryStatus = "En route"
hashTable.search(27).deliveryStatus = "En route"
hashTable.search(35).deliveryStatus = "En route"
hashTable.search(39).deliveryStatus = "En route" # updating packages that are loaded on the third truck to "en route" as the first truck has taken off.
while truck3.loadAmount != 0:
    miles = 50.0
    minPackage = ""
    for i in range(1, truck3.loadAmount+1):
        pack = truck3.packageDetail(i)
        val = distanceLookup(truck3.location,pack.address)
        if val <= miles:
            miles = val
            minPackage = pack
        else:
            continue
    truck3.location = minPackage.address
    truck3.deliveredPackage(minPackage)
    totalMiles = totalMiles + miles
    truck3Time = timeManaged(truck3Time,miles,minPackage.id)
    #print("Package Delivered:", minPackage.id, "|", "Mile Amount From Previous Stop:", miles, "|", "Total Miles:", totalMiles, "|", "Current Truck Location:", truck3.location, "|", "Time Stamp:", truck3Time) # TESTING PURPOSE ONLY

#---------TRUCK 3 RETURN TO HUB---------#
hubReturnMiles = distanceLookup(truck3.location,"4001 South 700 East")
truck3.location = "4001 South 700 East"
totalMiles = totalMiles + hubReturnMiles
truck3Time = timeManaged(truck3Time,hubReturnMiles,None)
#print("\nTruck returned to Hub","|", "Miles to Return to Hub:", hubReturnMiles, "|", "Total Miles:", round(totalMiles,2), "|", "Current Truck Location:", truck3.location, "|", "Time Stamp:", truck3Time)
#print("Truck 3 Complete \n") # TESTING PURPOSE ONLY


#Capture 3
#captureTime = datetime.timedelta(hours=12,minutes=3)
#timeManaged(captureTime,miles,minPackage.id)

def inputTime(inputTime, id):
    packID = hashTable.search(id).id
    packDelTime = datetime.datetime.strptime(hashTable.search(id).deliveryTime,"%H:%M:%S")
    deliveryTime = datetime.timedelta(hours = packDelTime.hour,minutes=packDelTime.minute,seconds=packDelTime.second)
    packArivTime = datetime.datetime.strptime(hashTable.search(id).arrivalTime,"%H:%M:%S")
    arrivalTime = datetime.timedelta(hours = packArivTime.hour,minutes=packArivTime.minute,seconds=packArivTime.second)
    pack9Change = datetime.timedelta(hours = 10,minutes=20,seconds=0)
    if inputTime > arrivalTime and inputTime > deliveryTime:
        hashTable.search(id).deliveryStatus = "Delivered"
    elif inputTime > arrivalTime and inputTime < deliveryTime:
        hashTable.search(id).deliveryStatus = "En Route"
    else:
        if packID != 6 and 25 and 28 and 32:
            hashTable.search(id).deliveryStatus = "Hub"
        else:
            hashTable.search(id).deliveryStatus = "Delayed"
    if packID == 9:
         if inputTime < pack9Change:
             hashTable.search(id).address = "300 State St"
             hashTable.search(id).zip = 84103
         else:
              hashTable.search(id).address = "410 S State St"
              hashTable.search(id).zip = 84111
         if inputTime > arrivalTime and inputTime > deliveryTime:
            hashTable.search(id).deliveryStatus = "Delivered"
         elif inputTime > arrivalTime and inputTime < deliveryTime:
            hashTable.search(id).deliveryStatus = "En Route"
         else:
            hashTable.search(id).deliveryStatus = "Hub"
    print("\n",hashTable.search(id),"\n")
    userInterface()


#---------USER INTERFACE---------#
def userInterface():
    print(" ********************************** \n 1. Print The Status of All Packages and Total Miles \n 2. Print a Status of a Single Package \n 3. Pick a Package and Time \n 4. Quit \n **********************************")
    inp = int(input(" What Would You Like To Do? : "))
    if inp == 1:
        print("\n" " ID ", "|", "ADDRESS", "|", "CITY", "|", "STATE", "|", "ZIP", "|", "DEADLINE", "|", "WEIGHT", "|", "STATUS", "|", "ARRIVAL TIME", "|", "DELIVERY TIME")
        for package in packages:
           print("\n",hashTable.search(package.id))
        print("\n") # Cosmetic
        print(" Total Miles: ", round(totalMiles,2))
        print("\n") # Cosmetic
        userInterface()
    elif inp == 2:
        inp2 = int(input("\n What Package Would You Like To see? : "))
        print("\n" " ID ", "|", "ADDRESS", "|", "CITY", "|", "STATE", "|", "ZIP", "|", "DEADLINE", "|", "WEIGHT", "|", "STATUS", "|", "ARRIVAL TIME", "|", "DELIVERY TIME", "\n")
        print("",hashTable.search(inp2))
        print("\n") # Cosmetic
        userInterface()
    elif inp == 3:
        specPackage = int(input("\n What Package Would You Like To see? : "))
        hTime = int(input("\n What Hour? : "))
        mTime = int(input("\n What Minute(s)? : "))
        sTime = int(input("\n What Second(s)? : "))
        specTime = datetime.timedelta(hours = hTime,minutes=mTime,seconds=sTime)
        inputTime(specTime, specPackage)
    elif inp == 4:
        print("\nTHANK YOU, PROGRAM FINSIHED")
    else:
        print("\nThat number is out of range, please try again \n")
        userInterface()

#------INTERFACE START------#
userInterface()

#------PROJECT WRITTEN REQUIREMENTS (TASK 2)------#
# F.1
#THE ALOGRITHM TO DETERMINE THE 3 TRUCKS IS THE NEAREST NEIGHBOR ALGORITHM:
#ONE SRENGTH OF THIS ALOGRITHM IS THAT IT WILL ALWAYS CHURN OUT THE LOWEST POSSIBLE NEXT PACKAGE TO HELP KEEP THE MILES LOW.
#THE SECOND STRENGTH OF THIS ALGORITHM IS THE SCALABILITY. THIS ALGORTIHM CAN TAKE IN ANY NUMBER OF PACKAGES AND DETERMINE THE LOWEST VALUE. HOWEVER DUE TO RESTRICTIONS IN THE PROJECT, THIS ONE'S MAX IS 16.

# F.3
# TWO OTHER ALOGRITHMS THAT COULD BE USED, ARE LINEAR SEARCH AND A BINARY TREE
# HOW THESE DIFFER ARE IN MANY WAYS. LINEAR SEARCH IS GOING TO REQUIRE GOING THROUGH EVERY SINGLE PACKAGE ONE BY ONE, EVERYTIME YOU TRIED TO SEARCH FOR IT, WHICH WOULD BE SLOWER THAN A HASH TABLE. BINARY TREE COULD BE DONE A COUPLE OF WAYS, HYPOTHETICALLY YOU (CONT.)
# (CONT.) COULD MAKE THE ROOT THE HUB AND THEN TRICKLE DOWN THE TREE THE ADDRESS THAT WERE CLOSER (SOMETHING SIMILAR TO NEAREST NEIGHBOR), HOWEVER I BELIEVE A BINARY TREE, IN THIS SENARIO, (CONT.)
# (CONT.) GOING TO REQUIRE A LOT OF WORK AROUNDS TO GET WORKING CORRECTLY. BOTH OF THESE ALGORITHMS COULD WORK FOR ALL REQUIREMENTS, THEY WOULD ALL REQUIRE DIFFERENT LENGTHS AND WORKAROUNDS IN CODE.

# G
# THERE ARE A FEW THINGS I WOULD DO DIFFERENTLY, FIRSLY, I WOULD NOT ACTUALLY LOAD THE WHOLE PACKAGE OBJECT INTO THE TRUCK, I WOULD LOAD JUST THE PACKAGE ID, THIS CAUSED SOME HEADACHES IN THE CODE THAT HAD SOME KINKS I HAD (CONT.)
# (CONT.) TO WORK AROUND. I WOULD ALSO PROBALY OPTIMIZE MORE AND FUTURE PROOF THE CODE. THE CODE ITSELF WORKS AND RELATIVELY QUICK, HOWEVER NOT UNDERSTAND THE PROJECT TO ITS FULL AT THE BEGINNING, THERE IS SOME OPTIMIZATION AND (CONT.)
# (CONT.) FUTURE CODE THAT WOULD HAVE BEEN BENEFICIAL.

# H.1
# YOU COULD USE A TRADIONAL DICTIONARY, AND YOU COULD ALSO USE A TRADITIONAL ARRAY.
# H.1.A
# A TRADITIONAL DICTIONARY IS NOT MUCH DIFFERENT THAN THE HASH TABLE WE USED. HOWEVER THE WAY WE DID THE HASH TABLE, WE ARE ABLE TO MANIPULATE IT. USING A STANDARD DICTIONARY WOULD HAVE LEFT THE "UNDER THE HOOD" CODE UP TO PYTHON (CONT.T)
# (CONT.) AND THE TRANSLATOR. AN ARRAY WOULD NOT HAVE RETURNED THE VALUE FROM USING A KEY, INSTEAD IN THE CODE I WOULD HAVE HAD TO DIRECTLY ASK FOR THE OBJECT IN THE ARRAY INSTEAD OF USING A KEY TO FIND IT AND RETURN THE VALUE.

# I
# ANY SOURCES WERE ADDING AS A COMMENT IN THE LINE OF CODE, I BELIEVE THERE WAS ONLY ONE WHICH WAS FOR DATETIME.TIMEDELTA. THE REST WAS CONFIGURED ORIGINALLY, HELP WITH A COURSE INSTRUCTOR, AND ZYBOOKS