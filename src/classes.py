import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from abc import ABC, abstractmethod


class AnalysisStrategy(ABC):
    @abstractmethod
    def analyse(self, df):
        pass


class RegressionAnalysis(AnalysisStrategy):
    def analyse(self, df):
        feature = df[["MRO Rate (%)"]]
        target = df[["German 10-Year Government Bond Yields (%)"]]

        feature_with_intercept = sm.add_constant(feature)
        model = sm.OLS(target, feature_with_intercept).fit()

        summary = {
            "R_squared": model.rsquared,
            "Adj. R-squared": model.rsquared_adj,
            "F-statistic": model.fvalue,
            "P-value": model.f_pvalue,
            "Intercept": model.params[0],
            "Slope (MRO Rate)": model.params[1]
        }

        summary_df = pd.DataFrame(summary.items(), columns=["Metric", "Value"])
        return summary_df


class BondWizard:
    """A class to encapsulate visualization functions for bond yields and MRO rate analysis."""

    def __init__(self, df, t, language, analysis_strategy: AnalysisStrategy):
        self.df = df
        self.t = t
        self.language = language
        self.analysis_strategy = analysis_strategy

    def plot_time_series(self):
        """Plot German Bond Yields & MRO Rate Over Time"""
        st.write(f"## {self.t['time_series']}")
        fig = px.line(self.df, x="Date", y=["German 10-Year Government Bond Yields (%)", "MRO Rate (%)"],
                      title=self.t["time_series"])
        st.plotly_chart(fig, use_container_width=True)

    def plot_scatter_mro_vs_bonds(self):
        """Scatter plot of MRO Rate vs. German Bond Yields"""
        st.write(f"## {self.t['scatter_plot']}")
        fig = px.scatter(self.df, x="MRO Rate (%)", y="German 10-Year Government Bond Yields (%)",
                         trendline="ols", title=self.t["scatter_plot"])
        st.plotly_chart(fig, use_container_width=True)

    def plot_correlation_matrix(self):
        """Plot correlation matrix heatmap with better formatting"""
        st.write(f"## {self.t['correlation']}")

        corr_df = self.df.drop(columns=["Date"], errors="ignore")
        corr_matrix = corr_df.corr()

        fig, ax = plt.subplots(figsize=(6, 4))

        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax, fmt=".2f", linewidths=0.5)
        ax.set_title(self.t["correlation"], fontsize=14)

        st.pyplot(fig)

    def regression_summary(self):
        """Use the injected strategy to analyze data"""
        summary_df = self.analysis_strategy.analyse(self.df)
        st.write(f"### Regression Summary")
        st.table(summary_df.style.format(precision=4))

    def plot_all(self):
        col1, col2 = st.columns(2)

        with col1:
            self.plot_time_series()

        with col2:
            self.plot_scatter_mro_vs_bonds()

        self.regression_summary()
        self.plot_correlation_matrix()

