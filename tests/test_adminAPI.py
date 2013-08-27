import logging as app_logger
import pytest

from vidyo_api_tests.api import AdminApi
from vidyo_api_tests import conf

######################
#### MEMBER TESTS ####
######################

@pytest.fixture(scope="function") 
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
    response = AdminApi(app_logger).InsertMember(member)
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

def test_deleteMember(member):
    filters = {'query': member['username']}
    results = AdminApi(app_logger).GetMembers(filters)
    m = results['member'][0]
    memberID = m['memberID']
    response = AdminApi(app_logger).DeleteMember(memberID)
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

def test_addMember():
    member = {
        'username' : 'test1',
        'displayName' : 'Test 1',
        'employeeID' : '11001',
        'proxyName' : 'No Proxy',
        'groupName' : 'Default',
        'email' : 'test1@cern.ch',
        'locationTag' : 'Default'
    }
    response = AdminApi(app_logger).InsertMember(member)
    filters = {'query': member['username']}
    results = AdminApi(app_logger).GetMembers(filters)
    if 'total' in results and int(results['total']) > 0 and 'member' in results and results['member'] > 0:
        m = results['member'][0]
        memberID = m['memberID']
        AdminApi(app_logger).DeleteMember(memberID)
    assert 'OK' in response


######################
#### ROOM TESTS ####
######################
    
@pytest.fixture(scope="function")
def room(request):
    room = {
        'name' : 'room1',
        'RoomType' : 'Public',
        'ownerName' : 'test1',
        'groupName' : 'Default',
        'extension' : '50000'
    }
    response = AdminApi(app_logger).AddRoom(room)
    def fin():
        print ("finalizing %s" % room)
        filters = {'query': room['name']}
        results = AdminApi(app_logger).GetRooms(filters)
        if 'total' in results and int(results['total']) > 0 and 'room' in results and results['room'] > 0:
            r = results['room'][0]
            roomID = r['roomID']
            response = AdminApi(app_logger).DeleteRoom(roomID)
    request.addfinalizer(fin)
    return room 

def test_deleteRoom(member, room):
    filters = {'query': room['name']}
    results = AdminApi(app_logger).GetRooms(filters)
    r = results['room'][0]
    roomID = r['roomID']
    response = AdminApi(app_logger).DeleteRoom(roomID)
    assert 'OK' in response

def test_getRooms(member, room):
    filters = {'query': room['name']}
    results = AdminApi(app_logger).GetRooms(filters)
    assert results['total'] == 1

def test_getRoom(member, room):
    filters = {'query': room['name']}
    results = AdminApi(app_logger).GetRooms(filters)
    r = results['room'][0]
    roomID = r['roomID']
    results = AdminApi(app_logger).GetRoom(roomID)
    assert results['name'] == room['name']

def test_addRoom(member):
    room = {
        'name' : 'room1',
        'RoomType' : 'Public',
        'ownerName' : 'test1',
        'groupName' : 'Default',
        'extension' : '50000'
    }
    response = AdminApi(app_logger).AddRoom(room)
    filters = {'query': room['name']}
    results = AdminApi(app_logger).GetRooms(filters)
    if 'total' in results and int(results['total']) > 0 and 'room' in results and results['room'] > 0:
        r = results['room'][0]
        roomID = r['roomID']
        AdminApi(app_logger).DeleteRoom(roomID)
    assert 'OK' in response


'''def test_updateMember(member):
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
    assert 'OK' in response'''


