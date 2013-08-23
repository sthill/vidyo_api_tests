import logging as app_logger
import pytest

from vidyo_api_tests.api import AdminApi
from vidyo_api_tests import conf

@pytest.fixture(scope="module")
def member(request):
    member = {
        'username' : 'test1',
        'displayName' : 'Test 1',
        'employeeID' : '11001',
        'proxyName' : 'No Proxy',
        'groupName' : 'Default',
        'email' : 'test1@cern.ch',
        'locationTag' : 'Default'
    }
    def fin():
        print ("finalizing %s" % member)
        filters = {'query': member['username']}
        results = AdminApi(app_logger).GetMembers(filters)
        if 'total' in results and int(results['total']) > 0 and 'member' in results and results['member'] > 0:
            m = results['member'][0]
            memberID = m['memberID']
            response = AdminApi(app_logger).DeleteMember(memberID)
    request.addfinalizer(fin)
    return member

def test_addMember(member):
    response = AdminApi(app_logger).InsertMember(member)
    assert 'OK' in response

def test_updateMember(member):
    filters = {'query': member['username']}
    results = AdminApi(app_logger).GetMembers(filters)
    m = results['member'][0]
    memberID = m['memberID']
    vidyo_member_update = {
        'memberID': memberID,
        'username': member['username'],
        'displayName': member['displayName'],
        'employeeID': member['employeeID'],
        'groupName': member['groupName'],
        'locationTag': member['locationTag'],
        'email': member['email']
    }
    response = AdminApi(app_logger).UpdateMember(vidyo_member_update) 
    assert 'OK' in response

def test_getMembers(member):
    filters = {'query': member['username']}
    results = AdminApi(app_logger).GetMembers(filters)
    assert results['total'] == 1

def test_getMember(member):
    filters = {'query': member['username']}
    results = AdminApi(app_logger).GetMembers(filters)
    m = results['member'][0]
    memberID = m['memberID']
    results = AdminApi(app_logger).GetMember(memberID)
    assert results['name'] == member['username']
    
def test_deleteMember(member):
    filters = {'query': member['username']}
    results = AdminApi(app_logger).GetMembers(filters)
    m = results['member'][0]
    memberID = m['memberID']
    response = AdminApi(app_logger).DeleteMember(memberID)
    assert 'OK' in response
