from datetime import date, timedelta
import sys

import requests
from requests.exceptions import ConnectionError


def execute_get_request(request_string):
    try:
        response = requests.get(request_string)
        return response
    except ConnectionError:
        return None


def check_response_ok(response):
    if response is None:
        return 'Response not received. Check your Internet connection'

    if response.status_code != requests.codes.ok:
        return 'Response status code is {}, should be 200'.format(
            response.status_code
        )


def main():
    date_week_ago = date.today() - timedelta(weeks=1)

    request_string = '{}?q=created:>{}&{}&{}'.format(
        'https://api.github.com/search/repositories',
        date_week_ago,
        'sort=stars',
        'order=desc',
    )

    print('Getting info about top starred repositories created last week...')

    github_response = execute_get_request(request_string)

    error_message = check_response_ok(github_response)

    if error_message:
        sys.exit(error_message)

    if github_response.status_code != requests.codes.ok:
        sys.exit('GitHub response with status code {}, should be 200'.format(
            github_response.status_code
        ))


if __name__ == '__main__':
    main()
