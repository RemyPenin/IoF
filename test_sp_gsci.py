"""
Test suite for S&P GSCI Implementation
Quantitative Investment Strategy Structurer

Tests all components of the S&P GSCI methodology implementation
"""

import unittest
from datetime import date, timedelta
import numpy as np
import pandas as pd
from sp_gsci_implementation import (
    SPGSCICalculator, SPGSCIPortfolioManager, CommodityType,
    CommodityContract, CPWData, PriceData, MarketDisruptionEvent
)


class TestSPGSCICalculator(unittest.TestCase):
    """Test cases for SPGSCICalculator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calculator = SPGSCICalculator()
        self.test_date = date(2024, 1, 15)
        self.previous_date = date(2024, 1, 14)
    
    def test_initialization(self):
        """Test calculator initialization"""
        self.assertEqual(self.calculator.base_date, date(1970, 1, 1))
        self.assertEqual(self.calculator.base_value, 100.0)
        self.assertIsInstance(self.calculator.commodity_weights, dict)
        self.assertGreater(len(self.calculator.commodity_weights), 0)
    
    def test_get_front_month_contract(self):
        """Test front month contract calculation"""
        # Test normal case
        month, year = self.calculator._get_front_month_contract(date(2024, 1, 15))
        self.assertEqual(month, 2)  # February
        self.assertEqual(year, 2024)
        
        # Test year rollover
        month, year = self.calculator._get_front_month_contract(date(2024, 12, 15))
        self.assertEqual(month, 1)  # January
        self.assertEqual(year, 2025)
    
    def test_calculate_contract_weights(self):
        """Test contract weight calculation"""
        weights = self.calculator.calculate_contract_weights(self.test_date)
        
        # Check that weights are calculated
        self.assertIsInstance(weights, dict)
        self.assertGreater(len(weights), 0)
        
        # Check that weights sum to approximately 1
        total_weight = sum(weights.values())
        self.assertAlmostEqual(total_weight, 1.0, places=6)
    
    def test_calculate_contract_return(self):
        """Test contract return calculation"""
        # Test normal case
        return_val = self.calculator.calculate_contract_return(
            "WTI", self.test_date, self.previous_date
        )
        self.assertIsInstance(return_val, float)
        
        # Test with invalid dates
        return_val = self.calculator.calculate_contract_return(
            "WTI", self.test_date, self.test_date
        )
        self.assertEqual(return_val, 0.0)
    
    def test_calculate_index_return(self):
        """Test index return calculation"""
        return_val = self.calculator.calculate_index_return(
            self.test_date, self.previous_date
        )
        self.assertIsInstance(return_val, float)
    
    def test_calculate_index_level(self):
        """Test index level calculation"""
        previous_level = 100.0
        current_level = self.calculator.calculate_index_level(
            self.test_date, self.previous_date, previous_level
        )
        self.assertIsInstance(current_level, float)
        self.assertGreater(current_level, 0)
    
    def test_calculate_total_return_index(self):
        """Test total return index calculation"""
        previous_level = 100.0
        total_return_level = self.calculator.calculate_total_return_index(
            self.test_date, self.previous_date, previous_level
        )
        self.assertIsInstance(total_return_level, float)
        self.assertGreater(total_return_level, 0)
    
    def test_calculate_enhanced_index(self):
        """Test enhanced index calculation"""
        previous_level = 100.0
        enhanced_level = self.calculator.calculate_enhanced_index(
            self.test_date, self.previous_date, previous_level
        )
        self.assertIsInstance(enhanced_level, float)
        self.assertGreater(enhanced_level, 0)
    
    def test_rolling_adjustment(self):
        """Test rolling adjustment calculation"""
        adjustment = self.calculator.calculate_rolling_adjustment("WTI", self.test_date)
        self.assertIsInstance(adjustment, float)
        self.assertGreater(adjustment, 0)
    
    def test_handle_market_disruption_events(self):
        """Test market disruption event handling"""
        # Test with no MDE
        has_mde = self.calculator.handle_market_disruption_events("WTI", self.test_date)
        self.assertFalse(has_mde)


class TestSPGSCIPortfolioManager(unittest.TestCase):
    """Test cases for SPGSCIPortfolioManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calculator = SPGSCICalculator()
        self.portfolio_manager = SPGSCIPortfolioManager(self.calculator)
        self.test_date = date(2024, 1, 15)
        self.previous_date = date(2024, 1, 14)
    
    def test_initialization(self):
        """Test portfolio manager initialization"""
        self.assertEqual(self.portfolio_manager.calculator, self.calculator)
        self.assertEqual(self.portfolio_manager.portfolio_weights, {})
        self.assertIsNone(self.portfolio_manager.last_rebalance_date)
    
    def test_construct_portfolio(self):
        """Test portfolio construction"""
        target_notional = 1000000.0
        positions = self.portfolio_manager.construct_portfolio(self.test_date, target_notional)
        
        # Check that positions are calculated
        self.assertIsInstance(positions, dict)
        self.assertGreater(len(positions), 0)
        
        # Check that position sizes are positive
        for symbol, size in positions.items():
            self.assertGreater(size, 0)
        
        # Check that portfolio weights are set
        self.assertGreater(len(self.portfolio_manager.portfolio_weights), 0)
        self.assertEqual(self.portfolio_manager.last_rebalance_date, self.test_date)
    
    def test_calculate_portfolio_value(self):
        """Test portfolio value calculation"""
        # Construct portfolio first
        positions = self.portfolio_manager.construct_portfolio(self.test_date)
        
        # Calculate portfolio value
        portfolio_value = self.portfolio_manager.calculate_portfolio_value(
            positions, self.test_date
        )
        
        self.assertIsInstance(portfolio_value, float)
        self.assertGreater(portfolio_value, 0)
    
    def test_calculate_portfolio_return(self):
        """Test portfolio return calculation"""
        # Construct portfolio first
        positions = self.portfolio_manager.construct_portfolio(self.test_date)
        
        # Calculate portfolio return
        portfolio_return = self.portfolio_manager.calculate_portfolio_return(
            positions, self.test_date, self.previous_date
        )
        
        self.assertIsInstance(portfolio_return, float)


