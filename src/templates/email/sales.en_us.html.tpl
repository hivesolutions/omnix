{% extends "email/layout.en_us.html.tpl" %}
{% block title %}Sales Report{% endblock %}
{% block content %}
    <p>
        This email contaiins information about the latest operations made on the omni
        system on your behalf.
    </p>
    {{ h2("Sales & Returns") }}
    <p>
        <table cellspacing="0" width="100%">
            {% for operation in operations %}
                <tr>
                    <td>{{ operation.date_f }}</td>
                    {% if operation._class == 'SaleTransaction' %}
                        <td >
                            <a href="#">{{ operation.identifier }}</a>
                        </td>
                    {% else %}
                        <td class="left">
                            <a href="#">{{ operation.identifier }}</a>
                        </td>
                    {% endif %}
                    {% if operation._class == 'SaleTransaction' %}
                        <td>{{ "%.2f" % (operation.price.value * commission_rate) }} €</td>
                        <td>{{ "%.2f" % operation.price.value }} / {{ "%.2f" % operation.price_vat }} €</td>
                    {% else %}
                        <td>{{ "%.2f" % (operation.price.value * commission_rate * -1) }} €</td>
                        <td>{{ "%.2f" % (operation.price.value * -1) }} / {{ "%.2f" % (operation.price_vat * -1) }} €</td>
                    {% endif %}
                </tr>
            {% endfor %}
        </table>
    </p>
    {{ h2("We've Got You Covered") }}
    <p>
        Have any problems? Our support team is available at the drop of a hat.
        Send us an email, day or night, on {{ link("mailto:help@lugardajoia.com", "help@lugardajoia.com", False) }}.
    </p>
{% endblock %}
