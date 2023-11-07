import standard
import voted
import average

get = input(
    "Enter s for standard Perceptron result, v for voted Perceptron result and a for average Perceptron result. \n"
).upper()
if get == "S":
    standard.main()
elif get == "V":
    voted.main()
elif get == "A":
    average.main()
else:
    print("Wrong input.")
