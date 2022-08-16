import requests
from bs4 import BeautifulSoup


from flask import Flask, render_template, request

app = Flask(__name__)


def get_link(name):
    base_link = "https://communities.americanbar.org/people?who="
    name_list = name.split(" ")
    first = True
    for name in name_list:
        if first:
            base_link = f"{base_link}{name}"
            base_link += name
            first = False
        else:
            base_link = f"{base_link}+{name}"

    return base_link


def get_lawyers_super_lawyers(search_url):
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find_all(name="div", class_="floating_lawyers")

    lawyers = []
    for lawyer in results:
        lawyer_image = lawyer.find(name="a").attrs["href"]
        lawyer_name = lawyer.find(name="p", class_="full_name").text or ""
        lawyer_firm = lawyer.find(name="p", class_="firm_name").text or ""
        link = get_link(lawyer_name)

        lawyer_dict = {"image": lawyer_image, "name": lawyer_name, "firm": lawyer_firm, "link": link}
        lawyers.append(lawyer_dict)

    return lawyers


def get_lawyers_lsba(search_url):
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find_all(name="div", class_="col-sm-8")

    lawyers = []
    for lawyer in results:
        lawyer_image = lawyer.find(name="a").attrs["href"] or ""
        if "Mr." or "Ms." or "Mrs." in lawyer:
            lawyer_name = lawyer.text or ""
        lawyer_firm = lawyer.find(name="p", class_="firm_name").text or ""
        link = get_link(lawyer_name)

        lawyer_dict = {"image": lawyer_image, "name": lawyer_name, "firm": lawyer_firm, "link": link}
        lawyers.append(lawyer_dict)

    return lawyers


def get_lawyers_shreveportbar(search_url):
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find_all(name="div", class_="member")

    lawyers = []
    for lawyer in results:
        lawyer_image = lawyer.find(name="img").attrs["href"]
        lawyer_name = lawyer.find(name="div", class_="name").text or ""
        lawyer_firm = lawyer.find(name="div", class_="firm").text or ""
        link = get_link(lawyer_name)

        lawyer_dict = {"image": lawyer_image, "name": lawyer_name, "firm": lawyer_firm, "link": link}
        lawyers.append(lawyer_dict)

    return lawyers


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/lawyer_list", methods=['POST'])
def lawyer_list():
    url = request.form['url']
    lawyers = None
    if "superlawyers" in url:
        lawyers = get_lawyers_super_lawyers(url)

    if "lsba" in url:
        lawyers = get_lawyers_lsba(url)

    if "shreveportbar" in url:
        lawyers = get_lawyers_shreveportbar(url)

    if lawyers:
        return render_template('lawyer-list.html', lawyers=lawyers)
