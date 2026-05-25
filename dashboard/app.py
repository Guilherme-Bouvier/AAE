import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import threading

# ==========================
# IA CORE
# ==========================
from analysis.pattern_detector import PatternDetector
from analysis.predictor_engine import PredictorEngine

# ==========================
# CAPTURA
# ==========================
from data_collector.scraper_playwright import PlaywrightScraper
from core_stream.stream_engine import StreamEngine

# ==========================
# VISÃO (OCR + OVERLAY)
# ==========================
from vision.screen_overlay import ScreenOverlayOCR
from vision.overlay_window import run_overlay

# ==========================
# ALERTAS
# ==========================
from alerts.stream_alert_manager import StreamAlertManager

# ==========================
# CÉREBRO DO SISTEMA
# ==========================
from core.control_center import ControlCenter
from core.engine_master import EngineMaster


# ==================================================
# CONFIG STREAMLIT
# ==================================================

st.set_page_config(
    page_title="AAE PRO - FINAL SYSTEM",
    layout="wide"
)

st.title("🧠 AAE PRO - Control Center AI System")


# ==================================================
# BANCO
# ==================================================

engine = create_engine("sqlite:///data/rounds.db")


@st.cache_data(ttl=5)
def load_data():

    df = pd.read_sql("""
        SELECT * FROM rounds
        ORDER BY id DESC
        LIMIT 200
    """, engine)

    return df


df = load_data()

history = df["multiplier"].tolist() if not df.empty else [1.0]


# ==================================================
# IA ENGINE
# ==================================================

detector = PatternDetector(history)

predictor = PredictorEngine(
    type("obj", (), {"df": {"multiplier": history}})
)


# ==================================================
# OCR + ALERTS
# ==================================================

ocr = ScreenOverlayOCR()

telegram = StreamAlertManager(
    token="SEU_TOKEN",
    chat_id="SEU_CHAT_ID"
)


# ==================================================
# CONTROL CENTER
# ==================================================

control = ControlCenter(
    ia_engine=predictor,
    alert_manager=telegram,
    ocr_engine=ocr
)


# ==================================================
# ENGINE MASTER (START / STOP GLOBAL)
# ==================================================

engine_master = EngineMaster(control)


# ==================================================
# STREAM STATE
# ==================================================

if "stream_data" not in st.session_state:
    st.session_state.stream_data = []


# ==================================================
# CALLBACK CENTRAL
# ==================================================

def on_new_value(value):

    result = control.process(value)

    if result:

        st.session_state.stream_data.append(result["value"])

        if len(st.session_state.stream_data) > 300:
            st.session_state.stream_data = st.session_state.stream_data[-300:]


# ==================================================
# MENU LATERAL
# ==================================================

page = st.sidebar.radio(
    "📌 MENU",
    [
        "📊 Dashboard",
        "⚡ Stream URL",
        "🪟 OCR Sensor",
        "🧠 Control Center",
        "⚙️ Engine Master"
    ]
)


# ==================================================
# 📊 DASHBOARD PRINCIPAL
# ==================================================

if page == "📊 Dashboard":

    st.subheader("📊 Visão Geral do Sistema")

    col1, col2, col3 = st.columns(3)

    col1.metric("Último valor", history[-1])
    col2.metric("Volatilidade", detector.volatility())
    col3.metric("Streak", detector.low_streak())

    st.divider()

    fig = px.line(x=list(range(len(history))), y=history)
    st.plotly_chart(fig, use_container_width=True)


# ==================================================
# ⚡ STREAM URL
# ==================================================

elif page == "⚡ Stream URL":

    st.subheader("⚡ Captura em Tempo Real")

    url = st.text_input("URL do sistema")

    col1, col2 = st.columns(2)

    if url:

        scraper = PlaywrightScraper(url)

        if col1.button("▶ START STREAM"):

            stream = StreamEngine(
                scraper=scraper,
                callback=on_new_value,
                interval=2
            )

            threading.Thread(target=stream.start, daemon=True).start()

            st.success("Stream iniciado")

        if col2.button("⛔ STOP STREAM"):

            st.warning("Controle agora via Engine Master")


# ==================================================
# 🪟 OCR SENSOR
# ==================================================

elif page == "🪟 OCR Sensor":

    st.subheader("🪟 Sensor Visual (OCR + Overlay)")

    st.info("Selecione a área da tela para captura")

    if st.button("🪟 Abrir Overlay"):

        region = run_overlay()

        if region:

            ocr.set_region(region)

            st.success("Região configurada com sucesso")

    if st.button("📸 Capturar Agora"):

        value = ocr.get_value()

        if value:
            st.success(f"Vela detectada: {value}x")
            on_new_value(value)
        else:
            st.warning("Nenhum dado detectado")


# ==================================================
# 🧠 CONTROL CENTER
# ==================================================

elif page == "🧠 Control Center":

    st.subheader("🧠 Núcleo de Inteligência")

    st.json(control.status())

    st.divider()

    if st.session_state.stream_data:

        fig = px.line(
            x=list(range(len(st.session_state.stream_data))),
            y=st.session_state.stream_data,
            title="Stream Controlado pela IA"
        )

        st.plotly_chart(fig, use_container_width=True)


# ==================================================
# ⚙️ ENGINE MASTER
# ==================================================

elif page == "⚙️ Engine Master":

    st.subheader("⚙️ Controle Global do Sistema")

    col1, col2 = st.columns(2)

    if col1.button("▶ START GLOBAL"):

        msg = engine_master.start()

        st.success(msg)

    if col2.button("⛔ STOP GLOBAL"):

        msg = engine_master.stop()

        st.warning(msg)

    st.divider()

    st.subheader("📡 Status Geral")

    st.json(engine_master.status())