"""
Example Usage of S&P GSCI Implementation
Quantitative Investment Strategy Structurer

This script demonstrates practical usage of the S&P GSCI implementation
"""

from datetime import date, timedelta
import numpy as np
import pandas as pd
from sp_gsci_implementation import SPGSCICalculator, SPGSCIPortfolioManager
from config import SPGSCIConfig


def example_basic_calculations():
    """Example of basic S&P GSCI calculations"""
    print("=== Basic S&P GSCI Calculations ===")
    
    # Initialize calculator
    calculator = SPGSCICalculator()
    
    # Set up dates
    current_date = date(2024, 1, 15)
    previous_date = date(2024, 1, 14)
    
    # Calculate index return
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
    
    # Calculate enhanced index
    enhanced_level = calculator.calculate_enhanced_index(
        current_date, previous_date, previous_level
    )
    print(f"Enhanced Index: {enhanced_level:.2f}")


def example_portfolio_management():
    """Example of portfolio management"""
    print("\n=== Portfolio Management ===")
    
    # Initialize calculator and portfolio manager
    calculator = SPGSCICalculator()
    portfolio_manager = SPGSCIPortfolioManager(calculator)
    
    # Set up dates
    target_date = date(2024, 1, 15)
    previous_date = date(2024, 1, 14)
    
    # Construct portfolio
    target_notional = 1000000.0  # $1M notional
    positions = portfolio_manager.construct_portfolio(target_date, target_notional)
    
    print(f"Portfolio constructed with {len(positions)} positions")
    print(f"Target notional: ${target_notional:,.2f}")
    
    # Calculate portfolio metrics
    portfolio_value = portfolio_manager.calculate_portfolio_value(positions, target_date)
    portfolio_return = portfolio_manager.calculate_portfolio_return(
        positions, target_date, previous_date
    )
    
    print(f"Portfolio Value: ${portfolio_value:,.2f}")
    print(f"Portfolio Return: {portfolio_return:.4f}")
    
    # Show top positions
    print("\nTop 5 Positions:")
    sorted_positions = sorted(positions.items(), key=lambda x: x[1], reverse=True)
    for symbol, size in sorted_positions[:5]:
        print(f"  {symbol}: {size:,.0f} contracts")


def example_rolling_analysis():
    """Example of rolling analysis"""
    print("\n=== Rolling Analysis ===")
    
    calculator = SPGSCICalculator()
    
    # Analyze rolling for different commodities
    commodities = ['WTI', 'GOLD', 'CORN']
    analysis_date = date(2024, 1, 15)
    
    for commodity in commodities:
        rolling_adjustment = calculator.calculate_rolling_adjustment(commodity, analysis_date)
        print(f"{commodity} Rolling Adjustment: {rolling_adjustment:.4f}")


def example_market_disruption_handling():
    """Example of market disruption event handling"""
    print("\n=== Market Disruption Event Handling ===")
    
    calculator = SPGSCICalculator()
    
    # Check for MDEs on different commodities
    commodities = ['WTI', 'GOLD', 'CORN']
    check_date = date(2024, 1, 15)
    
    for commodity in commodities:
        has_mde = calculator.handle_market_disruption_events(commodity, check_date)
        status = "MDE DETECTED" if has_mde else "No MDE"
        print(f"{commodity}: {status}")


def example_configuration_usage():
    """Example of configuration usage"""
    print("\n=== Configuration Usage ===")
    
    # Validate configuration
    is_valid = SPGSCIConfig.validate_config()
    print(f"Configuration Valid: {is_valid}")
    
    # Get commodity configurations
    commodities = ['WTI', 'GOLD', 'CORN']
    
    for commodity in commodities:
        config = SPGSCIConfig.get_commodity_config(commodity)
        weight = SPGSCIConfig.get_commodity_weight(commodity)
        
        if config:
            print(f"{commodity}:")
            print(f"  Exchange: {config.exchange}")
            print(f"  Contract Size: {config.contract_size}")
            print(f"  Weight: {weight:.3f}")
            print(f"  Currency: {config.currency}")


def example_time_series_analysis():
    """Example of time series analysis"""
    print("\n=== Time Series Analysis ===")
    
    calculator = SPGSCICalculator()
    
    # Generate time series
    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 31)
    current_date = start_date
    
    index_levels = []
    dates = []
    previous_level = 100.0
    
    while current_date <= end_date:
        if current_date > start_date:
            current_level = calculator.calculate_index_level(
                current_date, current_date - timedelta(days=1), previous_level
            )
            index_levels.append(current_level)
            dates.append(current_date)
            previous_level = current_level
        
        current_date += timedelta(days=1)
    
    # Calculate statistics
    returns = np.diff(np.log(index_levels))
    
    print(f"Analysis Period: {start_date} to {end_date}")
    print(f"Number of observations: {len(index_levels)}")
    print(f"Final Index Level: {index_levels[-1]:.2f}")
    print(f"Total Return: {(index_levels[-1] / 100.0 - 1) * 100:.2f}%")
    print(f"Average Daily Return: {np.mean(returns) * 100:.4f}%")
    print(f"Daily Volatility: {np.std(returns) * 100:.4f}%")
    print(f"Sharpe Ratio: {np.mean(returns) / np.std(returns):.4f}")


def example_risk_analysis():
    """Example of risk analysis"""
    print("\n=== Risk Analysis ===")
    
    # Get risk parameters from config
    max_position = SPGSCIConfig.MAX_POSITION_SIZE
    max_sector = SPGSCIConfig.MAX_SECTOR_WEIGHT
    target_vol = SPGSCIConfig.TARGET_VOLATILITY
    max_drawdown = SPGSCIConfig.MAX_DRAWDOWN
    
    print(f"Risk Management Parameters:")
    print(f"  Max Position Size: {max_position * 100:.0f}%")
    print(f"  Max Sector Weight: {max_sector * 100:.0f}%")
    print(f"  Target Volatility: {target_vol * 100:.0f}%")
    print(f"  Max Drawdown: {max_drawdown * 100:.0f}%")
    
    # Analyze commodity weights
    weights = SPGSCIConfig.COMMODITY_WEIGHTS
    sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nLargest Commodity Exposures:")
    for commodity, weight in sorted_weights[:5]:
        print(f"  {commodity}: {weight * 100:.1f}%")
    
    # Check for concentration risk
    top_5_weight = sum(weight for _, weight in sorted_weights[:5])
    print(f"\nTop 5 Concentration: {top_5_weight * 100:.1f}%")


def main():
    """Main function to run all examples"""
    print("S&P GSCI Implementation Examples")
    print("=" * 50)
    
    try:
        # Run all examples
        example_basic_calculations()
        example_portfolio_management()
        example_rolling_analysis()
        example_market_disruption_handling()
        example_configuration_usage()
        example_time_series_analysis()
        example_risk_analysis()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Please check your configuration and data sources.")


if __name__ == "__main__":
    main()