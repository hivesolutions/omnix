{% extends "email/layout.pt_pt.html.tpl" %}
{% block title %}Relatório de Vendas{% endblock %}
{% block content %}
    <p>
        Este email contêm informação sobre as suas ultimas operações feitas
        no sistema omni.
    </p>
    {{ h2("Vendas & Devoluções") }}
    <p>
        <table cellspacing="0" width="100%">
            {% for operation in operations %}
                <tr>
                    <td>{{ operation.date_f }}</td>
                    {% if operation._class == 'SaleTransaction' %}
                        <td >
                            <a href="{{ omnix_base_url }}sam/sales/{{ operation.object_id }}">{{ operation.identifier }}</a>
                        </td>
                    {% else %}
                        <td class="left">
                            <a href="{{ omnix_base_url }}sam/returns/{{ operation.object_id }}">{{ operation.identifier }}</a>
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
    {{ h2("Estamos Sempre Consigo") }}
    <p>
        Algum problema? A nossa equipa de apoio está disponível para o ajudar.
        Envie-nos um email para {{ link("mailto:ajuda@omnix.com", "ajuda@omnix.com", False) }}.
    </p>
{% endblock %}
