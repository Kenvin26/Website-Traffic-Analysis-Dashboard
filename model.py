import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Website Traffic Analysis", layout="wide")

# Load the dataset
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

def main():
    st.title("Website Traffic Analysis Dashboard")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type="csv")
    
    if uploaded_file is not None:
        # Load data
        df = load_data(uploaded_file)
        
        st.subheader("Dataset Overview")
        st.write("### First 5 rows of the dataset:")
        st.dataframe(df.head())
        
        st.write("### Dataset Summary:")
        st.write(df.describe())
        
        # Display column data types
        st.write("### Column Data Types:")
        st.write(df.dtypes)

        # Add visuals
        st.subheader("Visualizations")

        # Correlation Heatmap
        st.write("### Correlation Heatmap:")
        fig_corr = correlation_heatmap(df)
        if fig_corr is not None:
            st.pyplot(fig_corr)
        
        # Line plot for trends
        st.write("### Yearly Trends (if applicable):")
        if "YEAR" in df.columns:
            st.line_chart(df.groupby("YEAR").size())
        else:
            st.warning("No 'YEAR' column found in the dataset.")
        
        # Distribution of a numeric column
        numeric_columns = df.select_dtypes(include=np.number).columns
        if not numeric_columns.empty:
            st.write("### Distribution of a Numeric Column:")
            column_to_plot = st.selectbox("Select a numeric column", numeric_columns)
            fig_dist = distribution_plot(df, column_to_plot)
            st.pyplot(fig_dist)
        else:
            st.warning("No numeric columns available for distribution plot.")
        
        # Insights
        st.subheader("Insights")
        st.write("### Key Observations:")
        st.write("- The correlation heatmap helps understand relationships between numeric variables.")
        st.write("- Yearly trends (if available) provide insights into data variations over time.")
        st.write("- Distribution plots highlight the spread of specific numeric columns.")
    
    else:
        st.info("Please upload a dataset to begin analysis.")

# Helper functions

def correlation_heatmap(df):
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=np.number)
    
    # Check if there are numeric columns to process
    if numeric_df.empty:
        st.warning("No numeric columns available for correlation heatmap.")
        return None

    # Compute the correlation
    corr = numeric_df.corr()

    # Plot the heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap")
    return fig

def distribution_plot(df, column):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df[column], kde=True, ax=ax, bins=20)
    ax.set_title(f"Distribution of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    return fig

if __name__ == "__main__":
    main()
