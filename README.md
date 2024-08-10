
# RevOps Bowtie Funnel MRR Pipeline - Tkinter Application

## Overview

This Python script creates a graphical user interface (GUI) for visualizing and analyzing revenue operations (RevOps) metrics using the bowtie funnel model. The application allows users to input key metrics that drive **Monthly Recurring Revenue (MRR)** and visualizes these metrics using bar charts. The interface is built with `Tkinter`, and the charts are generated using `Matplotlib`.

## Features

- **Interactive Input Fields**: Users can input key metrics related to their sales funnel, such as the number of prospects and various conversion rates.
- **Real-Time Visualization**: As users adjust inputs, the charts and calculated MRR values update in real-time.
- **Comparison Capability**: The tool provides side-by-side comparison of two different sets of metrics, allowing users to visualize differences and understand their impact on MRR.
- **Detailed Metrics Breakdown**: The application calculates and displays the key metrics at each stage of the funnel, providing a detailed breakdown of the entire process.

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

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

For any questions or issues, please open an issue on GitHub or contact the repository owner directly.
