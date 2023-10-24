import AdaBoost
import Bagging
import Bagging2
import RandomForest
import RandomForest2

print("Enter adaBoost for adaBoost")
print("Enter bagging for bagging tree")
print("Enter bagging2 for result of bagging trees vs single trees")
print("Enter random for random forest")
print("Enter random2 for result of random forests vs single trees")
get = input("Enter code. \n").upper()
if get == "adaBoost".upper():
    AdaBoost.main()
elif get == "bagging".upper():
    Bagging.main()
elif get == "bagging2".upper():
    Bagging2.main()
elif get == "random".upper():
    RandomForest.main()
elif get == "random2".upper():
    RandomForest2.main()
else:
    print("Wrong input.")
