import NN
import SGDNN
import SGDNN0

get = input("Enter a for part(a), b for part(b), c for part(c). \n").upper()
if get == "A":
    NN.main()
elif get == "B":
    SGDNN.main()
elif get == "C":
    SGDNN0.main()
else:
    print("Wrong input.")
