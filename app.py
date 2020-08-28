import csv
import locale
import json
import matplotlib
import pandas as pd
import numpy as np
import requests
import folium
import re
from flask import Flask, render_template, request
from pandas.core.strings import str_replace
from wtforms import Form, TextAreaField, validators, FloatField, IntegerField, RadioField
import pickle
import sqlite3
import os
from yandex_geocoder import Client
from decimal import Decimal

import matplotlib.pyplot as plt

headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0'}
matplotlib.use('TkAgg')
locale.setlocale(locale.LC_ALL)


app = Flask(__name__)

pred = pickle.load(open(os.path.join('PREDICT_SALE', 'predict_BASE_Sale2.pkl'), 'rb'))
sale_moscow = pickle.load(open(os.path.join('PREDICT_SALE', 'predict_BASE_Sale-moscow.pkl'), 'rb'))
rent = pickle.load(open(os.path.join('PREDICT_RENT', 'predict_Base_Rent2.pkl'), 'rb'))
rent_moscow = pickle.load(open(os.path.join('PREDICT_RENT', 'predict_rent_moscow.pkl'), 'rb'))
predict_class = pickle.load(open(os.path.join('PREDICT_CLASS', 'Cat_rent_light.pkl'), 'rb'))


def predict_sale(document):
    X = np.array([[document]]).reshape(1, -1)
    y = pred(X)[0]
    d = int(y)
    return format(d, ',d')

def predict_sale_Moscow(document):
    X = np.array([[document]]).reshape(1, -1)
    y = sale_moscow(X)[0]
    d = int(y)
    return format(d, ',d')


def predict_rent(document):
    X = np.array([[document]]).reshape(1, -1)
    g = rent(X)[0]
    s = int(g)
    return format(s, ',d')

def predict_rent_Moscow(document):
    X = np.array([[document]]).reshape(1, -1)
    g = rent_moscow(X)[0]
    s = int(g)
    return format(s, ',d')

def predict_class1(cls_):
    X = np.array([[cls_]]).reshape(1, -1)
    y = pred(X)
    cl = int(y)
    return format(cl, ',d')

def Geokoder(document):
    client = Client("9577d1e2-cf09-4dea-94cc-5c80d4de81e6")

    coordinates = client.coordinates("Москва Льва Толстого 16")
    assert coordinates == (Decimal("37.587093"), Decimal("55.733969"))

    address = client.address(Decimal("37.587093"), Decimal("55.733969"))
    assert address == "Россия, Москва, улица Льва Толстого, 16"
    d = client.coordinates(document)
    return d


class HelloForm(Form):
    Metr = FloatField('')
    Flor = RadioField('')
    Metro = RadioField('')
    Metro_metr = RadioField('')
    Vitrin = RadioField('')
    Enter = RadioField('')
    Remont = RadioField('')
    Arendator = RadioField('')
    GK = RadioField('')


@app.route('/', methods=['POST', 'GET'])
def index():
    form = HelloForm(request.form)
    return render_template('first_app.html', form=form)


