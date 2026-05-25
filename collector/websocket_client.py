# ==========================================================
# CLIENTE WEBSOCKET
# ==========================================================

# FUTURAMENTE:
#
# este módulo fará conexão real.

import websocket

# ==========================================================
# MENSAGEM RECEBIDA
# ==========================================================

def on_message(ws, message):

    print(message)

# ==========================================================
# CONEXÃO
# ==========================================================

def start_websocket(url):

    ws = websocket.WebSocketApp(
        url,
        on_message=on_message
    )

    ws.run_forever()