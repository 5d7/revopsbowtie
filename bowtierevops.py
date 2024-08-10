import tkinter as tk  # Import the Tkinter library for creating GUI applications.
from tkinter import ttk  # Import ttk for themed widgets.
import matplotlib.pyplot as plt  # Import Matplotlib for plotting charts.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import backend to integrate Matplotlib with Tkinter.
import numpy as np  # Import NumPy for numerical operations.

# Function to calculate metrics and update the chart when inputs change
def calculate_and_update_chart(*args):
    try:
        # Collecting input values from the entries and sliders on both left and right panels
        values_left = [float(entries_left[0].get())] + [slider.get() for slider in sliders_left] + [float(entries_left[1].get())]
        values_right = [float(entries_right[0].get())] + [slider.get() for slider in sliders_right] + [float(entries_right[1].get())]

        # Update slider labels to display current values in percentage format
        for i, slider in enumerate(sliders_left):
            slider_labels_left[i].config(text=f"{slider.get():.0f}%")
        for i, slider in enumerate(sliders_right):
            slider_labels_right[i].config(text=f"{slider.get():.0f}%")

        # Calculate MRR and metrics for both left and right inputs
        mrr_left, metrics_left = calculate_metrics(values_left)
        mrr_right, metrics_right = calculate_metrics(values_right)

        # Update the charts with the new metrics
        update_chart(ax_left, metrics_left, "Bowtie Funnel Conversion Metrics A")
        update_chart(ax_right, metrics_right, "Bowtie Funnel Conversion Metrics B")

        # Update the labels to show MRR for both left and right panels
        result_labels_left.config(text=f"MRR (Left): ${mrr_left:.2f}")
        result_labels_right.config(text=f"MRR (Right): ${mrr_right:.2f}")

        # Calculate and display the differences between left and right metrics
        for i, (value_left, value_right) in enumerate(zip(metrics_left, metrics_right)):
            delta = value_right - value_left  # Difference between left and right
            delta_text = f"{labels[i]} Δ: {delta:.0f}, {100 * delta / value_left:.1f}%"  # Show difference as absolute and percentage
            if i == 5:  # For 'Retained' stage, calculate dollar difference as well
                delta_dollars = delta * values_right[6]
                delta_text += f", Δ$: {delta_dollars:.2f}"
            differences[i].config(text=delta_text)  # Update the difference labels

        # Calculate and display the MRR difference
        mrr_delta = mrr_right - mrr_left
        result_labels_diff.config(text=f"MRR Difference: ${mrr_delta:.2f}")

        # Redraw the charts to reflect updated values
        canvas_left.draw()
        canvas_right.draw()

    except ValueError:
        # Handle the case where the user enters an invalid input (not a number)
        result_labels_left.config(text="Invalid input")
        result_labels_right.config(text="Invalid input")

# Function to calculate the key metrics based on the input values
def calculate_metrics(values):
    prospects, cr1, cr2, cr3, cr4, cr5, fee_mo = values  # Unpack the values list into respective metrics
    mql = prospects * cr1 / 100  # Calculate Marketing Qualified Leads (MQL)
    sql = mql * cr2 / 100  # Calculate Sales Qualified Leads (SQL)
    opportunities = sql * cr3 / 100  # Calculate Opportunities
    won = opportunities * cr4 / 100  # Calculate Won deals
    retained = won * (1 - cr5 / 100)  # Calculate Retained customers
    mrr = retained * fee_mo  # Calculate Monthly Recurring Revenue (MRR)
    return mrr, [prospects, mql, sql, opportunities, won, retained]  # Return MRR and list of calculated metrics

# Function to update the chart based on calculated metrics
def update_chart(ax, values, title):
    stages = ['Prospects/Leads', 'MQL', 'SQL', 'Opportunities', 'Won', 'Retained']  # Define the funnel stages
    ax.clear()  # Clear previous chart
    ax.axis('off')  # Turn off axis for cleaner appearance
    ax.set_title(title, fontsize=14, fontweight='bold')  # Set the chart title

    # Normalize values for display
    max_value = max(values)  # Get the maximum value to normalize the bars
    heights = np.linspace(0, 1, len(stages) + 1)  # Define the positions of bars on y-axis
    for i, (stage, value) in enumerate(zip(stages, values)):
        width = value / max_value  # Normalize bar width relative to the maximum value
        ax.barh(heights[i], width, height=0.1, color=plt.cm.viridis(i / len(stages)), align='center')  # Draw the horizontal bar
        ax.text(width + 0.02, heights[i], f"{stage}: {value:.0f} ({value / max_value * 100:.1f}%)",  # Annotate the bar with text
                ha='left', va='center', fontweight='bold', fontsize=10, color='black')

    ax.set_xlim(0, 1.2)  # Extend x-axis limit to fit the text annotations
    ax.set_ylim(0, 1)  # Set y-axis limits

# Initialize the Tkinter root window
root = tk.Tk()
root.title("RevOps Bowtie - Revenue Operations Planning MRR Pipeline")  # Set the title of the window
root.geometry("1400x900")  # Set the size of the window

