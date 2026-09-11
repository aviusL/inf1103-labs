
#wk2 lab

inventory = 0
totalUnits = 0
failedCount = 0
cleanedInput = 0

while inventory != "quit":
    try:
        userInput = input("Enter a stock quantity, or quit.  :")
        cleanedInput = int(userInput)

    except:
        if type(userInput) is str and userInput == "quit":
            print(f"Total units processed :{inventory}")
            print(f"Number of Failed/Rejected Entries :{failedCount}")
            break 
        else:
            print("Invalid Input!")
            failedCount += 1

    else:
        if (inventory+cleanedInput) < 500 and cleanedInput > 0:
            inventory += cleanedInput
            print(f"Valid Input! Inventory is now {inventory}")
        elif cleanedInput >= 500:
            print("ALERT!")
            failedCount += 1
            break
        elif cleanedInput < 1:
            print("Inventory cannot be a negative number.")
            failedCount += 1
        else:
            print("Invalid Input!")




    


