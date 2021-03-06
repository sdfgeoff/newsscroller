
from __future__ import print_function
import httplib2
import os
import news
import colors
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'




class Gmail(object):
    def __init__(self, user, max=None, keywords=None):
        self.user = user
        self.credentials = self._get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=self.http)
        self.max = max
        self.keywords = keywords

    def update(self):
        '''Returns a list of messages from the users inbox '''
        messages = list()

        msgList = self._ListMessagesMatchingQuery(self.service, self.user, 'label:unread')
        for msgId in msgList:
            message = self._getMessage(self.service, self.user, msgId[u'id'])
            address = [h for h in message['payload']['headers'] if h[u'name'] == 'From'][0][u'value']
            subject = [h for h in message['payload']['headers'] if h[u'name'] == 'Subject'][0][u'value']
            body    = message['snippet']

            messages.append(news.News(
                subject,
                body,
                address,
                time.localtime(float(message['internalDate'])/1000),
                colors.RED
            ))

        return messages

    def _get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail-python-{}.json'.format(self.user))

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials


    def _ListMessagesMatchingQuery(self, service, user_id, query=''):
      """List all Messages of the user's mailbox matching the query.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

      Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
      """
      try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
          messages.extend(response['messages'])

        while 'nextPageToken' in response:
          page_token = response['nextPageToken']
          response = service.users().messages().list(userId=user_id, q=query,
                                             pageToken=page_token).execute()
          messages.extend(response['messages'])

        return messages
      except errors.HttpError as error:
        print( 'An error occurred: %s' % error)



    def _getMessage(self, service, user_id, msg_id):
      """Get a Message with given ID.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

      Returns:
        A Message.
      """
      try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return message
      except errors.HttpError as error:
        print('An error occurred: %s' % error)