@app.route('/hello', methods=['POST', 'GET'])
def hello():
    form = HelloForm(request.form)
    if request.method == 'GET':
        Adress = request.args.get('Adress')
        City = request.args.get('City')
        Metr = request.args.get('Metr')
        Flor = request.args.get('Flor')
        Metro = request.args.get('Metro')
        Metro_metr = request.args.get('Metro_metr')
        Vitrin = request.args.get('Vitrin')
        Enter = request.args.get('Enter')
        Remont = request.args.get('Remont')
        Arendator = request.args.get('Arendator')
        GK = request.args.get('GK')

        Adress = [Adress]
        #Geo = Geokoder(Adress)
        City_1 = [[City]]
        # расчет стоимости с поправками
        d = [[Metr, Flor, Metro, Metro_metr, Vitrin, Enter, Remont, Arendator, GK]]
        if int(Flor) == -1 and int(City) == 1 and int(Arendator) == 3:
            p1 = predict_sale(d)
            p2 = int(p1.replace(',', ''))
            p3 = p2-(p2*0.1)
            p4 = int(p3)
            y = p4
        elif int(Enter) == 2:
            p01 = predict_sale(d)
            p02 = int(p01.replace(',', ''))
            p03 = p02-(p02*0.025)
            p04 = int(p03)
            y = p04
        elif int(Enter) == 1:
            p05 = predict_sale(d)
            p06 = int(p05.replace(',', ''))
            p07 = p06-(p06*0.33)
            p08 = int(p07)
            y = p08
        elif int(Flor) == -1 and int(City) == 1 and int(Arendator) == 1:
            p5 = predict_sale(d)
            p6 = int(p5.replace(',', ''))
            p7 = p6 - (p6 * 0.15)
            p8 = int(p7)
            y = p8
        elif int(Flor) == -2 and int(City) == 1 and int(Arendator) == 3:
            p9 = predict_sale(d)
            p10 = int(p9.replace(',', ''))
            p11 = p10 - (p10 * 0.2)
            p12 = int(p11)
            y = p12
        elif int(Flor) == -2 and int(City) == 1 and int(Arendator) == 1:
            p13 = predict_sale(d)
            p14 = int(p13.replace(',', ''))
            p15 = p14 - (p14 * 0.3)
            p16 = int(p15)
            y = p16
        elif int(Flor) == -1 and int(City) == 2 and int(Arendator) == 1:
            p19 = predict_sale_Moscow(d)
            p20 = int(p19.replace(',', ''))
            p21 = p20 - (p20 * 0.1)
            p22 = int(p21)
            y = p22
        elif int(Flor) == -1 and int(City) == 2 and int(Arendator) == 3:
            p23 = predict_sale_Moscow(d)
            p24 = int(p23.replace(',', ''))
            p25 = p24 - (p24 * 0.07)
            p26 = int(p25)
            y = p26
        elif int(Flor) == -2 and int(City) == 2 and int(Arendator) == 1:
            p27 = predict_sale_Moscow(d)
            p28 = int(p27.replace(',', ''))
            p29 = p28 - (p28 * 0.2)
            p30 = int(p29)
            y = p30
        elif int(Flor) == -2 and int(City) == 2 and int(Arendator) == 3:
            p31 = predict_sale_Moscow(d)
            p32 = int(p31.replace(',', ''))
            p33 = p32 - (p32 * 0.15)
            p34 = int(p33)
            y = p34
        elif int(City) == 2:
            p17 = predict_sale_Moscow(d)
            p18 = int(p17.replace(',', ''))
            y = p18
        else:
            ss = predict_sale(d)
            y = int(ss.replace(',', ''))
        k_1 = format(y, ',d').replace(",", " ")
        q = float(Metr.replace(',', ''))
        m_2 = y / q
        m_2 = int(m_2)
        m_kv = format(m_2, ',d'). replace(",", " ")

        # расчет арендной ставки с поправками
        e = [[Metr, Flor, Metro, Metro_metr, Vitrin, Enter, Remont, GK]]
        if int(City) == 1:
            rr = predict_rent(e)
            g = int(rr.replace(',', ''))
        elif int(Enter) == 2:
            r01 = predict_rent(e)
            r02 = int(r01.replace(',', ''))
            r03 = r02-(r02*0.08)
            r04 = int(r03)
            g = r04
        elif int(Enter) == 1:
            r05 = predict_rent(e)
            r06 = int(r05.replace(',', ''))
            r07 = r06-(r06*0.33)
            r08 = int(r07)
            g = r08
        elif int(Flor) == -1 and int(City) == 1 and int(Metro) == 5:
            r1 = predict_rent(e)
            r2 = int(r1.replace(',', ''))
            r3 = r2-(r2*0.25)
            r4 = int(r3)
            g = r4
        elif int(Flor) == -1 and int(City) == 1:
            r5 = predict_rent(e)
            r6 = int(r5.replace(',', ''))
            r7 = r6-(r6*0.2)
            r8 = int(r7)
            g = r8
        elif int(Flor) == -2 and int(City) == 1:
            r9 = predict_rent(e)
            r10 = int(r9.replace(',', ''))
            r11 = r10 - (r10 * 0.3)
            r12 = int(r11)
            g = r12
        elif int(Flor) == -1 and int(City) == 2:
            r17 = rent_moscow(e)
            r19 = r17-(r17*0.15)
            r20 = int(r19)
            g = r20
        elif int(Flor) == -2 and int(City) == 2:
            r21 = rent_moscow(e)
            r22 = int(r21.replace(',', ''))
            r23 = r22-(r22*0.25)
            r24 = int(r23)
            g = r24
        elif int(Flor) == -1 and int(City) == 2 and int(Metro) == 5:
            r13 = rent_moscow(e)
            r15 = r13-(r13*0.15)
            r16 = int(r15)
            g = r16
        elif int(City) == 2:
            r25 = rent_moscow(e)
            r26 = int(r25)
            g = r26
        else:
            rr = predict_rent(e)
            g = int(rr.replace(',', ''))

        k_2 = format(g, ',d'). replace(",", " ")
        # расчет окупаемости
        d = g*110
        z = format(d, ',d'). replace(",", " ")
        # расчет стоимости квадратного метра
        m_3 = d / q
        m_3 = int(m_3)
        m_kv_1 = format(m_3, ',d'). replace(",", " ")
        # расчет стоимости квадратного метра аренды
        m_6 = g / q
        m_6 = int(m_6)
        m_kv_r = format(m_6, ',d'). replace(",", " ")
        v = y/(g*12)
        v_1 = format("%.1f" % v)
        # расчет средневзвешанной стоимости объекта
        m = (d * 0.46)+(y * 0.54)
        p = int(m)
        balans = format(p, ',d'). replace(",", " ")
        # расчет квадратного метра средневзвешанной стоимости объекта
        m_4 = p / q
        m_4 = int(m_4)
        m_kv_2 = format(m_4, ',d'). replace(",", " ")
        # расчет ликвидационной стоимости
        l1 = p-(p*0.2)
        l = int(l1)
        diskont = format(l, ',d'). replace(",", " ")
        # расчет квадратного метра ликвидационной стоимости
        m_5 = l / q
        m_5 = int(m_5)
        m_kv_3 = format(m_5, ',d'). replace(",", " ")

        # классификатор доустимых категорий арендаторов
        cls1 = [[Metr]]
        class_2 = predict_class(cls1)
        class_1 = str(class_2)[1:-1]



        return render_template('hello.html',
                               #Adress=Adress,
                               City=City,
                               class_1=class_1,
                               Metr=Metr,
                               Flor=Flor,
                               Metro=Metro,
                               Metro_metr=Metro_metr,
                               Vitrin=Vitrin,
                               Enter=Enter,
                               Remont=Remont,
                               Arendator=Arendator,
                               GK=GK,
                               prediction_s=k_1,
                               prediction_r=k_2,
                               summ=z,
                               balans=balans,
                               diskont=diskont,
                               #Geo=Geo,
                               m_kv=m_kv,
                               m_kv_1=m_kv_1,
                               m_kv_2=m_kv_2,
                               m_kv_3=m_kv_3,
                               m_kv_r=m_kv_r,
                               v_1=v_1
                               )

    return render_template('hello.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
