import tkinter as tk  # Import tkinter for GUI components
from tkinter import ttk  # Import ttk for themed widgets in tkinter
import matplotlib.pyplot as plt  # Import matplotlib for plotting charts
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import for embedding matplotlib plots in tkinter
import numpy as np  # Import numpy for numerical operations
from matplotlib.figure import Figure  # Import for creating matplotlib figures
from matplotlib.patches import Polygon  # Import for creating polygon shapes in matplotlib
from matplotlib.animation import FuncAnimation  # Import for animating matplotlib plots
import seaborn as sns  # Import seaborn for color palettes
from ttkbootstrap import Style  # Import ttkbootstrap for enhanced ttk themes

# Custom slider class to extend ttk.Scale with additional styling or behavior
class ModernSlider(ttk.Scale):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

# Class to create and animate a funnel chart in matplotlib
class AnimatedFunnel:
    def __init__(self, ax, values, stages):
        self.ax = ax  # Matplotlib axis to draw on
        self.values = values  # Initial values for each funnel stage
        self.stages = stages  # Labels for each funnel stage
        self.polygons = []  # List to hold funnel polygons
        self.texts = []  # List to hold text annotations
        
        self.setup_chart()  # Initialize the chart setup
        
    def setup_chart(self):
        self.ax.clear()  # Clear the axis
        self.ax.set_xlim(0, 1)  # Set x-axis limits
        self.ax.set_ylim(0, 1)  # Set y-axis limits
        self.ax.axis('off')  # Hide the axis
        
        width = 0.8  # Base width of the funnel
        height = 0.8 / len(self.stages)  # Height of each stage
        y = 1 - height  # Starting y position
        
        max_value = max(self.values)  # Maximum value to normalize widths
        colors = sns.color_palette("viridis", len(self.stages))  # Generate a color palette
        
        for stage, value, color in zip(self.stages, self.values, colors):
            # Calculate width and position of each stage
            width_scaled = width * (value / max_value)
            left = (1 - width_scaled) / 2
            
            # Define the points of the polygon
            points = [[left, y], 
                      [left + width_scaled, y],
                      [left + width_scaled - 0.05, y - height],
                      [left + 0.05, y - height]]
            
            # Create and add the polygon to the axis
            polygon = Polygon(points, facecolor=color, edgecolor='white')
            self.ax.add_patch(polygon)
            self.polygons.append(polygon)
            
            # Add text annotation in the center of the polygon
            text = self.ax.text(0.5, y - height/2, f"{stage}\n{value:,.0f}\n({value/self.values[0]*100:.1f}%)", 
                                ha='center', va='center', fontweight='bold', color='black', fontsize=8)
            self.texts.append(text)
            
            y -= height  # Move to the next stage position
    
    def animate(self, new_values):
        max_value = max(new_values)  # Recalculate maximum value for normalization
        width = 0.8  # Base width of the funnel
        height = 0.8 / len(self.stages)  # Height of each stage
        y = 1 - height  # Starting y position
        
        for i, (polygon, text, value) in enumerate(zip(self.polygons, self.texts, new_values)):
            # Update the polygon's position and size based on new values
            width_scaled = width * (value / max_value)
            left = (1 - width_scaled) / 2
            
            points = [[left, y], 
                      [left + width_scaled, y],
                      [left + width_scaled - 0.05, y - height],
                      [left + 0.05, y - height]]
            
            polygon.set_xy(points)  # Update polygon points
            text.set_text(f"{self.stages[i]}\n{value:,.0f}\n({value/new_values[0]*100:.1f}%)")  # Update text
            
            y -= height  # Move to the next stage position
        
        self.values = new_values  # Update the values

# Tooltip manager class to create and manage tooltips in tkinter
class TooltipManager:
    def __init__(self, widget):
        self.widget = widget  # Widget to attach the tooltip to
        self.tipwindow = None  # Tooltip window
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)  # Remove window borders
        tw.wm_geometry(f"+{x}+{y}")  # Position the tooltip
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

