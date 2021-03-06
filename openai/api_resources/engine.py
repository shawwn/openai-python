from __future__ import absolute_import, division, print_function

import time

from openai import api_requestor, util
from openai.api_resources.abstract import (
    APIResource,
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
)
from openai.error import TryAgain


class Engine(ListableAPIResource):
    OBJECT_NAME = "engine"

    def generate(self, timeout=None, **params):
        start = time.time()
        while True:
            try:
                return self.request(
                    "post",
                    self.instance_url() + "/generate",
                    params,
                    stream=params.get("stream"),
                    plain_old_data=True,
                )
            except TryAgain as e:
                if timeout is not None and time.time() > start + timeout:
                    raise

                util.log_info("Waiting for snapshot to warm up", error=e)

    def search(self, **params):
        return self.request("post", self.instance_url() + "/search", params)