# Create frames for inputs and differences
input_frame_left = ttk.Frame(root, padding="10")  # Left input frame
input_frame_right = ttk.Frame(root, padding="10")  # Right input frame
diff_frame = ttk.Frame(root, padding="20")  # Frame for differences

# Grid layout for the frames
input_frame_left.grid(row=0, column=0, sticky="nwes")
input_frame_right.grid(row=0, column=2, sticky="nwes")
diff_frame.grid(row=1, column=0, columnspan=3, sticky="nwes")

# Labels for inputs and sliders
labels = ["Prospects", "CR1 (Prospect to MQL)", "CR2 (MQL to SQL)", "CR3 (Show Rate & Hand-off)", "CR4/WR (Win Rate)", "CR5 (Churn/Upsell rate during Onboarding)", "ACV/Monthly ($)"]
entries_left, entries_right, sliders_left, sliders_right = [], [], [], []  # Lists to store entry and slider widgets
slider_labels_left, slider_labels_right = [], []  # Lists to store slider label widgets
differences = []  # List to store difference label widgets

# Loop through each label and create corresponding entry or slider in both left and right frames
for i, label in enumerate(labels):
    ttk.Label(input_frame_left, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)  # Left frame label
    ttk.Label(input_frame_right, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)  # Right frame label
    
    if i in [0, 6]:  # For "Prospects" and "ACV/Monthly ($)", create entry fields
        entry_left = ttk.Entry(input_frame_left, width=15)
        entry_right = ttk.Entry(input_frame_right, width=15)
        entry_left.grid(row=i, column=1, padx=5, pady=5)
        entry_right.grid(row=i, column=1, padx=5, pady=5)
        entry_left.insert(0, "1000" if i == 0 else "30")  # Default values for entries
        entry_right.insert(0, "1000" if i == 0 else "30")
        entries_left.append(entry_left)  # Add to list of left entries
        entries_right.append(entry_right)  # Add to list of right entries
    else:  # For conversion rates (CRs), create sliders
        slider_left = ttk.Scale(input_frame_left, from_=-100 if i == 5 else 0, to=100, orient="horizontal", value=25)  # Left slider
        slider_right = ttk.Scale(input_frame_right, from_=-100 if i == 5 else 0, to=100, orient="horizontal", value=25)  # Right slider
        slider_label_left = ttk.Label(input_frame_left, text="25%")  # Left slider label
        slider_label_right = ttk.Label(input_frame_right, text="25%")  # Right slider label
        
        slider_left.grid(row=i, column=1, padx=5, pady=5)
        slider_right.grid(row=i, column=1, padx=5, pady=5)
        slider_label_left.grid(row=i, column=2, padx=5)
        slider_label_right.grid(row=i, column=2, padx=5)
        
        sliders_left.append(slider_left)  # Add to list of left sliders
        sliders_right.append(slider_right)  # Add to list of right sliders
        slider_labels_left.append(slider_label_left)  # Add to list of left slider labels
        slider_labels_right.append(slider_label_right)  # Add to list of right slider labels

    # Create labels for displaying differences between left and right metrics
    diff_label = ttk.Label(diff_frame, text="Δ: 0", font=("Helvetica", 10))
    diff_label.grid(row=i, column=0, padx=5, pady=5)
    differences.append(diff_label)

# Labels to display MRR values for left and right inputs
result_labels_left = ttk.Label(input_frame_left, text="MRR (Left): $0.00")
result_labels_left.grid(row=8, column=0, columnspan=3, pady=10)

result_labels_right = ttk.Label(input_frame_right, text="MRR (Right): $0.00")
result_labels_right.grid(row=8, column=0, columnspan=3, pady=10)

# Label to display the difference in MRR between left and right inputs
result_labels_diff = ttk.Label(diff_frame, text="MRR Difference: $0.00", font=("Helvetica", 12))
result_labels_diff.grid(row=7, column=0, pady=10)

# Create Matplotlib figures and embed them in Tkinter canvas widgets
fig_left, ax_left = plt.subplots(figsize=(6, 4), dpi=100)
canvas_left = FigureCanvasTkAgg(fig_left, master=input_frame_left)  # Left chart
canvas_widget_left = canvas_left.get_tk_widget()
canvas_widget_left.grid(row=9, column=0, columnspan=3, padx=10, pady=10, sticky="nwes")

fig_right, ax_right = plt.subplots(figsize=(6, 4), dpi=100)
canvas_right = FigureCanvasTkAgg(fig_right, master=input_frame_right)  # Right chart
canvas_widget_right = canvas_right.get_tk_widget()
canvas_widget_right.grid(row=9, column=0, columnspan=3, padx=10, pady=10, sticky="nwes")

# Bind events to sliders and entries to trigger recalculation and chart update
for slider in sliders_left + sliders_right:
    slider.bind("<Motion>", calculate_and_update_chart)  # Recalculate when slider is moved
    slider.bind("<ButtonRelease-1>", calculate_and_update_chart)  # Recalculate when slider is released

for entry in entries_left + entries_right:
    entry.bind("<KeyRelease>", calculate_and_update_chart)  # Recalculate when key is released in entry field

# Initial calculation and chart update on program start
calculate_and_update_chart()

# Configure grid layout weights to ensure proper resizing behavior
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Start the Tkinter event loop
root.mainloop()

