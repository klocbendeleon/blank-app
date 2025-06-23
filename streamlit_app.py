import streamlit as st

# Title
st.title("BDL's Water Profile Calculator")

# Source Profile
st.sidebar.header("Source Water Profile")
source_profile = st.sidebar.selectbox("Select Source", ["Le Minerale", "Custom"])
if source_profile == "Le Minerale":
    KH_src = 133.2
    GH_src = 63.3
    TDS_src = 255.5
    st.sidebar.markdown("**Le Minerale defaults:** KH=133.2, GH=63.3, TDS=255.5 mg/L")
else:
    st.sidebar.header("Custom Source Data (mg/L)")
    KH_src = st.sidebar.number_input("KH Source", value=40.0)
    GH_src = st.sidebar.number_input("GH Source", value=20.0)
    TDS_src = st.sidebar.number_input("TDS Source", value=150.0)

# Target Profile
st.sidebar.header("Target Profile")
preset = st.sidebar.selectbox("Preset", ["Custom", "Simplified Rao/Perger", "Classic Rao/Perger"])
if preset == "Simplified Rao/Perger":
    KH_tgt, GH_tgt = 40.0, 88.0
elif preset == "Classic Rao/Perger":
    KH_tgt, GH_tgt = 40.0, 50.0
else:
    st.sidebar.header("Custom Targets")
    KH_tgt = st.sidebar.number_input("Target KH", value=40.0)
    GH_tgt = st.sidebar.number_input("Target GH", value=80.0)

# Batch size
batch_l = st.number_input("Batch size (L)", value=1.0, step=0.1)
batch_ml = batch_l * 1000

# Booster concentration strength (ppm GH per mL concentrate)
booster_strength = 6.6  # ppm GH improved per mL of concentrate

# Calculation function with booster_ppm return
def calculate_recipe(KH_src, GH_src, TDS_src, KH_tgt, GH_tgt, batch_ml, batch_l, booster_strength):
    # Dilution fraction for KH
    frac = KH_tgt / KH_src if KH_src else 0
    LM_vol = frac * batch_ml  # mL of source water
    # Base GH and TDS after dilution
    base_GH = GH_src * frac
    base_TDS = TDS_src * frac
    # Booster dosing
    delta_GH = max(GH_tgt - base_GH, 0)
    booster_per_l = delta_GH / booster_strength  # mL per L
    total_booster_ml = booster_per_l * batch_l
    # Distilled water adjusted for booster volume
    DI_vol = batch_ml - LM_vol - total_booster_ml
    # Final TDS: base TDS + booster solids (11 mg per mL)
    total_booster_solids_mg = total_booster_ml * 11  # mg total
    booster_ppm = total_booster_solids_mg / batch_l  # mg/L contributed
    final_TDS = base_TDS + booster_ppm
    return LM_vol, DI_vol, base_GH, base_TDS, booster_per_l, total_booster_ml, booster_ppm, final_TDS

# Perform calculation
LM_vol, DI_vol, base_GH, base_TDS, booster_per_l, total_booster_ml, booster_ppm, final_TDS = calculate_recipe(
    KH_src, GH_src, TDS_src, KH_tgt, GH_tgt, batch_ml, batch_l, booster_strength
)

# Display Results
st.subheader(f"Recipe for {batch_l:.1f} L Batch")
st.write(f"- Source: {source_profile}")
st.write(f"- Source KH: {KH_src:.1f} ppm, GH: {GH_src:.1f} ppm, TDS: {TDS_src:.1f} mg/L")
st.write(f"- Le Minerale Volume: {LM_vol:.1f} mL")
st.write(f"- Distilled Water Volume: {DI_vol:.1f} mL")
st.write(f"- Base GH: {base_GH:.1f} ppm, Base TDS: {base_TDS:.1f} mg/L")

st.subheader("GH Booster Dosage")
st.write(f"- Add {booster_per_l:.2f} mL per litre ({total_booster_ml:.1f} mL total)")

st.subheader("Final Water Parameters")
st.write(f"- KH: {KH_tgt:.1f} ppm")
st.write(f"- GH: {GH_tgt:.1f} ppm")
st.write(f"- TDS: {final_TDS:.1f} mg/L")
st.write(f"- Booster contributed: {booster_ppm:.1f} ppm")

st.markdown("---")
st.subheader("Booster Concentrate Recipe (1 L)")
st.write("- 4.40 g Calcium chloride (CaCl₂)\n- 6.60 g Epsom salt (MgSO₄·7H₂O)\n- Fill to 1 L with distilled water")