# RetailMonteCarlo
A Monte Carlo Simulation Of Customer Purchases at a Retail Store

## Overview
The retail_simulation.ipynb notebook simulates retail customer purchases based on predefined customer personas and their buying habits. It incorporates inter-item dynamics to model how the purchase of one item can influence the likelihood of purchasing another, providing a more nuanced understanding of customer behavior.

The `personas`, `prices`, and `item_relations` are currently customized for a cafe establishment, but these can be easily customized to your needs in the notebook directly.

The simulation uses a Monte Carlo method to run multiple iterations, each representing a different potential outcome based on random chance, reflecting the variability in real-world customer behavior. This approach helps café owners and managers estimate average sales volume and revenue for each menu item, along with understanding popular item combinations.

## Features
- **Customer Personas**: Simulates purchases for different customer types, including morning commuters, students, remote workers, and more.
You can determine personas based on demographics studies for your area and the likelyhood each persona is to visit your establishment (For example: https://libguides.bentley.edu/consumers/mosaicusa)
- **Inter-Item Dynamics**: Adjusts purchase probabilities to account for common item pairings (e.g., coffee and pastries).
- **Monte Carlo Simulation**: Provides robust estimates by running thousands of simulations.
- **Average Sales and Revenue Calculation**: Calculates average total purchases and revenues for each item and overall.

## Setup
1. **Python Installation**: Ensure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Script Download**: Download the `retail_simulation.ipynb` script from this repository.

3. **Dependencies**: This script uses the `random` module, which is part of the Python Standard Library and requires no additional installation.

## How to Run
1. **Open Terminal or Command Prompt**: Navigate to the directory containing the downloaded script.

2. **Modify Presets**: `estimated_total_customers`, `num_simulations`, `personas`, `prices`, and `item_relations` should be modified to meet your needs

3. **Execute the Script**: Run the script using Python by typing the following command:
