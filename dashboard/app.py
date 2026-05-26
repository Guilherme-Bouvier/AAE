import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

from analysis.pattern_detector import PatternDetector
from analysis.predictor_engine import PredictorEngine

from data_collector.scraper_playwright import PlaywrightScraper
from core_stream.stream_engine import StreamEngine

from alerts.stream_alert_manager import StreamAlertManager
from alerts.contact_manager import ContactManager


# ==================================================
# CONFIG STREAMLIT
# ==================================================

st.set_page_config(
    page_title="AAE - IA Tempo Real",
    layout="wide"
)

st.title("📊 AAE - Inteligência Artificial em Tempo Real")
st.caption("Sistema leve otimizado")


# ==================================================
# ALERT SYSTEM
# ==================================================

BOT_TOKEN = "SEU_TOKEN_AQUI"

alert_manager = StreamAlertManager(
    token=BOT_TOKEN
)

contact_manager = ContactManager(BOT_TOKEN)


# ==================================================
# OCR IMPORT LEVE
# ==================================================

try:
    from vision.screen_overlay import ScreenOverlayOCR
except Exception:
    ScreenOverlayOCR = None

ocr = None


# ==================================================
# BANCO
# ==================================================

engine = create_engine("sqlite:///data/rounds.db")


# ==================================================
# SESSION STATE
# ==================================================

if "stream_data" not in st.session_state:
    st.session_state.stream_data = []

if "stream_running" not in st.session_state:
    st.session_state.stream_running = False

if "contacts" not in st.session_state:
    st.session_state.contacts = []


contact_manager.contacts = st.session_state.contacts


# ==================================================
# CACHE LOAD DATA
# ==================================================

@st.cache_data(ttl=5)
def load_data():

    try:
        df = pd.read_sql(
            "SELECT * FROM rounds ORDER BY id DESC LIMIT 200",
            engine
        )

        return df

    except:
        return pd.DataFrame()


# ==================================================
# CACHE IA
# ==================================================

@st.cache_resource
def get_predictor(history):

    return PredictorEngine(
        type(
            "obj",
            (),
            {
                "df": {
                    "multiplier": history
                }
            }
        )
    )


# ==================================================
# LOAD
# ==================================================

df = load_data()

history = df["multiplier"].tolist() if not df.empty else [1.0]

detector = PatternDetector(history)

predictor = get_predictor(history)


# ==================================================
# CALLBACK STREAM
# ==================================================

def on_new_value(value):

    st.session_state.stream_data.append(value)

    alert_manager.check(
        value=value,
        confidence=0.7
    )

    contact_manager.broadcast(
        f"📊 Nova vela detectada: {value}x"
    )

    if len(st.session_state.stream_data) > 300:
        st.session_state.stream_data = st.session_state.stream_data[-300:]


# ==================================================
# MENU
# ==================================================

st.sidebar.title("📌 MENU")

page = st.sidebar.radio(
    "Navegação",
    [
        "📈 Dashboard",
        "🌐 Captura",
        "⚡ Stream",
        "🔮 Previsão",
        "🪟 OCR",
        "📱 Telegram"
    ]
)


# ==================================================
# DASHBOARD
# ==================================================

if page == "📈 Dashboard":

    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Último", history[-1])
    col2.metric("Volatilidade", detector.volatility())
    col3.metric("Streak", detector.low_streak())

    st.divider()

    fig = px.line(
        x=list(range(len(history))),
        y=history,
        title="Histórico"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ==================================================
# CAPTURA
# ==================================================

elif page == "🌐 Captura":

    st.subheader("🌐 Captura")

    url = st.text_input("URL")

    if url:

        if st.button("Capturar"):

            with st.spinner("Capturando..."):

                scraper = PlaywrightScraper(url)

                value = scraper.get_latest()

                if value:

                    st.success(f"{value}x")

                    alert_manager.check(
                        value=value,
                        confidence=0.6
                    )

                else:
                    st.warning("Nada encontrado")


# ==================================================
# STREAM
# ==================================================

elif page == "⚡ Stream":

    st.subheader("⚡ Stream Tempo Real")

    url = st.text_input("Stream URL")

    if url:

        if st.button("▶️ Iniciar"):

            scraper = PlaywrightScraper(url)

            stream = StreamEngine(
                scraper,
                on_new_value,
                2
            )

            stream.start()

            st.session_state.stream_running = True

            st.success("Stream iniciado")

    if st.session_state.stream_data:

        fig2 = px.line(
            x=list(range(len(st.session_state.stream_data))),
            y=st.session_state.stream_data,
            title="Tempo Real"
        )

        st.plotly_chart(
            fig2,
            width="stretch"
        )

        st.metric(
            "Última",
            st.session_state.stream_data[-1]
        )


# ==================================================
# PREVISÃO
# ==================================================

elif page == "🔮 Previsão":

    st.subheader("🔮 IA")

    future = predictor.predict_next(10)

    fig = px.line(
        x=list(range(10)),
        y=future,
        title="Próximos passos"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ==================================================
# OCR
# ==================================================

elif page == "🪟 OCR":

    st.subheader("🪟 OCR")

    if st.button("Testar OCR"):

        if ScreenOverlayOCR is None:

            st.error("OCR indisponível")

        else:

            try:

                if ocr is None:
                    ocr = ScreenOverlayOCR()

                value = ocr.get_value()

                if value:

                    st.success(f"Detectado: {value}x")

                    alert_manager.check(
                        value=value,
                        confidence=0.8
                    )

                else:
                    st.warning("Nada detectado")

            except Exception as e:

                st.error(f"Erro OCR: {e}")


# ==================================================
# TELEGRAM
# ==================================================

elif page == "📱 Telegram":

    st.subheader("📱 Contatos Telegram")

    new_contact = st.text_input("Chat ID")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("➕ Adicionar"):

            contact_manager.add_contact(new_contact)

            st.session_state.contacts = contact_manager.contacts

            st.success("Contato adicionado")

    with col2:

        if st.button("🗑 Remover"):

            contact_manager.remove_contact(new_contact)

            st.session_state.contacts = contact_manager.contacts

            st.warning("Contato removido")

    st.divider()

    st.write("📋 Lista")

    for c in st.session_state.contacts:
        st.code(c)