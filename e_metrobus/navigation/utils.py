import copy

import posthog
from django.urls import reverse
from django.utils.translation import gettext as _

from e_metrobus import __version__
from e_metrobus.navigation import constants, stations


def posthog_event(request, event=None):
    data = copy.deepcopy(request.session._session)
    data["session_id"] = request.session.session_key
    data["version"] = __version__
    if event is None:
        event = request.path
    else:
        if event not in constants.POSTHOG_EVENTS:
            raise ValueError("Not a valid posthog event!")
    posthog.capture(
        request.session.session_key,
        event,
        properties=data,
    )


def share_url(request):
    host = f"{request.scheme}://{request.get_host()}"
    return f"{host}{reverse('navigation:welcome')}"


def share_text(request):
    if "non_bus_user" in request.session:
        text = _("Ich bin gerade in einem E-Bus auf der Linie 200 gefahren. Schau mal hier:")
    else:
        current_stations = [
            stations.STATIONS[station] for station in request.session["stations"]
        ]
        route_data = stations.STATIONS.get_route_data(*current_stations)
        co2 = route_data["bus"].co2 - route_data["e-bus"].co2
        text = _("Ich bin gerade in einem E-Bus auf der Linie 200 gefahren und habe der Welt dabei %(co2)s g CO2-Emissionen erspart. Schau mal hier:") % {"co2": round(co2, 2)}
    return text
