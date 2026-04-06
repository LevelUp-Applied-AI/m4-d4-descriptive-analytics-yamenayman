'''
"""Core Skills Drill — Descriptive Analytics

Compute summary statistics, plot distributions, and create a correlation
heatmap for the sample sales dataset.

Usage:
    python drill_eda.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def compute_summary(df):
    """Compute summary statistics for all numeric columns.

    Args:
        df: pandas DataFrame with at least some numeric columns

    Returns:
        DataFrame containing count, mean, median, std, min, max
        for each numeric column. Save the result to output/summary.csv.
    """
    # TODO: Compute descriptive statistics (count, mean, median, std, min, max)
    #       for all numeric columns and save to output/summary.csv
    pass


def plot_distributions(df, columns, output_path):
    """Create a 2x2 subplot figure with histograms for the specified columns.

    Args:
        df: pandas DataFrame
        columns: list of 4 column names to plot (use numeric columns)
        output_path: file path to save the figure (e.g., 'output/distributions.png')

    Returns:
        None — saves the figure to output_path
    """
    # TODO: Create a 2x2 figure with sns.histplot (KDE overlay) for each column
    #       Add titles, labels, and tight layout before saving
    pass


def plot_correlation(df, output_path):
    """Compute Pearson correlation matrix and visualize as a heatmap.

    Args:
        df: pandas DataFrame with numeric columns
        output_path: file path to save the figure (e.g., 'output/correlation.png')

    Returns:
        None — saves the figure to output_path
    """
    # TODO: Compute the correlation matrix for numeric columns and
    #       visualize it as an annotated Seaborn heatmap
    pass


def main():
    """Load data, compute summary, and generate all plots."""
    os.makedirs("output", exist_ok=True)

    # TODO: Load the CSV from data/sample_sales.csv
    # TODO: Call compute_summary and save the result
    # TODO: Choose 4 numeric-friendly columns and call plot_distributions
    # TODO: Call plot_correlation


if __name__ == "__main__":
    main()
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def compute_summary(df):
    """
    Computes count, mean, median, std, min, max for numeric columns.
    Saves the result to output/summary.csv.
    """
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Calculate summary using describe() which gives count, mean, std, min, max
    summary = numeric_df.describe()
    
    # Add median as a new row
    summary.loc['median'] = numeric_df.median()
    
    # Filter only the requested rows
    summary = summary.loc[['count', 'mean', 'median', 'std', 'min', 'max']]
    
    # Save to CSV
    summary.to_csv('output/summary.csv')
    return summary

def plot_distributions(df, columns, output_path):
    """
    Creates a 2x2 subplot figure with histograms and KDE overlays.
    Saves the figure to output_path.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten() # Flatten to easily loop over 1D array of axes
    
    for i, col in enumerate(columns):
        if i < 4: # Prevent index out of bounds if there are more than 4 columns
            sns.histplot(df[col], kde=True, ax=axes[i], color='skyblue')
            axes[i].set_title(f'Distribution of {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Frequency')
            
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_correlation(df, output_path):
    """
    Computes Pearson correlation matrix and visualizes it as a heatmap.
    Saves the figure to output_path.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr(method='pearson')
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", 
                vmin=-1, vmax=1, center=0, square=True)
    plt.title('Pearson Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    # 1. Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # 2. Load the dataset
    df = pd.read_csv('data/sample_sales.csv')
    
    # Run Task 1: Summary Statistics
    compute_summary(df)
    
    # Prepare 4 numeric columns for Task 2
    # The original dataset has only 'quantity' and 'unit_price'. 
    # We create two derived columns to satisfy the 2x2 plot requirement smoothly.
    if 'quantity' in df.columns and 'unit_price' in df.columns:
        df['total_sales'] = df['quantity'] * df['unit_price']
        df['tax_amount'] = df['total_sales'] * 0.16
    
    # Grab the first 4 numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # In case there are somehow still less than 4, we repeat them to avoid errors
    while len(numeric_cols) < 4:
        numeric_cols.append(numeric_cols[0])
        
    cols_to_plot = numeric_cols[:4]
    
    # Run Task 2: Distribution Plots
    plot_distributions(df, cols_to_plot, 'output/distributions.png')
    
    # Run Task 3: Correlation Heatmap
    plot_correlation(df, 'output/correlation.png')
    
    print("EDA Drill completed! Check the 'output/' directory for the results.")