#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app import (app, logging)
from flask import (make_response, request)

# globals

import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
from app import settings


@app.route('/api/voice/callback/', methods=['POST'])
def voice_callback():
    is_active     = request.values.get('isActive', None)
    session_id    = request.values.get('sessionId', None)
    caller_number = request.values.get('callerNumber', None)
    direction     = request.values.get('direction', None)
    destination   = request.values.get('destination', None)

    if isActive:
	    r.hset(destination, 'phoneNumber', caller_number)
	    r.hset(destination, 'sessionId', session_id)

	    response = '<?xml version="1.0" encoding="UTF-8"?>'
	    response += '<Response>'
	    response += '<Say maxDuration="5" playBeep="false"> Demo ... </Say>' # dial?
	    response += '</Response>'

    else:
        durationInSeconds   = request.values.get('durationInSeconds', None)
        if int(durationInSeconds) > 0:
            # publish call conversion - initiated event
            visitor = Visitor()
            visitor.ip_address = request.remote_addr
            session = Session()
            event = Event(‘conversion’, ‘call-initiated’) # category — action
        else:
            # publish call conversion - droppped event
            visitor = Visitor()
            visitor.ip_address = request.remote_addr
            session = Session()
            event = Event(‘conversion’, ‘call-dropped’)
            tracker.track_event(event, session, visitor)


    resp = make_response(response, 200)
    resp.headers['Content-Type'] = "application/xml"
    resp.cache_control.no_cache = True
    return resp
