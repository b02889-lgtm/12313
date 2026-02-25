#!/usr/bin/env python3
"""
Statistics Calculator - Statistical analysis tools
Supports descriptive statistics, distributions, and hypothesis testing
"""

import math
import numpy as np
from scipy import stats


class StatisticsCalculator:
    """Statistical analysis calculator"""
    
    def __init__(self):
        pass
    
    def mean(self, data):
        """Calculate arithmetic mean"""
        return np.mean(data)
    
    def median(self, data):
        """Calculate median"""
        return np.median(data)
    
    def mode(self, data):
        """Calculate mode"""
        return stats.mode(data, keepdims=True).mode[0]
    
    def variance(self, data, ddof=1):
        """Calculate variance (sample variance by default)"""
        return np.var(data, ddof=ddof)
    
    def standard_deviation(self, data, ddof=1):
        """Calculate standard deviation (sample std dev by default)"""
        return np.std(data, ddof=ddof)
    
    def percentile(self, data, q):
        """Calculate q-th percentile (0-100)"""
        return np.percentile(data, q)
    
    def skewness(self, data):
        """Calculate skewness"""
        return stats.skew(data)
    
    def kurtosis(self, data):
        """Calculate kurtosis"""
        return stats.kurtosis(data)
    
    def correlation(self, x, y):
        """Calculate Pearson correlation coefficient"""
        return np.corrcoef(x, y)[0, 1]
    
    def spearman_correlation(self, x, y):
        """Calculate Spearman rank correlation"""
        return stats.spearmanr(x, y).correlation
    
    def z_score(self, x, mean, std_dev):
        """Calculate Z-score"""
        return (x - mean) / std_dev
    
    def linear_regression(self, x, y):
        """
        Perform simple linear regression: y = slope * x + intercept
        
        Returns:
            dict: {slope, intercept, r_value, p_value, std_err}
        """
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        return {
            "slope": slope,
            "intercept": intercept,
            "r_value": r_value,
            "r_squared": r_value**2,
            "p_value": p_value,
            "std_err": std_err
        }
    
    def t_test_1samp(self, data, popmean):
        """One-sample T-test"""
        t_stat, p_val = stats.ttest_1samp(data, popmean)
        return t_stat, p_val
    
    def t_test_ind(self, data1, data2):
        """Independent two-sample T-test"""
        t_stat, p_val = stats.ttest_ind(data1, data2)
        return t_stat, p_val
    
    def chi_square_test(self, observed, expected=None):
        """Chi-square test of independence"""
        chi2, p_val = stats.chisquare(observed, f_exp=expected)
        return chi2, p_val
    
    def normal_pdf(self, x, mean=0, std=1):
        """Normal distribution PDF"""
        return stats.norm.pdf(x, mean, std)
    
    def normal_cdf(self, x, mean=0, std=1):
        """Normal distribution CDF"""
        return stats.norm.cdf(x, mean, std)
    
    def binomial_pmf(self, k, n, p):
        """Binomial distribution PMF (probability of k successes in n trials with prob p)"""
        return stats.binom.pmf(k, n, p)


def main():
    """Example usage"""
    calc = StatisticsCalculator()
    
    # Sample data
    data = [23, 25, 27, 29, 31, 33, 35, 37, 39, 41]
    
    print("Dataset:", data)
    print(f"Mean: {calc.mean(data)}")
    print(f"Median: {calc.median(data)}")
    print(f"Std Dev: {calc.standard_deviation(data)}")
    
    # Linear Regression
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]
    print("\nLinear Regression (x=[1-5], y=[2,4,5,4,5]):")
    result = calc.linear_regression(x, y)
    print(f"Slope: {result['slope']}")
    print(f"Intercept: {result['intercept']}")
    print(f"R-squared: {result['r_squared']}")


if __name__ == "__main__":
    main()