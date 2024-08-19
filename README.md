
# RevOps Bowtie Funnel MRR Pipeline - Revenue Operations Python/Tkinter Application Scenario Analysis

# RevOps Bowtie - Revenue Operations Planning Tool

## Overview

This Python script creates an interactive revenue operations planning tool using `tkinter` for the graphical user interface (GUI), `matplotlib` for funnel chart visualizations, and `ttkbootstrap` for enhanced styling. The application is designed to help revenue operations (RevOps) professionals simulate and visualize the impact of various conversion rates and metrics on **Monthly Recurring Revenue (MRR)**. Users can input key metrics, compare scenarios side-by-side, and analyze the effects on the sales funnel and revenue outcomes.

## Features

- **Interactive Sliders & Inputs**: 
  - Users can adjust key metrics such as conversion rates (CR1 to CR5), number of prospects, and Average Contract Value (ACV) through intuitive sliders and input fields.
  - The application provides immediate visual and numerical feedback as these inputs are adjusted.

- **Dual-Scenario Comparison**: 
  - Compare two different sets of input values side-by-side to evaluate how changes in strategy or performance impact MRR and other funnel metrics.

- **Real-Time Funnel Visualization**:
  - An animated funnel chart represents the stages of the sales process, from prospects to retained customers, showing both percentages and absolute values at each stage.

- **MRR & Delta Analysis**:
  - The tool calculates and displays the **MRR** for each scenario and highlights the differences (Δ) between the two, both in absolute numbers and percentages.

- **Tooltips for Enhanced Usability**:
  - Tooltips are provided for each input field, explaining the significance of each metric, making the tool accessible for both seasoned professionals and newcomers.

## Potential Uses

- **Forecasting**: 
  - Use the tool to forecast MRR based on different conversion rates and sales metrics, gaining insights into how changes in the sales funnel can affect revenue.

- **Scenario Analysis**: 
  - Evaluate the effectiveness of different strategies or adjustments in the sales process by comparing two scenarios side-by-side.

- **Reporting**:
  - Generate visual reports or presentations that clearly demonstrate the impact of specific improvements or setbacks on the sales funnel and revenue.

- **Training**:
  - Leverage the tool as a training resource to educate team members on the relationship between key metrics and revenue outcomes.

## How It Works

1. **Funnel Chart Visualization**:
   - The funnel chart is created using `matplotlib`, with polygons representing each stage of the sales funnel. The chart updates dynamically as inputs change.

2. **Real-Time Calculation**:
   - Inputs are bound to a function that recalculates the funnel metrics and MRR in real-time, providing immediate visual and numerical feedback.

3. **Side-by-Side Comparison**:
   - The application allows users to compare two different scenarios, with the differences clearly highlighted, helping to identify which metrics have the most significant impact.

4. **Responsive Design**:
   - The layout adjusts dynamically to fit different screen sizes, ensuring a seamless user experience.

## Installation

To run this application, you will need to have Python installed along with the following libraries:

- `tkinter`
- `matplotlib`
- `numpy`

## Running the Application

Simply run the script using Python:

```python
python revops_bowtie_mrr_pipeline.py
```

This will launch a GUI window where you can input your metrics and visualize the results.

## Understanding the Bowtie Funnel

The bowtie funnel is a model used in Revenue Operations (RevOps) to track and optimize the customer journey from initial contact through to long-term retention and upsell opportunities. The funnel is divided into different stages, each with specific volume metrics (VM) and conversion rates (CR) that are crucial for tracking performance and predicting revenue outcomes.

### Key Concepts

1. **Conversion Rates (CR)**: These represent the success rates between different stages of the funnel. For example:
   - **CR1**: Conversion rate from Prospects to Marketing Qualified Leads (MQL).
   - **CR2**: Conversion rate from MQL to Sales Qualified Leads (SQL).
   - **CR3**: Conversion rate during the handoff and show rate process.
   - **CR4**: Win rate, representing the success rate in closing deals.
   - **CR5**: Churn rate during onboarding, representing customer loss before achieving full product impact.
   - **CR6**: Churn rate due to a lack of impact after onboarding.
   - **CR7**: Upsell rate during the usage phase over the length of the contract.

2. **Volume Metrics (VM)**: These are the stages between which the conversion rates are measured. For instance:
   - **VM1**: Initial prospect identification.
   - **VM2**: Prospects showing interest.
   - **VM3**: Engaged leads ready for sales interaction.
   - **VM4**: Prioritized opportunities.
   - **VM5**: Committed opportunities.
   - **VM6**: Customers ready for onboarding.
   - **VM7**: Customers achieving recurring impact, signaling long-term retention.

### LTO (Lead to Opportunity)

- **Stages**: Awareness and Education.
- **Volume Metrics**: VM1 (Identified) to VM2 (Interested) to VM3 (Engaged).
- **Conversion Rates**: CR1 and CR2, tracking movement from initial awareness to engagement.

### OTC (Opportunity to Close)

- **Stage**: Selection.
- **Volume Metrics**: VM4 (Priority) to VM5 (Committed).
- **Conversion Rates**: CR3 and CR4, tracking the process from prioritization to closing the deal.

### Churn

- **Stages**: Onboard and Achieve Impact.
- **Volume Metrics**: VM6 (Ready) to VM7 (Recurring Impact).
- **Conversion Ratios**: CR5 and CR6, focusing on retention and churn post-customer commitment.

### Benefits of the Bowtie Funnel Model

- **Unified Language**: Establishing a common language around these metrics allows RevOps professionals to communicate more effectively and make data-driven decisions.
- **Holistic View**: By incorporating both LTO and churn ratios, this model provides a comprehensive view of the customer journey and its impact on revenue.
- **Centralized Data**: Integrating these metrics into a CRM allows for a single source of truth, enabling better forecasting and operational efficiency.

## Example Use Case

Imagine you are a RevOps professional trying to forecast MRR for two different scenarios. By entering the relevant metrics into this application, you can instantly see how changes in conversion rates or churn might impact revenue, enabling you to make more informed strategic decisions.

## Contributing

If you wish to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the  GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007. See the LICENSE file for more details.

## Contact

For any questions or issues, please open an issue on GitHub or contact me directly.
