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


def add_issues_info(repositories_info):
    for repository_info in repositories_info:
        open_issues_info = execute_get_request(
            repository_info['issues_url'].rstrip('{/number}')
        )
        error_message = check_response_ok(open_issues_info)

        if error_message:
            return error_message

        repository_info['open_issues_info'] = open_issues_info.json()


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

    print('Getting info about open issues for every repository...')

    count_repositories = 20

    repositories_info = github_response.json()['items'][:count_repositories]

    error_message = add_issues_info(repositories_info)

    if error_message:
        sys.exit(error_message)



if __name__ == '__main__':
    main()
