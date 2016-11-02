#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2016, Artem Feofanov <artem.feofanov@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#


DOCUMENTATION = """

module: telegram
version_added: "2.2"
author: "Artem Feofanov (@tyouxa)"

short_description: module for sending notifications via telegram

description:
    - Send notifications via telegram bot, to a verified group or user
notes:
    - You will require a telegram account and create telegram bot to use this module.
options:
  msg:
    description:
      - What message you wish to send.
    required: true
  token:
    description:
      - Token identifying your telegram bot.
    required: true
  chat_id:
    description:
      - Telegram group or user chat_id
    required: true
  disable_web_page_preview:
    description:
      - Disables link previews for links in this message
    required: false
    default: 'True'
    choices:
      - 'True'
      - 'False'
    version_added: "2.3"
  disable_notification:
    description:
      - Sends the message silently.
    required: false
    default: 'False'
    choices:
      - 'True'
      - 'False'
    version_added: "2.3"
  

"""

EXAMPLES = """

send a message to chat in playbook
- telegram:  token=bot9999999:XXXXXXXXXXXXXXXXXXXXXXX
    chat_id=000000
    msg="Ansible task finished"
    disable_web_page_preview="False"
    disable_notification="True"

"""

RETURN = """

msg:
  description: The message you attempted to send
  returned: success
  type: string
  sample: "Ansible task finished"


"""

import urllib

def main():

    module = AnsibleModule(
        argument_spec = dict(
            token = dict(type='str',required=True,no_log=True),
            chat_id = dict(type='str',required=True,no_log=True),
            msg = dict(type='str',required=True),
            disable_web_page_preview = dict(type='str',default='True'),
            disable_notification = dict(type='str',default='False')),
        supports_check_mode=True
    )

    token = urllib.quote(module.params.get('token'))
    chat_id = urllib.quote(module.params.get('chat_id'))
    msg = urllib.quote(module.params.get('msg'))
    disable_web_page_preview = urllib.quote(module.params.get('disable_web_page_preview'))
    disable_notification = urllib.quote(module.params.get('disable_notification'))


    url = 'https://api.telegram.org/' + token + '/sendMessage?text=' + msg + '&chat_id=' + chat_id + '&disable_web_page_preview=' + disable_web_page_preview + '&disable_notification=' + disable_notification

    if module.check_mode:
        module.exit_json(changed=False)

    response, info = fetch_url(module, url)
    if info['status'] == 200:
        module.exit_json(changed=True)
    else:
        module.fail_json(msg="failed to send message, return status=%s" % str(info['status']))


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
if __name__ == '__main__':
    main()
