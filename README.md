![python](https://img.shields.io/badge/Python-blue)
[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)

This is a lightweight library that works as a connector to [Sms-Man public API](https://sms-man.com/site/docs-apiv2)  
## Installation

```bash
pip install smsmanpy
```
## Documentation  
[https://sms-man.com/site/docs-apiv2](https://sms-man.com/site/docs-apiv2)
## RESTful APIs
Usage examples:
```python
from smsmanpy import Smsman

#To receive an API key, you need to register on the sms-man.com website.
api_key = ""

client = Smsman(api_key)

#  Get current balance
print(client.get_balance())

#  Get information about all services
print(client.get_all_services())

#  Get information about all countries
print(client.get_all_countries())

#  Get the number of numbers for the selected country and service
print(client.get_limits(country_id=1, application_id=1))

#  Buy new number
request_id, phone_number = client.request_phone_number(country_id=1,
                                                       application_id=1)
# Buy many numbers
print(client.request_phone_numbers(country_id=1,
                                   application_id=1,
                                   amount=10))

#  Receive a SMS to the number
sms_code = client.get_sms(request_id)

```

  

## Contributing

Contributions are welcome.<br/>
If you've found a bug within this project, please open an issue to discuss what you would like to change.<br/>
If it's an issue with the API, please write it on out site [Sms-man Feedback](https://sms-man.com/site/feedback)