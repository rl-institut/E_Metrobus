
from collections import namedtuple

import plotly
import plotly.graph_objects as go
from django.utils.translation import gettext as _

from e_metrobus.navigation.utils import set_separators

# at max_value = 50
MARGIN = 10
OFFSET = 1
SIZE = MARGIN - 2 * OFFSET
TEXTSIZE = 5
TROPHY_OFFSET = 2
ICON_SIZE = 40

DEFAULT_COLOR = "Gainsboro"
FONT_COLOR = "#B0B0B0"
E_BUS_COLOR = "#F0D722"

Sizes = namedtuple("Sizes", ["margin", "offset", "size", "textsize"])


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
        self.div_id = plotly_div[div_id_start + 9 : div_id_end]

        self.div = f'<div id="{self.div_id}" class="plotly-graph-div"></div>'


def get_sizes(max_value):
    return Sizes(*map(lambda x: x / 50 * max_value, [MARGIN, OFFSET, SIZE, TEXTSIZE]))


def get_mobility_figure(values, title):
    rounding = get_rounding(max(values))
    if rounding == 0:
        rounded_values = [int(v) for v in values]
    else:
        rounded_values = [round(v, rounding) for v in values]
    colors = [DEFAULT_COLOR] * 5
    colors[1] = E_BUS_COLOR
    mobiles = [
        _("Zu Fuß/<br>Fahrrad"),
        _("E-Bus"),
        _("E-Pkw"),
        _("Dieselbus"),
        _("Pkw (Diesel)"),
    ]
    scaled_values = [
        (v + min(rounded_values)) / max(rounded_values) * 100 for v in rounded_values
    ]
    max_value = max(scaled_values)
    sizes = get_sizes(max_value)

    bar = go.Bar(
        x=mobiles,
        y=scaled_values,
        marker_color=colors,
        text=[set_separators(v) for v in rounded_values],
        textposition="outside",
        width=0.6,
    )
    bar.textfont.size = 15
    bar.textfont.color = FONT_COLOR
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
    fig.layout.font.color = FONT_COLOR
    fig.layout.yaxis.visible = False
    fig.layout.yaxis.range = [-sizes.margin, max_value + sizes.margin]
    fig.add_annotation(
        x=1.2,
        y=max_value,
        text=title,
        font={"size": 15, "color": FONT_COLOR},
        align="left",
        showarrow=False,
    )

    # Mobility icons:
    for i, icon in enumerate(["pedestrian_bike", "ebus", "e_car", "bus", "car"]):
        color = "small"
        if icon == "ebus":
            color = "yellow_circle"
        fig.add_layout_image(
            go.layout.Image(
                source=f"/static/images/icons/i_{icon}_{color}.svg",
                x=i,
                y=-sizes.offset,
                sizex=sizes.size,
                sizey=sizes.size,
            )
        )
    # Trophy Icons:
    trophy_number = 1
    for i in range(3):
        if i > 0 and scaled_values[i] > scaled_values[i - 1]:
            trophy_number += 1
        fig.add_layout_image(
            go.layout.Image(
                source=f"/static/images/icons/i_trophy_{trophy_number}_{'black' if i == 1 else 'gray'}.svg",
                x=i,
                y=scaled_values[i]
                + sizes.textsize
                + sizes.size
                + sizes.offset
                + TROPHY_OFFSET,
                sizex=sizes.size,
                sizey=sizes.size,
            )
        )
    fig.update_layout_images(
        {"xref": "x", "yref": "y", "xanchor": "center", "yanchor": "top"}
    )
    return DjangoFigure(fig, displayModeBar=False, staticPlot=True)


def get_co2_figure(values):
    title = _("CO<sub>2</sub> Emissionen [in g]<br>nach Verkehrsmittel")
    return get_mobility_figure(values, title)


def get_nitrogen_figure(values):
    title = _("Stickoxid Emissionen [in g]<br>nach Verkehrsmittel")
    return get_mobility_figure(values, title)


def get_fine_dust_figure(values):
    title = _("Feinstaub Emissionen [in g]<br>nach Verkehrsmittel")
    return get_mobility_figure(values, title)


def get_rounding(max_value):
    if max_value >= 10:
        return 0
    str_value = str(max_value).split(".")
    if len(str_value) == 1:
        return 0
    dec = str_value[1]
    i = 0
    while len(dec) > i and dec[i] == "0":
        i += 1
    if len(dec) == i + 1:
        return i + 1
    return i + 2
