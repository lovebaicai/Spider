# -*- encoding:utf-8 -*-

import random
from . import user_agents
from scrapy.conf import settings



class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(user_agents.agents)
        request.headers["User-Agent"] = agent
