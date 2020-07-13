import copy

import posthog
import logging
from django.urls import reverse
from django.utils.translation import gettext as _

from e_metrobus import __version__
from e_metrobus.navigation import constants, stations

from exchangelib import (
    Credentials,
    Account,
    Message,
    Mailbox,
)
from django.conf import settings


FEEDBACK_SUBJECT = "E-MetroBus App Feedback"


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
        request.session.session_key, event, properties=data,
    )


def share_url(request):
    host = f"{request.scheme}://{request.get_host()}"
    return f"{host}{reverse('navigation:welcome')}"


def share_text(request):
    if "non_bus_user" in request.session:
        text = _(
            "Ich bin gerade in einem E-Bus auf der Linie 200 gefahren. Schau mal hier:"
        )
    else:
        current_stations = [
            stations.STATIONS[station] for station in request.session["stations"]
        ]
        route_data = stations.STATIONS.get_route_data(*current_stations)
        co2 = route_data["bus"].co2 - route_data["e-bus"].co2
        text = _(
            "Ich bin gerade in einem E-Bus auf der Linie 200 gefahren und habe der Welt dabei %(co2)s g CO2-Emissionen erspart. Schau mal hier:"
        ) % {"co2": round(co2, 2)}
    return text


def set_separators(value):
    svalue = str(f"{value:,}")
    return svalue.replace(".", "_").replace(",", ".").replace("_", ",")


def send_mail(subject, message, recipients):
    """Send E-mail via MS Exchange Server using credentials from settings"""
    try:
        credentials = Credentials(settings.EXCHANGE_ACCOUNT, settings.EXCHANGE_PW)
        account = Account(
            settings.EXCHANGE_EMAIL, credentials=credentials, autodiscover=True
        )

        m = Message(
            account=account,
            folder=account.sent,
            subject=subject,
            body=message,
            to_recipients=recipients,
        )
        m.send_and_save()
    except Exception as e:
        logging.error(e)


def send_feedback(message):
    recipients = [
        Mailbox(email_address=recipient) for recipient in settings.FEEDBACK_RECIPIENTS
    ]
    send_mail(FEEDBACK_SUBJECT, message, recipients)


def send_bug_report(subject, message):
    recipients = [
        Mailbox(email_address=recipient) for recipient in settings.BUG_RECIPIENTS
    ]
    send_mail(subject, message, recipients)


def get_slogan(percent):
    if percent < 33:
        return constants.FINISHED_SLOGANS[0]
    elif percent < 66:
        return constants.FINISHED_SLOGANS[1]
    else:
        return constants.FINISHED_SLOGANS[2]
