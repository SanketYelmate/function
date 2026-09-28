rent = int(input("enter the flat rent : "))
food = int(input("enter the food order bill : "))
electricity_charge = int(input("enter the electricity unit you can use : "))
unitcharge = int(input("enter the unit R10ate : "))
person = int(input("enter the person leaving in flat/room : "))

total_bill = electricity_charge*unitcharge
total_amount = (rent + food + total_bill)//person
print("the total expense of flat/room : ", total_amount)