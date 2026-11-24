
import streamlit as st
import pandas as pd

from models import Applicant, Loan, LoanApplication, is_valid_cnic
from analysis import LoanMathematicalAnalyzer


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Loan Wise | Financial Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. PROFESSIONAL DESIGN
# =====================================================

st.markdown("""
<style>
.stApp {
    background-color: #0F172A;
    color: #F8FAFC;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stMetric"] {
    background-color: #1E293B;
    padding: 18px;
    border: 1px solid #334155;
    border-radius: 12px;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

p, label {
    color: #CBD5E1;
}

.stButton > button {
    background-color: #6366F1;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 9px 18px;
}

.stButton > button:hover {
    background-color: #4F46E5;
    color: white;
}

hr {
    border-color: #334155;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. INITIAL DATA
# =====================================================

if "application" not in st.session_state:

    applicant = Applicant(
        full_name="Demo Applicant",
        cnic="",
        monthly_income=150000,
        monthly_expenses=30000,
        existing_debt=15000,
        credit_score=700
    )

    loan = Loan(
        principal=500000,
        annual_rate=0.14,
        months=24
    )

    st.session_state.application = LoanApplication(
        app_id="LN-2026-001",
        applicant=applicant,
        loan=loan
    )


app = st.session_state.application
applicant = app.applicant
loan = app.loan

analyzer = LoanMathematicalAnalyzer()


# =====================================================
# 4. NAVIGATION
# =====================================================

screens = [
    "Executive Overview",
    "Applicant & Eligibility",
    "EMI & Loan Simulator",
    "Amortization Schedule",
    "Numerical & Math Lab",
    "KYC Verification",
    "Document Vault",
    "Terms & APR Disclosure",
    "Application Workflow",
    "Repayment & Receipts"
]


st.sidebar.markdown("# 🏦 LOAN WISE")
st.sidebar.caption("Financial Analytics Suite")
st.sidebar.divider()

selected = st.sidebar.radio(
    "NAVIGATION",
    screens
)

st.sidebar.divider()

st.sidebar.markdown("### Application Details")
st.sidebar.write(f"**Reference:** {app.app_id}")
st.sidebar.write(f"**Status:** {app.status}")
st.sidebar.caption("Financial Analytics Project")


st.title(selected)
st.caption(f"Loan Wise | {app.app_id}")
st.divider()


# =====================================================
# 5. COMMON CALCULATIONS
# =====================================================

emi = loan.calculate_emi()
total = loan.total_payable()
interest = loan.total_interest()
schedule = loan.generate_schedule()


# =====================================================
# 6. EXECUTIVE OVERVIEW
# =====================================================

if selected == screens[0]:

    st.subheader("Financial Overview")

    st.write(
        "A professional financial analytics platform "
        "for loan evaluation, EMI simulation, amortization "
        "and repayment tracking."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Loan Principal",
        f"PKR {loan.principal:,.0f}"
    )

    c2.metric(
        "Monthly EMI",
        f"PKR {emi:,.2f}"
    )

    c3.metric(
        "Total Interest",
        f"PKR {interest:,.2f}"
    )

    c4.metric(
        "Application Status",
        app.status
    )

    st.divider()

    st.subheader("Loan Principal vs Interest")

    chart_data = pd.DataFrame({
        "Amount (PKR)": {
            "Principal": loan.principal,
            "Interest": interest
        }
    })

    st.bar_chart(chart_data)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Applicant")

        st.write(applicant.full_name)

        st.write(
            f"Monthly Income: PKR "
            f"{applicant.monthly_income:,.2f}"
        )

        st.write(
            f"Credit Score: {applicant.credit_score}"
        )

    with col2:

        st.markdown("### Loan Summary")

        st.write(f"Tenure: {loan.months} months")

        st.write(
            f"Annual Rate: "
            f"{loan.annual_rate * 100:.2f}%"
        )

        st.write(
            f"Total Payable: PKR {total:,.2f}"
        )


# =====================================================
# 7. APPLICANT & ELIGIBILITY
# =====================================================

elif selected == screens[1]:

    st.subheader("Applicant Profile")

    with st.form("applicant_form"):

        name = st.text_input(
            "Full Name",
            applicant.full_name
        )

        cnic = st.text_input(
            "CNIC (13 digits)",
            applicant.cnic
        )

        income = st.number_input(
            "Monthly Income (PKR)",
            min_value=0.0,
            value=float(applicant.monthly_income)
        )

        expenses = st.number_input(
            "Monthly Expenses (PKR)",
            min_value=0.0,
            value=float(applicant.monthly_expenses)
        )

        debt = st.number_input(
            "Existing Debt / EMI (PKR)",
            min_value=0.0,
            value=float(applicant.existing_debt)
        )

        score = st.number_input(
            "Credit Score",
            min_value=0,
            max_value=900,
            value=int(applicant.credit_score)
        )

        submitted = st.form_submit_button(
            "Save & Evaluate Eligibility"
        )

        if submitted:

            if not name.strip():

                st.error("Applicant name is required.")

            elif income <= 0:

                st.error(
                    "Monthly income must be greater than zero."
                )

            else:

                applicant.full_name = name.strip()
                applicant.cnic = cnic.strip()
                applicant.monthly_income = income
                applicant.monthly_expenses = expenses
                applicant.existing_debt = debt
                applicant.credit_score = int(score)

                applicant.kyc_verified = False

                st.success(
                    "Applicant profile saved."
                )

                eligible, message = app.is_eligible()

                if eligible:
                    st.success(message)
                else:
                    st.warning(message)

    st.divider()

    st.subheader("Affordability Analysis")

    st.metric(
        "Disposable Income",
        f"PKR {applicant.disposable_income():,.2f}"
    )

    st.metric(
        "Proposed Monthly EMI",
        f"PKR {emi:,.2f}"
    )


# =====================================================
# 8. EMI & LOAN SIMULATOR
# =====================================================

elif selected == screens[2]:

    st.subheader("Loan Parameters")

    col1, col2 = st.columns(2)

    with col1:

        principal = st.number_input(
            "Principal Amount (PKR)",
            min_value=1.0,
            value=float(loan.principal)
        )

        annual_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(loan.annual_rate * 100)
        )

        months = st.number_input(
            "Tenure (Months)",
            min_value=1,
            max_value=600,
            value=int(loan.months)
        )

        if st.button("Apply Loan Simulation"):

            loan.principal = principal
            loan.annual_rate = annual_rate / 100
            loan.months = int(months)

            st.success(
                "Loan simulation updated successfully."
            )

            st.rerun()

    with col2:

        current_emi = loan.calculate_emi()

        st.markdown("### Simulation Results")

        st.metric(
            "Monthly EMI",
            f"PKR {current_emi:,.2f}"
        )

        st.metric(
            "Total Interest",
            f"PKR {loan.total_interest():,.2f}"
        )

        st.metric(
            "Total Payable",
            f"PKR {loan.total_payable():,.2f}"
        )

    st.divider()

    st.subheader("Compounding Comparison")

    years = st.number_input(
        "Comparison Period (Years)",
        min_value=0.0,
        max_value=100.0,
        value=2.0
    )

    comparison = analyzer.compare_discrete_vs_continuous(
        loan,
        years
    )

    comparison_df = pd.DataFrame(
        [
            [
                "Monthly",
                comparison["monthly_compounding"]
            ],
            [
                "Daily",
                comparison["daily_compounding"]
            ],
            [
                "Continuous",
                comparison["continuous_limit"]
            ]
        ],
        columns=[
            "Compounding Method",
            "Future Value (PKR)"
        ]
    )

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# 9. AMORTIZATION SCHEDULE
# =====================================================

elif selected == screens[3]:

    st.subheader("Monthly Amortization Schedule")

    rows = []

    for row in schedule:

        rows.append({
            "Month": row.month,
            "Opening Balance": row.opening_balance,
            "Payment": row.payment,
            "Principal": row.principal_paid,
            "Interest": row.interest_paid,
            "Remaining Balance": row.remaining_balance
        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df.style.format({
            "Opening Balance": "{:,.2f}",
            "Payment": "{:,.2f}",
            "Principal": "{:,.2f}",
            "Interest": "{:,.2f}",
            "Remaining Balance": "{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Amortization Schedule (CSV)",
        df.to_csv(index=False),
        file_name="LoanWise_Amortization.csv",
        mime="text/csv"
    )


# =====================================================
# 10. NUMERICAL & MATHEMATICAL LAB
# =====================================================

elif selected == screens[4]:

    st.subheader("Mathematical Analysis Lab")

    mono = analyzer.verify_monotonic_decrease(
        schedule
    )

    bounded = analyzer.verify_boundedness(
        schedule,
        loan.principal
    )

    implied = analyzer.solve_implied_annual_rate(
        loan.principal,
        loan.months,
        emi
    )

    comparison = analyzer.compare_discrete_vs_continuous(
        loan,
        2
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Monotonic Balance Decrease",
        "PASS" if mono else "FAIL"
    )

    c2.metric(
        "Boundedness Verification",
        "PASS" if bounded else "FAIL"
    )

    st.divider()

    st.markdown("### Bisection Method")

    st.metric(
        "Implied Annual Interest Rate",
        f"{implied * 100:.4f}%"
    )

    st.divider()

    st.markdown("### Compounding Analysis (2 Years)")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Monthly",
        f"PKR {comparison['monthly_compounding']:,.2f}"
    )

    c2.metric(
        "Daily",
        f"PKR {comparison['daily_compounding']:,.2f}"
    )

    c3.metric(
        "Continuous",
        f"PKR {comparison['continuous_limit']:,.2f}"
    )

    st.info(
        "The mathematical lab evaluates loan balance behavior, "
        "boundedness and the relationship between discrete "
        "and continuous compounding."
    )


# =====================================================
# 11. KYC VERIFICATION
# =====================================================

elif selected == screens[5]:

    st.subheader("Identity Verification Control")

    st.write(
        "Applicant:",
        applicant.full_name
    )

    cnic = st.text_input(
        "Enter 13-digit CNIC",
        value=applicant.cnic
    )

    st.warning(
        "Demo verification only. This does not connect to "
        "NADRA or verify the applicant's real identity."
    )

    if st.button("Verify CNIC Format"):

        if is_valid_cnic(cnic):

            applicant.cnic = cnic
            applicant.kyc_verified = True

            st.success(
                "CNIC format check passed."
            )

        else:

            applicant.kyc_verified = False

            st.error(
                "CNIC must contain exactly 13 digits."
            )

    st.write(
        "KYC Status:",
        "Verified" if applicant.kyc_verified else "Pending"
    )


# =====================================================
# 12. DOCUMENT VAULT
# =====================================================

elif selected == screens[6]:

    st.subheader("Document Management Vault")

    uploaded_files = st.file_uploader(
        "Upload Supporting Documents",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if uploaded_files:

        for file in uploaded_files:

            if file.name not in applicant.documents_uploaded:

                applicant.documents_uploaded.append(
                    file.name
                )

    st.markdown("### Uploaded Documents")

    if applicant.documents_uploaded:

        for i, document in enumerate(
            applicant.documents_uploaded,
            1
        ):

            st.write(
                f"{i}. 📄 {document}"
            )

    else:

        st.info(
            "No documents uploaded yet."
        )

    st.caption(
        "Demo application: uploaded files are not stored "
        "in a secure permanent document vault."
    )


# =====================================================
# 13. TERMS & APR DISCLOSURE
# =====================================================

elif selected == screens[7]:

    st.subheader("APR Disclosure & Loan Agreement")

    disclosures = {
        "Application Reference": app.app_id,
        "Principal Amount": f"PKR {loan.principal:,.2f}",
        "Annual Interest Rate": f"{loan.annual_rate * 100:.2f}%",
        "Monthly EMI": f"PKR {emi:,.2f}",
        "Repayment Tenure": f"{loan.months} Months",
        "Total Interest": f"PKR {interest:,.2f}",
        "Total Payable": f"PKR {total:,.2f}"
    }

    for key, value in disclosures.items():

        c1, c2 = st.columns(2)

        c1.write(f"**{key}**")
        c2.write(value)

    st.divider()

    accepted = st.checkbox(
        "I have reviewed and accept the displayed project terms.",
        value=app.terms_accepted
    )

    if st.button("Save Agreement Status"):

        app.terms_accepted = accepted

        if accepted:

            st.success("Agreement accepted.")

        else:

            st.info("Agreement not accepted.")


# =====================================================
# 14. APPLICATION WORKFLOW
# =====================================================

elif selected == screens[8]:

    st.subheader("Application Readiness & Workflow")

    eligible, message = app.is_eligible()

    checks = [
        (
            "Income & Eligibility",
            eligible,
            message
        ),
        (
            "KYC Verification",
            applicant.kyc_verified,
            "Demo KYC completed"
            if applicant.kyc_verified
            else "Pending"
        ),
        (
            "Document Vault",
            len(applicant.documents_uploaded) > 0,
            f"{len(applicant.documents_uploaded)} document(s) recorded"
        ),
        (
            "Terms Acceptance",
            app.terms_accepted,
            "Accepted"
            if app.terms_accepted
            else "Pending"
        )
    ]

    passed = sum(
        1 for item in checks if item[1]
    )

    progress = passed / len(checks)

    st.progress(progress)

    st.write(
        f"Application Readiness: {progress * 100:.0f}%"
    )

    for title, status, detail in checks:

        if status:

            st.success(
                f"✓ {title}: {detail}"
            )

        else:

            st.warning(
                f"○ {title}: {detail}"
            )

    approved = all(
        item[1] for item in checks
    )

    app.status = (
        "Approved"
        if approved
        else "In Review"
    )

    if approved:

        st.success(
            "APPLICATION STATUS: APPROVED"
        )

    else:

        st.warning(
            "APPLICATION STATUS: IN REVIEW"
        )

        st.info(
            "Complete all pending requirements to proceed."
        )


# =====================================================
# 15. REPAYMENT & RECEIPTS
# =====================================================

elif selected == screens[9]:

    st.subheader("Repayment Management")

    # Count completed payments
    paid = len(app.receipts)

    total_months = int(loan.months)

    # Payment summary
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Payments Completed",
        f"{paid}/{total_months}"
    )

    c2.metric(
        "Monthly EMI",
        f"PKR {emi:,.2f}"
    )

    c3.metric(
        "Receipts Issued",
        str(len(app.receipts))
    )

    # Payment progress
    progress = paid / max(total_months, 1)

    st.progress(
        min(max(progress, 0.0), 1.0)
    )

    st.write(
        f"Repayment Progress: {progress * 100:.1f}%"
    )

    st.divider()

    st.markdown("### Payment Records")

    if app.receipts:

        receipt_data = []

        for receipt in app.receipts:

            receipt_data.append({
                "Receipt ID": receipt.receipt_id,
                "Month": receipt.month_number,
                "Amount Paid": receipt.amount_paid
            })

        receipt_df = pd.DataFrame(
            receipt_data
        )

        st.dataframe(
            receipt_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Payment History (CSV)",
            receipt_df.to_csv(index=False),
            file_name="LoanWise_Payment_History.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No payments recorded yet."
        )

    st.divider()

    st.markdown("### Make Payment")

    if paid >= total_months:

        st.success(
            "All installments have been paid."
        )

    elif app.status != "Approved":

        st.warning(
            "Complete and approve your application workflow first."
        )

    else:

        st.write(
            f"Next Installment: {paid + 1}"
        )

        if st.button(
            "Pay Next Installment & Generate Receipt"
        ):

            receipt = app.pay_next_installment()

            if receipt is None:

                st.success(
                    "All installments have been paid."
                )

            else:

                st.success(
                    "Payment recorded successfully!"
                )

                st.write(
                    f"Receipt ID: {receipt.receipt_id}"
                )

                st.write(
                    f"Amount: PKR {receipt.amount_paid:,.2f}"
                )

            st.rerun()


# =====================================================
# 16. FOOTER
# =====================================================

st.divider()

st.caption(
    "LOAN WISE | Financial Analytics System | "
    "Academic Demonstration Project"
)
