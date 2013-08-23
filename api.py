import datetime
import suds

import conf
#from sync_vidyo_ldap.mail_handler import VidyoMail


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
        #newMember.memberID = member.memberID
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

            '''email_body = """Dear %s,\n please note that your registration to the CERN Vidyo service is now active.\n
You can start using the service at https://vidyoportal.cern.ch where you login with your CERN account.\n
General service information can be found here: http://cern.ch/vidyo/\n\n
Best regards,\n
CERN Vidyo Service""" % newMember.displayName
            email_subject = "Vidyo registration completed"
            email_to = [newMember.emailAddress]

            m = VidyoMail(email_to, email_subject, email_body)
            m.send()'''

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
