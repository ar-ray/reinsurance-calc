# ReinsuranceCalc 📊

A Python-based treaty reinsurance premium calculator designed for reinsurance brokers to quickly analyze and compare different treaty structures.

## 🎯 Features

- **Multiple Treaty Types Support**
  - Quota Share treaties with commission calculations
  - Surplus Share treaties with line limits
  - Excess of Loss (XOL) with reinstatements
  
- **Comprehensive Analysis**
  - Premium and claims distribution calculations
  - Profit commission calculations
  - Multi-period cashflow analysis
  - Loss ratio tracking

- **Export Capabilities**
  - Excel report generation
  - PDF summaries
  - Interactive visualizations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/reinsurance-calc.git
cd reinsurance-calc
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from reinsurance_calc.treaties.quota_share import QuotaShareTreaty

# Create a quota share treaty
treaty = QuotaShareTreaty(
    cession_rate=40,  # 40% cession
    commission_rate=27.5,  # 27.5% commission
    profit_commission_rate=15,
    annual_aggregate_limit=5_000_000
)

# Calculate premium distribution
result = treaty.calculate_premium(gross_premium=1_000_000)
print(f"Ceded Premium: ${result['ceded_premium']:,.2f}")
print(f"Net to Reinsurer: ${result['net_premium_to_reinsurer']:,.2f}")
```

## 📁 Project Structure

```
reinsurance-calc/
├── src/
│   └── reinsurance_calc/
│       ├── treaties/        # Treaty calculation modules
│       ├── utils/          # Validation and helper functions
│       └── reports/        # Report generation
├── tests/                  # Unit tests
├── examples/               # Usage examples
└── docs/                   # Documentation
```

## 📊 Example Output

### Quota Share Analysis
```
Period     Gross_Premium  Ceded_Premium  Reinsurer_Claims  Loss_Ratio
Q1 2024    2,500,000     1,250,000      750,000          60.0%
Q2 2024    3,000,000     1,500,000      900,000          60.0%
Q3 2024    2,800,000     1,400,000      1,050,000        75.0%
Q4 2024    3,200,000     1,600,000      950,000          59.4%
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

With coverage report:
```bash
pytest tests/ --cov=reinsurance_calc --cov-report=html
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 Roadmap

- [ ] Add Excess of Loss (XOL) calculations
- [ ] Implement Stop Loss treaties
- [ ] Add Monte Carlo simulation for aggregate analysis
- [ ] Create web API endpoint
- [ ] Build interactive dashboard
- [ ] Add Solvency II capital calculations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Amiya Ranjan Ray - Initial work - [ar-ray](https://github.com/ar-ray)

## 🙏 Acknowledgments

- Inspired by real-world reinsurance broking challenges
- Built for the reinsurance broking community

## 📧 Contact

For questions or suggestions, please open an issue or contact: amiya.ranjan.ray@gmail.com

---
*Made with ❤️ for the reinsurance broking industry*