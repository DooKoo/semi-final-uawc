from app import app
import urllib.request
from urllib.parse import quote
import xml.etree.ElementTree as ET
from flask import request, render_template

#PAGES


@app.route('/rates/privat/')
def rates_roure():
    return '<p> <a href="/">Main page</a </p>'\
           '<p> If you want to see <b><a href="/rates/privat/cash">Cash</a> course</b></p>' \
           '<p> If you want to see <b><a href="/rates/privat/card">Cashless</a> course</b>(conversion by the card)</p>'


@app.route('/rates/privat/<type>')
def rates_privat(type):
    if type == 'cash':
        url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'
    elif type == 'card':
        url = 'https://api.privatbank.ua/p24api/pubinfo?cardExchange'
    else:
        return 'Incorrect type :('

    try:
        answer = str(urllib.request.urlopen(url).read())
        xml_doc = ET.fromstring(answer[2:-1])

        result = '<p> <a href="/">Main page</a </p>'
        for item in xml_doc:
            doc_dict = item[0].attrib
            result += str("<p>" + doc_dict['ccy'] + ": buy: " + doc_dict['buy'] + "; sale:" + doc_dict['sale'] + "; </p>")

        return result
    except Exception:
        return "Some error. Try again"


@app.route('/rates/nbu')
def rates_nbu():
    try:
        answer = str(urllib.request.urlopen('https://privat24.privatbank.ua/p24/accountorder?'
                                            'oper=prp&PUREXML&apicour&country=ua').read())

        xml_doc = ET.fromstring(answer[2:-1])
        result = '<p> <a href="/">Main page</a </p>'
        for item in xml_doc:
            doc_dict = item.attrib
            result += str("<p>" + doc_dict['ccy'] + ": Course: " + doc_dict['buy'] + "/" + doc_dict['unit'] + "; </p>")

    except Exception:
        return "Some error. Try again :("
    return result


@app.route('/')
def test():
    return render_template('form.html')


#API


@app.route('/query', methods=['POST'])
def query():
    try:
        if request.method == 'POST':
            query_type = request.form['type']
            city = request.form['city']
            street = request.form['street']

        if query_type == '1':
            url = 'https://privat24.privatbank.ua/p24/accountorder?' \
                  'oper=prp&PUREXML&pboffice&city='+quote(city)+'&address=' + quote(street)
        elif query_type == '2':
            url = 'https://privat24.privatbank.ua/p24/accountorder?oper=prp&bonus&PUREXML=' \
                  '&city='+quote(city)+'&address=' + quote(street)
        else:
            return 'Incorrect type :('

        answer = str(urllib.request.urlopen(url).read(), encoding='utf8')

        xml_doc = ET.fromstring(answer)
        if query_type == '1':
            result = '<table border="0"> \
                      <caption>Offices</caption>\
                      <tr>\
                        <th>Name</th>\
                        <th>Address</th>\
                        <th>Phone</th>\
                        <th>Email</th>\
                      </tr>'

            for i in xml_doc[5]:
                item = i.attrib

                result += str("<tr> <th>" + item['name'] + '</th><th>' + item['address']
                              + '</th><th>' + item['phone'] + '</th><th>' + item['email'] + '<th></tr>')
        else:
            result = '<table border="0"> \
                      <caption>Partners</caption>\
                      <tr>\
                        <th>Name</th>\
                        <th>Address</th>\
                        <th>Bonus</th>\
                        <th>Type</th>\
                      </tr>'
            for i in xml_doc[5]:
                item = i.attrib
                result += str("<tr><th>" + item['name'] + '</th><th>' + item['address']
                              + '</th><th>' + item['bonus_plus'] + '</th><th>' + item['type'] + '</th></tr>')
        if not result:
            result = 'Nothing :( Try other options!'

        return result
    except Exception:
        return 'Some error. Try again :('