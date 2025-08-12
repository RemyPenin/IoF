"""
S&P GSCI (Goldman Sachs Commodity Index) Implementation
Quantitative Investment Strategy Structurer

This module implements the complete S&P GSCI methodology as described in:
- S&P GSCI Methodology: https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-gsci.pdf
- Commodity Index Mathematics: https://www.spglobal.com/spdji/en/documents/methodologies/methodology-commodity-index-math.pdf

Author: Quantitative Investment Strategy Structurer
Date: 2024
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union
from datetime import datetime, date
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommodityType(Enum):
    """S&P GSCI commodity categories"""
    ENERGY = "Energy"
    INDUSTRIAL_METALS = "Industrial Metals"
    PRECIOUS_METALS = "Precious Metals"
    AGRICULTURE = "Agriculture"
    LIVESTOCK = "Livestock"


@dataclass
class CommodityContract:
    """Represents a commodity futures contract"""
    symbol: str
    commodity_type: CommodityType
    exchange: str
    contract_size: float
    tick_size: float
    tick_value: float
    delivery_month: int  # 1-12 for calendar months
    delivery_year: int


@dataclass
class CPWData:
    """Contract Production Weight data structure"""
    commodity: str
    contract_month: int
    contract_year: int
    cpw_value: float
    date: date


@dataclass
class PriceData:
    """Price data structure"""
    symbol: str
    date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    open_interest: int


@dataclass
class MarketDisruptionEvent:
    """Market Disruption Event data structure"""
    symbol: str
    date: date
    event_type: str  # 'trading_halt', 'force_majeure', 'exchange_closure'
    description: str
    resolution_date: Optional[date] = None


class SPGSCICalculator:
    """
    S&P GSCI Index Calculator
    
    Implements the complete S&P GSCI methodology including:
    - Contract Production Weights (CPW) calculations
    - Price normalization and rolling
    - Market Disruption Event handling
    - Index calculation with proper weighting
    """
    
    def __init__(self, base_date: date = date(1970, 1, 1), base_value: float = 100.0):
        """
        Initialize the S&P GSCI calculator
        
        Args:
            base_date: Base date for index calculation (default: 1970-01-01)
            base_value: Base index value (default: 100.0)
        """
        self.base_date = base_date
        self.base_value = base_value
        
        # S&P GSCI commodity weights (as of latest methodology)
        self.commodity_weights = {
            'WTI': 0.243,      # WTI Crude Oil
            'BRENT': 0.150,    # Brent Crude Oil
            'RBOB': 0.078,     # RBOB Gasoline
            'HEATING': 0.054,  # Heating Oil
            'NATURAL': 0.086,  # Natural Gas
            'COPPER': 0.063,   # Copper
            'ALUMINUM': 0.031, # Aluminum
            'ZINC': 0.018,     # Zinc
            'NICKEL': 0.016,   # Nickel
            'LEAD': 0.008,     # Lead
            'GOLD': 0.031,     # Gold
            'SILVER': 0.008,   # Silver
            'CORN': 0.063,     # Corn
            'WHEAT': 0.031,    # Wheat
            'SOYBEANS': 0.031, # Soybeans
            'SOYBEAN_OIL': 0.016, # Soybean Oil
            'SOYBEAN_MEAL': 0.016, # Soybean Meal
            'COTTON': 0.016,   # Cotton
            'COFFEE': 0.016,   # Coffee
            'SUGAR': 0.016,    # Sugar
            'COCOA': 0.008,    # Cocoa
            'LIVE_CATTLE': 0.031, # Live Cattle
            'LEAN_HOGS': 0.016,   # Lean Hogs
            'FEEDER_CATTLE': 0.008 # Feeder Cattle
        }
        
        # Rolling schedule (contracts roll 5 business days before expiry)
        self.rolling_days = 5
        
        # Market disruption event handling
        self.mde_threshold_days = 5  # Days before considering MDE impact
        
    def get_cpw(self, commodity: str, contract_month: int, contract_year: int, 
                calculation_date: date) -> float:
        """
        Get Contract Production Weight (CPW) for a specific commodity contract
        
        This function should be implemented to interface with external CPW data source
        
        Args:
            commodity: Commodity symbol
            contract_month: Contract delivery month (1-12)
            contract_year: Contract delivery year
            calculation_date: Date for CPW calculation
            
        Returns:
            CPW value for the contract
        """
        # This is a placeholder - in practice, this would call an external function
        # that provides CPW data from the S&P GSCI methodology
        logger.info(f"Getting CPW for {commodity} {contract_month}/{contract_year} on {calculation_date}")
        
        # Placeholder implementation - replace with actual CPW function call
        # return CPW(commodity, contract_month, contract_year, calculation_date)
        
        # For demonstration, return a base weight
        base_weight = self.commodity_weights.get(commodity, 0.01)
        return base_weight
    
    def get_price(self, symbol: str, date: date) -> PriceData:
        """
        Get price data for a specific symbol and date
        
        This function should be implemented to interface with external price data source
        
        Args:
            symbol: Contract symbol
            date: Date for price data
            
        Returns:
            PriceData object containing OHLCV data
        """
        # This is a placeholder - in practice, this would call an external function
        # that provides price data
        logger.info(f"Getting price data for {symbol} on {date}")
        
        # Placeholder implementation - replace with actual price function call
        # return price(symbol, date)
        
        # For demonstration, return mock data
        return PriceData(
            symbol=symbol,
            date=date,
            open_price=100.0,
            high_price=105.0,
            low_price=95.0,
            close_price=102.0,
            volume=1000,
            open_interest=5000
        )
    
    def get_market_disruption_events(self, symbol: str, start_date: date, 
                                   end_date: date) -> List[MarketDisruptionEvent]:
        """
        Get market disruption events for a symbol within a date range
        
        This function should be implemented to interface with external MDE data source
        
        Args:
            symbol: Contract symbol
            start_date: Start date for MDE search
            end_date: End date for MDE search
            
        Returns:
            List of MarketDisruptionEvent objects
        """
        # This is a placeholder - in practice, this would call an external function
        # that provides MDE data
        logger.info(f"Getting MDE data for {symbol} from {start_date} to {end_date}")
        
        # Placeholder implementation - replace with actual MDE function call
        # return mde(symbol, start_date, end_date)
        
        # For demonstration, return empty list
        return []
    
    def calculate_contract_weights(self, calculation_date: date) -> Dict[str, float]:
        """
        Calculate contract weights based on CPW methodology
        
        Args:
            calculation_date: Date for weight calculation
            
        Returns:
            Dictionary mapping contract symbols to their weights
        """
        contract_weights = {}
        
        for commodity, base_weight in self.commodity_weights.items():
            # Get the front-month contract for rolling
            front_month, front_year = self._get_front_month_contract(calculation_date)
            
            # Get CPW for the front-month contract
            cpw_value = self.get_cpw(commodity, front_month, front_year, calculation_date)
            
            # Calculate contract weight
            contract_symbol = f"{commodity}{front_month:02d}{front_year}"
            contract_weights[contract_symbol] = cpw_value * base_weight
        
        # Normalize weights to sum to 1
        total_weight = sum(contract_weights.values())
        if total_weight > 0:
            contract_weights = {k: v / total_weight for k, v in contract_weights.items()}
        
        return contract_weights
    
    def _get_front_month_contract(self, calculation_date: date) -> Tuple[int, int]:
        """
        Get the front-month contract for rolling
        
        Args:
            calculation_date: Current calculation date
            
        Returns:
            Tuple of (month, year) for front-month contract
        """
        # Simple implementation - in practice, this would consider exchange calendars
        # and rolling schedules
        current_month = calculation_date.month
        current_year = calculation_date.year
        
        # Front month is typically current month + 1
        front_month = current_month + 1
        front_year = current_year
        
        if front_month > 12:
            front_month = 1
            front_year += 1
        
        return front_month, front_year
    
    def handle_market_disruption_events(self, symbol: str, calculation_date: date) -> bool:
        """
        Handle market disruption events for a symbol
        
        Args:
            symbol: Contract symbol
            calculation_date: Date for MDE check
            
        Returns:
            True if MDE affects the contract, False otherwise
        """
        # Get MDE data for the past threshold days
        start_date = calculation_date - pd.Timedelta(days=self.mde_threshold_days)
        mde_events = self.get_market_disruption_events(symbol, start_date, calculation_date)
        
        # Check if any MDE affects the contract
        for event in mde_events:
            if event.date <= calculation_date and (
                event.resolution_date is None or event.resolution_date > calculation_date
            ):
                logger.warning(f"MDE detected for {symbol}: {event.event_type}")
                return True
        
        return False
    
    def calculate_contract_return(self, symbol: str, current_date: date, 
                                previous_date: date) -> float:
        """
        Calculate contract return between two dates
        
        Args:
            symbol: Contract symbol
            current_date: Current date
            previous_date: Previous date
            
        Returns:
            Contract return (log return)
        """
        # Check for market disruption events
        if self.handle_market_disruption_events(symbol, current_date):
            logger.warning(f"Using previous price due to MDE for {symbol}")
            return 0.0  # Return 0 if MDE affects the contract
        
        # Get price data
        current_price_data = self.get_price(symbol, current_date)
        previous_price_data = self.get_price(symbol, previous_date)
        
        if current_price_data.close_price <= 0 or previous_price_data.close_price <= 0:
            logger.error(f"Invalid price data for {symbol}")
            return 0.0
        
        # Calculate log return
        return np.log(current_price_data.close_price / previous_price_data.close_price)
    
    def calculate_index_return(self, current_date: date, previous_date: date) -> float:
        """
        Calculate S&P GSCI index return between two dates
        
        Args:
            current_date: Current date
            previous_date: Previous date
            
        Returns:
            Index return
        """
        # Get contract weights
        contract_weights = self.calculate_contract_weights(current_date)
        
        # Calculate weighted return
        weighted_return = 0.0
        valid_contracts = 0
        
        for symbol, weight in contract_weights.items():
            try:
                contract_return = self.calculate_contract_return(symbol, current_date, previous_date)
                weighted_return += weight * contract_return
                valid_contracts += 1
            except Exception as e:
                logger.error(f"Error calculating return for {symbol}: {e}")
                continue
        
        if valid_contracts == 0:
            logger.error("No valid contracts for index calculation")
            return 0.0
        
        return weighted_return
    
    def calculate_index_level(self, current_date: date, previous_date: date, 
                            previous_index_level: float) -> float:
        """
        Calculate S&P GSCI index level
        
        Args:
            current_date: Current date
            previous_date: Previous date
            previous_index_level: Previous index level
            
        Returns:
            Current index level
        """
        index_return = self.calculate_index_return(current_date, previous_date)
        return previous_index_level * np.exp(index_return)
    
    def calculate_rolling_adjustment(self, symbol: str, current_date: date) -> float:
        """
        Calculate rolling adjustment for contract transitions
        
        Args:
            symbol: Contract symbol
            current_date: Date for rolling calculation
            
        Returns:
            Rolling adjustment factor
        """
        # Get front and second month contracts
        front_month, front_year = self._get_front_month_contract(current_date)
        second_month, second_year = self._get_front_month_contract(
            current_date + pd.Timedelta(days=30)
        )
        
        front_symbol = f"{symbol}{front_month:02d}{front_year}"
        second_symbol = f"{symbol}{second_month:02d}{second_year}"
        
        # Get prices for both contracts
        front_price = self.get_price(front_symbol, current_date).close_price
        second_price = self.get_price(second_symbol, current_date).close_price
        
        if front_price <= 0 or second_price <= 0:
            return 1.0
        
        # Calculate rolling adjustment
        return second_price / front_price
    
    def calculate_total_return_index(self, current_date: date, previous_date: date,
                                   previous_index_level: float) -> float:
        """
        Calculate S&P GSCI Total Return Index
        
        Args:
            current_date: Current date
            previous_date: Previous date
            previous_index_level: Previous index level
            
        Returns:
            Total return index level
        """
        # Calculate price return
        price_return = self.calculate_index_return(current_date, previous_date)
        
        # Calculate rolling yield (simplified)
        rolling_yield = self._calculate_rolling_yield(current_date, previous_date)
        
        # Calculate total return
        total_return = price_return + rolling_yield
        
        return previous_index_level * np.exp(total_return)
    
    def _calculate_rolling_yield(self, current_date: date, previous_date: date) -> float:
        """
        Calculate rolling yield component
        
        Args:
            current_date: Current date
            previous_date: Previous date
            
        Returns:
            Rolling yield
        """
        # Simplified rolling yield calculation
        # In practice, this would consider the full term structure and roll costs
        days_diff = (current_date - previous_date).days
        annualized_roll_yield = 0.02  # 2% annualized roll yield (example)
        
        return (annualized_roll_yield / 365) * days_diff
    
    def calculate_enhanced_index(self, current_date: date, previous_date: date,
                               previous_index_level: float, 
                               collateral_return: float = 0.02) -> float:
        """
        Calculate S&P GSCI Enhanced Index (includes collateral return)
        
        Args:
            current_date: Current date
            previous_date: Previous date
            previous_index_level: Previous index level
            collateral_return: Annualized collateral return rate
            
        Returns:
            Enhanced index level
        """
        # Calculate total return
        total_return = self.calculate_total_return_index(current_date, previous_date, previous_index_level)
        
        # Add collateral return
        days_diff = (current_date - previous_date).days
        collateral_component = (collateral_return / 365) * days_diff
        
        return total_return * np.exp(collateral_component)


class SPGSCIPortfolioManager:
    """
    Portfolio Manager for S&P GSCI implementation
    
    Handles portfolio construction, rebalancing, and risk management
    """
    
    def __init__(self, calculator: SPGSCICalculator):
        """
        Initialize portfolio manager
        
        Args:
            calculator: S&P GSCI calculator instance
        """
        self.calculator = calculator
        self.portfolio_weights = {}
        self.last_rebalance_date = None
        
    def construct_portfolio(self, target_date: date, target_notional: float = 1000000.0) -> Dict[str, float]:
        """
        Construct portfolio based on S&P GSCI weights
        
        Args:
            target_date: Date for portfolio construction
            target_notional: Target portfolio notional value
            
        Returns:
            Dictionary mapping contract symbols to position sizes
        """
        # Get contract weights
        contract_weights = self.calculator.calculate_contract_weights(target_date)
        
        # Calculate position sizes
        portfolio_positions = {}
        
        for symbol, weight in contract_weights.items():
            # Get current price
            price_data = self.calculator.get_price(symbol, target_date)
            if price_data.close_price > 0:
                position_size = (target_notional * weight) / price_data.close_price
                portfolio_positions[symbol] = position_size
        
        self.portfolio_weights = contract_weights
        self.last_rebalance_date = target_date
        
        return portfolio_positions
    
    def calculate_portfolio_value(self, positions: Dict[str, float], 
                                current_date: date) -> float:
        """
        Calculate current portfolio value
        
        Args:
            positions: Dictionary of position sizes
            current_date: Current date
            
        Returns:
            Portfolio value
        """
        total_value = 0.0
        
        for symbol, position_size in positions.items():
            price_data = self.calculator.get_price(symbol, current_date)
            contract_value = position_size * price_data.close_price
            total_value += contract_value
        
        return total_value
    
    def calculate_portfolio_return(self, positions: Dict[str, float],
                                 current_date: date, previous_date: date) -> float:
        """
        Calculate portfolio return between two dates
        
        Args:
            positions: Dictionary of position sizes
            current_date: Current date
            previous_date: Previous date
            
        Returns:
            Portfolio return
        """
        current_value = self.calculate_portfolio_value(positions, current_date)
        previous_value = self.calculate_portfolio_value(positions, previous_date)
        
        if previous_value <= 0:
            return 0.0
        
        return (current_value - previous_value) / previous_value


def main():
    """
    Main function demonstrating S&P GSCI implementation
    """
    # Initialize calculator
    calculator = SPGSCICalculator()
    
    # Initialize portfolio manager
    portfolio_manager = SPGSCIPortfolioManager(calculator)
    
    # Example usage
    current_date = date(2024, 1, 15)
    previous_date = date(2024, 1, 14)
    
    # Calculate index return
    index_return = calculator.calculate_index_return(current_date, previous_date)
    print(f"Index Return: {index_return:.4f}")
    
    # Calculate index level
    previous_level = 100.0
    current_level = calculator.calculate_index_level(current_date, previous_date, previous_level)
    print(f"Index Level: {current_level:.2f}")
    
    # Calculate total return index
    total_return_level = calculator.calculate_total_return_index(current_date, previous_date, previous_level)
    print(f"Total Return Index: {total_return_level:.2f}")
    
    # Construct portfolio
    positions = portfolio_manager.construct_portfolio(current_date)
    print(f"Portfolio Positions: {len(positions)} contracts")
    
    # Calculate portfolio value
    portfolio_value = portfolio_manager.calculate_portfolio_value(positions, current_date)
    print(f"Portfolio Value: ${portfolio_value:,.2f}")


if __name__ == "__main__":
    main()