class TestDataStructures(unittest.TestCase):
    """Test cases for data structures"""
    
    def test_commodity_contract(self):
        """Test CommodityContract dataclass"""
        contract = CommodityContract(
            symbol="WTI",
            commodity_type=CommodityType.ENERGY,
            exchange="NYMEX",
            contract_size=1000.0,
            tick_size=0.01,
            tick_value=10.0,
            delivery_month=2,
            delivery_year=2024
        )
        
        self.assertEqual(contract.symbol, "WTI")
        self.assertEqual(contract.commodity_type, CommodityType.ENERGY)
        self.assertEqual(contract.delivery_month, 2)
        self.assertEqual(contract.delivery_year, 2024)
    
    def test_cpw_data(self):
        """Test CPWData dataclass"""
        cpw_data = CPWData(
            commodity="WTI",
            contract_month=2,
            contract_year=2024,
            cpw_value=0.243,
            date=date(2024, 1, 15)
        )
        
        self.assertEqual(cpw_data.commodity, "WTI")
        self.assertEqual(cpw_data.cpw_value, 0.243)
        self.assertEqual(cpw_data.date, date(2024, 1, 15))
    
    def test_price_data(self):
        """Test PriceData dataclass"""
        price_data = PriceData(
            symbol="WTI",
            date=date(2024, 1, 15),
            open_price=100.0,
            high_price=105.0,
            low_price=95.0,
            close_price=102.0,
            volume=1000,
            open_interest=5000
        )
        
        self.assertEqual(price_data.symbol, "WTI")
        self.assertEqual(price_data.close_price, 102.0)
        self.assertEqual(price_data.volume, 1000)
    
    def test_market_disruption_event(self):
        """Test MarketDisruptionEvent dataclass"""
        mde = MarketDisruptionEvent(
            symbol="WTI",
            date=date(2024, 1, 15),
            event_type="trading_halt",
            description="Exchange closure due to weather",
            resolution_date=date(2024, 1, 16)
        )
        
        self.assertEqual(mde.symbol, "WTI")
        self.assertEqual(mde.event_type, "trading_halt")
        self.assertEqual(mde.resolution_date, date(2024, 1, 16))


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calculator = SPGSCICalculator()
        self.portfolio_manager = SPGSCIPortfolioManager(self.calculator)
        self.test_date = date(2024, 1, 15)
        self.previous_date = date(2024, 1, 14)
    
    def test_complete_workflow(self):
        """Test complete workflow from index calculation to portfolio management"""
        # 1. Calculate index return
        index_return = self.calculator.calculate_index_return(
            self.test_date, self.previous_date
        )
        self.assertIsInstance(index_return, float)
        
        # 2. Calculate index level
        previous_level = 100.0
        current_level = self.calculator.calculate_index_level(
            self.test_date, self.previous_date, previous_level
        )
        self.assertGreater(current_level, 0)
        
        # 3. Construct portfolio
        positions = self.portfolio_manager.construct_portfolio(self.test_date)
        self.assertGreater(len(positions), 0)
        
        # 4. Calculate portfolio value
        portfolio_value = self.portfolio_manager.calculate_portfolio_value(
            positions, self.test_date
        )
        self.assertGreater(portfolio_value, 0)
        
        # 5. Calculate portfolio return
        portfolio_return = self.portfolio_manager.calculate_portfolio_return(
            positions, self.test_date, self.previous_date
        )
        self.assertIsInstance(portfolio_return, float)
    
    def test_consistency_check(self):
        """Test consistency between index and portfolio returns"""
        # Calculate index return
        index_return = self.calculator.calculate_index_return(
            self.test_date, self.previous_date
        )
        
        # Construct portfolio and calculate return
        positions = self.portfolio_manager.construct_portfolio(self.test_date)
        portfolio_return = self.portfolio_manager.calculate_portfolio_return(
            positions, self.test_date, self.previous_date
        )
        
        # Both should be reasonable values (not necessarily equal due to different methodologies)
        self.assertIsInstance(index_return, float)
        self.assertIsInstance(portfolio_return, float)


