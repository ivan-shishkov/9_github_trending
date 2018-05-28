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


def main():
    date_week_ago = date.today() - timedelta(weeks=1)

    request_string = '{}?q=created:>{}&{}&{}'.format(
        'https://api.github.com/search/repositories',
        date_week_ago,
        'sort=stars',
        'order=desc',
    )

    github_response = execute_get_request(request_string)

    if not github_response:
        sys.exit('Could not connect to GitHub. Check your Internet connection')

    if github_response.status_code != requests.codes.ok:
        sys.exit('GitHub response with status code {}, should be 200'.format(
            github_response.status_code
        ))


if __name__ == '__main__':
    main()
