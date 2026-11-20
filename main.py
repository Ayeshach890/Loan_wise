from models import Applicant, Loan, LoanApplication
from analysis import LoanMathematicalAnalyzer
from screens import (
    SplashScreen,
    EligibilityScreen,
    CalculatorSimulatorScreen,
    AmortizationAnalysisScreen,
    KycVerificationScreen,
    DocumentUploadScreen,
    TermsReviewScreen,
    SubmissionTrackerScreen,
    ActiveDashboardScreen,
    PaymentHistoryScreen,
)


def main():
    applicant = Applicant(
        full_name="Ayesha Arif",
        cnic="32203-1234567-8",
        monthly_income=150000,
        existing_emi=15000,
    )
    loan = Loan(principal=500000, annual_rate=0.14, months=24)
    application = LoanApplication(app_id="LN-2026-001", applicant=applicant, loan=loan)

    screens = [
        SplashScreen(1, "Splash & Welcome"),
        EligibilityScreen(2, "Onboarding & Eligibility Check"),
        CalculatorSimulatorScreen(3, "Loan Calculator & Simulator"),
        AmortizationAnalysisScreen(4, "Amortization & Mathematical Analysis"),
        KycVerificationScreen(5, "KYC & Identity Verification"),
        DocumentUploadScreen(6, "Document Upload"),
        TermsReviewScreen(7, "Loan Summary & Terms Review"),
        SubmissionTrackerScreen(8, "Application Submission & Status Tracker"),
        ActiveDashboardScreen(9, "Active Loan Dashboard"),
        PaymentHistoryScreen(10, "Payment History & Receipts"),
    ]

    for screen in screens:
        screen.render(application)

    implied_rate = LoanMathematicalAnalyzer.solve_implied_annual_rate(
        principal=500000, months=24, target_emi=24006.44
    )
    print(f"\n[Numerical Analysis Demo] Implied Annual Rate via Bisection Method: {implied_rate}%")


if __name__ == "__main__":
    main()