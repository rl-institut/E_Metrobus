import plotly


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

        self.div = f'<div id="{self.div_id}" class="plotly-graph-div"></div>'
