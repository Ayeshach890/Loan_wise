import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from analysis import LoanMathematicalAnalyzer
from models import Applicant, Loan, LoanApplication


FONT_FAMILY = "Times New Roman"


class LoanWiseUniversityApp:
    def __init__(self, root: tk.Tk, app_data: LoanApplication):
        self.root = root
        self.app_data = app_data
        self.analyzer = LoanMathematicalAnalyzer()

        self.root.title("Loan Wise — Financial Engineering & Loan Analytics System")
        self.root.geometry("1160x700")
        self.root.minsize(1020, 640)

        # Palette
        self.bg_app = "#0F172A"
        self.bg_sidebar = "#111827"
        self.bg_surface = "#1E293B"
        self.bg_card = "#1E293B"
        self.bg_subtle = "#0F172A"
        self.border_col = "#334155"
        self.fg_primary = "#F8FAFC"
        self.fg_secondary = "#94A3B8"
        self.primary = "#6366F1"
        self.primary_hover = "#4F46E5"
        self.cyan = "#06B6D4"
        self.emerald = "#10B981"
        self.amber = "#F59E0B"
        self.rose = "#F43F5E"

        self.root.configure(bg=self.bg_app)
        self._configure_styles()

        self.screens_info = [
            (1, "Executive Overview"),
            (2, "Applicant & Eligibility"),
            (3, "EMI & Loan Simulator"),
            (4, "Amortization Schedule"),
            (5, "Numerical & Math Lab"),
            (6, "KYC Verification"),
            (7, "Document Vault"),
            (8, "Terms & APR Disclosure"),
            (9, "Application Workflow"),
            (10, "Repayment & Receipts"),
        ]
        self.current_index = 0

        self._build_shell()
        self.refresh_screen()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure(
            "Dark.Treeview",
            background="#0F172A",
            foreground="#E2E8F0",
            fieldbackground="#0F172A",
            bordercolor="#334155",
            rowheight=28,
            font=(FONT_FAMILY, 10),
        )
        style.configure(
            "Dark.Treeview.Heading",
            background="#1E293B",
            foreground="#F8FAFC",
            relief="flat",
            font=(FONT_FAMILY, 10, "bold"),
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", "#4F46E5")],
            foreground=[("selected", "#FFFFFF")],
        )

    def _build_shell(self) -> None:
        sidebar = tk.Frame(self.root, bg=self.bg_sidebar, width=245, highlightthickness=1, highlightbackground=self.border_col)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg=self.bg_sidebar, padx=18, pady=20)
        brand.pack(fill=tk.X)
        tk.Label(
            brand,
            text="LOAN WISE",
            bg=self.bg_sidebar,
            fg=self.fg_primary,
            font=(FONT_FAMILY, 18, "bold"),
            anchor="w",
        ).pack(fill=tk.X)
        tk.Label(
            brand,
            text="OOP FinTech & Numerical Suite",
            bg=self.bg_sidebar,
            fg=self.cyan,
            font=(FONT_FAMILY, 10, "bold"),
            anchor="w",
        ).pack(fill=tk.X, pady=(2, 0))

        tk.Frame(sidebar, bg=self.border_col, height=1).pack(fill=tk.X, padx=14, pady=(0, 8))

        self.nav_buttons = []
        for idx, (num, title) in enumerate(self.screens_info):
            btn = tk.Button(
                sidebar,
                text=f"  {num:02d}  {title}",
                bg=self.bg_sidebar,
                fg=self.fg_secondary,
                activebackground=self.primary,
                activeforeground="#FFFFFF",
                relief=tk.FLAT,
                anchor="w",
                font=(FONT_FAMILY, 11),
                padx=12,
                pady=7,
                cursor="hand2",
                command=lambda i=idx: self.go_to_screen(i),
            )
            btn.pack(fill=tk.X, padx=10, pady=1)
            self.nav_buttons.append(btn)

        right_panel = tk.Frame(self.root, bg=self.bg_app)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        header = tk.Frame(right_panel, bg=self.bg_surface, height=66, padx=24, highlightthickness=1, highlightbackground=self.border_col)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        self.header_lbl = tk.Label(
            header,
            text="",
            bg=self.bg_surface,
            fg=self.fg_primary,
            font=(FONT_FAMILY, 16, "bold"),
        )
        self.header_lbl.pack(side=tk.LEFT, pady=15)

        self.status_badge = tk.Label(
            header,
            text="",
            bg="#1E1B4B",
            fg="#A5B4FC",
            font=(FONT_FAMILY, 10, "bold"),
            padx=12,
            pady=5,
        )
        self.status_badge.pack(side=tk.RIGHT, pady=16)

        self.body = tk.Frame(right_panel, bg=self.bg_app, padx=22, pady=18)
        self.body.pack(fill=tk.BOTH, expand=True)

        footer = tk.Frame(right_panel, bg=self.bg_surface, height=58, padx=24, highlightthickness=1, highlightbackground=self.border_col)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)

        self.step_lbl = tk.Label(
            footer,
            text="",
            bg=self.bg_surface,
            fg=self.fg_secondary,
            font=(FONT_FAMILY, 11),
        )
        self.step_lbl.pack(side=tk.LEFT, pady=15)

        self.next_btn = tk.Button(
            footer,
            text="Next Screen  ->",
            bg=self.primary,
            fg="#FFFFFF",
            activebackground=self.primary_hover,
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            font=(FONT_FAMILY, 11, "bold"),
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.next_screen,
        )
        self.next_btn.pack(side=tk.RIGHT, pady=11, padx=(10, 0))

        self.prev_btn = tk.Button(
            footer,
            text="<-  Previous",
            bg="#334155",
            fg=self.fg_primary,
            activebackground="#475569",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            font=(FONT_FAMILY, 11, "bold"),
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.prev_screen,
        )
        self.prev_btn.pack(side=tk.RIGHT, pady=11)

    def _clear_body(self) -> None:
        for w in self.body.winfo_children():
            w.destroy()

    def _card(self, parent, padx=18, pady=16) -> tk.Frame:
        return tk.Frame(
            parent,
            bg=self.bg_card,
            highlightbackground=self.border_col,
            highlightthickness=1,
            padx=padx,
            pady=pady,
        )

    def _kpi_card(self, parent, title: str, value: str, subtitle: str, accent: str) -> tk.Frame:
        card = tk.Frame(
            parent,
            bg=self.bg_card,
            highlightbackground=self.border_col,
            highlightthickness=1,
            padx=16,
            pady=14,
        )
        tk.Frame(card, bg=accent, height=3).pack(fill=tk.X, pady=(0, 10))
        tk.Label(card, text=title, bg=self.bg_card, fg=self.fg_secondary, font=(FONT_FAMILY, 9, "bold"), anchor="w").pack(fill=tk.X)
        tk.Label(card, text=value, bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 16, "bold"), anchor="w").pack(fill=tk.X, pady=(4, 2))
        tk.Label(card, text=subtitle, bg=self.bg_card, fg=accent, font=(FONT_FAMILY, 10, "bold"), anchor="w").pack(fill=tk.X)
        return card

    def _styled_entry(self, parent, default_text: str) -> tk.Entry:
        entry = tk.Entry(
            parent,
            bg=self.bg_subtle,
            fg=self.fg_primary,
            insertbackground=self.fg_primary,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.border_col,
            highlightcolor=self.primary,
            font=(FONT_FAMILY, 12),
        )
        entry.insert(0, default_text)
        return entry

    def _draw_progress_bar(self, canvas: tk.Canvas, ratio: float, color: str) -> None:
        canvas.update_idletasks()
        canvas.delete("all")
        w = canvas.winfo_width() if canvas.winfo_width() > 50 else int(canvas["width"])
        h = canvas.winfo_height() if canvas.winfo_height() > 10 else int(canvas["height"])
        clamped = max(0.0, min(1.0, ratio))
        canvas.create_rectangle(0, 0, w, h, fill=self.bg_subtle, outline=self.border_col)
        fill_w = int(w * clamped)
        if fill_w > 0:
            canvas.create_rectangle(0, 0, fill_w, h, fill=color, outline="")
        canvas.create_text(w / 2, h / 2, text=f"{clamped * 100:.0f}%", fill=self.fg_primary, font=(FONT_FAMILY, 10, "bold"))

    def _draw_donut_chart(self, canvas: tk.Canvas, principal_amt: float, interest_amt: float) -> None:
        canvas.update_idletasks()
        canvas.delete("all")
        total = max(principal_amt + interest_amt, 1.0)
        p_angle = (principal_amt / total) * 360.0
        i_angle = 360.0 - p_angle

        x0, y0, x1, y1 = 14, 22, 148, 156
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2

        canvas.create_arc(x0, y0, x1, y1, start=90, extent=-p_angle, fill=self.primary, outline=self.bg_card, width=2)
        canvas.create_arc(x0, y0, x1, y1, start=90 - p_angle, extent=-i_angle, fill=self.amber, outline=self.bg_card, width=2)
        canvas.create_oval(x0 + 30, y0 + 30, x1 - 30, y1 - 30, fill=self.bg_card, outline="")

        p_pct = (principal_amt / total) * 100
        i_pct = (interest_amt / total) * 100
        canvas.create_text(cx, cy, text=f"{p_pct:.0f}%\nPrin", fill=self.fg_primary, font=(FONT_FAMILY, 9, "bold"))

        lx = 166
        canvas.create_rectangle(lx, 42, lx + 12, 54, fill=self.primary, outline="")
        canvas.create_text(
            lx + 18,
            48,
            text=f"Principal ({p_pct:.1f}%)\nPKR {principal_amt:,.0f}",
            anchor="w",
            fill=self.fg_primary,
            font=(FONT_FAMILY, 9, "bold"),
        )

        canvas.create_rectangle(lx, 96, lx + 12, 108, fill=self.amber, outline="")
        canvas.create_text(
            lx + 18,
            102,
            text=f"Interest ({i_pct:.1f}%)\nPKR {interest_amt:,.0f}",
            anchor="w",
            fill=self.fg_primary,
            font=(FONT_FAMILY, 9, "bold"),
        )

    def _draw_schedule_chart(self, canvas: tk.Canvas, schedule) -> None:
        canvas.update_idletasks()
        canvas.delete("all")
        sample = schedule[:10]
        if not sample:
            return
        max_val = max(row.remaining_balance for row in sample) or 1.0
        w = canvas.winfo_width() if canvas.winfo_width() > 50 else int(canvas["width"])
        h = canvas.winfo_height() if canvas.winfo_height() > 50 else int(canvas["height"])
        n = len(sample)
        gap = 8
        usable_w = max(w - 44, 120)
        bar_w = max(14, (usable_w - gap * (n - 1)) // n)
        total_bars_w = bar_w * n + gap * (n - 1)
        start_x = max(16, (w - total_bars_w) // 2)
        base_y = h - 26

        canvas.create_line(14, base_y, w - 14, base_y, fill=self.border_col)
        for i, row in enumerate(sample):
            x0 = start_x + i * (bar_w + gap)
            bar_h = int((row.remaining_balance / max_val) * max(base_y - 28, 20))
            y0 = base_y - bar_h
            canvas.create_rectangle(x0, y0, x0 + bar_w, base_y, fill=self.cyan, outline="")
            canvas.create_text(
                x0 + bar_w / 2,
                base_y + 12,
                text=f"M{row.month}",
                fill=self.fg_secondary,
                font=(FONT_FAMILY, 8, "bold"),
            )

    def render_screen(self, num: int) -> None:
        self._clear_body()
        app = self.app_data
        emi = app.loan.calculate_emi()
        total_pay = emi * app.loan.months
        total_int = max(total_pay - app.loan.principal, 0.0)
        schedule = app.loan.generate_schedule()

        if num == 1:
            kpi_grid = tk.Frame(self.body, bg=self.bg_app)
            kpi_grid.pack(fill=tk.X, pady=(0, 16))
            kpi_grid.columnconfigure((0, 1, 2, 3), weight=1, uniform="kpi")

            cards = [
                self._kpi_card(kpi_grid, "PRINCIPAL AMOUNT", f"PKR {app.loan.principal:,.0f}", f"Tenure: {app.loan.months} Months", self.primary),
                self._kpi_card(kpi_grid, "MONTHLY INSTALLMENT", f"PKR {emi:,.2f}", f"APR: {app.loan.annual_rate * 100:.2f}%", self.cyan),
                self._kpi_card(kpi_grid, "TOTAL INTEREST", f"PKR {total_int:,.0f}", f"Payable: PKR {total_pay:,.0f}", self.amber),
                self._kpi_card(kpi_grid, "APPLICATION STATE", app.status.upper(), f"Applicant: {app.applicant.full_name}", self.emerald),
            ]
            for idx, c in enumerate(cards):
                c.grid(row=0, column=idx, sticky="nsew", padx=(0 if idx == 0 else 7, 7 if idx < 3 else 0))

            charts_row = tk.Frame(self.body, bg=self.bg_app)
            charts_row.pack(fill=tk.BOTH, expand=True)
            charts_row.columnconfigure((0, 1), weight=1, uniform="charts")
            charts_row.rowconfigure(0, weight=1)

            c_left = self._card(charts_row)
            c_left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
            tk.Label(c_left, text="Principal vs. Interest Composition", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 12, "bold"), anchor="w").pack(fill=tk.X)
            pie = tk.Canvas(c_left, width=430, height=190, bg=self.bg_card, highlightthickness=0)
            pie.pack(fill=tk.X, pady=10)
            self._draw_donut_chart(pie, app.loan.principal, total_int)

            c_right = self._card(charts_row)
            c_right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
            tk.Label(c_right, text="Remaining Balance Trajectory (M1 - M10)", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 12, "bold"), anchor="w").pack(fill=tk.X)
            bars = tk.Canvas(c_right, width=440, height=190, bg=self.bg_card, highlightthickness=0)
            bars.pack(fill=tk.X, pady=10)
            self._draw_schedule_chart(bars, schedule)
            return

        if num == 2:
            card = self._card(self.body)
            card.pack(fill=tk.BOTH, expand=True)
            tk.Label(card, text="Applicant Profile & Eligibility Engine", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 14, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 12))

            form = tk.Frame(card, bg=self.bg_card)
            form.pack(fill=tk.X, pady=(0, 12))
            form.columnconfigure(1, weight=1)

            tk.Label(form, text="Full Name", bg=self.bg_card, fg=self.fg_secondary, font=(FONT_FAMILY, 11, "bold"), anchor="w").grid(row=0, column=0, sticky="w", pady=6, padx=(0, 16))
            name_e = self._styled_entry(form, app.applicant.full_name)
            name_e.grid(row=0, column=1, sticky="ew", pady=6)

            tk.Label(form, text="CNIC Number", bg=self.bg_card, fg=self.fg_secondary, font=(FONT_FAMILY, 11, "bold"), anchor="w").grid(row=1, column=0, sticky="w", pady=6, padx=(0, 16))
            cnic_e = self._styled_entry(form, app.applicant.cnic)
            cnic_e.grid(row=1, column=1, sticky="ew", pady=6)

            tk.Label(form, text="Monthly Income (PKR)", bg=self.bg_card, fg=self.fg_secondary, font=(FONT_FAMILY, 11, "bold"), anchor="w").grid(row=2, column=0, sticky="w", pady=6, padx=(0, 16))
            inc_e = self._styled_entry(form, f"{app.applicant.monthly_income:.0f}")
            inc_e.grid(row=2, column=1, sticky="ew", pady=6)

            eligible, msg = app.is_eligible()
            verdict_lbl = tk.Label(
                card,
                text=f"Eligibility Verdict: {msg}  |  Current EMI: PKR {emi:,.2f}",
                bg=self.bg_subtle,
                fg=self.emerald if eligible else self.amber,
                font=(FONT_FAMILY, 11, "bold"),
                padx=14,
                pady=10,
                anchor="w",
            )
            verdict_lbl.pack(fill=tk.X, pady=(4, 12))

            def update_applicant():
                try:
                    inc_val = float(inc_e.get())
                    if inc_val <= 0:
                        raise ValueError
                    app.applicant.full_name = name_e.get().strip() or app.applicant.full_name
                    app.applicant.cnic = cnic_e.get().strip() or app.applicant.cnic
                    app.applicant.monthly_income = inc_val
                    ok, status_msg = app.is_eligible()
                    verdict_lbl.config(
                        text=f"Eligibility Verdict: {status_msg}  |  Current EMI: PKR {app.loan.calculate_emi():,.2f}",
                        fg=self.emerald if ok else self.amber,
                    )
                    self.refresh_screen()
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid positive monthly income.")

            tk.Button(
                card,
                text="Save & Evaluate Eligibility",
                bg=self.primary,
                fg="#FFFFFF",
                relief=tk.FLAT,
                font=(FONT_FAMILY, 11, "bold"),
                padx=16,
                pady=8,
                cursor="hand2",
                command=update_applicant,
            ).pack(anchor="w")
            return

        if num == 3:
            split = tk.Frame(self.body, bg=self.bg_app)
            split.pack(fill=tk.BOTH, expand=True)
            split.columnconfigure((0, 1), weight=1, uniform="sim")
            split.rowconfigure(0, weight=1)

            left = self._card(split)
            left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
            tk.Label(left, text="Loan Parameters", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 13, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 10))

            tk.Label(left, text="Principal (PKR)", bg=self.bg_card, fg=self.fg_secondary, font=(FONT_FAMILY, 10, "bold"), anchor="w").pack(fill=tk.X)
            p_entry = self._styled_entry(left, f"{app.loan.principal:.0f}")
            p_entry.pack(fill=tk.X, pady=(3, 10))

            tk.Label(left, text="Annual Interest Rate (%)", bg=self.bg_card, fg=self.fg_secondary, font=(FONT_FAMILY, 10, "bold"), anchor="w").pack(fill=tk.X)
            r_entry = self._styled_entry(left, f"{app.loan.annual_rate * 100:.2f}")
            r_entry.pack(fill=tk.X, pady=(3, 10))

            tk.Label(left, text="Tenure (Months)", bg=self.bg_card, fg=self.fg_secondary, font=(FONT_FAMILY, 10, "bold"), anchor="w").pack(fill=tk.X)
            m_entry = self._styled_entry(left, str(app.loan.months))
            m_entry.pack(fill=tk.X, pady=(3, 14))

            right = self._card(split)
            right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
            tk.Label(right, text="Live Simulation Output", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 13, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 6))

            emi_lbl = tk.Label(right, text=f"Monthly EMI : PKR {emi:,.2f}", bg=self.bg_card, fg=self.cyan, font=(FONT_FAMILY, 14, "bold"), anchor="w")
            emi_lbl.pack(fill=tk.X)
            int_lbl = tk.Label(right, text=f"Interest    : PKR {total_int:,.2f}", bg=self.bg_card, fg=self.amber, font=(FONT_FAMILY, 11, "bold"), anchor="w")
            int_lbl.pack(fill=tk.X, pady=(2, 2))
            tot_lbl = tk.Label(right, text=f"Total Pay   : PKR {total_pay:,.2f}", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 11, "bold"), anchor="w")
            tot_lbl.pack(fill=tk.X, pady=(0, 8))

            pie = tk.Canvas(right, width=410, height=185, bg=self.bg_card, highlightthickness=0)
            pie.pack(fill=tk.X)
            self._draw_donut_chart(pie, app.loan.principal, total_int)

            def apply_sim():
                try:
                    p_val = float(p_entry.get())
                    r_val = float(r_entry.get()) / 100.0
                    m_val = int(m_entry.get())
                    if p_val <= 0 or r_val < 0 or m_val <= 0:
                        raise ValueError
                    app.loan.principal = p_val
                    app.loan.annual_rate = r_val
                    app.loan.months = m_val
                    n_emi = app.loan.calculate_emi()
                    n_tot = n_emi * app.loan.months
                    n_int = max(n_tot - app.loan.principal, 0.0)
                    emi_lbl.config(text=f"Monthly EMI : PKR {n_emi:,.2f}")
                    int_lbl.config(text=f"Interest    : PKR {n_int:,.2f}")
                    tot_lbl.config(text=f"Total Pay   : PKR {n_tot:,.2f}")
                    self._draw_donut_chart(pie, app.loan.principal, n_int)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Check principal, interest rate, and tenure values.")

            tk.Button(
                left,
                text="Simulate Loan",
                bg=self.primary,
                fg="#FFFFFF",
                relief=tk.FLAT,
                font=(FONT_FAMILY, 11, "bold"),
                pady=8,
                cursor="hand2",
                command=apply_sim,
            ).pack(fill=tk.X)
            return

        if num == 4:
            card = self._card(self.body)
            card.pack(fill=tk.BOTH, expand=True)
            tk.Label(card, text="Full Amortization Schedule Table", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 13, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 8))

            cols = ("month", "payment", "principal", "interest", "balance")
            tree = ttk.Treeview(card, columns=cols, show="headings", style="Dark.Treeview", height=13)
            headers = {
                "month": "Month",
                "payment": "Installment (PKR)",
                "principal": "Principal Paid (PKR)",
                "interest": "Interest Paid (PKR)",
                "balance": "Remaining Balance (PKR)",
            }
            for col in cols:
                tree.heading(col, text=headers[col])
                tree.column(col, anchor="e" if col != "month" else "center", width=150)

            for row in schedule:
                tree.insert(
                    "",
                    tk.END,
                    values=(
                        f"{row.month:02d}",
                        f"{row.payment:,.2f}",
                        f"{row.principal_paid:,.2f}",
                        f"{row.interest_paid:,.2f}",
                        f"{row.remaining_balance:,.2f}",
                    ),
                )

            sb = ttk.Scrollbar(card, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=sb.set)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            sb.pack(side=tk.RIGHT, fill=tk.Y)
            return

        if num == 5:
            card = self._card(self.body)
            card.pack(fill=tk.BOTH, expand=True)
            tk.Label(card, text="Mathematical & Numerical Analysis Lab", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 14, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 12))

            mono = self.analyzer.verify_monotonic_decrease(schedule)
            bounded = self.analyzer.verify_boundedness(schedule, app.loan.principal)
            implied = self.analyzer.solve_implied_annual_rate(
                principal=app.loan.principal,
                months=app.loan.months,
                target_emi=emi,
            )

            checks = [
                ("Monotonic Balance Decrease", str(mono), self.emerald if mono else self.rose),
                ("Boundedness in [0, Principal]", str(bounded), self.emerald if bounded else self.rose),
                ("Bisection Implied Annual Rate", f"{implied * 100:.2f}%", self.cyan),
            ]
            for label, val, col in checks:
                row = tk.Frame(card, bg=self.bg_subtle, padx=14, pady=10)
                row.pack(fill=tk.X, pady=5)
                tk.Label(row, text=label, bg=self.bg_subtle, fg=self.fg_secondary, font=(FONT_FAMILY, 11, "bold"), width=32, anchor="w").pack(side=tk.LEFT)
                tk.Label(row, text=val, bg=self.bg_subtle, fg=col, font=(FONT_FAMILY, 12, "bold"), anchor="w").pack(side=tk.LEFT)
            return

        if num == 6:
            kpi = tk.Frame(self.body, bg=self.bg_app)
            kpi.pack(fill=tk.X, pady=(0, 14))
            kpi.columnconfigure((0, 1, 2), weight=1, uniform="kyc")

            cnic_digits = "".join(ch for ch in app.applicant.cnic if ch.isdigit())
            app.applicant.kyc_verified = len(cnic_digits) >= 13

            c1 = self._kpi_card(kpi, "APPLICANT", app.applicant.full_name, "Primary Borrower", self.primary)
            c2 = self._kpi_card(kpi, "CNIC RECORD", app.applicant.cnic, f"{len(cnic_digits)} Digits Detected", self.cyan)
            c3 = self._kpi_card(
                kpi,
                "KYC CLEARANCE",
                "VERIFIED" if app.applicant.kyc_verified else "ACTION NEEDED",
                "Identity Check Passed" if app.applicant.kyc_verified else "Enter valid 13-digit CNIC",
                self.emerald if app.applicant.kyc_verified else self.amber,
            )
            for i, c in enumerate((c1, c2, c3)):
                c.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 7, 7 if i < 2 else 0))

            card = self._card(self.body)
            card.pack(fill=tk.BOTH, expand=True)
            tk.Label(card, text="Identity & CNIC Verification Control", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 13, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 10))

            cnic_box = self._styled_entry(card, app.applicant.cnic)
            cnic_box.pack(fill=tk.X, pady=(0, 12))

            def verify_cnic():
                entered = cnic_box.get().strip()
                digits = "".join(ch for ch in entered if ch.isdigit())
                if len(digits) < 13:
                    app.applicant.kyc_verified = False
                    messagebox.showwarning("CNIC Check", "Please enter a valid 13-digit CNIC number.")
                else:
                    app.applicant.cnic = entered
                    app.applicant.kyc_verified = True
                    messagebox.showinfo("KYC Verified", f"CNIC {entered} verified successfully.")
                self.refresh_screen()

            tk.Button(
                card,
                text="Verify CNIC & Update KYC",
                bg=self.emerald,
                fg="#0F172A",
                relief=tk.FLAT,
                font=(FONT_FAMILY, 11, "bold"),
                padx=16,
                pady=8,
                cursor="hand2",
                command=verify_cnic,
            ).pack(anchor="w")
            return

        if num == 7:
            if not app.applicant.documents_uploaded:
                app.applicant.documents_uploaded = ["CNIC_Front_Back.pdf", "Salary_Certificate.pdf", "Bank_Statement_6M.pdf"]

            split = tk.Frame(self.body, bg=self.bg_app)
            split.pack(fill=tk.BOTH, expand=True)
            split.columnconfigure((0, 1), weight=1, uniform="docs")
            split.rowconfigure(0, weight=1)

            left = self._card(split)
            left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
            tk.Label(left, text="Uploaded Verification Files", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 13, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 10))

            for idx, doc in enumerate(app.applicant.documents_uploaded, start=1):
                item = tk.Frame(left, bg=self.bg_subtle, padx=12, pady=9)
                item.pack(fill=tk.X, pady=4)
                tk.Label(item, text=f"0{idx}. {doc}", bg=self.bg_subtle, fg=self.fg_primary, font=(FONT_FAMILY, 11, "bold"), anchor="w").pack(side=tk.LEFT)
                tk.Label(item, text="READY", bg=self.bg_subtle, fg=self.emerald, font=(FONT_FAMILY, 9, "bold")).pack(side=tk.RIGHT)

            right = self._card(split)
            right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
            tk.Label(right, text="Upload New Document", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 13, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 8))
            tk.Label(right, text=f"Total Files in Vault: {len(app.applicant.documents_uploaded)}", bg=self.bg_card, fg=self.cyan, font=(FONT_FAMILY, 11, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 10))

            doc_entry = self._styled_entry(right, "Tax_Return_2026.pdf")
            doc_entry.pack(fill=tk.X, pady=(0, 10))

            def add_doc():
                name = doc_entry.get().strip()
                if name:
                    app.applicant.documents_uploaded.append(name)
                    self.refresh_screen()

            def browse_doc():
                path = filedialog.askopenfilename(title="Select Supporting Document")
                if path:
                    fname = path.split("/")[-1].split("\\")[-1]
                    app.applicant.documents_uploaded.append(fname)
                    self.refresh_screen()

            tk.Button(right, text="+ Add Document Name", bg=self.primary, fg="#FFFFFF", relief=tk.FLAT, font=(FONT_FAMILY, 11, "bold"), pady=8, cursor="hand2", command=add_doc).pack(fill=tk.X, pady=(0, 8))
            tk.Button(right, text="Browse File from PC", bg="#334155", fg=self.fg_primary, relief=tk.FLAT, font=(FONT_FAMILY, 11, "bold"), pady=8, cursor="hand2", command=browse_doc).pack(fill=tk.X)
            return

        if num == 8:
            card = self._card(self.body)
            card.pack(fill=tk.BOTH, expand=True)
            tk.Label(card, text="APR Disclosure & Loan Agreement Terms", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 14, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 10))

            summary_box = tk.Frame(card, bg=self.bg_subtle, padx=16, pady=12)
            summary_box.pack(fill=tk.X, pady=(0, 14))
            for k, v in [
                ("Application Reference", app.app_id),
                ("Annual Percentage Rate (APR)", f"{app.loan.annual_rate * 100:.2f}%"),
                ("Repayment Tenure", f"{app.loan.months} Monthly Installments"),
                ("Estimated Total Cost of Credit", f"PKR {total_int:,.2f}"),
            ]:
                r = tk.Frame(summary_box, bg=self.bg_subtle)
                r.pack(fill=tk.X, pady=3)
                tk.Label(r, text=k, bg=self.bg_subtle, fg=self.fg_secondary, font=(FONT_FAMILY, 11, "bold"), width=30, anchor="w").pack(side=tk.LEFT)
                tk.Label(r, text=v, bg=self.bg_subtle, fg=self.fg_primary, font=(FONT_FAMILY, 11, "bold"), anchor="w").pack(side=tk.LEFT)

            terms_var = tk.BooleanVar(value=bool(getattr(app, "terms_accepted", False)))
            chk = tk.Checkbutton(
                card,
                text="I confirm the APR, repayment schedule, and Loan Wise terms & conditions.",
                variable=terms_var,
                bg=self.bg_card,
                fg=self.fg_primary,
                selectcolor=self.bg_subtle,
                activebackground=self.bg_card,
                activeforeground=self.fg_primary,
                font=(FONT_FAMILY, 11, "bold"),
            )
            chk.pack(anchor="w", pady=(0, 12))

            def save_terms():
                app.terms_accepted = bool(terms_var.get())
                messagebox.showinfo("Terms Updated", "Terms Accepted: Yes" if app.terms_accepted else "Terms Accepted: No")
                self.refresh_screen()

            tk.Button(card, text="Confirm Agreement Status", bg=self.primary, fg="#FFFFFF", relief=tk.FLAT, font=(FONT_FAMILY, 11, "bold"), padx=16, pady=8, cursor="hand2", command=save_terms).pack(anchor="w")
            return

        if num == 9:
            elig, elig_msg = app.is_eligible()
            kyc_ok = bool(getattr(app.applicant, "kyc_verified", False))
            terms_ok = bool(getattr(app, "terms_accepted", False))
            docs_ok = len(getattr(app.applicant, "documents_uploaded", [])) >= 1

            score = sum([elig, kyc_ok, terms_ok, docs_ok])
            app.status = "Approved" if (elig and kyc_ok and terms_ok) else "In Review"

            card = self._card(self.body)
            card.pack(fill=tk.BOTH, expand=True)
            tk.Label(card, text="Application Readiness & Approval Pipeline", bg=self.bg_card, fg=self.fg_primary, font=(FONT_FAMILY, 14, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 6))

            prog = tk.Canvas(card, width=820, height=22, bg=self.bg_subtle, highlightthickness=0)
            prog.pack(fill=tk.X, pady=(0, 14))
            self._draw_progress_bar(prog, score / 4.0, self.emerald if score == 4 else self.amber)

            stages = [
                ("01. Income & Eligibility Check", elig, elig_msg),
                ("02. Applicant KYC Verification", kyc_ok, "CNIC Verified" if kyc_ok else "Pending CNIC Verification"),
                ("03. Supporting Documents Vault", docs_ok, f"{len(app.applicant.documents_uploaded)} Documents Ready"),
                ("04. APR & Terms Sign-off", terms_ok, "Accepted" if terms_ok else "Pending Acceptance"),
            ]
            for st_title, passed, detail in stages:
                row = tk.Frame(card, bg=self.bg_subtle, padx=14, pady=9)
                row.pack(fill=tk.X, pady=4)
                tk.Label(row, text=st_title, bg=self.bg_subtle, fg=self.fg_primary, font=(FONT_FAMILY, 11, "bold"), width=32, anchor="w").pack(side=tk.LEFT)
                tk.Label(row, text=detail, bg=self.bg_subtle, fg=self.fg_secondary, font=(FONT_FAMILY, 10), anchor="w").pack(side=tk.LEFT)
                tk.Label(
                    row,
                    text="PASSED" if passed else "PENDING",
                    bg=self.bg_subtle,
                    fg=self.emerald if passed else self.amber,
                    font=(FONT_FAMILY, 10, "bold"),
                ).pack(side=tk.RIGHT)
            return

        if num == 10:
            paid_count = getattr(app, "paid_installments", len(app.receipts))
            ratio = paid_count / max(app.loan.months, 1)

            top_kpi = tk.Frame(self.body, bg=self.bg_app)
            top_kpi.pack(fill=tk.X, pady=(0, 14))
            top_kpi.columnconfigure((0, 1, 2), weight=1, uniform="pay")

            c1 = self._kpi_card(top_kpi, "INSTALLMENTS PAID", f"{paid_count} / {app.loan.months}", "Repayment Progress", self.emerald)
            c2 = self._kpi_card(top_kpi, "MONTHLY EMI DUE", f"PKR {emi:,.2f}", "Standard Installment", self.cyan)
            c3 = self._kpi_card(top_kpi, "RECEIPTS ISSUED", str(len(app.receipts)), "Digital Payment Slips", self.primary)
            for i, c in enumerate((c1, c2, c3)):
                c.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 7, 7 if i < 2 else 0))

            card = self._card(self.body)
            card.pack(fill=tk.BOTH, expand=True)

            bar_canvas = tk.Canvas(card, width=820, height=20, bg=self.bg_subtle, highlightthickness=0)
            bar_canvas.pack(fill=tk.X, pady=(0, 12))
            self._draw_progress_bar(bar_canvas, ratio, self.cyan)

            cols = ("receipt", "month", "amount")
            tree = ttk.Treeview(card, columns=cols, show="headings", style="Dark.Treeview", height=6)
            tree.heading("receipt", text="Receipt ID")
            tree.heading("month", text="Installment Month")
            tree.heading("amount", text="Amount Paid (PKR)")
            tree.column("receipt", anchor="w", width=220)
            tree.column("month", anchor="center", width=160)
            tree.column("amount", anchor="e", width=180)

            for r in app.receipts:
                tree.insert("", tk.END, values=(r.receipt_id, f"Month {r.month_number:02d}", f"{r.amount_paid:,.2f}"))
            tree.pack(fill=tk.X, pady=(0, 12))

            def record_payment():
                rec = app.pay_next_installment()
                if rec:
                    messagebox.showinfo("Payment Recorded", f"Receipt {rec.receipt_id} issued for PKR {rec.amount_paid:,.2f}")
                    self.refresh_screen()
                else:
                    messagebox.showinfo("Completed", "All installments have already been paid.")

            tk.Button(
                card,
                text="+ Pay Next Installment & Generate Receipt",
                bg=self.emerald,
                fg="#0F172A",
                relief=tk.FLAT,
                font=(FONT_FAMILY, 11, "bold"),
                padx=16,
                pady=8,
                cursor="hand2",
                command=record_payment,
            ).pack(anchor="w")

    def refresh_screen(self) -> None:
        num, title = self.screens_info[self.current_index]
        self.header_lbl.config(text=title)
        self.status_badge.config(text=f"{self.app_data.app_id}  •  {self.app_data.status}")
        self.step_lbl.config(text=f"Screen {num} of 10")

        for i, btn in enumerate(self.nav_buttons):
            if i == self.current_index:
                btn.config(bg=self.primary, fg="#FFFFFF", font=(FONT_FAMILY, 11, "bold"))
            else:
                btn.config(bg=self.bg_sidebar, fg=self.fg_secondary, font=(FONT_FAMILY, 11))

        self.prev_btn.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_index < len(self.screens_info) - 1 else tk.DISABLED)
        self.render_screen(num)

    def go_to_screen(self, idx: int) -> None:
        self.current_index = idx
        self.refresh_screen()

    def next_screen(self) -> None:
        if self.current_index < len(self.screens_info) - 1:
            self.current_index += 1
            self.refresh_screen()

    def prev_screen(self) -> None:
        if self.current_index > 0:
            self.current_index -= 1
            self.refresh_screen()


if __name__ == "__main__":
    applicant = Applicant(
        full_name="Ayesha Arif",
        cnic="36302-1234567-1",
        monthly_income=135000.0,
    )
    loan = Loan(principal=500000.0, annual_rate=0.14, months=24)
    application = LoanApplication(app_id="LN-2026-001", applicant=applicant, loan=loan)

    root = tk.Tk()
    app = LoanWiseUniversityApp(root, application)
    root.mainloop()
    