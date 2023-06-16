import asyncio
import aiohttp
from smsmanpy.exeptions import WrongTokenError, SMSnotReceivedError, LowBalance, NoNumbers


class Smsman:
    __base_url = "http://api.sms-man.ru/control"
    __method_balance = "/get-balance"
    __method_get_limits = "/limits"
    __method_get_number = "/get-number"
    __method_get_sms = "/get-sms"
    __method_get_all_countries = "/countries"
    __method_get_all_services = "/applications"
    __method_reject_number = "/set-status"

    def __init__(self, token: str):
        """
        :param token: Your Token from sms-man.com
        """

        self.__token = token
        self.__params = {"token": token}

    async def __get_balance(self):
        """
        Information about your balance in RUB

        GET /get-balance

        :return: The amount of your balance, RUB
        :rtype: float
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(self.__base_url + self.__method_balance, params=self.__params) as response:
                data = await response.json()
                if "balance" in data:
                    return float(data['balance'])
                else:
                    raise WrongTokenError(data['error_msg'])

    async def __get_limits(self, country_id=None, application_id=None):
        """
        Information about amount of available numbers in country for service
        If country_id is None or application_id is None send information about
        all countries and applications

        :param country_id: id of country, str
        :param application_id: if of application, str
        :return: The amount of available numbers
        :rtype: json
        """

        params = self.__check_params(country_id, application_id)

        async with aiohttp.ClientSession() as session:
            async with session.get(self.__base_url + self.__method_get_limits, params=params) as response:
                data = await response.json()
                return data

    async def __get_sms(self, request_id: str):
        """
        Texts out the request number.
        If the SMS has not yet arrived, an error will be returned.

        :param request_id: Number of ID (get with phone number)
        :return: sms_code
        :rtype: str
        """

        params = self.__check_params(request_id=request_id)

        async with aiohttp.ClientSession() as session:
            async with session.get(self.__base_url + self.__method_get_sms, params=params) as response:
                data = await response.json()
                if "sms_code" in data:
                    return data['sms_code']
                else:
                    raise SMSnotReceivedError(data['error_msg'])

    async def __get_all_countries(self):
        """
        Return information about all countries

        :return: JSON of all countries with ID, name
        :rtype: json
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(self.__base_url + self.__method_get_all_countries, params=self.__params) as response:
                data = await response.json()
                if "1" in data:
                    return data
                else:
                    raise WrongTokenError(data['error_msg'])

    async def __get_all_services(self):
        """
        Return information about all applications

        :return: JSON of all applications with ID, name
        :rtype: json
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(self.__base_url + self.__method_get_all_services, params=self.__params) as response:
                data = await response.json()
                if "1" in data:
                    return data
                else:
                    raise WrongTokenError(data['error_msg'])

    async def __request_phone_number(self, country_id: str, application_id: str):
        """
        Queries the phone number by country id and service id.
        Returns request number (needed to receive sms) and phone number.

        :param country_id: id of country. Can check list on web-site or with method get_all_countries
        :param application_id: id of application. Can check list on web-site or with method get_all_services
        :return: request_id, number
        :rtype: str, str
        """

        params = self.__check_params(country_id, application_id)

        async with aiohttp.ClientSession() as session:
            async with session.get(self.__base_url + self.__method_get_number, params=params) as response:
                resp_json = await response.json()
                if "request_id" in resp_json and "number" in resp_json:
                    return resp_json['request_id'], resp_json["number"]
                elif resp_json['error_code'] == "balance":
                    raise LowBalance(resp_json['error_msg'])
                elif resp_json["error_code"] == "no_numbers":
                    raise NoNumbers(resp_json["error_msg"])
                else:
                    raise WrongTokenError(resp_json['error_msg'])

    async def __request_many_phone_numbers(self, country_id: str, application_id: str, semaphore: asyncio.Semaphore):
        params = self.__check_params(country_id, application_id)
        async with aiohttp.ClientSession() as session:
            for _ in range(3):
                async with semaphore:
                    async with session.get(self.__base_url + self.__method_get_number, params=params) as response:
                        resp_json = await response.json()
                        if "request_id" in resp_json and "number" in resp_json:
                            return resp_json['request_id'], resp_json["number"]
                        elif resp_json['error_code'] == "balance":
                            raise LowBalance(resp_json['error_msg'])
                        elif resp_json["error_code"] == "no_numbers":
                            continue
                        else:
                            raise WrongTokenError(resp_json['error_msg'])

    async def _request_phone_numbers(self, country_id: str, application_id: str, amount: int):

        semaphore = asyncio.Semaphore(2)
        tasks = [self.__request_many_phone_numbers(country_id, application_id, semaphore) for i in range(amount)]
        responses = await asyncio.gather(*tasks)

        return responses

    def __check_params(self, country_id=None, application_id=None, request_id=None, status=None):
        """
        Create params for request

        :param country_id:
        :param application_id:
        :param request_id:
        :return: params
        :rtype: dict
        """

        params = self.__params.copy()

        if country_id:
            params['country_id'] = country_id
        if application_id:
            params['application_id'] = application_id
        if status:
            params['status'] = status
        if request_id:
            params['request_id'] = request_id

        return params

    def get_all_services(self):
        return asyncio.run(self.__get_all_services())

    def get_all_countries(self):
        return asyncio.run(self.__get_all_countries())

    def get_balance(self):
        return asyncio.run(self.__get_balance())

    def get_limits(self, country_id=None, application_id=None):
        return asyncio.run(self.__get_limits(country_id, application_id))

    def get_sms(self, request_id: str):
        return asyncio.run(self.__get_sms(request_id))

    def request_phone_number(self, country_id: str, application_id: str):
        return asyncio.run(self.__request_phone_number(country_id, application_id))

    def request_phone_numbers(self, country_id: str, application_id: str, amount: int):
        return asyncio.run(self._request_phone_numbers(country_id, application_id, amount))


client = Smsman('acDJv1u-S1tjXqps1eKhMwt7yDHO30hU')
a = client.get_balance()
print(a)
