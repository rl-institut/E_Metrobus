import copy

import posthog
from e_metrobus.navigation import constants


def posthog_event(request, event=None):
    data = copy.deepcopy(request.session._session)
    data["session_id"] = request.session.session_key
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
