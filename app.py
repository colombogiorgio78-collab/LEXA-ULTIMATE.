import streamlit as st
import fitz
import google.generativeai as genai
import streamlit.components.v1 as components

# 1. SETTINGS ESTETICI
st.set_page_config(page_title="LEXA EUROPE - AI Legal", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1E3A8A; color: white; font-weight: bold; }
    .report-card { padding: 20px; border-radius: 12px; background-color: white; border: 1px solid #e0e0e0; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR
with st.sidebar:
    st.title("⚖️ LEXA PANEL")
    api_key = st.text_input("Inserisci Gemini API Key", type="password")
    jurisdiction = st.selectbox("Seleziona Giurisdizione", 
        ["Italia", "Unione Europea", "Francia", "Spagna", "International"])
    st.info("LEXA analizzerà il contratto secondo le leggi della nazione scelta.")

# 3. INTERFACCIA PRINCIPALE
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

# 4. MOTORE AI CON FALLBACK (PER EVITARE ERRORI 404)
with col_out:
    st.subheader("📊 Report LEXA")
    if st.button("🚀 AVVIA ANALISI PROFESSIONALE"):
        if not api_key or not testo_da_analizzare:
            st.error("Inserisci la chiave API e il testo!")
        else:
            try:
                genai.configure(api_key=api_key)
                # Prova diversi nomi di modello per sicurezza
                model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
                response_text = ""
                for m_name in model_names:
                    try:
                        model = genai.GenerativeModel(m_name)
                        prompt = f"Sei un avvocato esperto in {jurisdiction}. Analizza questo contratto per rischi IP, recesso e penali. Sii schematico: \n\n {testo_da_analizzare[:20000]}"
                        response = model.generate_content(prompt)
                        response_text = response.text
                        break
                    except: continue
                
                if response_text:
                    st.markdown(f"<div class='report-card'>{response_text}</div>", unsafe_allow_html=True)
                    
                    # --- TASTO PER ASCOLTARE LA RISPOSTA ---
                    clean_text = response_text.replace("`", "").replace("'", " ").replace("\n", " ")
                    tts_script = f"""
                    <script>
                    function speak() {{
                        var msg = new SpeechSynthesisUtterance();
                        msg.text = '{clean_text}';
                        msg.lang = 'it-IT';
                        window.speechSynthesis.speak(msg);
                    }}
                    </script>
                    <button onclick="speak()" style="width:100%; height:50px; background-color:#FFD700; border-radius:10px; font-weight:bold; cursor:pointer; border:none;">
                        🔊 ASCOLTA L'ANALISI (VOCE AI)
                    </button>
                    """
                    components.html(tts_script, height=70)
                else:
                    st.error("Errore di connessione AI. Riprova.")
            except Exception as e:
                st.error(f"Errore: {e}")
