import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pandas as pd

# Set up the figure and subplot
fig, ax = plt.subplots()

# Function to update the animation
def animate(i):
    # Re-read the CSV file for each frame
    df = pd.read_csv("merged.csv")
    
    # Drop unnecessary columns and set index
    df = df.drop(['total', 'percent_buy', 'Unnamed: 0'], axis=1)
    df.set_index('rounded_price', inplace=True)
    
    # Clear the previous plot and plot the new data
    ax.clear()  # Clear previous plot
    df.plot.barh(ax=ax)  # Plot the new data

# Create the animation object
ani = animation.FuncAnimation(fig, animate, interval=250)

# Show the plot
plt.show()