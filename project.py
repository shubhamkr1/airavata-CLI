from apache.airavata.api import Airavata
from apache.airavata.api.ttypes import *

from apache.airavata.model.workspace.ttypes import *
from apache.airavata.model.security.ttypes import AuthzToken

import argparse
import configparser

from thrift import Thrift
from thrift.transport import TSSLSocket
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

def get_transport(hostname, port):
    # Create a socket to the Airavata Server
    # TODO: validate server certificate
    transport = TSSLSocket.TSSLSocket(hostname, port, validate=False)

    # Use Buffered Protocol to speedup over raw sockets
    transport = TTransport.TBufferedTransport(transport)
    return transport


def get_airavata_client(transport):
    # Airavata currently uses Binary Protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a Airavata client to use the protocol encoder
    airavataClient = Airavata.Client(protocol)
    return airavataClient


def get_authz_token(token,username):
    return AuthzToken(accessToken=token, claimsMap={'gatewayID': "default", 'userName': username})

def get_all_projects(airavataClient, authzToken, username):

    gatewayId = "default"
    projectLists = airavataClient.getUserProjects(authzToken, gatewayId, username, -1, 0)

    return projectLists


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Options to create project')
    parser_1 = subparsers.add_parser('create-proj', help='Create project')
    parser_1.add_argument('projname', type=str, help='Name of the project')
    parser_1.set_defaults(parser1=True)
    parser_1.add_argument('owner', type=str, help='Owner(username) of the project')
    parser_1.set_defaults(parser1=True)


    parser_1.add_argument('--description', type=str, help='Description of the project')
    parser_1.set_defaults(parser1=True)
    args = parser.parse_args()
    print(args)

    config = configparser.ConfigParser()
    config.read('airavata-client.ini')
    token = config['credentials']['AccessToken']


    username = args.owner
    authz_token = get_authz_token(token,username)
    #print(authz_token)

    hostname = "apidev.scigap.org"
    port = "9930"
    transport = get_transport(hostname, port)
    transport.open()
    airavataClient = get_airavata_client(transport)
    print('Airavata client -> ' + str(airavataClient))

    #creating project object
    Proj = Project()
    Proj.gatewayId = "default"
    Proj.name = args.projname
    Proj.owner= args.owner

    #projectId = airavataClient.createProject(authz_token,"default",Proj)
    #print("Newly created projectID: "+projectId)

    projects = get_all_projects(airavataClient, authz_token, username)
    transport.close()
    print(projects)

    for proj in projects:
        if proj.name == "abcd":
            print(proj.name)
