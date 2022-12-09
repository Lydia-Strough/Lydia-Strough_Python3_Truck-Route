import HashTable
import Truck
import readCSV
import datetime


def distance_in_between(add1, add2, addressData, distanceData):
    distance = 0
    h = addressData.index(add1)
    j = addressData.index(add2)
    if distanceData[h][j] == '':
        distance = distanceData[j][h]
    else:
        distance = distanceData[h][j]
    return float(distance)


def min_distance_from(currAddress, packageList, pHashTable, addressData, distanceData):
    minDistance = 1000
    nextAddress = ''
    nextId = 0
    print('Determining Closest Address!')
    for pkgId in packageList:
        pkg = pHashTable.search(pkgId)
        address2 = pkg.address
        distance = distance_in_between(currAddress, address2, addressData, distanceData)
        print('Package ID: %d Distance: %.1f' % (pkgId, distance))
        if distance == 0:
            minDistance = distance  # new min distance
            nextAddress = address2  # new min address
            nextId = pkg.package_id  # new package ID
            print('Closest Package Details: ID: %d Address: %s Distance: %.1f' % (nextId, nextAddress, minDistance))
            print()
            return nextAddress, nextId, minDistance
        elif distance < minDistance:
            minDistance = distance  # new min distance
            nextAddress = address2  # new min address
            nextId = pkg.package_id  # new package ID
    print('Closest Package Details: ID: %d Address: %s Distance: %.1f' % (nextId, nextAddress, minDistance))
    print()
    return nextAddress, nextId, minDistance


def load_truck_packages(truck1, truck2, truck3):
    # DELIVERY CONSTRAINTS
    # Can only be on truck 2: 3, 18, 36, 38
    # Must be on the SAME truck: 13, 14, 15, 16, 19, 20
    # Delayed on Flight (will not arrive to hub until 09:05:00): 6, 25, 28, 32
    # Wrong address listed (correct address arrives at 10:20:00): 9 (correct address: 410 S State St)

    # Manually Load Packages to Trucks
    list1 = [1, 2, 5, 7, 10, 13, 14, 15, 16, 19, 20, 29, 33, 34, 37, 39]
    list2 = [3, 8, 11, 12, 18, 23, 27, 35, 36, 38]
    list3 = [4, 6, 9, 17, 21, 22, 24, 25, 26, 28, 30, 31, 32, 40]
    truck1.packages = list1
    truck2.packages = list2
    truck3.packages = list3

    print('Truck 1 is Loaded:', list1)
    print('Truck 2 is Loaded:', list2)
    print('Truck 3 is Loaded:', list3)
    print()


def deliver_truck_packages(truck, time, pHashTable, addressData, distanceData):
    delivered = []
    not_delivered = truck.packages
    currAddress = truck.location
    distanceTraveled = 0
    # Time Object
    startTime = time
    h, m, s = startTime.split(':')
    timeObject = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    while len(not_delivered) > 0:
        for pkg in not_delivered:
            print('Delivered:', delivered)
            print('Not Delivered:', not_delivered)
            address, id, miles = min_distance_from(currAddress, not_delivered, pHashTable, addressData, distanceData)
            currAddress = address
            distanceTraveled += miles
            print('Total Distance traveled:', distanceTraveled)
            if miles == 0:
                print('Current time:', timeObject)
                # update package status
                currPkg = pHashTable.search(id)
                currPkg.status = 'Delivered at ' + str(timeObject)
            else:
                # update time
                time_passed = (miles / 18) * 60 * 60
                dts = datetime.timedelta(seconds=int(time_passed))
                timeObject += dts
                print('Current time:', timeObject)
                # update package status
                currPkg = pHashTable.search(id)
                currPkg.status = 'Delivered at ' + str(timeObject)
            delivered.append(id)
            not_delivered.remove(id)
            # print delivered package
            print('Package', currPkg.package_id, 'Delivered!')
            # update truck
            truck.location = currAddress
            truck.time = timeObject
            truck.mileage = distanceTraveled
            print(truck)
            print()
    print('Delivery Completed!')
    print('Delivered:', delivered)
    print('Not Delivered:', not_delivered)
    return truck.mileage


def main():
    # Hash table instance
    pHashTable = HashTable.ChainingHashTable()
    # Distance List instance
    distanceData = []
    # Address List instance
    addressData = []

    # Load Packages to Hash Table
    readCSV.load_package_data('WGUPS Package File.csv', pHashTable)
    # readCSV.print_package_table(pHashTable)
    # print(pHashTable.search(1))

    # Load Distances to 2-D List
    readCSV.load_distance_data('WGUPS Distance Table.csv', distanceData)
    # print(distanceData)

    # Load Addresses to List
    readCSV.load_address_data('WGUPS Address File.csv', addressData)
    # print(addressData)

    # Instantiate Truck Objects
    hub = '4001 South 700 East'
    list1 = []
    list2 = []
    list3 = []
    truck1 = Truck.Truck(hub, '08:00:00', '08:00:00', 16, 18, 0, list1)
    truck2 = Truck.Truck(hub, '08:00:00', '08:00:00', 16, 18, 0, list2)
    truck3 = Truck.Truck(hub, '10:20:00', '10:20:00', 16, 18, 0, list3)

    # Load Packages to Trucks
    print('Loading Packages!')
    load_truck_packages(truck1, truck2, truck3)

    # Deliver Truck Packages
    # print('Delivery Started!')
    # print('Truck 1 total miles:', deliver_truck_packages(truck1, truck1.timeLeftHub, pHashTable, addressData, distanceData))
    # t1_miles = truck1.mileage

    # Deliver Truck Packages
    # print('Delivery Started!')
    # print('Truck 2 total miles:', deliver_truck_packages(truck2, truck2.timeLeftHub, pHashTable, addressData, distanceData))
    # t2_miles = truck2.mileage

    # Deliver Truck Packages
    print('Delivery Started!')
    print('Truck 3 total miles:', deliver_truck_packages(truck3, truck3.timeLeftHub, pHashTable, addressData, distanceData))
    # t3_miles = truck3.mileage

    # totalMiles = t1_miles + t2_miles + t3_miles
    # print('Total Miles:', totalMiles)


if __name__ == '__main__':
    main()
