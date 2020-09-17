import json
import logging
import psutil
import os

from squirro.common.config import get_config
from squirro.common.resource import Resource
from squirro.common.dependency import get_injected
import wsgiservice
import requests
import json

config = get_config('squirro.service.extauth')
log = logging.getLogger(__name__)

#start time of proc, to enable cache busting on restart
pid = os.getpid()

@wsgiservice.mount('/v0/authenticate')
class AuthenticateResource(Resource):

    def get_header(self, parameter_name, headers):
        """gets any header value based on the extauth.ini file
           support multiple value lookups,

           e.g. if  the config file contains:

           [somedomain]
           email = mail email e-mail
           then ot will first look for mail, then email etc.

           returns False if no result found
        """

        #get config
        section = 'somedomain'
        header_string = config.get(section, parameter_name)

        if not header_string:
            log.warn("parameter %r not found in %r section of extauth.ini", parameter_name, section)
            return False

        header_names = header_string.strip().replace(',', ' ').split(' ')
        log.debug('Lookup %r parameter in these http headers: %r', parameter_name, header_names)

        for header_name in header_names:
            log.debug("Looking up header %r not defined", header_name)
            header_value = headers.get(header_name)

            if header_value:
                header_value = header_value.strip()

                if header_value == "":
                    log.warn("header %r is empty", header_name)
                    continue
                else:

                    log.info("Parameter: %r -> %r", parameter_name, header_value)
                    return header_value
            else:
                log.warn("header %r is not defined", header_name)


        log.warn('Parameter %r (%r) not found in http header', parameter_name, header_names)
        return False


    def POST(self):
        section = 'somedomain'
        request = self.request.json_body
        headers = request.get('headers', {})

        log.debug('Request data %s', json.dumps(self.request.json_body, indent=4))

        #debug the request
        log.debug('Request cookies %r', self.request.cookies)
        log.debug('Request params %r', self.request.params)

        #get the user id from WAF based on extauth.ini config
        userid = self.get_header('userid', headers)

        if not userid:
            log.debug('Userid is not defined, returning code 400')
            wsgiservice.raise_400(self, 'No userid found, deny access')

        email = "{0}@vt.ch".format(user_id)
        fullname = userid

        #TODO Potentially add a ldap lookup here if really needed

        #get group mapping
        groups_mapping_str = config.get(section, 'group_mapping')

        #parse the json string
        group_mapping = json.loads(groups_mapping_str)

        #get  the groups information from WAF based on extauth.ini config
        group_header = self.get_header('groups', headers)

        groups = group_header.split(",")
        normalized_groups = []

        for group in groups:
            normalized_groups.append(group.strip())

        group_ids = []

        for group in normalized_groups:
            if group in group_mapping:
                group_ids.append(group_mapping.get(group))

        #deduplicate
        group_ids = list(set(group_ids))

        #assemble the userinfo that we can use to extend the query string
        retval = {
            'user_id': userid,
            'user_information': {
                'user_id': userid
            },
            'tenant': config.get('somedomain', 'tenant'),
            'email': email,
            'fullname': fullname,
            'group_ids': group_ids
        }

        log.debug('User %s, returning %s', userid, json.dumps(retval, indent=4))

        return retval

app = wsgiservice.get_app(globals())
