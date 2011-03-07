import logging, json
from lr.lib.harvest import harvest
from datetime import datetime
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from lr.lib.base import BaseController, render

log = logging.getLogger(__name__)

class HarvestController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('harvest', 'harvest')

    def index(self, format='html'):
        """GET /harvest: All items in the collection"""
        # url('harvest')

    def create(self):
        """POST /harvest: Create a new item"""
        # url('harvest')

    def new(self, format='html'):
        """GET /harvest/new: Form to create a new item"""
        # url('new_harvest')

    def update(self, id):
        """PUT /harvest/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('harvest', id=ID),
        #           method='put')
        # url('harvest', id=ID)

    def delete(self, id):
        """DELETE /harvest/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('harvest', id=ID),
        #           method='delete')
        # url('harvest', id=ID)

    def show(self, id, format='html'):
        """GET /harvest/id: Show a specific item"""
        h = harvest()
        def getrecord():
          return json.dumps(h.get_record(request.params['doc_id']))
        def listidentifiers():
            from_date = datetime.strptime(request.params['from'],'%Y-%m-%d %H:%M:%S.%f')
            until_date = datetime.strptime(request.params['until'],'%Y-%m-%d %H:%M:%S.%f')
            return json.dumps(h.list_identifiers(from_date,until_date))
        def listrecords():
            from_date = datetime.strptime(request.params['from'],'%Y-%m-%d %H:%M:%S.%f')
            until_date = datetime.strptime(request.params['until'],'%Y-%m-%d %H:%M:%S.%f')
            return json.dumps(h.list_records(from_date,until_date))
        def identify():
            return 'identify'
        def listmetadataformats():
            return json.dumps(h.list_metadata_formats())
        def listsets():
            return 'listsets'
        switch = {
                    'getrecord':getrecord,
                    'listrecords':listrecords,
                    'listidentifiers':listidentifiers,
                    'identify': identify,
                    'listmetadataformats': listmetadataformats,                   
                    'listsets': listsets
                 }
        return switch[id]()
        # url('harvest', id=ID)

    def edit(self, id, format='html'):
        """GET /harvest/id/edit: Form to edit an existing item"""
        # url('edit_harvest', id=ID)
