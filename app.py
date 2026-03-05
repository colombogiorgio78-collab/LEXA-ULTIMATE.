import streamlit as st
import fitz
import google.generativeai as genai
import streamlit.components.v1 as components

st.set_page_config(page_title="LEXA EUROPE", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1E3A8A; color: white; font-weight: bold; }
    .report-card { padding: 20px; border-radius: 12px; background-color: white; border: 1px solid #e0e0e0; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("⚖️ LEXA PANEL")
    api_key = st.text_input("Inserisci Gemini API Key", type="password")
    jurisdiction = st.selectbox("Seleziona Giurisdizione", ["Italia", "Unione Europea", "International"])

st.title("⚖️ LEXA EUROPE: Intelligenza Legale")
col_in, col_out = st.columns([1, 1], gap="large")

testo_da_analizzare = ""

with col_in:
    st.subheader("📂 Carica o Incolla")
    tab1, tab2 = st.tabs(["📄 PDF", "✍️ Testo"])
    with tab1:
        file = st.file_uploader("Upload Contratto", type="pdf")
        if file:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            testo_da_analizzare = "".join([p.get_text() for p in doc])
    with tab2:
        testo_manuale = st.text_area("Incolla clausole qui...", height=300)
        if testo_manuale:
            testo_da_analizzare = testo_manuale

with col_out:
    st.subheader("📊 Report LEXA")
    if st.button("🚀 AVVIA ANALISI PROFESSIONALE"):
        if not api_key or not testo_da_analizzare:
            st.error("Inserisci la chiave API e il testo!")
        else:
            try:
                genai.configure(api_key=api_key)
                # Proviamo il modello più stabile
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                with st.spinner("Analisi in corso..."):
                    prompt = f"Sei un avvocato esperto in {jurisdiction}. Analizza questo contratto per rischi IP e clausole critiche: \n\n {testo_da_analizzare[:20000]}"
                    response = model.generate_content(prompt)
                    
                    if response:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                        # Tasto audio
                        clean_text = response.text.replace("'", " ").replace("\n", " ")
                        tts = f"""<script>function speak() {{ var m = new SpeechSynthesisUtterance(); m.text='{clean_text}'; m.lang='it-IT'; window.speechSynthesis.speak(m); }}</script>
                        <button onclick="speak()" style="width:100%;height:50px;background:#FFD700;border-radius:10px;font-weight:bold;cursor:pointer;border:none;">🔊 ASCOLTA ANALISI</button>"""
                        components.html(tts, height=70)
            except Exception as e:
                # QUESTA RIGA CI DIRÀ LA VERITÀ SULL'ERRORE
                st.error(f"ERRORE TECNICO: {str(e)}")

st.caption("LEXA EUROPE v2.1")
