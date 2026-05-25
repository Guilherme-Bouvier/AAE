# ==========================================================
# PARSER DE EVENTOS
# ==========================================================

# Futuramente:
#
# converterá:
# - websocket;
# - html;
# - api.
#
# em formato padronizado.

# ==========================================================
# EXEMPLO
# ==========================================================

def parse_websocket_message(message):

    return {
        "multiplier": message.get("multiplier"),
        "players": message.get("players"),
        "bet_volume": message.get("bet_volume")
    }