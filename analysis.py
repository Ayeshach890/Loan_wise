import math
from models import AmortizationRow, Loan


class LoanMathematicalAnalyzer:
    @staticmethod
    def verify_monotonic_decrease(schedule: list[AmortizationRow]) -> bool:
        return all(
            schedule[i + 1].remaining_balance <= schedule[i].remaining_balance
            for i in range(len(schedule) - 1)
        )

    @staticmethod
    def verify_boundedness(schedule: list[AmortizationRow], principal: float) -> bool:
        return all(0.0 <= row.remaining_balance <= principal for row in schedule)

    @staticmethod
    def compare_discrete_vs_continuous(loan: Loan, years: float) -> dict[str, float]:
        r = loan.annual_rate
        monthly = loan.principal * ((1 + r / 12) ** (12 * years))
        daily = loan.principal * ((1 + r / 365) ** (365 * years))
        continuous = loan.principal * math.exp(r * years)
        return {
            "monthly_compounding": round(monthly, 2),
            "daily_compounding": round(daily, 2),
            "continuous_limit": round(continuous, 2),
        }

    @staticmethod
    def solve_implied_annual_rate(principal: float, months: int, target_emi: float) -> float:
        min_emi = principal / months
        if target_emi < min_emi:
            raise ValueError("Target EMI cannot be less than zero-interest EMI (P / n).")
        if math.isclose(target_emi, min_emi, rel_tol=1e-7):
            return 0.0

        low, high = 0.0, 2.0
        for _ in range(100):
            mid = (low + high) / 2.0
            emi_mid = Loan(principal, mid, months).calculate_emi()
            if math.isclose(emi_mid, target_emi, rel_tol=1e-9):
                return round(mid * 100, 4)
            if emi_mid < target_emi:
                low = mid
            else:
                high = mid
        return round(((low + high) / 2.0) * 100, 4)