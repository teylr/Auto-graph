import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV data
data = pd.read_csv('test.csv')

# Display the data to check column names
print(data)

# Get column names for x and y from user input
x_column = input("Enter the column name for the x-axis: ")
y_column = input("Enter the column name for the y-axis: ")

# Check if the entered column names exist in the DataFrame
if x_column not in data.columns:
    print(f"Error: '{x_column}' is not a valid column name.")
elif y_column not in data.columns:
    print(f"Error: '{y_column}' is not a valid column name.")
else:
    # Plot the data
    x = data[x_column]
    y = data[y_column]

    # Plotting the points
    plt.plot(x, y)

    # Label the axes
    plt.xlabel(x_column)
    plt.ylabel(y_column)

    # Set the title
    plt.title(f'Plot of {y_column} vs {x_column}')

    # Show the plot
    plt.show()








