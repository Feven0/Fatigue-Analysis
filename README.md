# Real Madrid Fatigue Analysis & Error Tracking

## What This Project Does

### The Problem
Coaches need to know **when to substitute players** to prevent errors caused by fatigue.

### The Solution
This project:
1. **Reads raw GPS tracking data** (player positions every 0.1 seconds)
2. **Calculates fatigue metrics** for each player, for each minute
3. **Identifies error events** (bad passes, fouls, etc.)
4. **Correlates fatigue with errors** to find patterns
5. **Creates visualizations** showing when players are at risk

### Why It's Useful
- Data-driven substitution decisions
- Prevent injuries from over-fatigue
- Reduce errors in critical moments
- Optimize player performance

---
---

## How It Works

### Step-by-Step Process

#### Step 1: Load Raw Tracking Data
```python


#### Step 2: Calculate Frame-Level Metrics
For each frame (every 0.1 seconds):
```python
# Calculate distance moved using Euclidean Distance Formula
distance = sqrt((x_new - x_old)² + (y_new - y_old)²)

# Calculate velocity (speed)
velocity = distance / 0.1 # meters per second
```

### Why This Formula?
On a football field, players rarely run in straight horizontal or vertical lines. They run diagonally, they curve, and they zig-zag. The **Euclidean Distance Formula** (the mathematical application of the Pythagorean Theorem) is the only way to accurately measure the "straight-line" distance between any two coordinate points, regardless of what direction the player is facing. 

Because we calculate this **10 times every single second**, we are essentially measuring the **"Total Treadmill Distance"** the player has covered!

###  Millions of  Calculations
We perform the Pythagorean calculation ** million times** per match. Why?

Football is a game of constant high-speed zig-zags and rapid "stop-and-start" movements that would be completely lost if we only measured positions every few seconds. By calculating the distance ten times every second (10Hz), we avoid "cutting corners" and missing up to **20% of a player's actual effort**. 

This high-definition tracking is the only way to:
1. Capture the immense physiological toll of every micro-acceleration and turn.
2. Accurately measure a players true peak speed.
3. Build a scientifically valid **Fatigue Index** that explains why performance physically crumbles.

**The Math of the Match:**
$90 \text{ mins} \times 60 \text{ secs} \times 10 \text{ frames} \times 22 \text{ players} = \mathbf{1.18 \text{ million positions}}$
Our project "sweeps" through all 22+ players (including the ~5 substitutions Real Madrid uses, totaling 15-16 distinct players) and processes halftime/stoppage data, pushing the total data points into the **multi-millions**.


#### Step 3: Aggregate to Minutes
Group all frames within each minute:
```python
# For each player, for each minute:
minute_metrics = {
 'distance_m': sum(all distances in that minute),
 'avg_velocity': mean(all velocities),
 'max_velocity': max(all velocities),
 'high_speed_frames': count(frames where velocity > 5.5),
 'sprint_frames': count(frames where velocity > 7.0),
 # ... etc
}
```

#### Step 4: Calculate Fatigue Index
```python
# Cumulative distance = total distance covered so far
cumulative_distance = sum(distance from minute 0 to current minute)

# Fatigue index = how much work compared to expected
fatigue_index = cumulative_distance / (minute * 100)
# Where 100m per minute is the baseline expectation

# Interpretation:
# < 1.0 = Below expected workload
# 1.0-1.2 = Normal workload
# 1.2-1.5 = High workload 
# > 1.5 = Critical fatigue 
```

#### Step 5: Extract Error Events
```python
# Load dynamic event data
# Look for:
# - Unsuccessful passes
# - Fouls committed
# - Dispossessions
# - Lost duels
# - Turnovers

# Link each error to:
# - Player ID
# - Minute it occurred
# - Type of error
```

#### Step 6: Correlate Fatigue with Errors
```python
# For each minute:
# - Average fatigue across all players
# - Count of errors that occurred

# Calculate correlation coefficient
# Positive correlation = higher fatigue more errors
```

#### Step 7: Create Visualizations
- Graph 1: Fatigue over time (line chart)
- Graph 2: Player comparison (heatmap)
- Graph 3: Fatigue vs errors (scatter plot)
- Graph 4: Position analysis (bar charts)

---


## Running the Project

### Prerequisites
```bash
# Install required packages
pip install pandas numpy matplotlib seaborn tqdm pyarrow streamlit
```

**How to use it:**
1. Run: `python complete_fatigue_analysis.py`
2. View graphs in `analysis_output/`
3. Read report in `fatigue_analysis_report_1021404.txt`
4. Explore interactively: `streamlit run dashboard.py`
