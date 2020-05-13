from collections import namedtuple

import plotly
import plotly.graph_objects as go

from django.utils.translation import gettext as _

# at max_value = 50
MARGIN = 10
OFFSET = 1
SIZE = MARGIN - 2 * OFFSET
TEXTSIZE = 5
TROPHY_OFFSET = 20

DEFAULT_COLOR = "Gainsboro"
E_BUS_COLOR = "black"

Sizes = namedtuple("Sizes", ["margin", "offset", "size", "textsize"])


class DjangoFigure:
    def __init__(self, figure, **config):
        plotly_div = plotly.offline.plot(
            figure,
            include_plotlyjs=False,
            output_type="div",
            config=config
        )

        self.script = plotly_div[
            plotly_div.find("<script")
            + len('<script type="text/javascript">') : plotly_div.find("</script>")
        ]

        div_id_start = plotly_div.find('<div id="')
        div_id_end = plotly_div.find('"', div_id_start + 9)
        self.div_id = plotly_div[div_id_start + 9 : div_id_end]

        self.div = f'<div id="{self.div_id}" class="plotly-graph-div" style="height:60vh; width:100vw;"></div>'


def get_sizes(max_value):
    return Sizes(*map(lambda x: x / 50 * max_value, [MARGIN, OFFSET, SIZE, TEXTSIZE]))


def get_mobility_figure(values):
    colors = [DEFAULT_COLOR] * 5
    colors[2] = E_BUS_COLOR
    mobiles = [_("Zu Fuß"), _("Fahrrad"), _("E-Bus"), _("Dieselbus"), _("PKW")]

    max_value = max(values)
    sizes = get_sizes(max_value)

    bar = go.Bar(
        x=mobiles,
        y=values,
        marker_color=colors,
        text=values,
        textposition="outside",
        width=0.6,
    )
    bar.textfont.size = 15
    bar.textfont.color = E_BUS_COLOR
    fig = go.Figure([bar])
    fig.layout.margin.t = 0
    fig.layout.margin.b = 0
    fig.layout.margin.l = 10
    fig.layout.margin.r = 10
    fig.layout.autosize = True
    fig.layout.plot_bgcolor = "#fff"
    fig.layout.xaxis.tickangle = -45
    fig.layout.xaxis.tickfont.size = 15
    fig.layout.font.family = "Roboto"
    fig.layout.font.color = E_BUS_COLOR
    fig.layout.yaxis.visible = False
    fig.layout.yaxis.range = [-sizes.margin, max_value + sizes.margin]
    fig.add_annotation(
        x=0.5,
        y=max_value,
        text=_("CO2 Emissionen [in g]<br>nach Verkehrsmittel"),
        font={"size": 15, "color": E_BUS_COLOR},
        align="left",
        showarrow=False,
    )

    # Mobility icons:
    for i, icon in enumerate(["pedestrian", "bike", "ebus", "bus", "car"]):
        color = "gray"
        if icon == "ebus":
            color = "black_fill"
        fig.add_layout_image(
            go.layout.Image(
                source=f"/static/images/icons/i_{icon}_{color}.svg",
                x=i,
                y=-sizes.offset,
            )
        )
    # Trophy Icons:
    for i in range(3):
        fig.add_layout_image(
            go.layout.Image(
                source=f"/static/images/icons/i_trophy_{i+1}_{'black' if i == 2 else 'gray'}.svg",
                x=i,
                y=values[i]
                + sizes.textsize
                + sizes.size
                + sizes.offset
                + TROPHY_OFFSET,
            )
        )
    fig.update_layout_images(
        {
            "xref": "x",
            "yref": "y",
            "sizex": sizes.size,
            "sizey": sizes.size,
            "xanchor": "center",
            "yanchor": "top",
        }
    )
    return DjangoFigure(fig, displayModeBar=False, staticPlot=True)
