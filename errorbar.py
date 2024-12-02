import math
while True:
    SD = float(input("Enter a standard deviation: "))

    error_bar = SD/math.sqrt(5)
    print(round(error_bar, 3))