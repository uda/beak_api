import json
import webtest
import beak.api

app = webtest.TestApp(beak.api.app)

def test_apilist():
    resp = app.get('/api/list')
    assert resp.status_int == 200
    assert resp.content_type == 'application/json'
    items = resp.json['apis']
    assert items == beak.api._api_names

def test_api_commands():
    for api in beak.api._api_names:
        resp = app.get('/api/{0}/list'.format(api))
        assert resp.status_int == 200
        assert resp.content_type == 'application/json'
        items = resp.json['commands']

        apilib = getattr(beak.api, api)
        suffix = getattr(apilib, 'cmd_suffix', '')
        cmds = [x+suffix for x in apilib.__all__]
        assert items == cmds
