{% extends "partials/layout.html.tpl" %}
{% block title %}Top Sellers{% endblock %}
{% block name %}Top Sellers{% endblock %}
{% block content %}
    <div class="quote">January 2013</div>
    <div class="separator-horizontal"></div>
    <table class="table-resume three">
        <tbody>
            <tr>
                <td>
                    <span class="label strong">1º</span><br />
                    <a href="#">John Doe</a><br />
                    <span class="label">Dolce Vita Tejo</span><br />
                    <span class="label strong">240.00 €</span>
                </td>
                <td>
                    <span class="label strong">2º</span><br />
                    <a href="#">Sofia Albertina</a><br />
                    <span class="label">Sede</span><br />
                    <span class="label strong">280.00 €</span>
                </td>
                <td>
                    <span class="label strong">3º</span><br />
                    <a href="#">Adalberto Faria</a><br />
                    <span class="label">Dolce Vita Douro</span><br />
                    <span class="label strong">600.00 €</span>
                </td>
            </tr>
        </tbody>
    </table>
    <table class="table-list">
        <thead>
            <tr>
                <th class="left label" width="6%">Rank</th>
                <th class="left label" width="20%">Seller</th>
                <th class="left label" width="34%">Store</th>
                <th class="right label" width="20%">Sales</th>
                <th class="right label" width="20%">Commision</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="left">4º</td>
                <td class="left"><a href="#">Alberto F.</a></td>
                <td class="left">Sede</td>
                <td class="right"><a href="#">120.00 €</a></td>
                <td class="right">12.00 €</td>
            </tr>
            <tr>
                <td class="left">5º</td>
                <td class="left"><a href="#">Maria D.</a></td>
                <td class="left">NorteShopping</td>
                <td class="right"><a href="#">110.20 €</a></td>
                <td class="right">11.02 €</td>
            </tr>
            <tr>
                <td class="left">6º</td>
                <td class="left"><a href="#">Maria D.</a></td>
                <td class="left">NorteShopping</td>
                <td class="right"><a href="#">112.20 €</a></td>
                <td class="right">11.02 €</td>
            </tr>
            <tr>
                <td class="left">7º</td>
                <td class="left"><a href="#">Alberto F.</a></td>
                <td class="left">Sede</td>
                <td class="right"><a href="#">120.00 €</a></td>
                <td class="right">12.00 €</td>
            </tr>
            <tr>
                <td class="left">8º</td>
                <td class="left"><a href="#">Maria D.</a></td>
                <td class="left">NorteShopping</td>
                <td class="right"><a href="#">110.20 €</a></td>
                <td class="right">11.02 €</td>
            </tr>
            <tr>
                <td class="left">9º</td>
                <td class="left"><a href="#">Alberto F.</a></td>
                <td class="left">Sede</td>
                <td class="right"><a href="#">120.00 €</a></td>
                <td class="right">12.00 €</td>
            </tr>
            <tr>
                <td class="left">10º</td>
                <td class="left"><a href="#">Maria D.</a></td>
                <td class="left">NorteShopping</td>
                <td class="right"><a href="#">110.20 €</a></td>
                <td class="right">11.02 €</td>
            </tr>
        </tbody>
    </table>
    <table>
        <tbody>
            <tr>
                <td>
                    <div class="links">
                        <a href="#">previous</a> // <a href="#">next</a>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
{% endblock %}
