#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app import (app, logging)
from flask import (render_template, make_response, request, jsonify)
from random import shuffle
from pyga.requests import Tracker, Page, Session, Visitor, Event
import redis

from ga.pull_stats import main

from geopy.geocoders import Nominatim
geolocator = Nominatim()

r = redis.StrictRedis(host='localhost', port=6379, db=0)
tracker = Tracker('UA-78705248-1', 'http://127.0.0.1:8080')

# import reverse_geocoder as rg
PHONE_NUMBERS = ['+254 711 082 306', '+254 711 082 514', '+254 711 082 513']


@app.route('/', methods=['GET'])
def index():
    """
    render index page
    :return: index template
    """
    # join to another table
    try:
        resp = make_response(render_template('index.html'))
        resp.cache_control.no_cache = True
        return resp
    except Exception, e:
        logging.warning('Failed on -> /')
        raise e


@app.route('/ga', methods=['GET'])
def ga():
    data = main()
    print data
    try:
        resp = make_response(render_template('ga.html', data=data))
        resp.cache_control.no_cache = True
        return resp
    except Exception, e:
        logging.warning('Failed on -> /')
        raise e


@app.route('/detail', methods=['GET'])
def detail():
    try:
        voice_one   = r.hgetall('+254711082306')
        voice_two   = r.hgetall('+254711082513')
        voice_three = r.hgetall('+254711082514')

        visitor = Visitor()
        visitor.ip_address = request.remote_addr
        session = Session()
        page = Page('/detail')
        event = Event('convertion', 'call') # category - action
        tracker.track_pageview(page, session, visitor)

        tracker.track_event(event, session, visitor)

        data = [voice_one, voice_two, voice_three]

        print data

        resp = make_response(render_template('detail.html', data=data))
        resp.cache_control.no_cache = True
        return resp
    except Exception, e:
        logging.warning('failed on detail route')
        raise e


# handle google callBack
@app.route('/api/location', methods=['POST'])
def getLocation():
    text        = request.values.get('location', None)
    url         = request.values.get('url', None)
    phoneNumber = request.values.get('phoneNumber', None)

    print phoneNumber, url, text

    latitude  = text.split("++")[0].strip()
    longitude = text.split("++")[1].strip()
    ll = str(latitude) + "," + str(longitude)

    try:
        location = geolocator.reverse(ll)
        area = location.address
        x = phoneNumber.split()
        y = "".join(x)

        uri = url.split('/')[3::]
        url = "/".join(uri)

        r.hset(y, 'location', area.split(' ')[0])
        r.hset(y, 'url', url)
    except Exception as e:
        print e

    resp = make_response(jsonify({'OK': 200}))
    return resp


@app.route('/view/<viewId>', methods=['GET'])
def view(viewId):
    try:
        shuffle(PHONE_NUMBERS)
        url = '/view/' + viewId

        # r.hset(url, 'phoneNumber', PHONE_NUMBERS[0])
        # r.hset(url, 'location', 'location')

        visitor = Visitor()
        visitor.ip_address = request.remote_addr
        session = Session()
        page = Page('/view/' + viewId )

        event = Event('convertion', 'call-initiated') # category - action
        tracker.track_pageview(page, session, visitor)

        tracker.track_event(event, session, visitor)

        resp = make_response(render_template('view.html', phoneNumber=PHONE_NUMBERS[0]))
        resp.cache_control.no_cache = True
        return resp
    except Exception, e:
        logging.warning('failed on view route')
        raise e
