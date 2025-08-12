"""
Configuration file for S&P GSCI Implementation
Quantitative Investment Strategy Structurer

Contains all configuration parameters for the S&P GSCI methodology implementation
"""

from datetime import date
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ExchangeConfig:
    """Exchange configuration for commodity futures"""
    name: str
    timezone: str
    trading_hours: str
    holiday_calendar: List[str]
    rolling_schedule: Dict[str, int]  # Days before expiry for rolling


@dataclass
class CommodityConfig:
    """Commodity-specific configuration"""
    symbol: str
    exchange: str
    contract_size: float
    tick_size: float
    tick_value: float
    delivery_months: List[int]  # Available delivery months
    unit_of_measure: str
    currency: str


class SPGSCIConfig:
    """Main configuration class for S&P GSCI implementation"""
    
    # Base configuration
    BASE_DATE = date(1970, 1, 1)
    BASE_VALUE = 100.0
    
    # Rolling configuration
    ROLLING_DAYS_BEFORE_EXPIRY = 5
    ROLLING_SCHEDULE = {
        'ENERGY': 5,
        'METALS': 5,
        'AGRICULTURE': 5,
        'LIVESTOCK': 5
    }
    
    # Market disruption event configuration
    MDE_THRESHOLD_DAYS = 5
    MDE_TYPES = ['trading_halt', 'force_majeure', 'exchange_closure', 'settlement_failure']
    
    # Exchange configurations
    EXCHANGES = {
        'NYMEX': ExchangeConfig(
            name='NYMEX',
            timezone='America/New_York',
            trading_hours='09:00-14:30',
            holiday_calendar=['2024-01-01', '2024-01-15', '2024-02-19'],
            rolling_schedule={'ENERGY': 5, 'METALS': 5}
        ),
        'ICE': ExchangeConfig(
            name='ICE',
            timezone='America/New_York',
            trading_hours='08:00-14:30',
            holiday_calendar=['2024-01-01', '2024-01-15', '2024-02-19'],
            rolling_schedule={'ENERGY': 5, 'AGRICULTURE': 5}
        ),
        'CBOT': ExchangeConfig(
            name='CBOT',
            timezone='America/Chicago',
            trading_hours='08:30-13:20',
            holiday_calendar=['2024-01-01', '2024-01-15', '2024-02-19'],
            rolling_schedule={'AGRICULTURE': 5, 'LIVESTOCK': 5}
        ),
        'COMEX': ExchangeConfig(
            name='COMEX',
            timezone='America/New_York',
            trading_hours='08:20-13:30',
            holiday_calendar=['2024-01-01', '2024-01-15', '2024-02-19'],
            rolling_schedule={'PRECIOUS_METALS': 5}
        ),
        'LME': ExchangeConfig(
            name='LME',
            timezone='Europe/London',
            trading_hours='08:00-16:00',
            holiday_calendar=['2024-01-01', '2024-01-15', '2024-02-19'],
            rolling_schedule={'INDUSTRIAL_METALS': 5}
        )
    }
    
    # Commodity configurations
    COMMODITIES = {
        'WTI': CommodityConfig(
            symbol='WTI',
            exchange='NYMEX',
            contract_size=1000.0,  # barrels
            tick_size=0.01,
            tick_value=10.0,
            delivery_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            unit_of_measure='barrels',
            currency='USD'
        ),
        'BRENT': CommodityConfig(
            symbol='BRENT',
            exchange='ICE',
            contract_size=1000.0,  # barrels
            tick_size=0.01,
            tick_value=10.0,
            delivery_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            unit_of_measure='barrels',
            currency='USD'
        ),
        'RBOB': CommodityConfig(
            symbol='RBOB',
            exchange='NYMEX',
            contract_size=42000.0,  # gallons
            tick_size=0.0001,
            tick_value=4.2,
            delivery_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            unit_of_measure='gallons',
            currency='USD'
        ),
        'HEATING': CommodityConfig(
            symbol='HEATING',
            exchange='NYMEX',
            contract_size=42000.0,  # gallons
            tick_size=0.0001,
            tick_value=4.2,
            delivery_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            unit_of_measure='gallons',
            currency='USD'
        ),
        'NATURAL': CommodityConfig(
            symbol='NATURAL',
            exchange='NYMEX',
            contract_size=10000.0,  # MMBtu
            tick_size=0.001,
            tick_value=10.0,
            delivery_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            unit_of_measure='MMBtu',
            currency='USD'
        ),
        'COPPER': CommodityConfig(
            symbol='COPPER',
            exchange='COMEX',
            contract_size=25000.0,  # pounds
            tick_size=0.0005,
            tick_value=12.5,
            delivery_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            unit_of_measure='pounds',
            currency='USD'
        ),
        'ALUMINUM': CommodityConfig(
            symbol='ALUMINUM',
            exchange='LME',
            contract_size=25.0,  # metric tons
            tick_size=0.01,
            tick_value=0.25,
            delivery_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            unit_of_measure='metric tons',
            currency='USD'
        ),
        'ZINC': CommodityConfig(
            symbol='ZINC',
            exchange='LME',
            contract_size=25.0,  # metric tons
            tick_size=0.01,
            tick_value=0.25,
            delivery_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            unit_of_measure='metric tons',
            currency='USD'
        ),
        'NICKEL': CommodityConfig(
            symbol='NICKEL',
            exchange='LME',
            contract_size=6.0,  # metric tons
            tick_size=1.0,
            tick_value=6.0,
            delivery_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            unit_of_measure='metric tons',
            currency='USD'
        ),
        'LEAD': CommodityConfig(
            symbol='LEAD',
            exchange='LME',
            contract_size=25.0,  # metric tons
            tick_size=0.01,
            tick_value=0.25,
            delivery_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            unit_of_measure='metric tons',
            currency='USD'
        ),
        'GOLD': CommodityConfig(
            symbol='GOLD',
            exchange='COMEX',
            contract_size=100.0,  # troy ounces
            tick_size=0.1,
            tick_value=10.0,
            delivery_months=[2, 4, 6, 8, 10, 12],
            unit_of_measure='troy ounces',
            currency='USD'
        ),
        'SILVER': CommodityConfig(
            symbol='SILVER',
            exchange='COMEX',
            contract_size=5000.0,  # troy ounces
            tick_size=0.005,
            tick_value=25.0,
            delivery_months=[1, 3, 5, 7, 9, 12],
            unit_of_measure='troy ounces',
            currency='USD'
        ),
        'CORN': CommodityConfig(
            symbol='CORN',
            exchange='CBOT',
            contract_size=5000.0,  # bushels
            tick_size=0.25,
            tick_value=12.5,
            delivery_months=[3, 5, 7, 9, 12],
            unit_of_measure='bushels',
            currency='USD'
        ),
        'WHEAT': CommodityConfig(
            symbol='WHEAT',
            exchange='CBOT',
            contract_size=5000.0,  # bushels
            tick_size=0.25,
            tick_value=12.5,
            delivery_months=[3, 5, 7, 9, 12],
            unit_of_measure='bushels',
            currency='USD'
        ),
        'SOYBEANS': CommodityConfig(
            symbol='SOYBEANS',
            exchange='CBOT',
            contract_size=5000.0,  # bushels
            tick_size=0.25,
            tick_value=12.5,
            delivery_months=[1, 3, 5, 7, 8, 9, 11],
            unit_of_measure='bushels',
            currency='USD'
        ),
        'SOYBEAN_OIL': CommodityConfig(
            symbol='SOYBEAN_OIL',
            exchange='CBOT',
            contract_size=60000.0,  # pounds
            tick_size=0.01,
            tick_value=6.0,
            delivery_months=[1, 3, 5, 7, 8, 9, 10, 12],
            unit_of_measure='pounds',
            currency='USD'
        ),
        'SOYBEAN_MEAL': CommodityConfig(
            symbol='SOYBEAN_MEAL',
            exchange='CBOT',
            contract_size=100.0,  # short tons
            tick_size=0.1,
            tick_value=10.0,
            delivery_months=[1, 3, 5, 7, 8, 9, 10, 12],
            unit_of_measure='short tons',
            currency='USD'
        ),
        'COTTON': CommodityConfig(
            symbol='COTTON',
            exchange='ICE',
            contract_size=50000.0,  # pounds
            tick_size=0.01,
            tick_value=5.0,
            delivery_months=[3, 5, 7, 10, 12],
            unit_of_measure='pounds',
            currency='USD'
        ),
        'COFFEE': CommodityConfig(
            symbol='COFFEE',
            exchange='ICE',
            contract_size=37500.0,  # pounds
            tick_size=0.05,
            tick_value=18.75,
            delivery_months=[3, 5, 7, 9, 12],
            unit_of_measure='pounds',
            currency='USD'
        ),
        'SUGAR': CommodityConfig(
            symbol='SUGAR',
            exchange='ICE',
            contract_size=112000.0,  # pounds
            tick_size=0.01,
            tick_value=11.2,
            delivery_months=[3, 5, 7, 10],
            unit_of_measure='pounds',
            currency='USD'
        ),
        'COCOA': CommodityConfig(
            symbol='COCOA',
            exchange='ICE',
            contract_size=10.0,  # metric tons
            tick_size=1.0,
            tick_value=10.0,
            delivery_months=[3, 5, 7, 9, 12],
            unit_of_measure='metric tons',
            currency='USD'
        ),
        'LIVE_CATTLE': CommodityConfig(
            symbol='LIVE_CATTLE',
            exchange='CME',
            contract_size=40000.0,  # pounds
            tick_size=0.025,
            tick_value=10.0,
            delivery_months=[2, 4, 6, 8, 10, 12],
            unit_of_measure='pounds',
            currency='USD'
        ),
        'LEAN_HOGS': CommodityConfig(
            symbol='LEAN_HOGS',
            exchange='CME',
            contract_size=40000.0,  # pounds
            tick_size=0.025,
            tick_value=10.0,
            delivery_months=[2, 4, 6, 7, 8, 10, 12],
            unit_of_measure='pounds',
            currency='USD'
        ),
        'FEEDER_CATTLE': CommodityConfig(
            symbol='FEEDER_CATTLE',
            exchange='CME',
            contract_size=50000.0,  # pounds
            tick_size=0.025,
            tick_value=12.5,
            delivery_months=[1, 3, 4, 5, 8, 9, 10, 11],
            unit_of_measure='pounds',
            currency='USD'
        )
    }
    
    # S&P GSCI commodity weights (as of latest methodology)
    COMMODITY_WEIGHTS = {
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
    
    # Risk management parameters
    MAX_POSITION_SIZE = 0.25  # Maximum 25% in any single commodity
    MAX_SECTOR_WEIGHT = 0.60  # Maximum 60% in any single sector
    MIN_LIQUIDITY_THRESHOLD = 1000  # Minimum daily volume
    MAX_ROLLING_COST = 0.02  # Maximum 2% rolling cost
    
    # Performance parameters
    BENCHMARK_RETURN = 0.08  # 8% annual benchmark return
    TARGET_VOLATILITY = 0.20  # 20% target volatility
    MAX_DRAWDOWN = 0.15  # Maximum 15% drawdown
    
    # Data quality parameters
    MIN_PRICE_CHANGE = 0.0001  # Minimum price change threshold
    MAX_PRICE_CHANGE = 0.50  # Maximum 50% daily price change
    MIN_VOLUME_THRESHOLD = 100  # Minimum volume for valid price
    
    # Logging configuration
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'sp_gsci.log'
    
    # Database configuration (if using external database)
    DATABASE_CONFIG = {
        'host': 'localhost',
        'port': 5432,
        'database': 'sp_gsci',
        'username': 'sp_gsci_user',
        'password': 'password'
    }
    
    # API configuration (if using external data providers)
    API_CONFIG = {
        'bloomberg': {
            'host': 'localhost',
            'port': 8194,
            'timeout': 30
        },
        'reuters': {
            'host': 'localhost',
            'port': 8194,
            'timeout': 30
        },
        'quandl': {
            'api_key': 'your_api_key_here'
        }
    }
    
    @classmethod
    def get_commodity_config(cls, symbol: str) -> CommodityConfig:
        """Get commodity configuration by symbol"""
        return cls.COMMODITIES.get(symbol)
    
    @classmethod
    def get_exchange_config(cls, exchange: str) -> ExchangeConfig:
        """Get exchange configuration by name"""
        return cls.EXCHANGES.get(exchange)
    
    @classmethod
    def get_commodity_weight(cls, symbol: str) -> float:
        """Get commodity weight by symbol"""
        return cls.COMMODITY_WEIGHTS.get(symbol, 0.0)
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration parameters"""
        # Check that weights sum to approximately 1
        total_weight = sum(cls.COMMODITY_WEIGHTS.values())
        if abs(total_weight - 1.0) > 0.01:
            print(f"Warning: Commodity weights sum to {total_weight}, not 1.0")
            return False
        
        # Check that all commodities have configurations
        for symbol in cls.COMMODITY_WEIGHTS.keys():
            if symbol not in cls.COMMODITIES:
                print(f"Warning: No configuration found for commodity {symbol}")
                return False
        
        return True


if __name__ == "__main__":
    # Validate configuration
    if SPGSCIConfig.validate_config():
        print("Configuration validation passed!")
    else:
        print("Configuration validation failed!")