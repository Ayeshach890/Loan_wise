class Screen:
    def __init__(self, screen_number, title):
        self.screen_number = screen_number
        self.title = title

    def render(self, app):
        print(f"\n=== SCREEN {self.screen_number}/10: {self.title} ===")


class SplashScreen(Screen):
    def render(self, app):
        super().render(app)
        print("Welcome to Loan Wise.")


class EligibilityScreen(Screen):
    def render(self, app):
        super().render(app)
        eligible, msg = app.is_eligible()
        print(f"Applicant: {app.applicant.full_name} | {msg}")


class CalculatorSimulatorScreen(Screen):
    def render(self, app):
        super().render(app)
        emi = app.loan.calculate_emi()
        print(f"Principal: {app.loan.principal:,.2f} | Monthly EMI: {emi:,.2f}")


class AmortizationAnalysisScreen(Screen):
    def render(self, app):
        super().render(app)
        schedule = app.loan.generate_schedule()
        print(f"Total Schedule Rows: {len(schedule)}")


class KycVerificationScreen(Screen):
    def render(self, app):
        super().render(app)
        app.applicant.kyc_verified = len(app.applicant.cnic) >= 13
        print(f"CNIC: {app.applicant.cnic} | Verified: {app.applicant.kyc_verified}")


class DocumentUploadScreen(Screen):
    def render(self, app):
        super().render(app)
        app.applicant.documents_uploaded = ["Salary_Slip.pdf", "Bank_Statement.pdf"]
        print("Documents uploaded.")


class TermsReviewScreen(Screen):
    def render(self, app):
        super().render(app)
        app.terms_accepted = True
        print("Terms accepted.")


class SubmissionTrackerScreen(Screen):
    def render(self, app):
        super().render(app)
        print(f"Application ID: {app.app_id} | Status: {app.status}")


class ActiveDashboardScreen(Screen):
    def render(self, app):
        super().render(app)
        receipt = app.pay_next_installment()
        print(f"Paid Installments: {app.paid_installments}/{app.loan.months}")
        if receipt:
            print(f"Receipt: {receipt.receipt_id} | Amount: {receipt.amount_paid:,.2f}")


class PaymentHistoryScreen(Screen):
    def render(self, app):
        super().render(app)
        print(f"Total Receipts: {len(app.receipts)}")