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


def get_authz_token(token):
    #token = '''eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJsaHVqcnRpblpqMlV0Q3Faalg2bkR0Wm1zaDdYUUZsazZCdWRnMFFKQ29nIn0.eyJqdGkiOiJjMDNkNDM4ZS0wNDc5LTRjNmYtYjdmMi1lOWE1YjkxODAxNzciLCJleHAiOjE1MDY3OTcwMDQsIm5iZiI6MCwiaWF0IjoxNTA2Nzk2NzA0LCJpc3MiOiJodHRwczovL2lhbWRldi5zY2lnYXAub3JnL2F1dGgvcmVhbG1zL2RlZmF1bHQiLCJhdWQiOiJwZ2EiLCJzdWIiOiI2YzFlZWQwNy0wYzFiLTQ2NmEtYWUyNi02YTljMzc2ZDdmZDgiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJwZ2EiLCJhdXRoX3RpbWUiOjAsInNlc3Npb25fc3RhdGUiOiI1ODBkMDFlMy05MWRjLTRjNGMtYjlkNC1iYzJhZjE5MGI3YzMiLCJhY3IiOiIxIiwiY2xpZW50X3Nlc3Npb24iOiJhY2UxYmYxYi04N2YwLTQ5YzItOGE2Mi0yM2FjOTkzN2U3NDAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9kZXYudGVzdGRyaXZlLmFpcmF2YXRhLm9yZyJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiYWRtaW4iLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7InBnYSI6eyJyb2xlcyI6WyJnYXRld2F5LXVzZXIiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJ2aWV3LXByb2ZpbGUiXX19LCJuYW1lIjoiU2h1YmhhbSBLdW1hciIsInByZWZlcnJlZF91c2VybmFtZSI6InNodWJoYW1rcjEiLCJnaXZlbl9uYW1lIjoiU2h1YmhhbSIsImZhbWlseV9uYW1lIjoiS3VtYXIiLCJlbWFpbCI6InNodWt1bWFyQHVtYWlsLml1LmVkdSJ9.YWkcPZo5m96ZlUUsboS8wt_KdQqu1EFBchZhHsS2N_PZtkrMgTk-Ucn8qabU8-hSGmi4EuoR-IaSdqZAFP2M3PAOmSYkoECKeLiU-nuz2SXpGn8TsRTWAoo32DTKhUAX9IUND5uxzZ0oKEmT9yTwstvQY5iAdoQC-FWag70cHpM16YaMOp3Z1XIcKK8QjGQ0-cPUdkXg24BZ1Jd8Zpq2FFhy8G4Inh8ojuRrW_TPX1oH_0yYGIH5fEt95nHWLMWD19hxfRvEgY9HX-LsqziOOuU0Sf11EuNVq3c6sxexMiwh0923CgeQ5OmqWK6CQpQz9ORFC4rn-ni9TmiJqtvLTg'''
    return AuthzToken(accessToken=token, claimsMap={'gatewayID': "default", 'userName': "shubhamkr1"})

def get_all_projects(airavataClient, authzToken, username):

    gatewayId = "default"
    projectLists = airavataClient.getUserProjects(authzToken, gatewayId, username, -1, 0)

    return projectLists


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Options to create project')
    parser_1 = subparsers.add_parser('createproj', help='Create project')
    parser_1.add_argument('projname', type=str, help='Name of the project')
    parser_1.set_defaults(parser1=True)

    parser_1.add_argument('--description', type=str, help='Description of the project')
    parser_1.set_defaults(parser1=True)
    args = parser.parse_args()
    print(args)

    config = configparser.ConfigParser()
    config.read('airavata-client.ini')
    token = config['credentials']['AccessToken']

    authz_token = get_authz_token(token)
    #print(authz_token)
    username="shubhamkr1"
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
    Proj.owner= "shubhamkr1"

    projectId = airavataClient.createProject(authz_token,"default",Proj)
    print("Newly created projectID: "+projectId)

    projects = get_all_projects(airavataClient, authz_token, username)
    transport.close()
    print(projects)
