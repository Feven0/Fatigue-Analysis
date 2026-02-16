# Real Madrid Fatigue Analysis & Error Tracking

This project implements a professional-grade fatigue analysis system for football players, focusing on Real Madrid's performance data. It correlates high-resolution tracking data (10Hz) with event data to identify "breaking points" where physical fatigue lead to technical errors.

##  Overview
The system processes raw tracking and event data to build a narrative of player movement and performance throughout a match. It uses:
- **Pythagorean Theorem** for precise distance calculation at 10Hz.
- **Fatigue Index** based on Acute:Chronic Workload Ratio (ACWR) principles.
- **Error Correlation** by joining physiological load with technical outcomes (passes, fouls, dispossessions).

## Dataset Credit
The dataset used in this project is provided by **SkillCorner**. 
*Note: Due to the proprietary nature and size (~15GB) of the SkillCorner dataset, the raw data files are not included in this repository.*

## Tech Stack
- **Python**: Core logic and processing.
- **Pandas & NumPy**: Data manipulation and high-speed math.
- **Matplotlib & Seaborn**: Scientific visualizations.
- **Streamlit**: Interactive coaching dashboard.
- **Parquet**: Optimized data storage for large-scale analysis.

## Scientific Foundation
- **Speed Thresholds**: Based on Di Salvo et al. (2009).
- **Injury/Fatigue Logic**: Based on the Gabbett (2016) Training-Injury Prevention Paradox.

## Installation & Usage
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the analysis engine:
   ```bash
   python complete_fatigue_analysis.py
   ```
4. Launch the dashboard:
   ```bash
   streamlit run dashboard.py
   ```

---
*Created by Feven & Team (2026)*
