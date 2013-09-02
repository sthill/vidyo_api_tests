import logging as app_logger
import pytest

from vidyo_api_tests.api import AdminApi, UserApi
from vidyo_api_tests import conf

######################
#### MEMBER TESTS ####
######################

'''@pytest.fixture(scope="function", params=["1", "2"]) 
def member(request):
    member = {
        'username' : 'test' + request.param,
        'displayName' : 'Test ' + request.param,
        'employeeID' : '1100' + request.param,
        'proxyName' : 'No Proxy',
        'groupName' : 'Default',
        'email' : 'test' + request.param  + '@cern.ch',
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
    return member'''

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
    
'''@pytest.fixture(scope="function", params=["1","2"])
def room(request, member):
    room = {
        'name' : 'room' + request.param,
        'RoomType' : 'Public',
        'ownerName' : member['username'],
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
    return room'''

@pytest.fixture(scope="function")
def room(request, member):
    room = {
        'name' : 'room1',
        'RoomType' : 'Public',
        'ownerName' : member['username'],
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

def test_deleteRoom(room):
    filters = {'query': room['name']}
    results = AdminApi(app_logger).GetRooms(filters)
    r = results['room'][0]
    roomID = r['roomID']
    response = AdminApi(app_logger).DeleteRoom(roomID)
    assert 'OK' in response

def test_getRooms(room):
    filters = {'query': room['name']}
    results = AdminApi(app_logger).GetRooms(filters)
    assert results['total'] == 1

def test_getRoom(room):
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
        'ownerName' : member['username'],
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


def test_updateRoom(room):
    filters = {'query': room['name']}
    results = AdminApi(app_logger).GetRooms(filters)
    r = results['room'][0]
    roomID = r['roomID']
    vidyo_room_update = {
        'roomID': roomID,
        'name': room['name'],
        'RoomType' : room['RoomType'],
        'ownerName' : room['ownerName'],
        'groupName' : room['groupName'],
        'extension' : room['extension']
    }
    response = AdminApi(app_logger).UpdateRoom(vidyo_room_update) 
    assert 'OK' in response

def test_getParticipants(room):
    response = ''
    filters = {'query': room['name']}
    results = AdminApi(app_logger).GetRooms(filters)
    if 'total' in results and int(results['total']) > 0 and 'room' in results and results['room'] > 0:
        for result in results['room']:
            if result['name'] == room['name']:
                roomID = result['roomID']
                response = AdminApi(app_logger).GetParticipants(roomID)
    assert 'total' in response and int(results['total']) >= 0
    
# Timeout to prevent that the test gets stuck in while loop if something goes wrong
@pytest.mark.timeout(30)
def test_inviteToConference(room):
    response = ''
    memberName = 'ROOM_CERN_513-1-005'
    roomName = room['name']
    filters = {'query': roomName}
    results = AdminApi(app_logger).GetRooms(filters)
    if 'total' in results and int(results['total']) > 0 and 'room' in results and results['room'] > 0:
        for result in results['room']:
            if result['name'] == room['name']:
                roomID = result['roomID']
        filters = {'query': memberName}
        results = UserApi(app_logger).Search(filters)
        if 'total' in results and int(results['total']) > 0 and 'Entity' in results and results['Entity'] > 0:
            for result in results['Entity']:
                if result['displayName'] == memberName:
                    entityID = result['entityID']
                    response = AdminApi(app_logger).InviteToConference(roomID, entityID)

                    # Cleaning
                    found = False 
                    while not found:
                        results = AdminApi(app_logger).GetParticipants(roomID)
                        if 'total' in results and int(results['total']) > 0 and 'Entity' in results and results['Entity'] > 0:
                            found = True
                            for result in results['Entity']:
                                if result['displayName'] == memberName:
                                    participantID = result['participantID']
                            AdminApi(app_logger).LeaveConference(roomID, participantID)
    assert 'OK' in response

# Timeout to prevent that the test gets stuck in while loop if something goes wrong
@pytest.mark.timeout(30)
def test_leaveConference(room):
    # Setup conference
    response = ''
    memberName = 'ROOM_CERN_513-1-005'
    roomName = room['name']
    filters = {'query': roomName}
    results = AdminApi(app_logger).GetRooms(filters)
    if 'total' in results and int(results['total']) > 0 and 'room' in results and results['room'] > 0:
        for result in results['room']:
            if result['name'] == room['name']:
                roomID = result['roomID']
        filters = {'query': memberName}
        results = UserApi(app_logger).Search(filters)
        if 'total' in results and int(results['total']) > 0 and 'Entity' in results and results['Entity'] > 0:
            for result in results['Entity']:
                if result['displayName'] == memberName:
                    entityID = result['entityID']
                    response = AdminApi(app_logger).InviteToConference(roomID, entityID)

                    # Actual test
                    found = False 
                    while not found:
                        results = AdminApi(app_logger).GetParticipants(roomID)
                        if 'total' in results and int(results['total']) > 0 and 'Entity' in results and results['Entity'] > 0:
                            found = True
                            for result in results['Entity']:
                                if result['displayName'] == memberName:
                                    participantID = result['participantID']
                            response = AdminApi(app_logger).LeaveConference(roomID, participantID)
    assert 'OK' in response

    