# Helper function to create tooltips for widgets
def create_tooltip(widget, text):
    toolTip = TooltipManager(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# Function to calculate and update the funnel chart based on user input
def calculate_and_update_chart(*args):
    try:
        # Retrieve values from input fields and sliders
        values_left = [float(entries_left[0].get())] + [slider.get() for slider in sliders_left] + [float(entries_left[1].get())]
        values_right = [float(entries_right[0].get())] + [slider.get() for slider in sliders_right] + [float(entries_right[1].get())]

        # Update slider labels with current values
        for i, slider in enumerate(sliders_left):
            slider_labels_left[i].config(text=f"{slider.get():.0f}%")
        for i, slider in enumerate(sliders_right):
            slider_labels_right[i].config(text=f"{slider.get():.0f}%")

        # Calculate metrics for both scenarios
        mrr_left, metrics_left = calculate_metrics(values_left)
        mrr_right, metrics_right = calculate_metrics(values_right)

        # Update funnel charts with new metrics
        funnel_left.animate(metrics_left)
        funnel_right.animate(metrics_right)

        # Update result labels with MRR values
        result_labels_left.config(text=f"MRR (A): ${mrr_left:,.2f}")
        result_labels_right.config(text=f"MRR (B): ${mrr_right:,.2f}")

        # Calculate and display differences between scenarios
        for i, (value_left, value_right) in enumerate(zip(metrics_left, metrics_right)):
            delta = value_right - value_left
            delta_percent = 100 * delta / value_left if value_left != 0 else 0
            delta_text = f"{labels[i]} Δ: {delta:+,.0f} ({delta_percent:+.1f}%)"
            if i == 5:
                delta_dollars = delta * values_right[6]
                delta_text += f"\nΔ$: {delta_dollars:+,.2f}"
            differences[i].config(text=delta_text)

        # Update MRR difference label
        mrr_delta = mrr_right - mrr_left
        result_labels_diff.config(text=f"MRR Δ: ${mrr_delta:+,.2f}")

        # Redraw canvas to reflect changes
        canvas_left.draw()
        canvas_right.draw()

    except ValueError:
        # Handle invalid input
        result_labels_left.config(text="Invalid input")
        result_labels_right.config(text="Invalid input")

# Function to calculate MRR and funnel metrics based on input values
def calculate_metrics(values):
    prospects, cr1, cr2, cr3, cr4, cr5, fee_mo = values
    mql = prospects * cr1 / 100
    sql = mql * cr2 / 100
    opportunities = sql * cr3 / 100
    won = opportunities * cr4 / 100
    retained = won * (1 - cr5 / 100)
    mrr = retained * fee_mo
    return mrr, [prospects, mql, sql, opportunities, won, retained]

# Initialize tkinter window and set up styles
root = tk.Tk()
style = Style(theme='flatly')
root.title("RevOps Bowtie - Revenue Operations Planning")
root.geometry("1400x900")

# Set up main frames for the layout
main_frame = ttk.Frame(root, padding="5")
main_frame.pack(fill=tk.BOTH, expand=True)

input_frame_left = ttk.Frame(main_frame, padding="0")
input_frame_right = ttk.Frame(main_frame, padding="0")
diff_frame = ttk.Frame(main_frame, padding="5")

input_frame_left.grid(row=0, column=0, sticky="nsew", padx=5, pady=0)
input_frame_right.grid(row=0, column=2, sticky="nsew", padx=5, pady=0)
diff_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=0)

# Labels and input widgets for each metric
labels = ["Prospects", "CR1 (Prospect to MQL)", "CR2 (MQL to SQL)", "CR3 (Show Rate & Hand-off)", "CR4/WR (Win Rate)", "CR5 (Churn/Upsell rate)", "ACV/Monthly ($)"]
entries_left, entries_right, sliders_left, sliders_right = [], [], [], []
slider_labels_left, slider_labels_right = [], []
differences = []

