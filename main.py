import json
import numpy as np
import pandas as pd
import yfinance as yf
from pypfopt import risk_models, BlackLittermanModel, EfficientFrontier
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

with open('config.json', 'r') as file:
    config = json.load(file)

assets = config['assets']
start_date = config['start_date']
end_date = config['end_date']
risk_aversion = config['risk_aversion']
investor_views = config['investor_views']
confidence_levels = config['confidence_levels']

data = yf.download(assets, start=start_date, end=end_date)['Adj Close']
returns = data.pct_change().dropna()

cov_matrix = risk_models.sample_cov(returns)
market_caps = {asset: 100e9 for asset in assets}  # Placeholder values
market_weights = pd.Series(market_caps) / sum(market_caps.values())

implied_returns = risk_aversion * cov_matrix.dot(market_weights)
P = np.zeros((len(investor_views), len(assets)))
Q = np.array(list(investor_views.values()))

for i, (asset, view) in enumerate(investor_views.items()):
    P[i, assets.index(asset)] = 1

omega_values = list(confidence_levels.values())
omega = np.diag(omega_values)

bl = BlackLittermanModel(cov_matrix, pi=implied_returns, P=P, Q=Q, omega=omega)
bl_returns = bl.bl_returns()
bl_cov = bl.bl_cov()

ef = EfficientFrontier(bl_returns, bl_cov)
ef.add_constraint(lambda w: w >= 0)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
def calculate_var_cvar(returns, weights, confidence_level=0.95):
    portfolio_return = np.dot(returns.mean(), list(weights.values()))
    portfolio_std = np.sqrt(np.dot(list(weights.values()), np.dot(returns.cov(), list(weights.values()))))
    var = norm.ppf(1 - confidence_level, portfolio_return, portfolio_std)
    cvar = portfolio_return - (portfolio_std * norm.pdf(norm.ppf(confidence_level)) / (1 - confidence_level))
    return var, cvar

var, cvar = calculate_var_cvar(returns, cleaned_weights)

print("Optimized Portfolio Weights:", cleaned_weights)
print(f"Value at Risk (95% confidence): {var:.4f}")
print(f"Conditional VaR (95% confidence): {cvar:.4f}")
plt.figure(figsize=(10, 6))
plt.bar(cleaned_weights.keys(), cleaned_weights.values(), color='skyblue')
plt.title('QuantumFolio - Black-Litterman Optimized Portfolio Allocation')
plt.xlabel('Assets')
plt.ylabel('Allocation')
plt.show()

plt.figure(figsize=(10, 8))
sns.heatmap(returns.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix of Asset Returns')
plt.show()

plt.figure(figsize=(12, 6))
for asset in assets:
    plt.plot(data[asset], label=asset)
plt.title('Historical Price Data of Selected Assets')
plt.xlabel('Date')
plt.ylabel('Adjusted Close Price')
plt.legend()
plt.show()

returns_list = []
risk_list = []
sharpe_ratios = []

for risk_level in np.linspace(0, 0.5, 100):
    ef = EfficientFrontier(bl_returns, bl_cov)
    ef.add_constraint(lambda w: w >= 0)
    ef.efficient_risk(target_volatility=risk_level)
    performance = ef.portfolio_performance()
    returns_list.append(performance[0])  
    risk_list.append(performance[1])     
    sharpe_ratios.append(performance[2]) 

plt.figure(figsize=(10, 6))
plt.plot(risk_list, returns_list, 'b--', label='Efficient Frontier')
plt.scatter(risk_list[np.argmax(sharpe_ratios)], returns_list[np.argmax(sharpe_ratios)], c='red', marker='*', s=200, label='Max Sharpe Ratio Portfolio')
plt.title('Efficient Frontier with Optimized Portfolio')
plt.xlabel('Volatility (Standard Deviation)')
plt.ylabel('Expected Return')
plt.legend()
plt.show()

portfolio_mean = np.dot(returns.mean(), list(cleaned_weights.values()))
portfolio_std = np.sqrt(np.dot(list(cleaned_weights.values()), np.dot(returns.cov(), list(cleaned_weights.values()))))
x = np.linspace(portfolio_mean - 4*portfolio_std, portfolio_mean + 4*portfolio_std, 1000)
y = norm.pdf(x, portfolio_mean, portfolio_std)

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Portfolio Return Distribution')
plt.axvline(var, color='red', linestyle='--', label=f'VaR (95%): {var:.4f}')
plt.axvline(cvar, color='orange', linestyle='--', label=f'CVaR (95%): {cvar:.4f}')
plt.fill_between(x, y, where=(x < var), color='red', alpha=0.3)
plt.fill_between(x, y, where=(x < cvar), color='orange', alpha=0.2)
plt.title('Value at Risk (VaR) and Conditional VaR (CVaR) Visualization')
plt.xlabel('Portfolio Return')
plt.ylabel('Probability Density')
plt.legend()
plt.show()
