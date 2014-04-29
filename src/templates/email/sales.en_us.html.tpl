{% extends "email/layout.en_us.html.tpl" %}
{% block title %}Sales Report{% endblock %}
{% block content %}
    <p>
        This email confirms your reservation in {{ link(url_for("provider.show", name = schedule.provider.name), schedule.provider.full_name) }}
        with the reservation number {{ link(url_for("account.schedule_own", id = schedule.id), schedule.uuid_s()) }}. We hope you enjoy
        the service defined in the reservation.
    </p>
    {{ h2("Sales & Returns") }}
    <p>
        <table cellspacing="0" width="100%">
            <tr>
                <td width="100">
                    <strong>Nr.</strong>
                </td>
                <td>{{ schedule.uuid_s() }}</td>
            </tr>
            <tr>
                <td>
                    <strong>Name</strong>
                </td>
                <td>{{ schedule.account.full_name() }} ({{ schedule.account.phone }})</td>
            </tr>
            <tr>
                <td>
                    <strong>Date</strong>
                </td>
                <td>{{ schedule.start_s() }}</td>
            </tr>
            <tr>
                <td>
                    <strong>Address</strong>
                </td>
                <td>{{ schedule.account.street }}</td>
            </tr>
            <tr>
                <td></td>
                <td>{{ schedule.account.zip_code }} {{ schedule.account.province }}</td>
            </tr>
            <tr>
                <td></td>
                <td>{{ schedule.account.country }}</td>
            </tr>
        </table>
    </p>
    {{ h2("We've Got You Covered") }}
    <p>
        Have any problems? Our support team is available at the drop of a hat.
        Send us an email, day or night, on {{ link("mailto:help@lugardajoia.com", "help@lugardajoia.com", False) }}.
    </p>
{% endblock %}
