import SubGradient
import Dual

print("Enter s for Sub-Gradient")
get = input("Enter d for dual \n").upper()
if get == "S":
    SubGradient.main()
elif get == "D":
    print("Not Finished")
else:
    print("Wrong input.")
