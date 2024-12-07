# Tsyp-AESS
---
# **EcoScope:Land Cover Monitoring Dashboard**

This project is designed to monitor and visualize land cover changes over time using historical data and forecasted trends. It provides an interactive dashboard for stakeholders to analyze land cover types, trends, and predictions, enabling data-driven decision-making. The project integrates artificial intelligence (AI) for enhanced interactivity and insights.

---

## **Project Features**

### **1. Interactive Dashboard**
- **Visualizations**: Dynamic line charts, bar charts, scatter plots, and geographical visualizations to explore land cover data trends.
- **Customizable Filters**: Select time ranges and land cover types for detailed analysis.
- **Dark and Light Modes**: Toggle between themes for better user experience.

### **2. AI Chatbot Integration**
- Powered by OpenAI's GPT-3.5 for interactive queries.
- Provides real-time responses and insights based on dashboard data.
- Examples:
  - "What is the forest cover forecast for 2030?"
  - "How has urbanization changed over the years?"

### **3. Forecasting**
- Uses the **Prophet** library for machine learning-based predictions of land cover trends (2024–2033).
- Ensures accurate and interpretable future projections.

### **4. Data Quality and Validation**
- Ensures integrity, consistency, and usability of the data through a dedicated validation script.

---

## **Setup Instructions**

### **1. Prerequisites**
Ensure the following are installed on your system:
- Python 3.8 or later
- pip (Python package manager)
- Git (to clone the repository)

### **2. Clone the Repository**
```bash
git clone https://github.com/your-username/land-cover-dashboard.git
cd land-cover-dashboard
```

### **3. Create and Activate a Virtual Environment**

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### **4. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **5. Run the Dashboard**
```bash
python dashboard.py
```
Access the dashboard at [http://127.0.0.1:8050](http://127.0.0.1:8050) in your web browser.

---

## **Additional Tools Used**

### **1. Google Colab**
- **Purpose**: Cloud-based environment for machine learning model development and data preprocessing.
- **Advantages**:
  - GPU/TPU acceleration for faster computations.
  - Simplifies library management and local setup issues.

### **2. Anaconda Jupyter**
- **Purpose**: Facilitated data analysis and debugging workflows.
- **Advantages**:
  - Seamless integration with Python libraries.
  - Step-by-step analysis of datasets for better insights.

---

## **Data Files**

| **File**                          | **Description**                                             |
|-----------------------------------|-------------------------------------------------------------|
| `processed_land_cover_data.csv`   | Contains preprocessed data for analysis and visualization.  |
| `all_forecasted_land_cover.csv`   | Includes machine learning-based land cover predictions.     |
| `combined_land_cover_data.csv`    | Merged historical and forecasted data for dashboard input.  |

**Note**: Ensure these files are in the project directory for smooth execution.

---

## **Data Validation**

To validate the quality of the data, run the `data_validation.py` script:
```bash
python data_validation.py
```
This ensures datasets are consistent, error-free, and ready for dashboard integration.

---

## **How It Works**

1. **Data Integration**:
   - Historical MODIS land cover data (2001–2023).
   - Forecasted data (2024–2033) using the Prophet model.

2. **Dashboard**:
   - Built using Python, Dash, and Plotly.
   - Enables real-time data exploration with customizable filters.

3. **AI Integration**:
   - The chatbot leverages OpenAI's GPT-3.5 for contextual insights and dynamic queries.

---

## **Contribution Guidelines**

We welcome contributions to enhance this project. Here's how you can contribute:
1. Fork the repository.
2. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit and push your changes:
   ```bash
   git commit -m "Add your feature description"
   git push origin feature/your-feature-name
   ```
4. Open a pull request for review.

---

## **Sustainable Development Goals (SDGs)**

This project contributes to the following SDGs:
- **Goal 13: Climate Action**: Provides actionable insights into land cover changes to address environmental challenges.
- **Goal 15: Life on Land**: Facilitates data-driven decision-making to protect terrestrial ecosystems.

---
