from apache.airavata.api import Airavata
from apache.airavata.api.ttypes import *

from apache.airavata.model.workspace.ttypes import *
from apache.airavata.model.security.ttypes import AuthzToken
from apache.airavata.model.experiment.ttypes import *

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

def get_user_experiments(airavataClient, authzToken, username):
    gatewayId = "default"
    experiments =  airavataClient.getUserExperiments(authzToken,gatewayId,username,-1,0)
    return experiments

def launch_experiment(airavataClient, experimentId,authzToken):
    gatewayId = "default"
    try:
      airavataClient.launchExperiment(authzToken,experimentId,gatewayId)
      print("Experiment launch success!")
    except Exception as ex:
      print(ex)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Arguments to launch experiment')
    parser_1 = subparsers.add_parser('launch-exp', help='Launch existing experiment')
    parser_1.add_argument('expname', type=str, help='Name of the experiment')
    parser_1.set_defaults(parser1=True)
    parser_1.add_argument('username', type=str, help='Creator of the experiment')
    parser_1.set_defaults(parser1=True)

    args = parser.parse_args()
    print(args)

    config = configparser.ConfigParser()
    config.read('airavata-client.ini')
    token = config['credentials']['AccessToken']

    username=args.username
    authz_token = get_authz_token(token,username)
    #print(authz_token)

    hostname = "apidev.scigap.org"
    port = "9930"
    transport = get_transport(hostname, port)
    transport.open()
    airavataClient = get_airavata_client(transport)
    print('Airavata client -> ' + str(airavataClient))

    exps = get_user_experiments(airavataClient,authz_token,username)
    print(exps)

    expId = none
    for exp in exps:
        if exp.experimentName == args.expname:
              expId  = exp.experimentId

    launch_experiment(airavataClient, expId,authzToken)

    transport.close()

