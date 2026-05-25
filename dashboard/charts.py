# ==========================================================
# GRÁFICOS DO DASHBOARD
# ==========================================================

import plotly.express as px

# ==========================================================
# GRÁFICO DE MULTIPLICADORES
# ==========================================================

def multiplier_chart(df):

    fig = px.line(
        df,
        x="id",
        y="multiplier",
        title="MULTIPLIERS"
    )

    return fig