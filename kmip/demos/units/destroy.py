# Copyright (c) 2014 The Johns Hopkins University/Applied Physics Laboratory
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from kmip.core.enums import CredentialType
from kmip.core.enums import Operation
from kmip.core.enums import ResultStatus

from kmip.core.factories.attributes import AttributeFactory
from kmip.core.factories.credentials import CredentialFactory

from kmip.demos import utils

from kmip.services.kmip_client import KMIPProxy

import logging
import os
import sys


if __name__ == '__main__':
    # Build and parse arguments
    parser = utils.build_cli_parser(Operation.DESTROY)
    opts, args = parser.parse_args(sys.argv[1:])

    username = opts.username
    password = opts.password
    config = opts.config
    uuid = opts.uuid

    # Exit early if the UUID is not specified
    if uuid is None:
        logging.debug('No UUID provided, exiting early from demo')
        sys.exit()

    # Build and setup logging and needed factories
    f_log = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,
                         'logconfig.ini')
    logging.config.fileConfig(f_log)
    logger = logging.getLogger(__name__)

    attribute_factory = AttributeFactory()
    credential_factory = CredentialFactory()

    # Build the KMIP server account credentials
    # TODO (peter-hamilton) Move up into KMIPProxy
    if (username is None) and (password is None):
        credential = None
    else:
        credential_type = CredentialType.USERNAME_AND_PASSWORD
        credential_value = {'Username': username,
                            'Password': password}
        credential = credential_factory.create_credential(credential_type,
                                                          credential_value)
    # Build the client and connect to the server
    client = KMIPProxy(config=config)
    client.open()

    # Destroy the SYMMETRIC_KEY object
    result = client.destroy(uuid, credential)
    client.close()

    # Display operation results
    logger.info('destroy() result status: {0}'.format(
        result.result_status.enum))

    if result.result_status.enum == ResultStatus.SUCCESS:
        logger.info('destroyed UUID: {0}'.format(result.uuid.value))
    else:
        logger.info('destroy() result reason: {0}'.format(
            result.result_reason.enum))
        logger.info('destroy() result message: {0}'.format(
            result.result_message.value))
