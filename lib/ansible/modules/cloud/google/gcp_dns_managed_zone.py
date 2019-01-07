#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function
__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ["preview"],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_dns_managed_zone
description:
    - A zone is a subtree of the DNS namespace under one administrative responsibility.
      A ManagedZone is a resource that represents a DNS zone hosted by the Cloud DNS service.
short_description: Creates a GCP ManagedZone
version_added: 2.5
author: Google Inc. (@googlecloudplatform)
requirements:
    - python >= 2.6
    - requests >= 2.18.4
    - google-auth >= 1.3.0
options:
    state:
        description:
            - Whether the given object should exist in GCP
        choices: ['present', 'absent']
        default: 'present'
    description:
        description:
            - A mutable string of at most 1024 characters associated with this resource for the
              user's convenience. Has no effect on the managed zone's function.
        required: false
    dns_name:
        description:
            - The DNS name of this managed zone, for instance "example.com.".
        required: false
    name:
        description:
            - User assigned name for this resource.
            - Must be unique within the project.
        required: true
    name_server_set:
        description:
            - Optionally specifies the NameServerSet for this ManagedZone. A NameServerSet is
              a set of DNS name servers that all host the same ManagedZones. Most users will leave
              this field unset.
        required: false
extends_documentation_fragment: gcp
'''

EXAMPLES = '''
- name: create a managed zone
  gcp_dns_managed_zone:
      name: "test_object"
      dns_name: test.somewild2.example.com.
      description: test zone
      project: "test_project"
      auth_kind: "service_account"
      service_account_file: "/tmp/auth.pem"
      state: present
'''

RETURN = '''
    description:
        description:
            - A mutable string of at most 1024 characters associated with this resource for the
              user's convenience. Has no effect on the managed zone's function.
        returned: success
        type: str
    dns_name:
        description:
            - The DNS name of this managed zone, for instance "example.com.".
        returned: success
        type: str
    id:
        description:
            - Unique identifier for the resource; defined by the server.
        returned: success
        type: int
    name:
        description:
            - User assigned name for this resource.
            - Must be unique within the project.
        returned: success
        type: str
    name_servers:
        description:
            - Delegate your managed_zone to these virtual name servers; defined by the server
              .
        returned: success
        type: list
    name_server_set:
        description:
            - Optionally specifies the NameServerSet for this ManagedZone. A NameServerSet is
              a set of DNS name servers that all host the same ManagedZones. Most users will leave
              this field unset.
        returned: success
        type: list
    creation_time:
        description:
            - The time that this resource was created on the server.
            - This is in RFC3339 text format.
        returned: success
        type: str
'''

################################################################################
# Imports
################################################################################

from ansible.module_utils.gcp_utils import navigate_hash, GcpSession, GcpModule, GcpRequest, replace_resource_dict
import json

################################################################################
# Main
################################################################################


def main():
    """Main function"""

    module = GcpModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            description=dict(type='str'),
            dns_name=dict(type='str'),
            name=dict(required=True, type='str'),
            name_server_set=dict(type='list', elements='str')
        )
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/ndev.clouddns.readwrite']

    state = module.params['state']
    kind = 'dns#managedZone'

    fetch = fetch_resource(module, self_link(module), kind)
    changed = False

    if fetch:
        if state == 'present':
            if is_different(module, fetch):
                fetch = update(module, self_link(module), kind)
                changed = True
        else:
            delete(module, self_link(module), kind)
            fetch = {}
            changed = True
    else:
        if state == 'present':
            fetch = create(module, collection(module), kind)
            changed = True
        else:
            fetch = {}

    fetch.update({'changed': changed})

    module.exit_json(**fetch)


def create(module, link, kind):
    auth = GcpSession(module, 'dns')
    return return_if_object(module, auth.post(link, resource_to_request(module)), kind)


def update(module, link, kind):
    module.fail_json(msg="ManagedZone cannot be edited")


def delete(module, link, kind):
    auth = GcpSession(module, 'dns')
    return return_if_object(module, auth.delete(link), kind)


def resource_to_request(module):
    request = {
        u'kind': 'dns#managedZone',
        u'description': module.params.get('description'),
        u'dnsName': module.params.get('dns_name'),
        u'name': module.params.get('name'),
        u'nameServerSet': module.params.get('name_server_set')
    }
    return_vals = {}
    for k, v in request.items():
        if v:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, kind):
    auth = GcpSession(module, 'dns')
    return return_if_object(module, auth.get(link), kind)


def self_link(module):
    return "https://www.googleapis.com/dns/v1/projects/{project}/managedZones/{name}".format(**module.params)


def collection(module):
    return "https://www.googleapis.com/dns/v1/projects/{project}/managedZones".format(**module.params)


def return_if_object(module, response, kind):
    # If not found, return nothing.
    if response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError) as inst:
        module.fail_json(msg="Invalid JSON response with error: %s" % inst)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))
    if result['kind'] != kind:
        module.fail_json(msg="Incorrect result: {kind}".format(**result))

    return result


def is_different(module, response):
    request = resource_to_request(module)
    response = response_to_hash(module, response)

    # Remove all output-only from response.
    response_vals = {}
    for k, v in response.items():
        if k in request:
            response_vals[k] = v

    request_vals = {}
    for k, v in request.items():
        if k in response:
            request_vals[k] = v

    return GcpRequest(request_vals) != GcpRequest(response_vals)


# Remove unnecessary properties from the response.
# This is for doing comparisons with Ansible's current parameters.
def response_to_hash(module, response):
    return {
        u'description': response.get(u'description'),
        u'dnsName': response.get(u'dnsName'),
        u'id': response.get(u'id'),
        u'name': response.get(u'name'),
        u'nameServers': response.get(u'nameServers'),
        u'nameServerSet': response.get(u'nameServerSet'),
        u'creationTime': response.get(u'creationTime')
    }


if __name__ == '__main__':
    main()