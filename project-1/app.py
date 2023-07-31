import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_bar_chart():
    # Sample data for the bar graph
    categories = ['A', 'B', 'C', 'D']
    values = [30, 25, 20, 25]

    # Create a figure and axis for the bar graph
    fig = Figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.bar(categories, values)

    # Set labels and title
    ax.set_xlabel('Categories')
    ax.set_ylabel('Values')
    ax.set_title('Bar Graph Example')

    # Embed the bar graph in a Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Create the main application window
root = tk.Tk()
root.title("Bar Graph Example")

# Create a button to generate the bar graph
generate_button = ttk.Button(root, text="Generate Bar Graph", command=create_bar_chart)
generate_button.pack(pady=10)

# Start the main event loop
root.mainloop()
