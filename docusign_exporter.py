import requests
import json
import os
import sys

class DocusignService(object):
    def __init__(
            self,
            login=None,
            password=None,
            integrator_key=None):
        self.session = requests.Session()
        self.login_accounts = self.authenticate(login, password, integrator_key)
        self.base_url = self.login_accounts['loginAccounts'][0]['baseUrl']
        self.envelopes = None
        self.get_envelopes()
        self.get_documents()

    def authenticate(self, login, password, integrator_key):
        auth_data = {
            'Username': login,
            'Password': password,
            'IntegratorKey': integrator_key
        }

        self.session.headers['X-DocuSign-Authentication'] = json.dumps(auth_data)
        response = self.session.get('https://demo.docusign.net/restapi/v2/login_information')
        if response.ok:
            return response.json()
        else:
            print response.json()
            sys.exit()

    def get_envelopes(self):
        response = self.session.get(self.base_url + '/envelopes?from_date=1960-01-01T00:00:00Z')
        if response.ok:
            self.envelopes = response.json()['envelopes']
            while response.json()['nextUri']:
                response = self.session.get(self.base_url + response.json()['nextUri'])
                if response.ok:
                    self.envelopes.extend(response.json()['envelopes'])


    def get_documents(self):
        if self.envelopes:
            for envelope in self.envelopes:
                envelop_dir = os.path.join('.', envelope['envelopeId'])
                print('Downloading envelope: {}'.format(envelope['envelopeId']))
                if not os.path.exists(envelop_dir):
                    os.mkdir(envelop_dir)
                response = self.session.get(self.base_url + envelope['documentsUri'])
                if response.ok and response.json():
                    envelope_documents = response.json()['envelopeDocuments']
                    for document in envelope_documents:
                        print('Downloading document: {}'.format(document['name']))
                        with open(os.path.join(envelop_dir, document['name']), 'wb+') as file:
                            content = self.session.get(self.base_url + document['uri'])
                            if content.ok:
                                file.write(content.content)

                response = self.session.get(self.base_url + envelope['recipientsUri'])
                if response.ok and response.json():
                    for reciepient_type in response.json().keys():
                        if reciepient_type in ['currentRoutingOrder', 'recipientCount']:
                            continue
                        if response.json()[reciepient_type]:
                            with open(os.path.join(envelop_dir, reciepient_type), 'wb+') as file:
                                json.dump(response.json()[reciepient_type], file)



if __name__ == '__main__':
    args = sys.argv
    if '--help' in args or '-h' in args:
        print 'usage: python docusign-exporter.py [email] [password] [integrator_key]'
    else:
        DocusignService(*args[1:])