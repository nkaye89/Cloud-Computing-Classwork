# Copyright 2021 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#             http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

import webapp2

import model

#from boto3 import resource

#import dynamodb13


def AsDict(guest):
    return {'id': guest.key.id(), 'first': guest.first, 'last': guest.last}


class RestHandler(webapp2.RequestHandler):

    def dispatch(self):
        # time.sleep(1)
        super(RestHandler, self).dispatch()

    def SendJson(self, r):
        self.response.headers['content-type'] = 'text/plain'
        self.response.write(json.dumps(r))


class QueryHandler(RestHandler):

    def get(self):
        guests = model.AllGuests()
        r = [AsDict(guest) for guest in guests]
        self.SendJson(r)


class UpdateHandler(RestHandler):

    def post(self):
        r = json.loads(self.request.body)
        gid = r['id']
        first = r['first']
        last = r['last']
        guest = model.UpdateGuest(r['id'], r['first'], r['last'])
        r = AsDict(guest)
        self.SendJson(r)

        response = google.appengine.api.urlfetch.make_fetch_call(
            'http://ec2-id.compute-1.amazonaws.com:8080',           # replace with id with own ec2 id (e.g. 52-90-237-152)
            payload='{"gid":gid,"first":first,"last":last}', 
            method='PUT', 
            headers={
                'Content-Type': 'application/json'
            }, 
            allow_truncated=False,
            follow_redirects=True, 
            deadline=None, 
            validate_certificate=None
        )


class InsertHandler(RestHandler):

    def post(self):
        r = json.loads(self.request.body)
        first = r['first']
        last = r['last']
        guest = model.InsertGuest(r['first'], r['last'])
        r = AsDict(guest)
        self.SendJson(r)
        
        response = google.appengine.api.urlfetch.make_fetch_call(
            'http://ec2-id.compute-1.amazonaws.com:8080',           # replace with id with own ec2 id (e.g. 52-90-237-152)
            payload='{"first":first,"last":last}', 
            method='POST', 
            headers={
                'Content-Type': 'application/json'
            }, 
            allow_truncated=False, 
            follow_redirects=True, 
            deadline=None, 
            validate_certificate=None
        )


class DeleteHandler(RestHandler):

    def post(self):
        r = json.loads(self.request.body)
        gid = r['id']
        model.DeleteGuest(r['id'])

        response = google.appengine.api.urlfetch.make_fetch_call(
            'http://ec2-id.compute-1.amazonaws.com:8080',           # replace with id with own ec2 id (e.g. 52-90-237-152)
            payload='{"gid":gid}', 
            method='DELETE', 
            headers={
                'Content-Type': 'application/json'
            }, 
            allow_truncated=False, 
            follow_redirects=True, 
            deadline=None, 
            validate_certificate=None
        )


APP = webapp2.WSGIApplication([
    ('/rest/query', QueryHandler),
    ('/rest/insert', InsertHandler),
    ('/rest/delete', DeleteHandler),
    ('/rest/update', UpdateHandler),
], debug=True)