for i, label in enumerate(labels):
    # Create labels and input fields for the left and right inputs
    ttk.Label(input_frame_left, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
    ttk.Label(input_frame_right, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
    
    if i in [0, 6]:
        # Create entry fields for numeric inputs (Prospects, ACV)
        entry_left = ttk.Entry(input_frame_left, width=15)
        entry_right = ttk.Entry(input_frame_right, width=15)
        entry_left.grid(row=i, column=1, padx=5, pady=5)
        entry_right.grid(row=i, column=1, padx=5, pady=5)
        entry_left.insert(0, "1000" if i == 0 else "30")
        entry_right.insert(0, "1000" if i == 0 else "30")
        entries_left.append(entry_left)
        entries_right.append(entry_right)
    else:
        # Create sliders for percentage inputs (conversion rates)
        slider_left = ModernSlider(input_frame_left, from_=-100 if i == 5 else 0, to=100, orient="horizontal", value=25)
        slider_right = ModernSlider(input_frame_right, from_=-100 if i == 5 else 0, to=100, orient="horizontal", value=25)
        slider_label_left = ttk.Label(input_frame_left, text="25%")
        slider_label_right = ttk.Label(input_frame_right, text="25%")
        
        slider_left.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        slider_right.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        slider_label_left.grid(row=i, column=2, padx=5)
        slider_label_right.grid(row=i, column=2, padx=5)
        
        sliders_left.append(slider_left)
        sliders_right.append(slider_right)
        slider_labels_left.append(slider_label_left)
        slider_labels_right.append(slider_label_right)

    # Create labels to show differences between scenarios
    diff_label = ttk.Label(diff_frame, text="Δ: 0", style="info.TLabel")
    diff_label.grid(row=i, column=0, padx=5, pady=5)
    differences.append(diff_label)

# Result labels for MRR (Monthly Recurring Revenue)
result_labels_left = ttk.Label(input_frame_left, text="MRR (A): $0.00", style="success.TLabel")
result_labels_left.grid(row=8, column=0, columnspan=3, pady=0)

result_labels_right = ttk.Label(input_frame_right, text="MRR (B): $0.00", style="success.TLabel")
result_labels_right.grid(row=8, column=0, columnspan=3, pady=0)

result_labels_diff = ttk.Label(diff_frame, text="MRR Δ: $0.00", style="info.TLabel")
result_labels_diff.grid(row=7, column=0, pady=5)

# Create matplotlib figures for funnel charts
fig_left = Figure(figsize=(5, 4.5), dpi=100)
ax_left = fig_left.add_subplot(111)
canvas_left = FigureCanvasTkAgg(fig_left, master=input_frame_left)
canvas_widget_left = canvas_left.get_tk_widget()
canvas_widget_left.grid(row=9, column=0, columnspan=3, padx=5, pady=0, sticky="nsew")

fig_right = Figure(figsize=(5, 4.5), dpi=100)
ax_right = fig_right.add_subplot(111)
canvas_right = FigureCanvasTkAgg(fig_right, master=input_frame_right)
canvas_widget_right = canvas_right.get_tk_widget()
canvas_widget_right.grid(row=9, column=0, columnspan=3, padx=5, pady=0, sticky="nsew")

# Initialize funnel charts with starting values
stages = ['Prospects', 'MQL', 'SQL', 'Opportunities', 'Won', 'Retained']
initial_values = [1000, 250, 100, 50, 25, 20]

funnel_left = AnimatedFunnel(ax_left, initial_values, stages)
funnel_right = AnimatedFunnel(ax_right, initial_values, stages)

# Bind events to update charts on input changes
for slider in sliders_left + sliders_right:
    slider.bind("<Motion>", calculate_and_update_chart)
    slider.bind("<ButtonRelease-1>", calculate_and_update_chart)

for entry in entries_left + entries_right:
    entry.bind("<KeyRelease>", calculate_and_update_chart)

# Add tooltips to explain each input field
tooltips = [
    "Number of initial leads or prospects",
    "Conversion rate from Prospect to Marketing Qualified Lead",
    "Conversion rate from Marketing Qualified Lead to Sales Qualified Lead",
    "Conversion rate for successful demonstrations and hand-offs",
    "Win rate for closing deals",
    "Churn or upsell rate during the onboarding period",
    "Average Contract Value per month"
]

for i, (label, tooltip) in enumerate(zip(labels, tooltips)):
    create_tooltip(input_frame_left.grid_slaves(row=i, column=0)[0], tooltip)
    create_tooltip(input_frame_right.grid_slaves(row=i, column=0)[0], tooltip)

# Initial chart calculation and update
calculate_and_update_chart()

# Configure grid layout to be responsive
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)
main_frame.rowconfigure(0, weight=3)
main_frame.rowconfigure(1, weight=1)

# Start the tkinter main loop
root.mainloop()
