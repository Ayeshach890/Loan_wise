from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


def normalize_cnic(raw_cnic: str) -> str:
    digits = re.sub(r"\D", "", raw_cnic or "")
    return digits


def is_valid_cnic(raw_cnic: str) -> bool:
    return len(normalize_cnic(raw_cnic)) == 13


@dataclass
class Applicant:
    full_name: str
    cnic: str
    monthly_income: float
    monthly_expenses: float = 0.0
    existing_debt: float = 0.0
    credit_score: int = 700
    kyc_verified: bool = False
    documents_uploaded: list = field(default_factory=list)
    def __post_init__(self) -> None:
        self.monthly_income = float(self.monthly_income)
        self.monthly_expenses = float(self.monthly_expenses)
        self.existing_debt = float(self.existing_debt)
        self.credit_score = int(self.credit_score)
        if is_valid_cnic(self.cnic):
            self.kyc_verified = True

    def disposable_income(self) -> float:
        return max(0.0, self.monthly_income - self.monthly_expenses - self.existing_debt)

    def evaluate_eligibility(self, proposed_emi: float) -> tuple[bool, str]:
        emi = float(proposed_emi)
        if self.monthly_income <= 0:
            return False, "Monthly income must be greater than 0."
        max_allowed_emi = self.monthly_income * 0.40
        if emi <= max_allowed_emi and self.credit_score >= 600:
            return True, "Eligible: EMI is within 40% of monthly income and credit score is acceptable."
        if emi > max_allowed_emi:
            return False, f"Not Eligible: EMI exceeds 40% limit ({max_allowed_emi:,.2f} PKR)."
        return False, "Not Eligible: Credit score is below minimum threshold (600)."


@dataclass
class AmortizationRow:
    month: int
    opening_balance: float
    emi: float
    principal_component: float
    interest_component: float
    remaining_balance: float

    @property
    def closing_balance(self) -> float:
        return self.remaining_balance
    @property
    def payment(self) -> float:
        return self.emi
    @property
    def principal_paid(self) -> float:
        return self.principal_component

    @property
    def interest_paid(self) -> float:
        return self.interest_component
class Loan:
    def __init__(self, principal: float, annual_rate: float, months: int) -> None:
        if float(principal) <= 0 or float(annual_rate) < 0 or int(months) <= 0:
            raise ValueError("Invalid loan parameters.")
        self._principal = float(principal)
        self._annual_rate = float(annual_rate)
        self._months = int(months)

    @property
    def principal(self) -> float:
        return self._principal

    @principal.setter
    def principal(self, value: float) -> None:
        val = float(value)
        if val <= 0:
            raise ValueError("Principal must be positive.")
        self._principal = val

    @property
    def annual_rate(self) -> float:
        return self._annual_rate

    @annual_rate.setter
    def annual_rate(self, value: float) -> None:
        val = float(value)
        if val < 0:
            raise ValueError("Annual rate cannot be negative.")
        self._annual_rate = val

    @property
    def months(self) -> int:
        return self._months

    @months.setter
    def months(self, value: int) -> None:
        val = int(value)
        if val <= 0:
            raise ValueError("Months must be positive.")
        self._months = val

    @property
    def monthly_rate(self) -> float:
        rate = self._annual_rate
        if rate > 1.0:
            rate = rate / 100.0
        return rate / 12.0

    def calculate_emi(self) -> float:
        r = self.monthly_rate
        n = self._months
        if r == 0:
            return self._principal / n
        factor = (1.0 + r) ** n
        return self._principal * (r * factor) / (factor - 1.0)

    def total_payable(self) -> float:
        return self.calculate_emi() * self._months

    def total_interest(self) -> float:
        return self.total_payable() - self._principal

    def generate_schedule(self) -> list[AmortizationRow]:
        schedule: list[AmortizationRow] = []
        balance = self._principal
        emi = self.calculate_emi()
        r = self.monthly_rate

        for m in range(1, self._months + 1):
            opening = balance
            interest_comp = opening * r
            principal_comp = emi - interest_comp
            if m == self._months or principal_comp > opening:
                principal_comp = opening
                emi = principal_comp + interest_comp
            closing = max(0.0, opening - principal_comp)
            schedule.append(
                AmortizationRow(
                    month=m,
                    opening_balance=opening,
                    emi=emi,
                    principal_component=principal_comp,
                    interest_component=interest_comp,
                    remaining_balance=closing,
                )
            )
            balance = closing

        return schedule





@dataclass
class LoanApplication:
    app_id: str
    applicant: Applicant
    loan: Loan
    receipts: list = field(default_factory=list)
    status: str = "Pending"
    notes: str = ""
    terms_accepted: bool = False

    @property
    def paid_installments(self):
        return self.receipts

    def refresh_status(self) -> tuple[bool, str]:
        eligible, reason = self.applicant.evaluate_eligibility(
            self.loan.calculate_emi()
        )
        self.status = "Eligible" if eligible else "Ineligible"
        self.notes = reason
        return eligible, reason

    def is_eligible(self):
        return self.refresh_status()

    def pay_next_installment(self):
        from types import SimpleNamespace

        emi = self.loan.calculate_emi()
        installment_num = len(self.receipts) + 1

        receipt = SimpleNamespace(
            receipt_id=f"RCP-{self.app_id}-{installment_num:02d}",
            month=f"Month {installment_num}",
            month_number=installment_num,
            amount_paid=emi,
        )

        self.receipts.append(receipt)
        return receipt

