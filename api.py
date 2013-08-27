import datetime
import suds

import conf

class ClientBase():
    """
        Base class for AdminClient and UserClient
        Provides a method to obtain the correct transport for authentication.
    """

    @classmethod
    def getTransport(cls, url, username, password):
        """
            Note: we always use http.HttpAuthenticated, which implements basic authentication.
            https.HttpAuthenticated implements advanced authentication.
            Even if the 2 classes have "http" and "https" in the package names, they are just 2 ways
            of authenticating independant of http and https.
            Vidyo probably only supports basic authentication, be it through http or https.
        """
        return suds.transport.https.HttpAuthenticated(username=username, password=password, timeout=30.0)


class AdminClient(ClientBase):
    """
        Singleton for the client for Vidyo's admin API.
        We need to build a suds.client.Client with a transport argument (and not directly with username and password
        arguments) because Vidyo only supports preemptive http authentication for performance reasons.
        Suds supports this by first constructing an HttpAuthenticated transport and then passing it to the Client.
    """
    _instance = None

    @classmethod
    def getInstance(cls, adminAPIUrl=None, username=None, password=None):

        if cls._instance is None or (adminAPIUrl is not None or username is not None or password is not None):

            if adminAPIUrl is None:
                adminAPIUrl = conf.ADMIN_API_WSDL_URL
            if username is None:
                username = conf.ADMIN_API_USERNAME
            if password is None:
                password = conf.ADMIN_API_PSW

            location = conf.ADMIN_API_LOCATION

            try:
                cls._instance = suds.client.Client(adminAPIUrl, transport=ClientBase.getTransport(adminAPIUrl, username, password), location=location)
            except Exception as err:
                raise Exception(err)

        return cls._instance


class SOAPObjectFactory():
    """
        This is a class with several class methods.
        Each class method creates a different kind of SOAP object.
        These SOAP objects are passed as arguments to the SOAP service calls.
        The methods also set default values for some attributes.
    """

    def createMember(self, member):
        vidyoClient = AdminClient.getInstance()
        newMember = vidyoClient.factory.create('Member')
        newMember.name = member['username']
        newMember.password = "Use your CERN credentials"
        newMember.displayName = member['displayName']
        newMember.extension = member['employeeID']
        newMember.Language = "en"
        newMember.RoleName = "Normal"
        newMember.groupName = member['groupName']
        newMember.proxyName = "No Proxy"
        newMember.emailAddress = member['email']
        newMember.created = datetime.date.today().strftime("%Y-%m-%d")
        newMember.allowCallDirect = "True"
        newMember.allowPersonalMeeting = "True"
        newMember.locationTag = member['locationTag']
        return newMember

    def createRoom(self, room):
        vidyoClient = AdminClient.getInstance()
        newRoom = vidyoClient.factory.create('Room')
        newRoom.name = room['name']
        newRoom.RoomType = room['RoomType']
        newRoom.ownerName = room['ownerName']
        newRoom.groupName = room['groupName']
        newRoom.extension = room['extension']
        return newRoom

class ApiBase():
    """
        Provides the _handleServiceCallException method
    """

    @classmethod
    def _handleServiceCallException(cls, e):
        cause = e.args[0]
        if type(cause) is tuple and cause[0] == 401:
            pass
        else:
            raise


