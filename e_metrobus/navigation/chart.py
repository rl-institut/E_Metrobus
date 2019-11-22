import plotly
import plotly.graph_objects as go


class DjangoFigure:
    def __init__(self, figure, **config):
        plotly_div = plotly.offline.plot(
            figure, include_plotlyjs=False, output_type="div", config=config
        )

        self.script = plotly_div[
            plotly_div.find("<script")
            + len('<script type="text/javascript">') : plotly_div.find("</script>")
        ]

        div_id_start = plotly_div.find('<div id="')
        div_id_end = plotly_div.find('"', div_id_start + 9)
        self.div_id = plotly_div[div_id_start + 9:div_id_end]

        self.div = f'<div id="{self.div_id}" class="plotly-graph-div" style="height:60vh; width:100vw;"></div>'


def get_mobility_figure(values):
    colors = ["Gainsboro"] * 5
    colors[2] = "black"

    # Plotly Figure:
    mobiles = ["Zu Fuß", "Fahrrad", "E-Bus", "Dieselbus", "PKW"]
    fig = go.Figure([go.Bar(x=mobiles, y=values, marker_color=colors)])
    fig.layout.margin.t = 0
    fig.layout.margin.b = 0
    fig.layout.margin.l = 0
    fig.layout.margin.r = 0
    fig.layout.autosize = True
    fig.layout.plot_bgcolor = "#fff"
    fig.layout.yaxis.visible = False
    fig.layout.yaxis.range = [-1, 35]

    fig.add_layout_image(
        go.layout.Image(source="/static/images/icons/i_walk.svg", x=0, y=0.1)
    )
    fig.add_layout_image(
        go.layout.Image(source="/static/images/icons/i_bus.svg", x=1, y=0.1)
    )
    fig.update_layout_images(
        dict(
            xref="x", yref="y", sizex=0.2, sizey=0.2, xanchor="right", yanchor="bottom"
        )
    )
    return DjangoFigure(fig, displayModeBar=False)
