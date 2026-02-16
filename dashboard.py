"""
Interactive Dashboard for Real Madrid Fatigue Analysis
Run with: python -m streamlit run dashboard.py

"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np


st.set_page_config(
    page_title="Real Madrid Fatigue Tracker",
    layout="wide"
)


st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FFFFFF;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #F3F4F6;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #3B82F6;
    }
    .warning-box {
        background: #FEF3C7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #F59E0B;
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-header"> Real Madrid Fatigue Tracker</div>', unsafe_allow_html=True)


# Match Discovery & Selection
def get_available_matches():
    data_dir = Path("analysis_output")
    files = list(data_dir.glob("minute_metrics_*.parquet"))
    return sorted([f.stem.replace("minute_metrics_", "") for f in files])

available_matches = get_available_matches()

if not available_matches:
    st.error("⚠️ No processed match data found. Please run `complete_fatigue_analysis.py` first!")
    st.stop()

# Sidebar Match Selector
st.sidebar.header("🎛️ Match Selection")
selected_match_id = st.sidebar.selectbox("Select Match ID", available_matches, index=0)
st.sidebar.markdown("---")

# Load data for selected match
@st.cache_data
def load_data(match_id):
    """Load processed data for a specific match."""
    data_dir = Path("analysis_output")
    try:
        minute_metrics = pd.read_parquet(data_dir / f"minute_metrics_{match_id}.parquet")
        error_events = pd.read_parquet(data_dir / f"error_events_{match_id}.parquet")
        return minute_metrics, error_events
    except Exception as e:
        st.error(f"❌ Error loading data for Match {match_id}: {str(e)}")
        st.stop()

minute_metrics, error_events = load_data(selected_match_id)

# Sidebar Controls
st.sidebar.header(" Controls")
st.sidebar.markdown("---")

# Player selection
players = sorted(minute_metrics['player_name'].unique())
selected_player = st.sidebar.selectbox("Select Player", players)

# Metric selection
metric_options = {
    'Fatigue Index': 'fatigue_index',
    'Distance (m)': 'distance_m',
    'Avg Velocity (m/s)': 'avg_velocity_ms',
    'Max Velocity (m/s)': 'max_velocity_ms',
    'Cumulative Distance': 'cumulative_distance'
}
selected_metric = st.sidebar.selectbox("Select Metric", list(metric_options.keys()))

# Fatigue threshold
fatigue_threshold = st.sidebar.slider("Fatigue Alert Threshold", 0.5, 2.0, 1.2, 0.1)

st.sidebar.markdown("---")
st.sidebar.info(" **Tip:** Fatigue Index > 1.2 indicates high workload")

# Main content
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Players",
        len(minute_metrics['player_name'].unique()),
        delta=None
    )

with col2:
    st.metric(
        "Total Minutes Analyzed",
        len(minute_metrics),
        delta=None
    )

with col3:
    st.metric(
        "Error Events",
        len(error_events),
        delta=None
    )

with col4:
    avg_fatigue = minute_metrics['fatigue_index'].mean()
    st.metric(
        "Avg Fatigue Index",
        f"{avg_fatigue:.2f}",
        delta=f"{avg_fatigue - 1.0:.2f}" if avg_fatigue > 1.0 else None,
        delta_color="inverse"
    )

st.markdown("---")

def draw_pitch(ax, color='white', lw=2):
    """
    Draw a high-quality, professional football pitch without 'piano key' gaps.
    """
    # Pitch colors
    pitch_color = '#2e7d32'  # Base green
    stripe_color = '#388e3c' # Slightly different green for stripes
    
    # Pitch Dimensions (Standard 105m x 68m)
    length = 105
    width = 68
    
    # 1. Fill the ENTIRE axis area and background with the pitch color
    ax.set_facecolor(pitch_color)
    plt.gcf().patch.set_facecolor('#0E1117') # Streamlit dark background color
    
    # 2. Draw the main pitch rectangle base
    main_rect = plt.Rectangle((0, 0), length, width, color=pitch_color, zorder=0)
    ax.add_patch(main_rect)
    
    # 3. Draw field stripes (now with no gaps)
    stripe_width = length / 10
    for i in range(10):
        if i % 2 == 1: # Draw every second bar as a stripe
            rect = plt.Rectangle((i*stripe_width, 0), stripe_width, width, color=stripe_color, zorder=0)
            ax.add_patch(rect)
    
    # 4. Outer lines
    ax.plot([0, 0, length, length, 0], [0, width, width, 0, 0], color=color, lw=lw, zorder=1)
    
    # 5. Midline - Draw carefully to be centered
    ax.plot([length/2, length/2], [0, width], color=color, lw=lw, zorder=1)
    
    # 6. Center circle and point
    center_circle = plt.Circle((length/2, width/2), 9.15, color=color, fill=False, lw=lw, zorder=1)
    ax.add_artist(center_circle)
    ax.plot(length/2, width/2, 'o', color=color, zorder=2)
    
    # Left Side Markings
    ax.plot([0, 16.5, 16.5, 0], [width/2-20.16, width/2-20.16, width/2+20.16, width/2+20.16], color=color, lw=lw, zorder=1)
    ax.plot([0, 5.5, 5.5, 0], [width/2-9.16, width/2-9.16, width/2+9.16, width/2+9.16], color=color, lw=lw, zorder=1)
    arc_left = plt.matplotlib.patches.Arc((11, width/2), 18.3, 18.3, theta1=308, theta2=52, color=color, lw=lw, zorder=1)
    ax.add_patch(arc_left)
    ax.plot(11, width/2, 'o', color=color, zorder=2, markersize=4)
    
    # Right Side Markings
    ax.plot([length, length-16.5, length-16.5, length], [width/2-20.16, width/2-20.16, width/2+20.16, width/2+20.16], color=color, lw=lw, zorder=1)
    ax.plot([length, length-5.5, length-5.5, length], [width/2-9.16, width/2-9.16, width/2+9.16, width/2+9.16], color=color, lw=lw, zorder=1)
    arc_right = plt.matplotlib.patches.Arc((length-11, width/2), 18.3, 18.3, theta1=128, theta2=232, color=color, lw=lw, zorder=1)
    ax.add_patch(arc_right)
    ax.plot(length-11, width/2, 'o', color=color, zorder=2, markersize=4)
    
    # Corner Arcs
    ax.add_patch(plt.matplotlib.patches.Arc((0, 0), 2, 2, theta1=0, theta2=90, color=color, lw=lw))
    ax.add_patch(plt.matplotlib.patches.Arc((0, width), 2, 2, theta1=270, theta2=360, color=color, lw=lw))
    ax.add_patch(plt.matplotlib.patches.Arc((length, 0), 2, 2, theta1=90, theta2=180, color=color, lw=lw))
    ax.add_patch(plt.matplotlib.patches.Arc((length, width), 2, 2, theta1=180, theta2=270, color=color, lw=lw))
    
    # Goal Posts (slightly thickened)
    # Left Goal
    ax.plot([-2, 0], [width/2-3.66, width/2-3.66], color='white', lw=3, zorder=2)
    ax.plot([-2, 0], [width/2+3.66, width/2+3.66], color='white', lw=3, zorder=2)
    ax.plot([-2, -2], [width/2-3.66, width/2+3.66], color='white', lw=3, zorder=2)
    # Right Goal
    ax.plot([length, length+2], [width/2-3.66, width/2-3.66], color='white', lw=3, zorder=2)
    ax.plot([length, length+2], [width/2+3.66, width/2+3.66], color='white', lw=3, zorder=2)
    ax.plot([length+2, length+2], [width/2-3.66, width/2+3.66], color='white', lw=3, zorder=2)

    ax.set_xlim(-8, length + 8)
    ax.set_ylim(-3, width + 3)
    ax.set_aspect('equal')
    ax.axis('off')

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([" Player Analysis", "🏟️ Tactical Pitch", "⚠️ High Risk Periods", "🏃 Team Overview", "📈 Correlations"])

with tab1:
    # Existing Player Analysis code ...
    st.subheader(f"Analysis for {selected_player}")
    
    # Filter data for selected player
    player_data = minute_metrics[minute_metrics['player_name'] == selected_player].copy()
    
    if len(player_data) == 0:
        st.warning(f"No data available for {selected_player}")
    else:
        # Player stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_distance = player_data['distance_m'].sum()
            st.metric("Total Distance", f"{total_distance:.0f} m")
        
        with col2:
            max_velocity = player_data['max_velocity_ms'].max()
            st.metric("Max Velocity", f"{max_velocity:.1f} m/s")
        
        with col3:
            max_fatigue = player_data['fatigue_index'].max()
            st.metric("Max Fatigue Index", f"{max_fatigue:.2f}")
        
        # Plot
        fig, ax = plt.subplots(figsize=(12, 5))
        
        metric_col = metric_options[selected_metric]
        ax.plot(player_data['minute'], player_data[metric_col], 
                marker='o', linewidth=2, markersize=6, color='#3B82F6')
        
        # Add threshold line for fatigue
        if selected_metric == 'Fatigue Index':
            ax.axhline(y=fatigue_threshold, color='red', linestyle='--', 
                      label=f'Alert Threshold ({fatigue_threshold})')
            ax.legend()
        
        ax.set_xlabel('Minute', fontsize=12)
        ax.set_ylabel(selected_metric, fontsize=12)
        ax.set_title(f'{selected_metric} Over Time - {selected_player}', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        # High fatigue moments
        high_fatigue = player_data[player_data['fatigue_index'] > fatigue_threshold]
        if len(high_fatigue) > 0:
            st.markdown("###  High Fatigue Moments")
            st.dataframe(
                high_fatigue[['minute', 'fatigue_index', 'distance_m', 'avg_velocity_ms']]
                .sort_values('fatigue_index', ascending=False)
                .head(10),
                width="stretch"
            )

with tab2:
    st.subheader("🏟️ Tactical Error Map")
    st.markdown("Visualize exactly where errors occurred on the pitch, color-coded by player fatigue.")
    
    # Filter errors
    map_scope = st.radio("Display Scope", ["All Real Madrid Players", f"Only {selected_player}"], horizontal=True)
    
    if map_scope == "All Real Madrid Players":
        plot_errors = error_events.copy()
    else:
        plot_errors = error_events[error_events['player_name'] == selected_player].copy()
    
    if len(plot_errors) > 0:
        # ABSOLUTE SAFETY for fatigue_index column
        if 'fatigue_index' not in plot_errors.columns:
            plot_errors = pd.merge(
                plot_errors,
                minute_metrics[['player_id', 'minute', 'fatigue_index']],
                on=['player_id', 'minute'],
                how='left'
            )
            # Handle potential suffixes from merge
            if 'fatigue_index_x' in plot_errors.columns:
                plot_errors['fatigue_index'] = plot_errors['fatigue_index_x']
            elif 'fatigue_index_y' in plot_errors.columns:
                plot_errors['fatigue_index'] = plot_errors['fatigue_index_y']
        
        # Final fallback if still missing (should not happen)
        if 'fatigue_index' not in plot_errors.columns:
            plot_errors['fatigue_index'] = 1.0 
        
        # Ensure we have coordinates
        if 'x' in plot_errors.columns and 'y' in plot_errors.columns:
            plot_errors = plot_errors.dropna(subset=['x', 'y'])
            
            # Draw Pitch
            fig, ax = plt.subplots(figsize=(12, 8))
            draw_pitch(ax)
            
            # Scatter Plot of errors
            # Normalize color map dynamically based on actual data range
            min_f = plot_errors['fatigue_index'].min()
            max_f = plot_errors['fatigue_index'].max()
            norm = plt.Normalize(min_f, max_f)
            
            scatter = ax.scatter(plot_errors['x'], plot_errors['y'], 
                               c=plot_errors['fatigue_index'], 
                               s=150, cmap='YlOrRd', edgecolor='white', 
                               norm=norm, zorder=10, alpha=0.9)
            
            cbar = plt.colorbar(scatter, ax=ax, fraction=0.03, pad=0.02)
            cbar.set_label(f'Fatigue Index ({min_f:.1f} to {max_f:.1f})', fontsize=10, color='white')
            cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
            
            # Add player labels if filtered or small enough set
            if len(plot_errors) < 15:
                for idx, row in plot_errors.iterrows():
                    ax.annotate(row['player_name'], (row['x'], row['y']), 
                               textcoords="offset points", xytext=(0,10), 
                               ha='center', color='white', weight='bold',
                               bbox=dict(boxstyle='round,pad=0.2', fc='black', alpha=0.3))
            
            ax.set_title(f"Tactical Error Distribution: {map_scope}", fontsize=16, fontweight='bold', color='white', pad=20)
            st.pyplot(fig)
            
            # Breakdown table
            st.markdown("### Event Details")
            st.dataframe(plot_errors[['minute', 'player_name', 'error_type', 'fatigue_index']].sort_values('minute'), width="stretch")
        else:
            st.error(" Spatial data (X, Y) missing for error events. Please run analysis again.")
    else:
        st.info("No error events found for this selection.")

with tab3:
    st.subheader(" High Risk Periods (All Players)")
    
    # Find high fatigue moments
    high_risk = minute_metrics[minute_metrics['fatigue_index'] > fatigue_threshold].copy()
    high_risk = high_risk.sort_values('fatigue_index', ascending=False)
    
    if len(high_risk) > 0:
        st.markdown(f"**{len(high_risk)} high-risk player-minutes detected** (Fatigue > {fatigue_threshold})")
        
        # Group by minute
        risk_by_minute = high_risk.groupby('minute').agg({
            'player_name': 'count',
            'fatigue_index': 'mean'
        }).reset_index()
        risk_by_minute.columns = ['minute', 'players_at_risk', 'avg_fatigue']
        
        # Plot
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.bar(risk_by_minute['minute'], risk_by_minute['players_at_risk'], 
               color='#EF4444', alpha=0.7)
        ax.set_xlabel('Minute', fontsize=12)
        ax.set_ylabel('Number of Players at Risk', fontsize=12)
        ax.set_title('High-Risk Periods by Minute', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        st.pyplot(fig)
        
        # Top risk players
        st.markdown("### Players with Most High-Fatigue Minutes")
        risk_by_player = high_risk.groupby('player_name').size().sort_values(ascending=False).head(10)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.dataframe(risk_by_player, width="stretch")
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.barh(risk_by_player.index, risk_by_player.values, color='#F59E0B')
            ax.set_xlabel('High-Fatigue Minutes', fontsize=12)
            ax.set_title('Players Needing Monitoring', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='x')
            st.pyplot(fig)
    else:
        st.success(" No high-risk periods detected at current threshold!")

with tab4:
    st.subheader("🏃 Team Overview")
    
    # Position analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Distance by Position")
        position_distance = minute_metrics.groupby('position')['distance_m'].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(position_distance.index, position_distance.values, color='#10B981')
        ax.set_xlabel('Total Distance (m)', fontsize=12)
        ax.set_title('Distance Covered by Position', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        st.pyplot(fig)
    
    with col2:
        st.markdown("### Fatigue by Position")
        position_fatigue = minute_metrics.groupby('position')['fatigue_index'].mean().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(position_fatigue.index, position_fatigue.values, color='#8B5CF6')
        ax.set_xlabel('Average Fatigue Index', fontsize=12)
        ax.set_title('Fatigue by Position', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        st.pyplot(fig)
    
    # Player comparison table
    st.markdown("###  Player Metrics Comparison")
    
    player_summary = minute_metrics.groupby('player_name').agg({
        'distance_m': 'sum',
        'max_velocity_ms': 'max',
        'fatigue_index': 'max',
        'high_speed_frames': 'sum',
        'sprint_frames': 'sum'
    }).round(2)
    
    # Normalize for heatmap (0 to 1 scale)
    player_summary_norm = (player_summary - player_summary.min()) / (player_summary.max() - player_summary.min())
    
    # Rename for display
    display_names = {
        'distance_m': 'Distance (m)',
        'max_velocity_ms': 'Top Speed (m/s)',
        'fatigue_index': 'Max Fatigue',
        'high_speed_frames': 'High Speed Frames',
        'sprint_frames': 'Sprint Frames'
    }
    
    # Heatmap
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(player_summary_norm.T, annot=player_summary.T, fmt='.1f', 
               cmap='RdYlGn_r', cbar_kws={'label': 'Normalized Scale'}, ax=ax)
    
    ax.set_yticklabels([display_names.get(label.get_text(), label.get_text()) for label in ax.get_yticklabels()])
    plt.xticks(rotation=45, ha='right')
    plt.title("Team Physical Comparison Heatmap", fontsize=14, fontweight='bold', pad=20)
    st.pyplot(fig)

    st.markdown("###  Detailed Records")
    st.dataframe(player_summary, width="stretch")

with tab5:
    st.subheader("Fatigue-Error Correlation")
    
    if len(error_events) > 0:
        # Merge errors with metrics
        error_counts = error_events.groupby('minute').size().reset_index(name='error_count')
        avg_fatigue_by_minute = minute_metrics.groupby('minute')['fatigue_index'].mean().reset_index()
        
        correlation_data = pd.merge(error_counts, avg_fatigue_by_minute, on='minute', how='outer').fillna(0)
        
        # Calculate correlation
        if len(correlation_data) > 0:
            corr = correlation_data[['fatigue_index', 'error_count']].corr().iloc[0, 1]
            
            col1, col2, col3 = st.columns(3)
            with col2:
                st.metric("Correlation Coefficient", f"{corr:.3f}")
            
            # Scatter plot
            fig, ax = plt.subplots(figsize=(10, 6))
            scatter = ax.scatter(correlation_data['fatigue_index'], 
                               correlation_data['error_count'],
                               s=100, alpha=0.6, c=correlation_data['minute'], 
                               cmap='viridis')
            
            # Trend line
            if correlation_data['error_count'].sum() > 0:
                z = np.polyfit(correlation_data['fatigue_index'], 
                             correlation_data['error_count'], 1)
                p = np.poly1d(z)
                ax.plot(correlation_data['fatigue_index'], 
                       p(correlation_data['fatigue_index']), 
                       "r--", linewidth=2, label='Trend line')
            
            ax.set_xlabel('Average Fatigue Index', fontsize=12)
            ax.set_ylabel('Number of Errors', fontsize=12)
            ax.set_title('Fatigue vs Errors', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label('Minute', fontsize=10)
            
            st.pyplot(fig)
            
            # Interpretation
            if corr > 0.3:
                st.success(" **Positive correlation detected:** Higher fatigue is associated with more errors")
            elif corr < -0.3:
                st.warning(" **Negative correlation:** This is unexpected and needs investigation")
            else:
                st.info("ℹ**Weak correlation:** May need more data or refined error detection")
    else:
        st.info("No error events available for correlation analysis")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6B7280; padding: 2rem;'>
    <p><strong>Real Madrid Fatigue Error Tracking System</strong></p>
    <p>Data-driven insights for optimal player management</p>
</div>
""", unsafe_allow_html=True)
