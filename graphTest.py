import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Data Viewer")
        self.root.geometry("800x600")

        # Initialize instance variables
        self.data = None  # Store the uploaded DataFrame
        self.x_column = None
        self.y_column = None

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

        # Plot button (to plot the graph)
        button_plot = tk.Button(self.root, text="Plot Graph", command=self.graph_plot)
        button_plot.pack(pady=10)

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

        # If valid, update the status and store column names
        self.label_status.config(text="Valid columns", fg="green")

    def graph_plot(self):
        # Only plot if the columns are valid
        if self.label_status.cget("text") == "Valid columns":
            # Create a new Toplevel window to plot the graph
            plot_window = tk.Toplevel(self.root)
            plot_window.title("Graph")
            plot_window.geometry("800x600")

            # Create a Matplotlib figure and axis
            fig, ax = plt.subplots()

            # Plot the data for the selected X and Y columns
            ax.plot(self.data[self.x_column], self.data[self.y_column])

            # Set labels and title
            ax.set_xlabel(self.x_column)
            ax.set_ylabel(self.y_column)
            ax.set_title(f"{self.y_column} vs {self.x_column}")

            # Create a canvas to display the plot in the new window
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Redraw the canvas with the new plot
            canvas.draw()


# Create the Tkinter root window
root = tk.Tk()
app = CSVViewerApp(root)
root.mainloop()



