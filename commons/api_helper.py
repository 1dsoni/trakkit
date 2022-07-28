import logging

from requests import request, HTTPError, ConnectTimeout

from ..commons.error_lib import error_codes
from ..commons.error_lib.exceptions import ExternalApiError

logger = logging.getLogger(__name__)


class BaseApi(object):
    BASE_URL = None
    SERVICE_NAME = None
    TIMEOUT = 30

    def get_base_headers(self):
        return {
        }

    def get_headers(self):
        pass

    def _get(self, endpoint, *args, **kwargs):
        return self._make_request(endpoint, 'get', *args, **kwargs)

    def _post(self, endpoint, *args, **kwargs):
        return self._make_request(endpoint, 'post', *args, **kwargs)

    def _put(self, endpoint, *args, **kwargs):
        return self._make_request(endpoint, 'put', *args, **kwargs)

    def _patch(self, endpoint, *args, **kwargs):
        return self._make_request(endpoint, 'patch', *args, **kwargs)

    def _delete(self, endpoint, *args, **kwargs):
        return self._make_request(endpoint, 'delete', *args, **kwargs)

    @property
    def _base_url(self):
        if not self.BASE_URL:
            raise ValueError('BASE_URL cannot be empty')
        return self.BASE_URL.rstrip('/')

    def _get_url(self, endpoint):
        endpoint = endpoint.lstrip('/')
        endpoint = endpoint.strip()
        if not endpoint:
            raise ValueError('endpoint cannot be empty')
        return f'{self._base_url}/{endpoint}'

    def _make_request(self, endpoint, method, json=None, timeout=None,
                      headers=None, data=None, files=None, is_non_json=False,
                      can_log=True):
        url = self._get_url(endpoint)
        headers = {**self.get_base_headers(),
                   **(self.get_headers() or {}),
                   **(headers or {})}
        timeout = timeout or self.TIMEOUT

        # TODO remove f-strings from logs and use %s
        logger.debug(
            'Trying to make request to url:%s, method:%s', url, method
        )
        try:
            response = request(
                url=url, method=method, json=json, timeout=timeout,
                headers=headers, data=data, files=files
            )

            # checking if the response was ok (200-399);
            try:
                response.raise_for_status()
            except HTTPError:
                logger.error(
                    'Got error while making request to url:%s, method:%s, '
                    'status_code:%s', url, method, response.status_code
                )
        except ConnectTimeout:
            # should we create different exceptions? timeout etc?; since no
            # special use-case not creating now
            logger.exception(
                f'Got error while making request to url:{url}, method:{method}'
            )
            raise ExternalApiError(error_codes.request_timed_out)
        except:
            raise ExternalApiError(error_codes.undef_error)
        else:
            if can_log:
                logger.debug(
                    f'Got response: {response.text} making request to url:{url},'
                    f' method:{method}, json:{json}, headers: {headers}'
                )
            else:
                logger.debug(
                    f'Got response making request to url:{url}, method:{method}'
                )

            # in case of 204 responses it is possible no data is returned
            if response.content:
                # try to get the json content
                try:
                    json_response = response.json()
                except:
                    if not is_non_json:
                        logger.exception(
                            f'Failed to parse response as json'
                            f'url:{url}, method: {method}'
                        )
                        raise ExternalApiError(error_codes.undef_error)
                    else:
                        json_response = response.text
            else:
                json_response = {}

            status_code = response.status_code

        return json_response, status_code
