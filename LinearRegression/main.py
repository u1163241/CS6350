import BatchGradientDescent
import StochasticGradientDescent

get = input(
    "Enter bgd for Batch Gradient Descent or sgd for Stochastic Gradient Descent. \n"
).upper()
if get == "BGD":
    BatchGradientDescent.main()
elif get == "SGD":
    StochasticGradientDescent.main()
else:
    print("Wrong input.")
