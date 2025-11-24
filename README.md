# Public Health Surveillance Dashboard

## 📋 Project Overview
This project is an interactive public health surveillance dashboard developed with Python and Streamlit. It transforms 2023-2024 public health data into intuitive visualizations, showcasing disease trends, regional disparities, and vaccine impacts to deliver data-driven insights for evidence-based decision-making .

Public health surveillance serves as the cornerstone of disease prevention and control. Addressing global health challenges, this dashboard focuses on resolving critical issues such as early detection of outbreaks, rational allocation of medical resources, and policy effectiveness evaluation — turning complex datasets into actionable intelligence .

By adopting a modular design and user-centric interface, the dashboard ensures accessibility across devices, enabling public health professionals, policymakers, and researchers to retrieve critical information efficiently .

## 🎯 Core Objectives
1. **Data-Driven Storytelling**: Guide users from problem identification (e.g., "Why are rural cases higher?") to actionable solutions (e.g., "Improve vaccine accessibility in rural regions") through compelling data narratives .
2. **Interactive Exploration**: Support multi-dimensional data filtering (year, region, indicator) to uncover hidden patterns like "Winter + Rural + Low SES = High Case Count" .
3. **Transparent Presentation**: Disclose detailed data sources, cleaning protocols, and limitations to establish credibility of analytical results .
4. **Decision-Support Orientation**: Translate data insights into targeted policy recommendations, such as "Prioritize vaccination for elderly populations in rural low-SES areas" .

## 📂 Project Structure
```
dashboard/
├── app.py                  # Main program entry (global config + page rendering)
├── requirements.txt        # Dependencies list
├── assets/                 # Static resources folder
│   ├── wut_logo.png        # Wuhan University of Technology Logo
│   └── efrei_logo.png      # EFREI Paris Logo
├── sections/               # Page modules (core function implementation)
│   ├── intro.py            # Introduction page (background + objectives + affiliation + contacts)
│   ├── overview.py         # Overview page (KPIs + time-series trends)
│   ├── deep_dives.py       # In-depth analysis page (region-SES disparities + vaccine efficacy)
│   └── conclusions.py      # Conclusions page (core insights + policy recommendations)
└── utils/                  # Utility function module
    ├── io.py               # Data reading + data description (get_data_caveats())
    ├── prep.py             # Data preprocessing (cleaning + format conversion)
    └── viz.py              # Visualization tools (chart generation functions)
```

## 🔧 Environment Configuration & Dependencies
### 1. Environment Requirements
- Python 3.9+
- Operating System: Windows/macOS/Linux

### 2. Dependency Installation
First, create and activate a virtual environment in the project root directory (recommended), then install required packages:
```bash
# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Create virtual environment (macOS/Linux)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Contents of requirements.txt
```
streamlit==1.36.0
pandas==2.2.2
numpy==1.26.4
matplotlib==3.8.4
seaborn==0.13.2
plotly==5.22.0
```

## 🚀 Quick Start
After completing environment configuration, execute the following command in the project root directory to launch the dashboard:
```bash
streamlit run app.py
```
Upon successful execution, your browser will automatically open the dashboard (default address: http://localhost:8501). If not, copy the URL from the terminal and access it manually.

## 📊 Core Function Modules
| Module (Page) | Core Content | Interactive Features |
|---------------|--------------|----------------------|
| Introduction | Project background, objectives, dataset description, affiliation logos, contact information | None (information display only) |
| Overview | KPIs (total cases, average vaccination rate), disease trend time-series charts | Data filtering by year and indicator |
| Deep Dives | Region-SES disparity heatmaps, vaccine efficacy comparison analysis  | Region filtering, vaccine type switching |
| Conclusions | Summary of core insights, evidence-based policy recommendations | PDF export for recommendation reports |

## 📈 Dataset Description
- **Data Scope**: National public health surveillance data from 2023 to 2024
- **Core Fields**: Time (year/month), Region (province/city), SES (Socio-Economic Status), Number of cases, Vaccination rate, Vaccine type, etc.
- **Data Transparency**: Detailed sources, cleaning rules, and limitations are available in the "Dataset Overview" section on the Introduction page. Core descriptions are provided by the `get_data_caveats()` function in `utils/io.py`.

## 🤝 Affiliations
This is an individual academic assignment associated with the following institutions (Logos stored in the `assets/` folder):
- Wuhan University of Technology
- EFREI Paris (École Française d'Electronique et d'Informatique)

## 📞 Contact & Feedback
For questions, suggestions, or feedback regarding the project, please contact:
- **Author**: Zhu Enping
- **Mentor**: Mano Joseph Mathew
- **Email**: [1305927014@qq.com](mailto:1305927014@qq.com) (Click to send directly)

## 📄 License
This project is licensed for **Academic Use Only** . It may be used solely for educational purposes and academic research, excluding any commercial application or redistribution without prior authorization.

## 🏷️ Project Tags
#EFREIDataStoriesWUT2025 #EFREIParis #DataVisualization #Streamlit #PublicHealth #DataStorytelling #Python

