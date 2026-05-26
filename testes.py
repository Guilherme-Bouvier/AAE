# streamlit run dashboard/app.py

 # ✔ inicia o sistema como aplicação
 # ✔ abre o Streamlit automaticamente (via launcher)

 # streamlit run dashboard/app.py

#======================================================

# 2. Rodar direto o dashboard (modo debug)

 # ✔ útil para testar só a interface
 # ✔ ignora o launcher e o controle global

 #streamlit run dashboard/app.py

#====================================================|

# 3. Testar módulos individuais (IA / lógica)

 # Se quiser testar só o backend:

 # python -m analysis.predictor_engine
 # ou
 # python -m core.control_center

#====================================================

# 4. Se der erro de dependência
  # pip install -r requirements.txt
 
  # pip install streamlit pandas plotly sqlalchemy playwright
  #playwright install 

#====================================================

# 5. Teste rápido de funcionamento geral

  # python launcher.py && echo "Sistema iniciado com sucesso"

#====================================================

             #🚀 RECOMENDAÇÃO FINAL

      # ✔ Para uso normal → python launcher.py
      # ✔ Para debug → streamlit run dashboard/app.py