class AdminApi(ApiBase):
    """
        This class performs low-level operations by getting the corresponding
        client and calling a SOAP service.
        We write info statements to the log with the details of what we are doing.
        Each class method performs a single service call to Vidyo.
    """

    app_logger = None

    def __init__(self, app_logger):
        self.app_logger = app_logger

    def GetMember(self, memberID=None):
        """
            Use the API to retreive a member in Vidyo DB
        """

        self.app_logger.info("opening connection to Vidyo Admin API")
        try:
            vidyoClient = AdminClient().getInstance()
            if not vidyoClient:
                return None
        except Exception as err:
            self.app_logger.error("Error while using API: %s" % err)
            return None

        self.app_logger.debug("calling Admin API's GetMember operation")
        try:
            response = vidyoClient.service.getMember(memberID)
            return response
        except Exception as err:
            self.app_logger.error("Error while using API GetMember: %s" % err)
            return None

    def GetMembers(self, filters=None):
        """
            Use the API to retreive all the members in Vidyo DB
        """

        self.app_logger.info("opening connection to Vidyo Admin API")
        try:
            vidyoClient = AdminClient().getInstance()
            if not vidyoClient:
                return None
        except Exception as err:
            self.app_logger.error("Error while using API: %s" % err)
            return None

        self.app_logger.debug("calling Admin API's GetMembers operation")
        try:
            response = vidyoClient.service.getMembers(filters)
            return response
        except Exception as err:
            self.app_logger.error("Error while using API GetMembers: %s" % err)
            return None

    def UpdateMember(self, changed_member):
        """
            Use the API to update one specific member changed using its ID
        """
        self.app_logger.info("opening connection to Vidyo Admin API")
        try:
            vidyoClient = AdminClient().getInstance()
            if not vidyoClient:
                return None
        except Exception as err:
            self.app_logger.error("Error while using API: %s" % err)
            return None

        memberChanged = SOAPObjectFactory().createMember(changed_member)
        memberId = changed_member['memberID']
        self.app_logger.debug("calling Admin API's UpdateMember operation with member id: %s and member data: %s" % (memberId, changed_member))
        try:
            if conf.VIDYO_API_DRY_RUN:
                response = "API UPDATE:\n%s" % memberChanged
            else:
                response = vidyoClient.service.updateMember(memberId, memberChanged)
            self.app_logger.debug("Response: %s" % str(response))
            return response
        except Exception as err:
            self.app_logger.error("Error while using API UpdateMember: %s" % err)
            return None

    def InsertMember(self, new_member):
        """
            Use the API to insert a new member in Vidyo DB
        """
        self.app_logger.info("opening connection to Vidyo API")
        try:
            vidyoClient = AdminClient().getInstance()
            if not vidyoClient:
                return None
        except Exception as err:
            self.app_logger.error("Error while using API: %s" % err)
            return None

        newMember = SOAPObjectFactory().createMember(new_member)
        self.app_logger.debug("calling Admin API's addMember operation with member data: %s" % newMember)
        try:
            if conf.VIDYO_API_DRY_RUN:
                response = "API INSERT:\n%s" % newMember
            else:
                response = vidyoClient.service.addMember(newMember)
            self.app_logger.debug("Response: %s" % str(response))

            return response
        except Exception as err:
            self.app_logger.error("Error while using API InsertMember: %s" % err)
            return None

    def DeleteMember(self, memberId):
        """
            Use the API to delete one speficic member
        """
        self.app_logger.info("opening connection to Vidyo Admin API")
        try:
            vidyoClient = AdminClient().getInstance()
            if not vidyoClient:
                return None
        except Exception as err:
            self.app_logger.error("Error while using API: %s" % err)
            return None

        self.app_logger.debug("calling Admin API's DeleteMember operation with member id: %s" % memberId)
        try:
            if conf.VIDYO_API_DRY_RUN:
                response = "API DELETE FOR: %s" % memberId
            else:
                response = vidyoClient.service.deleteMember(memberId)
            self.app_logger.debug("Response: %s" % str(response))
            return response
        except Exception as err:
            self.app_logger.error("Error while using API DeleteMember: %s" % err)
            return None
    
    def AddRoom(self, new_room):
        """
            Use the API to insert a new room in Vidyo DB
        """
        self.app_logger.info("opening connection to Vidyo API")
        try:
            vidyoClient = AdminClient().getInstance()
            if not vidyoClient:
                return None
        except Exception as err:
            self.app_logger.error("Error while using API: %s" % err)
            return None

        newRoom = SOAPObjectFactory().createRoom(new_room)
        self.app_logger.debug("calling Admin API's addRoom operation with room data: %s" % newRoom)
        try:
            if conf.VIDYO_API_DRY_RUN:
                response = "API ADDROOM:\n%s" % newRoom
            else:
                response = vidyoClient.service.addRoom(newRoom)
            self.app_logger.debug("Response: %s" % str(response))

            return response
        except Exception as err:
            self.app_logger.error("Error while using API AddRoom: %s" % err)
            return None

    def GetRooms(self, filters=None):
        """
            Use the API to retreive all the rooms in Vidyo DB
        """

        self.app_logger.info("opening connection to Vidyo Admin API")
        try:
            vidyoClient = AdminClient().getInstance()
            if not vidyoClient:
                return None
        except Exception as err:
            self.app_logger.error("Error while using API: %s" % err)
            return None

        self.app_logger.debug("calling Admin API's GetRooms operation")
        try:
            response = vidyoClient.service.getRooms(filters)
            return response
        except Exception as err:
            self.app_logger.error("Error while using API GetRooms: %s" % err)
            return None

    def GetRoom(self, roomID=None):
        """
            Use the API to retreive a room in Vidyo DB
        """

        self.app_logger.info("opening connection to Vidyo Admin API")
        try:
            vidyoClient = AdminClient().getInstance()
            if not vidyoClient:
                return None
        except Exception as err:
            self.app_logger.error("Error while using API: %s" % err)
            return None

        self.app_logger.debug("calling Admin API's GetRoom operation")
        try:
            response = vidyoClient.service.getRoom(roomID)
            return response
        except Exception as err:
            self.app_logger.error("Error while using API GetRoom: %s" % err)
            return None


    def UpdateRoom(self, changed_room):
        """
            Use the API to update one specific room changed using its ID
        """
        self.app_logger.info("opening connection to Vidyo Admin API")
        try:
            vidyoClient = AdminClient().getInstance()
            if not vidyoClient:
                return None
        except Exception as err:
            self.app_logger.error("Error while using API: %s" % err)
            return None

        roomChanged = SOAPObjectFactory().createRoom(changed_room)
        roomId = changed_room['roomID']
        self.app_logger.debug("calling Admin API's UpdateRoom operation with room id: %s and room data: %s" % (roomId, changed_room))
        try:
            if conf.VIDYO_API_DRY_RUN:
                response = "API UPDATE:\n%s" % roomChanged
            else:
                response = vidyoClient.service.updateRoom(roomId, roomChanged)
            self.app_logger.debug("Response: %s" % str(response))
            return response
        except Exception as err:
            self.app_logger.error("Error while using API UpdateRoom: %s" % err)
            return None

    def DeleteRoom(self, roomId):
        """
            Use the API to delete one speficic room
        """
        self.app_logger.info("opening connection to Vidyo Admin API")
        try:
            vidyoClient = AdminClient().getInstance()
            if not vidyoClient:
                return None
        except Exception as err:
            self.app_logger.error("Error while using API: %s" % err)
            return None

        self.app_logger.debug("calling Admin API's DeleteRoom operation with room id: %s" % roomId)
        try:
            if conf.VIDYO_API_DRY_RUN:
                response = "API DELETE FOR: %s" % roomId
            else:
                response = vidyoClient.service.deleteRoom(roomId)
            self.app_logger.debug("Response: %s" % str(response))
            return response
        except Exception as err:
            self.app_logger.error("Error while using API DeleteRoom: %s" % err)
            return None
