import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Data Viewer")
        self.root.geometry("800x600")

        # Initialize instance variables
        self.data = None  # Store the uploaded DataFrame
        self.x_column = None
        self.y_column = None
        self.bin_num = 10  # Default bin number

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Upload CSV button
        button_upload = tk.Button(self.root, text="Upload CSV", command=self.upload_csv)
        button_upload.pack(pady=10)

        # File path label
        self.label_file_path = tk.Label(self.root, text="No file selected", wraplength=750)
        self.label_file_path.pack(pady=10)

        # Status label
        self.label_status = tk.Label(self.root, text="", fg="black")
        self.label_status.pack(pady=10)

        # Treeview to display CSV content
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Entry fields for X and Y column names
        labelX = tk.Label(self.root, text="Enter X column name:")
        labelX.pack(pady=5)
        self.entryX = tk.Entry(self.root)
        self.entryX.pack(pady=5)

        labelY = tk.Label(self.root, text="Enter Y column name:")
        labelY.pack(pady=5)
        self.entryY = tk.Entry(self.root)
        self.entryY.pack(pady=5)

        # Verify button
        button_verify = tk.Button(self.root, text="Verify Columns", command=self.column_verify)
        button_verify.pack(pady=10)

        # Intermediate window button
        button_gchoice = tk.Button(self.root, text="Next", command=self.open_choice_window)
        button_gchoice.pack(pady=10)

    def upload_csv(self):
        # Open a file dialog to select the CSV file
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.label_file_path.config(text=f"File: {file_path}")

            # Load the CSV file using pandas
            try:
                self.data = pd.read_csv(file_path)
                self.display_csv()
                self.label_status.config(text="CSV uploaded successfully!", fg="green")
            except Exception as e:
                self.label_status.config(text=f"Error: {e}", fg="red")

    def display_csv(self):
        # Clear any previous data in the Treeview
        self.tree.delete(*self.tree.get_children())

        # Set up the column headers
        self.tree["columns"] = list(self.data.columns)
        self.tree["show"] = "headings"  # Hide the default tree column
        for col in self.data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Adjust column width

        # Add data rows to the Treeview
        for _, row in self.data.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def column_verify(self):
        # Get the column names from entry fields
        self.x_column = self.entryX.get()
        self.y_column = self.entryY.get()

        # Validate the columns
        if self.data is None:
            self.label_status.config(text="Error: No data uploaded.", fg="red")
            return

        if self.x_column not in self.data.columns:
            self.label_status.config(text=f"Error: '{self.x_column}' is not a valid column name.", fg="red")
            return

        if self.y_column not in self.data.columns:
            self.label_status.config(text=f"Error: '{self.y_column}' is not a valid column name.", fg="red")
            return

        # If valid, update the status
        self.label_status.config(text="Valid columns", fg="green")

    def update_bin_num(self, plot_window, ax, bins_input_field):
        # Get the user input for the number of bins
        try:
            self.bin_num = int(bins_input_field.get())
            self.label_status.config(text=f"Bins updated to {self.bin_num}", fg="green")

            # Clear the previous plot and re-plot with the new number of bins
            ax.clear()
            self.plot_histogram(ax)
            plot_window.canvas.draw()

        except ValueError:
            self.label_status.config(text="Error: Please enter a valid number for bins.", fg="red")

    def open_choice_window(self):
        # Ensure the columns are valid and data is loaded
        if self.label_status.cget("text") != "Valid columns" or self.data is None:
            self.label_status.config(text="Error: Cannot proceed. Check your data and columns.", fg="red")
            return

        # Create the intermediate window
        graph_choice_window = tk.Toplevel(self.root)
        graph_choice_window.title("Graph Types")
        graph_choice_window.geometry("400x300")

        # Label and proceed button
        label_message = tk.Label(graph_choice_window, text="Click the button below to plot the graph.", wraplength=350)
        label_message.pack(pady=20)

        scatter_proceed = tk.Button(
            graph_choice_window,
            text="LINE",
            command=lambda: (graph_choice_window.destroy(), self.graph_plot("line"))
        )
        scatter_proceed.pack(pady=20)

        line_proceed = tk.Button(
            graph_choice_window,
            text="SCATTER",
            command=lambda: (graph_choice_window.destroy(), self.graph_plot("scatter"))
        )
        line_proceed.pack(pady=20)

        button_both = tk.Button(
            graph_choice_window,
            text="Scatter + Trendline",
            command=lambda: self.graph_plot("both")
        )
        button_both.pack(pady=10)

        histogram_proceed = tk.Button(
            graph_choice_window,
            text="HISTOGRAM",
            command=lambda: (graph_choice_window.destroy(), self.graph_plot("histogram"))
        )
        histogram_proceed.pack(pady=20)

    def graph_plot(self, plot_type):
        if self.data is None:
            self.label_status.config(text="Error: No data uploaded or invalid columns.", fg="red")
            return

        plot_window = tk.Toplevel(self.root)
        plot_window.title("Graph Plot")

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        x = self.data[self.x_column]
        y = self.data[self.y_column]

        # Add plot options (scatter, line, histogram, etc.)
        if plot_type == "scatter":
            ax.scatter(x, y, label="Data Points", color="blue", alpha=0.6)
        elif plot_type == "line":
            ax.plot(x, y, label="Line Plot", color="green")
        elif plot_type == "histogram":
            self.plot_histogram(ax)
        elif plot_type == "both":
            ax.scatter(x, y, label="Data Points", color="blue", alpha=0.6)
            coefficients = np.polyfit(x, y, 1)
            trendline_y = coefficients[0] * x + coefficients[1]
            ax.plot(x, trendline_y, label="Trendline", color="red")

        # Add Labels, Legends, etc.
        ax.set_xlabel(self.x_column)
        ax.set_ylabel(self.y_column)
        ax.legend()

        # Create input field and button for changing bins for histogram
        if plot_type == "histogram":
            label_bins = tk.Label(plot_window, text="Enter Number of Bins:")
            label_bins.pack(pady=5)

            bins_input_field = tk.Entry(plot_window)
            bins_input_field.pack(pady=5)
            bins_input_field.insert(0, str(self.bin_num))  # Set default bin number

            bin_change_button = tk.Button(plot_window, text="Change Bins",
                                          command=lambda: self.update_bin_num(plot_window, ax, bins_input_field))
            bin_change_button.pack(pady=10)

        # Embed the plot in the window
        plot_window.canvas = FigureCanvasTkAgg(fig, master=plot_window)
        plot_window.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plot_window.canvas.draw()

    def plot_histogram(self, ax):
        # Plot the histogram using the current bin number
        y = self.data[self.y_column]
        ax.hist(y, bins=self.bin_num, label="Histogram", color="blue", alpha=0.6)
        ax.set_title(f"Histogram of {self.y_column}")
        ax.set_ylabel(self.y_column)
        ax.legend()
        ax.grid(True)


# Create the Tkinter root window
root = tk.Tk()
app = CSVViewerApp(root)
root.mainloop()
