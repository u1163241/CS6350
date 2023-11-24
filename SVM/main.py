import SubGradient
import Dual
import Gaussian

print("Enter s for Sub-Gradient")
print("Enter d for dual SVM")
get = input("Enter g for Gaussian kern\n").upper()
if get == "S":
    SubGradient.main()
elif get == "D":
    Dual.main()
elif get == "G":
    Gaussian.main()
else:
    print("Wrong input.")
