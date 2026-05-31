import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="ChemSim", layout="wide")

# CSS Terpisah agar tidak merusak f-string
st.markdown("""
<style>
    .equation-box {
        background: #020617; color: #22d3ee; padding: 15px;
        border-radius: 10px; border: 1px solid #22d3ee;
        text-align: center; font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧪 Virtual Test Tube Simulator")

# Logika Simulasi
sampel = st.selectbox("Pilih Sampel:", ["-- Kosong --", "Formaldehida"])
reagen = st.selectbox("Pilih Reagen:", ["-- Tanpa Reagen --", "Tollens"])
suhu = st.slider("Suhu (°C)", 25, 100, 25)

# Tentukan warna dan status
warna = "#cbd5e1" if sampel != "-- Kosong --" else "rgba(255,255,255,0.1)"
status = "Sampel siap."

# Render HTML dengan cara yang aman (menggunakan .format() bukan f-string agar { } tidak error)
html_template = """
<div style="border: 5px solid #e2e8f0; width: 100px; height: 200px; margin: 0 auto; position: relative;">
    <div style="background: {color}; width: 100%; height: 50%; position: absolute; bottom: 0;"></div>
</div>
<p style="text-align: center;">Suhu: {temp}°C</p>
"""

st.components.v1.html(html_template.format(color=warna, temp=suhu), height=300)

if sampel == "Formaldehida" and reagen == "Tollens" and suhu >= 70:
    st.success("POSITIF! Terbentuk cermin perak.")
else:
    st.info(status)
