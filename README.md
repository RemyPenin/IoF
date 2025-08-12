# S&P GSCI (Goldman Sachs Commodity Index) Implementation

## Overview

This is a comprehensive implementation of the S&P GSCI methodology for quantitative investment strategy structuring in a banking environment. The implementation follows the official S&P GSCI methodology documents:

- [S&P GSCI Methodology](https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-gsci.pdf)
- [Commodity Index Mathematics](https://www.spglobal.com/spdji/en/documents/methodologies/methodology-commodity-index-math.pdf)

## Features

### Core Functionality
- **Contract Production Weights (CPW)**: Implements the CPW methodology for commodity weighting
- **Price Data Integration**: Handles price data through external function interfaces
- **Market Disruption Events (MDE)**: Manages market disruption events and their impact on index calculation
- **Index Calculation**: Complete S&P GSCI index calculation including:
  - Price Return Index
  - Total Return Index
  - Enhanced Index (with collateral return)
- **Portfolio Management**: Portfolio construction and management based on S&P GSCI weights
- **Risk Management**: Built-in risk management parameters and constraints

### Key Components

#### 1. SPGSCICalculator
The main calculator class that implements the S&P GSCI methodology:

```python
from sp_gsci_implementation import SPGSCICalculator
from datetime import date

calculator = SPGSCICalculator()

# Calculate index return
index_return = calculator.calculate_index_return(
    current_date=date(2024, 1, 15),
    previous_date=date(2024, 1, 14)
)

# Calculate index level
current_level = calculator.calculate_index_level(
    current_date=date(2024, 1, 15),
    previous_date=date(2024, 1, 14),
    previous_index_level=100.0
)
```

#### 2. SPGSCIPortfolioManager
Portfolio management and construction:

```python
from sp_gsci_implementation import SPGSCIPortfolioManager

portfolio_manager = SPGSCIPortfolioManager(calculator)

# Construct portfolio
positions = portfolio_manager.construct_portfolio(
    target_date=date(2024, 1, 15),
    target_notional=1000000.0
)

# Calculate portfolio value
portfolio_value = portfolio_manager.calculate_portfolio_value(
    positions=positions,
    current_date=date(2024, 1, 15)
)
```

#### 3. Configuration Management
Comprehensive configuration system for all parameters:

```python
from config import SPGSCIConfig

# Get commodity configuration
wti_config = SPGSCIConfig.get_commodity_config('WTI')

# Get commodity weight
wti_weight = SPGSCIConfig.get_commodity_weight('WTI')

# Validate configuration
is_valid = SPGSCIConfig.validate_config()
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Required packages (see requirements.txt)

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd sp-gsci-implementation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure external data sources:
   - Update `config.py` with your data provider credentials
   - Implement the external functions for CPW, price, and MDE data

## Usage

### Basic Usage

```python
from sp_gsci_implementation import SPGSCICalculator, SPGSCIPortfolioManager
from datetime import date

# Initialize calculator
calculator = SPGSCICalculator()

# Calculate daily index return
current_date = date(2024, 1, 15)
previous_date = date(2024, 1, 14)

index_return = calculator.calculate_index_return(current_date, previous_date)
print(f"Index Return: {index_return:.4f}")

# Calculate index level
previous_level = 100.0
current_level = calculator.calculate_index_level(
    current_date, previous_date, previous_level
)
print(f"Index Level: {current_level:.2f}")

# Calculate total return index
total_return_level = calculator.calculate_total_return_index(
    current_date, previous_date, previous_level
)
print(f"Total Return Index: {total_return_level:.2f}")
```

### Portfolio Management

```python
# Initialize portfolio manager
portfolio_manager = SPGSCIPortfolioManager(calculator)

# Construct portfolio
target_notional = 1000000.0  # $1M notional
positions = portfolio_manager.construct_portfolio(
    target_date=date(2024, 1, 15),
    target_notional=target_notional
)

# Calculate portfolio metrics
portfolio_value = portfolio_manager.calculate_portfolio_value(
    positions, date(2024, 1, 15)
)

portfolio_return = portfolio_manager.calculate_portfolio_return(
    positions, date(2024, 1, 15), date(2024, 1, 14)
)

print(f"Portfolio Value: ${portfolio_value:,.2f}")
print(f"Portfolio Return: {portfolio_return:.4f}")
```

### Advanced Features

#### Market Disruption Event Handling

```python
# Check for market disruption events
has_mde = calculator.handle_market_disruption_events("WTI", date(2024, 1, 15))
if has_mde:
    print("Market disruption event detected for WTI")
```

#### Rolling Adjustment

```python
# Calculate rolling adjustment
rolling_adjustment = calculator.calculate_rolling_adjustment("WTI", date(2024, 1, 15))
print(f"Rolling Adjustment: {rolling_adjustment:.4f}")
```

## External Data Integration

The implementation is designed to work with external data sources through function interfaces:

### CPW Data Function
```python
def CPW(commodity: str, contract_month: int, contract_year: int, calculation_date: date) -> float:
    """
    Get Contract Production Weight for a specific commodity contract
    
    Args:
        commodity: Commodity symbol
        contract_month: Contract delivery month (1-12)
        contract_year: Contract delivery year
        calculation_date: Date for CPW calculation
        
    Returns:
        CPW value for the contract
    """
    # Implement your CPW data source here
    pass
```

### Price Data Function
```python
def price(symbol: str, date: date) -> PriceData:
    """
    Get price data for a specific symbol and date
    
    Args:
        symbol: Contract symbol
        date: Date for price data
        
    Returns:
        PriceData object containing OHLCV data
    """
    # Implement your price data source here
    pass
```

### Market Disruption Event Function
```python
def mde(symbol: str, start_date: date, end_date: date) -> List[MarketDisruptionEvent]:
    """
    Get market disruption events for a symbol within a date range
    
    Args:
        symbol: Contract symbol
        start_date: Start date for MDE search
        end_date: End date for MDE search
        
    Returns:
        List of MarketDisruptionEvent objects
    """
    # Implement your MDE data source here
    pass
```

## Configuration

The system uses a comprehensive configuration system in `config.py`:

### Commodity Weights
```python
COMMODITY_WEIGHTS = {
    'WTI': 0.243,      # WTI Crude Oil
    'BRENT': 0.150,    # Brent Crude Oil
    'RBOB': 0.078,     # RBOB Gasoline
    # ... more commodities
}
```

### Risk Management Parameters
```python
MAX_POSITION_SIZE = 0.25  # Maximum 25% in any single commodity
MAX_SECTOR_WEIGHT = 0.60  # Maximum 60% in any single sector
TARGET_VOLATILITY = 0.20  # 20% target volatility
```

## Testing

Run the comprehensive test suite:

```bash
python test_sp_gsci.py
```

The test suite includes:
- Unit tests for all components
- Integration tests for complete workflows
- Performance tests for realistic workloads
- Data structure validation tests

## Performance

The implementation is optimized for:
- **Speed**: Efficient calculations using NumPy
- **Memory**: Minimal memory footprint for large datasets
- **Scalability**: Can handle multiple commodities and time periods
- **Accuracy**: Follows S&P GSCI methodology precisely

## Risk Management

Built-in risk management features:
- Position size limits
- Sector concentration limits
- Liquidity thresholds
- Market disruption event handling
- Rolling cost management

## Logging

Comprehensive logging system:
```python
import logging

# Configure logging level
logging.basicConfig(level=logging.INFO)

# Log messages are automatically generated for:
# - Index calculations
# - Portfolio operations
# - Market disruption events
# - Data quality issues
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This implementation is for educational and research purposes. Please ensure compliance with S&P Global's licensing requirements for commercial use.

## Support

For questions or issues:
1. Check the documentation
2. Run the test suite
3. Review the configuration
4. Contact the development team

## Disclaimer

This implementation is provided as-is for educational purposes. Users should:
- Validate all calculations independently
- Ensure compliance with regulatory requirements
- Test thoroughly before production use
- Consult with legal and compliance teams for commercial applications

## Version History

- **v1.0.0**: Initial implementation with core S&P GSCI methodology
- **v1.1.0**: Added portfolio management and risk controls
- **v1.2.0**: Enhanced configuration system and testing framework
