import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="🧵 SmartCut AI Platform", layout="wide")

# ---------------- HEADER BANNER ----------------
st.markdown(
    """
    <div style="background-color:#0E1117;padding:20px;border-radius:10px">
    <h1 style="color:white;text-align:center;">
    🧵 SmartCut: AI Textile Waste Optimization Platform
    </h1>
    <p style="color:white;text-align:center;">
    Predict and Reduce Fabric Waste in Garment Manufacturing 👕
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
page = st.sidebar.selectbox(
    "🧭 Navigation",
    ["Home", "Waste Prediction", "Simulation Dashboard", "About"]
)

# ---------------- SYNTHETIC DATASET ----------------
np.random.seed(42)
rows = 200

fabric_length_data = np.random.uniform(80, 130, rows)
fabric_width_data = np.random.uniform(1.3, 1.7, rows)
pattern_area_data = np.random.uniform(1.5, 2.2, rows)
quantity_data = np.random.randint(50, 120, rows)
layout_eff_data = np.random.uniform(0.70, 0.95, rows)
machine_eff_data = np.random.uniform(0.80, 0.95, rows)

waste_data = (
    (1 - layout_eff_data)*20 +
    (2 - pattern_area_data)*2 +
    (1 - machine_eff_data)*10 +
    np.random.normal(0, 1, rows)
)

data = pd.DataFrame({
    "fabric_length": fabric_length_data,
    "fabric_width": fabric_width_data,
    "pattern_area": pattern_area_data,
    "quantity": quantity_data,
    "layout_eff": layout_eff_data,
    "machine_eff": machine_eff_data,
    "waste": waste_data
})

# ---------------- ML MODEL ----------------
features = [
    "fabric_length",
    "fabric_width",
    "pattern_area",
    "quantity",
    "layout_eff",
    "machine_eff"
]

X = data[features]
y = data["waste"]

model = LinearRegression()
model.fit(X, y)

# ---------------- MODEL PERFORMANCE ----------------
pred_train = model.predict(X)
mae = mean_absolute_error(y, pred_train)

st.sidebar.markdown("### 🧠 Model Performance")
st.sidebar.metric("Mean Absolute Error", f"{mae:.2f}")

# ---------------- DATASET PREVIEW ----------------
st.sidebar.markdown("---")
if st.sidebar.checkbox("📊 View Training Dataset Sample"):
    st.subheader("Training Dataset Sample")
    st.dataframe(data.head(10))

# ---------------- HOME PAGE ----------------
if page == "Home":

    st.header("🏭 Textile Industry Challenge")

    st.write("""
    Textile manufacturing generates significant **fabric waste**
    during the **cutting stage** due to inefficient pattern layouts.
    SmartCut AI predicts fabric waste before production begins.
    """)

    st.header("📊 Industry Impact")

    col1, col2, col3 = st.columns(3)
    col1.metric("Typical Industry Waste", "15–20%")
    col2.metric("Optimized Waste Target", "5–8%")
    col3.metric("Potential Waste Reduction", "≈50%")

    st.success("👉 Use the navigation panel to start the AI simulation.")

    # KPI DASHBOARD
    st.markdown("---")
    st.subheader("📊 AI System Overview")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Dataset Samples", len(data))
    k2.metric("AI Model", "Linear Regression")
    k3.metric("Average Waste", f"{data['waste'].mean():.2f}%")
    k4.metric("Max Waste", f"{data['waste'].max():.2f}%")

    # SYSTEM WORKFLOW
    st.markdown("---")
    st.header("⚙ System Workflow")

    st.write("""
    **Production Inputs**  
    ↓  
    **AI Waste Prediction**  
    ↓  
    **Simulation Analysis**  
    ↓  
    **Optimization Recommendation**  
    ↓  
    **Production Planning**
    """)

    st.markdown("---")

    st.header("🧵 Garment Production Stages")
    st.write("""
    1️⃣ Fabric Sourcing  
    2️⃣ Fabric Spreading  
    3️⃣ Pattern Layout Planning  
    4️⃣ Fabric Cutting ✂  
    5️⃣ Sewing & Assembly  
    6️⃣ Finishing & Quality Check
    """)

# ---------------- WASTE PREDICTION PAGE ----------------
elif page == "Waste Prediction":

    st.header("🧵 Waste Prediction Tool")

    fabric_length = st.number_input(
        "Fabric Length (meters)",
        value=100.0,
        help="Total fabric roll length used in production"
    )

    fabric_width = st.number_input(
        "Fabric Width (meters)",
        value=1.5,
        help="Width of the fabric roll"
    )

    pattern_area = st.number_input(
        "Pattern Area per Garment (m²)",
        value=1.8,
        help="Fabric area required for one garment"
    )

    quantity = st.number_input(
        "Production Quantity",
        value=70,
        help="Number of garments to produce"
    )

    layout_eff = st.slider("Layout Efficiency (%)", 50, 100, 85)
    machine_eff = st.slider("Machine Efficiency (%)", 70, 100, 90)

    layout_eff = layout_eff / 100
    machine_eff = machine_eff / 100

    if layout_eff > 0.9:
        st.success("Excellent layout efficiency")

    elif layout_eff > 0.8:
        st.info("Moderate layout efficiency")

    else:
        st.warning("Low layout efficiency may increase waste")

    if st.button("🚀 Predict Waste"):

        progress = st.progress(0)

        for i in range(100):
            progress.progress(i + 1)

        with st.spinner("Running AI prediction... 🤖"):

            fabric_area = fabric_length * fabric_width
            fabric_required = pattern_area * quantity
            effective_usage = fabric_area * layout_eff

            waste = effective_usage - fabric_required
            waste_percent = (waste / fabric_area) * 100

            prediction = model.predict([[
                fabric_length,
                fabric_width,
                pattern_area,
                quantity,
                layout_eff,
                machine_eff
            ]])

        predicted_waste = prediction[0]

        # ---------------- TABS ----------------
        tab1, tab2, tab3 = st.tabs(
            ["📊 Prediction Results", "📈 Analytics", "💼 Business Impact"])

        with tab1:

            st.subheader("📐 Mathematical Waste Calculation")
            st.write(f"Fabric Area: {fabric_area:.2f} m²")
            st.write(f"Fabric Required: {fabric_required:.2f} m²")
            st.write(f"Waste Generated: {waste:.2f} m²")
            st.write(f"Waste Percentage: {waste_percent:.2f}%")

            st.subheader("🤖 AI Prediction")
            st.write(f"Predicted Waste (ML Model): {predicted_waste:.2f}%")

            efficiency_score = 100 - predicted_waste
            st.metric("Production Efficiency Score",
                      f"{efficiency_score:.0f}/100")

        with tab2:

            with st.expander("📈 Waste vs Layout Efficiency Graph", expanded=True):

                efficiencies = np.linspace(0.70, 0.95, 20)
                predictions = []

                for e in efficiencies:
                    pred = model.predict([[
                        fabric_length,
                        fabric_width,
                        pattern_area,
                        quantity,
                        e,
                        machine_eff
                    ]])
                    predictions.append(pred[0])

                fig, ax = plt.subplots()
                ax.plot(efficiencies*100, predictions)
                ax.set_xlabel("Layout Efficiency (%)")
                ax.set_ylabel("Predicted Waste (%)")
                ax.set_title("Waste vs Layout Efficiency")
                st.pyplot(fig)

        with tab3:

            st.subheader("💼 Business Profit / Loss Analysis")

            fabric_cost = st.number_input(
                "Fabric Cost per m² (₹)", value=400.0)
            garment_price = st.number_input(
                "Garment Selling Price (₹)", value=1200.0)
            production_cost = st.number_input(
                "Production Cost per Garment (₹)", value=800.0)

            waste_area = fabric_area * (predicted_waste/100)
            waste_cost = waste_area * fabric_cost

            revenue = garment_price * quantity
            total_cost = (production_cost * quantity) + waste_cost
            profit = revenue - total_cost

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Revenue (₹)", f"₹{revenue:,.2f}")
            col2.metric("Total Production Cost (₹)", f"₹{total_cost:,.2f}")
            col3.metric("Net Profit / Loss (₹)", f"₹{profit:,.2f}")

        # DOWNLOAD FULL REPORT
        report = pd.DataFrame({
            "Predicted Waste": [predicted_waste],
            "Efficiency Score": [efficiency_score],
            "Revenue": [revenue],
            "Total Cost": [total_cost],
            "Profit": [profit]
        })

        st.download_button(
            "📄 Download Full AI Report",
            report.to_csv(index=False),
            "smartcut_report.csv"
        )

# ---------------- SIMULATION DASHBOARD ----------------
elif page == "Simulation Dashboard":

    st.header("📊 Simulation Dashboard")

    efficiencies = np.linspace(0.70, 0.95, 20)
    waste_predictions = []

    for e in efficiencies:
        pred = model.predict([[100, 1.5, 1.8, 70, e, 0.9]])[0]
        waste_predictions.append(pred)

    fig, ax = plt.subplots()
    ax.plot(efficiencies*100, waste_predictions)
    ax.set_xlabel("Layout Efficiency (%)")
    ax.set_ylabel("Predicted Waste (%)")
    ax.set_title("Simulation: Layout Efficiency vs Waste")

    st.pyplot(fig)

    sim_table = pd.DataFrame({
        "Layout Efficiency (%)": efficiencies*100,
        "Predicted Waste (%)": waste_predictions
    })

    st.subheader("Simulation Data")
    st.dataframe(sim_table)

    csv_sim = sim_table.to_csv(index=False)

    st.download_button(
        label="Download Simulation Data",
        data=csv_sim,
        file_name="simulation_results.csv",
        mime="text/csv"
    )

# ---------------- ABOUT PAGE ----------------
elif page == "About":

    st.header("ℹ About the System")

    st.write("""
    SmartCut is an **AI-based textile waste optimization platform**
    designed to help garment manufacturers reduce fabric waste during
    the cutting stage of production.
    """)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("🧵 SmartCut AI | Developed for Tex-Research Hackathon")
