from pyga.requests import Tracker, Page, Session, Visitor, Event

tracker = Tracker('UA-78705248-1', 'http://127.0.0.1:8080')

visitor = Visitor()
visitor.ip_address = '194.54.176.12'
session = Session()
page = Page('/call')

event = Event('convertion', 'call') # category - action
tracker.track_pageview(page, session, visitor)
tracker.track_event(event, session, visitor)
