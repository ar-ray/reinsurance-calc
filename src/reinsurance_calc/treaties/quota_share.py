"""
Quota Share Treaty Calculator Module
Used for calculating premiums under proportional quota share treaties
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import pandas as pd


@dataclass
class QuotaShareTreaty:
    """
    Represents a Quota Share reinsurance treaty.
    
    Attributes:
        cession_rate: Percentage of risk ceded to reinsurer (0-100)
        commission_rate: Ceding commission percentage (0-100)
        profit_commission_rate: Profit commission percentage (0-100)
        profit_commission_threshold: Loss ratio threshold for profit commission
        annual_aggregate_limit: Maximum annual payout limit
    """
    cession_rate: float
    commission_rate: float
    profit_commission_rate: float = 0
    profit_commission_threshold: float = 0.65
    annual_aggregate_limit: Optional[float] = None
    
    def __post_init__(self):
        """Validate treaty parameters"""
        if not 0 <= self.cession_rate <= 100:
            raise ValueError("Cession rate must be between 0 and 100")
        if not 0 <= self.commission_rate <= 100:
            raise ValueError("Commission rate must be between 0 and 100")
            
    def calculate_premium(self, gross_premium: float) -> Dict[str, float]:
        """
        Calculate reinsurance premium and related metrics.
        
        Args:
            gross_premium: Original gross written premium
            
        Returns:
            Dictionary containing calculated values
        """
        # Calculate ceded premium
        ceded_premium = gross_premium * (self.cession_rate / 100)
        
        # Calculate ceding commission
        ceding_commission = ceded_premium * (self.commission_rate / 100)
        
        # Net premium to reinsurer
        net_premium_to_reinsurer = ceded_premium - ceding_commission
        
        # Retained premium by cedant
        retained_premium = gross_premium - ceded_premium
        
        return {
            'gross_premium': gross_premium,
            'cession_rate': self.cession_rate,
            'ceded_premium': ceded_premium,
            'retained_premium': retained_premium,
            'ceding_commission': ceding_commission,
            'net_premium_to_reinsurer': net_premium_to_reinsurer,
            'commission_rate': self.commission_rate
        }
    
    def calculate_claims(self, gross_claims: float) -> Dict[str, float]:
        """
        Calculate how claims are split between cedant and reinsurer.
        
        Args:
            gross_claims: Total claims amount
            
        Returns:
            Dictionary with claims distribution
        """
        # Claims follow the same proportion as premiums
        reinsurer_claims = gross_claims * (self.cession_rate / 100)
        
        # Apply annual aggregate limit if specified
        if self.annual_aggregate_limit:
            reinsurer_claims = min(reinsurer_claims, self.annual_aggregate_limit)
            
        cedant_claims = gross_claims - reinsurer_claims
        
        return {
            'gross_claims': gross_claims,
            'reinsurer_claims': reinsurer_claims,
            'cedant_claims': cedant_claims,
            'claims_ratio': (reinsurer_claims / gross_claims * 100) if gross_claims > 0 else 0
        }
    
    def calculate_profit_commission(self, 
                                   ceded_premium: float, 
                                   ceded_claims: float) -> float:
        """
        Calculate profit commission based on loss ratio.
        
        Args:
            ceded_premium: Premium ceded to reinsurer
            ceded_claims: Claims paid by reinsurer
            
        Returns:
            Profit commission amount
        """
        if ceded_premium == 0:
            return 0
            
        loss_ratio = ceded_claims / ceded_premium
        
        if loss_ratio < self.profit_commission_threshold:
            profit = ceded_premium - ceded_claims
            profit_commission = profit * (self.profit_commission_rate / 100)
            return max(0, profit_commission)
        
        return 0
    
    def generate_cashflow_analysis(self, 
                                  premiums: List[float], 
                                  claims: List[float],
                                  periods: List[str]) -> pd.DataFrame:
        """
        Generate period-by-period cashflow analysis.
        
        Args:
            premiums: List of gross premiums by period
            claims: List of gross claims by period
            periods: List of period labels (e.g., ['Q1', 'Q2', 'Q3', 'Q4'])
            
        Returns:
            DataFrame with detailed cashflow analysis
        """
        results = []
        cumulative_ceded_premium = 0
        cumulative_ceded_claims = 0
        
        for period, premium, claim in zip(periods, premiums, claims):
            # Calculate premium components
            premium_calc = self.calculate_premium(premium)
            claims_calc = self.calculate_claims(claim)
            
            cumulative_ceded_premium += premium_calc['ceded_premium']
            cumulative_ceded_claims += claims_calc['reinsurer_claims']
            
            # Calculate profit commission for the period
            profit_comm = self.calculate_profit_commission(
                cumulative_ceded_premium, 
                cumulative_ceded_claims
            )
            
            # Reinsurer's net position
            reinsurer_net = (premium_calc['net_premium_to_reinsurer'] - 
                           claims_calc['reinsurer_claims'] - 
                           profit_comm)
            
            results.append({
                'Period': period,
                'Gross_Premium': premium,
                'Ceded_Premium': premium_calc['ceded_premium'],
                'Retained_Premium': premium_calc['retained_premium'],
                'Ceding_Commission': premium_calc['ceding_commission'],
                'Gross_Claims': claim,
                'Reinsurer_Claims': claims_calc['reinsurer_claims'],
                'Cedant_Claims': claims_calc['cedant_claims'],
                'Profit_Commission': profit_comm,
                'Reinsurer_Net_Position': reinsurer_net,
                'Loss_Ratio': (claims_calc['reinsurer_claims'] / 
                              premium_calc['ceded_premium'] * 100 
                              if premium_calc['ceded_premium'] > 0 else 0)
            })
        
        return pd.DataFrame(results)


# Example usage function
def example_quota_share_calculation():
    """
    Example calculation for a typical quota share treaty.
    """
    # Create a 50% quota share treaty with 30% commission
    treaty = QuotaShareTreaty(
        cession_rate=50,  # 50% cession
        commission_rate=30,  # 30% ceding commission
        profit_commission_rate=20,  # 20% profit commission
        profit_commission_threshold=0.60,  # 60% loss ratio threshold
        annual_aggregate_limit=10_000_000  # $10M annual limit
    )
    
    # Calculate for a single premium
    result = treaty.calculate_premium(gross_premium=1_000_000)
    
    print("Single Period Calculation:")
    print("-" * 40)
    for key, value in result.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: ${value:,.2f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}%")
    
    # Multi-period analysis
    print("\n\nQuarterly Analysis:")
    print("-" * 40)
    
    quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
    premiums = [2_500_000, 3_000_000, 2_800_000, 3_200_000]
    claims = [1_500_000, 1_800_000, 2_100_000, 1_900_000]
    
    df = treaty.generate_cashflow_analysis(premiums, claims, quarters)
    
    # Format the DataFrame for display
    pd.options.display.float_format = '{:,.0f}'.format
    print(df.to_string(index=False))
    
    # Summary statistics
    print("\n\nAnnual Summary:")
    print("-" * 40)
    print(f"Total Ceded Premium: ${df['Ceded_Premium'].sum():,.2f}")
    print(f"Total Reinsurer Claims: ${df['Reinsurer_Claims'].sum():,.2f}")
    print(f"Total Ceding Commission: ${df['Ceding_Commission'].sum():,.2f}")
    print(f"Average Loss Ratio: {df['Loss_Ratio'].mean():.2f}%")
    print(f"Reinsurer Net Result: ${df['Reinsurer_Net_Position'].sum():,.2f}")


if __name__ == "__main__":
    example_quota_share_calculation()