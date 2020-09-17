import logging

from flask import jsonify, request

from squirro.common.dependency import get_injected
from squirro.sdk.studio import StudioPlugin

plugin = StudioPlugin(__name__)
log = logging.getLogger(__name__)

@plugin.route('/example', methods=['POST'])
def example():

    data = request.json

    header = request.headers.get('header_name')
    url_param = request.args.get('arg_name')
    parameter = data.get('param_name')

    client = get_injected('squirro_client')

    try:
        client.do_something()

    except Exception as e:
        res = jsonify({'error': unicode(e)})
        res.status_code = 500
        return res

    else:
        return jsonify({'status': 'Success!'})
