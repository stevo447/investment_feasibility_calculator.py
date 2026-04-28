import streamlit as st

st.set_page_config(page_title="Investment Feasibility Calculator", page_icon="📈", layout="centered")

def calculate_investment_feasibility(initial_investment, annual_revenue,
                                     annual_operating_cost, project_duration_years,
                                     discount_rate, growth_rate=0):
    cash_flows = [-initial_investment]
    for year in range(1, int(project_duration_years) + 1):
        revenue_t = annual_revenue * ((1 + growth_rate / 100) ** (year - 1))
        net_cash_flow = revenue_t - annual_operating_cost
        cash_flows.append(net_cash_flow)

    npv = 0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate / 100) ** t)

    cumulative = 0
    payback_period = None
    for i, cf in enumerate(cash_flows[1:], start=1):
        cumulative += cf
        if cumulative >= initial_investment and payback_period is None:
            payback_period = i

    irr = None
    for r in [x / 10 for x in range(0, 1000)]:
        test_npv = sum(cf / ((1 + r/100) ** t) for t, cf in enumerate(cash_flows))
        if abs(test_npv) < 1000:
            irr = r
            break

    viability = "Viable" if npv > 0 else "Not Attractive"

    return {
        "npv": round(npv, 2),
        "irr": round(irr, 2) if irr is not None else None,
        "payback_period": payback_period,
        "viability": viability
    }

st.title("Investment Feasibility Calculator")
st.write("Assess project viability using revenue, cost, duration, and discount rate assumptions.")

with st.form("investment_form"):
    initial_investment = st.number_input("Initial Investment", min_value=0.0, step=1000.0)
    annual_revenue = st.number_input("Expected Annual Revenue", min_value=0.0, step=1000.0)
    annual_operating_cost = st.number_input("Expected Annual Operating Cost", min_value=0.0, step=1000.0)
    project_duration_years = st.number_input("Project Duration (Years)", min_value=1, step=1)
    discount_rate = st.number_input("Discount Rate (%)", min_value=0.0, step=0.5)
    growth_rate = st.number_input("Growth Rate (%)", min_value=0.0, step=0.5)
    submitted = st.form_submit_button("Calculate Feasibility")

if submitted:
    result = calculate_investment_feasibility(
        initial_investment, annual_revenue, annual_operating_cost,
        project_duration_years, discount_rate, growth_rate
    )

    st.success("Calculation Complete")
    st.metric("NPV", f"₦{result['npv']:,.2f}")
    st.metric("IRR", f"{result['irr']}%" if result['irr'] is not None else "N/A")
    st.metric("Payback Period", f"{result['payback_period']} year(s)" if result['payback_period'] else "Not recovered")
    st.write(f"**Viability:** {result['viability']}")

    st.info("Indicative output only. For a detailed feasibility review, contact Quant Vision Labs.")
    st.markdown("[Request Consultation](https://yourwebsite.com/request-consultation)")
