# QuantumFolio
QuantumFolio - Advanced Portfolio Optimization Tool Based on Black-Litterman Model

Author: Muskaan Kathuria 
---

Description

QuantumFolio is an advanced portfolio optimization tool designed to help portfolio managers, quantitative analysts, and investors integrate market data with subjective views using the **Black-Litterman (BL)** model. The tool combines historical market data with personal forecasts to generate optimized portfolios under various risk constraints and optimization methodologies. 

The Black-Litterman model is a Bayesian framework that integrates investor views with market equilibrium data to produce updated expected returns and covariance matrices. This enables more consistent and diversified portfolio allocations, making it ideal for both technical users and non-technical portfolio managers looking to make informed investment decisions.

QuantumFolio supports automated data fetching from Yahoo Finance, advanced risk metrics like Value-at-Risk (VaR) and Conditional VaR (CVaR), and dynamic visualizations to provide clear insights into portfolio performance.

1. Black-Litterman Model: Combines historical data with subjective views to optimize portfolios.
2. Risk Metrics: Calculates advanced risk metrics such as VaR and CVaR.
3. Portfolio Optimization Techniques: Supports Mean-Variance Optimization, Efficient Frontier Analysis, and more.
4. Dynamic Visualizations: Provides clear, intuitive graphs for portfolio allocations, risk-return tradeoffs, and more.
5. Real-World Constraints: Incorporates constraints like no short-selling, sector caps, and transaction costs.
6. Automated Data Fetching: Pulls real-time data from Yahoo Finance or proprietary data from CSV files.
7. Customizable Configurations: Easily adjust assets, views, and risk preferences using the `config.json` file.

---

Step 1: Install Required Libraries
Run the following command in your terminal to install the necessary Python libraries:

```bash
pip install numpy pandas yfinance matplotlib seaborn scipy PyPortfolioOpt
```

---

Project Structure

```
QuantumFolio/
|├── config.json        # Configuration file for assets, views, and risk preferences
|├── main.py            # Main script to run the portfolio optimization
|└── README.md          # Documentation and instructions
```

---

Configuration File (`config.json`)

The `config.json` file is where you customize your assets, investor views, and risk preferences.

Sample `config.json`:

```json
{
  "assets": ["IVV", "AGG", "EFA", "IEMG", "IJH"],
  "start_date": "2018-01-01",
  "end_date": "2023-12-31",
  "risk_aversion": 2.5,
  "investor_views": {
    "IVV": 0.02,
    "EFA": -0.01,
    "AGG": 0.015,
    "IEMG": 0.025
  },
  "confidence_levels": {
    "IVV": 0.0001,
    "EFA": 0.0001,
    "AGG": 0.0002,
    "IEMG": 0.00015
  }
}
```

Explanation of Config Fields:
- `assets`: List of ticker symbols (e.g., iShares ETFs).
- `start_date` / `end_date`: Date range for historical data.
- `risk_aversion`: Determines the trade-off between risk and return.
- `investor_views`: Your expectations on asset returns.
- `confidence_levels`: How confident you are in your views (lower value = higher confidence).

---

Running QuantumFolio

Step 1: Run the Script
Execute the script from your terminal:

```bash
python main.py
```

---

Output and Visualization

1. Optimized Portfolio Weights:
   - Displays the optimal asset allocations based on the Black-Litterman model.

2. Risk Metrics:
   - Value at Risk (VaR) and Conditional VaR (CVaR) provide insights into potential losses.

3. Visualizations:
   - Portfolio Allocation Bar Chart: Shows asset distribution.
   - Correlation Matrix Heatmap:** Displays relationships between assets.
   - Historical Price Trends:** Visualizes historical performance.
   - Efficient Frontier Plot:** Compares risk-return trade-offs.
   - VaR & CVaR Distribution Plot: Visualizes downside risk.

---

Optimization Techniques

1. Black-Litterman Model: Integrates subjective views with market data for balanced portfolios.
2. Mean-Variance Optimization: Finds portfolios with the highest expected return for a given risk.
3. Efficient Frontier Analysis: Visualizes optimal portfolios for different risk levels.
4. Max Sharpe Ratio Portfolio: Maximizes return per unit of risk.
5. Minimum Volatility Portfolio: Minimizes total portfolio risk.

---
Example Use Case

Imagine you believe that:
- The S&P 500 ETF (IVV) will outperform by 2%.
- The MSCI EAFE ETF (EFA) will underperform by 1%.
- You have moderate confidence in your views.

QuantumFolio will integrate these views with historical data to generate optimized portfolio allocations and risk metrics.

---

License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
Contact
For any questions or feature requests, feel free to reach out:
Email: muskaankathuria.n@gmail.com