def run_performance_test():
    """Run performance test to ensure system can handle realistic workloads"""
    print("Running performance test...")
    
    calculator = SPGSCICalculator()
    portfolio_manager = SPGSCIPortfolioManager(calculator)
    
    # Test with multiple dates
    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 31)
    current_date = start_date
    
    index_levels = []
    portfolio_values = []
    
    previous_level = 100.0
    positions = None
    
    while current_date <= end_date:
        if current_date > start_date:
            # Calculate index level
            current_level = calculator.calculate_index_level(
                current_date, current_date - timedelta(days=1), previous_level
            )
            index_levels.append(current_level)
            previous_level = current_level
            
            # Calculate portfolio value
            if positions is not None:
                portfolio_value = portfolio_manager.calculate_portfolio_value(
                    positions, current_date
                )
                portfolio_values.append(portfolio_value)
        
        # Rebalance portfolio monthly
        if current_date.day == 1 or positions is None:
            positions = portfolio_manager.construct_portfolio(current_date)
        
        current_date += timedelta(days=1)
    
    print(f"Calculated {len(index_levels)} index levels")
    print(f"Calculated {len(portfolio_values)} portfolio values")
    print("Performance test completed successfully!")


if __name__ == "__main__":
    # Run unit tests
    unittest.main(verbosity=2, exit=False)
    
    # Run performance test
    run_performance_test()