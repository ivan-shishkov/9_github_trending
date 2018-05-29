from datetime import date, timedelta
import sys

import requests
from requests.exceptions import ConnectionError


class ResponseError(Exception):
    pass


def print_repository_issues_info(repository_issues_info):
    for issue_number, issue_info in enumerate(repository_issues_info, start=1):
        print('    Issue #{}'.format(issue_number))
        print('    Title: {}'.format(issue_info['title']))
        print('    HTML URL: {}'.format(issue_info['html_url']))
        print()


def print_repository_info(repository_info):
    print('Name: {}'.format(repository_info['name']))
    print('Description: {}'.format(repository_info['description']))
    print('Stars: {}'.format(repository_info['stargazers_count']))
    print('Created at: {}'.format(repository_info['created_at']))
    print('HTML URL: {}'.format(repository_info['html_url']))
    print('Language: {}'.format(repository_info['language']))
    print('Open issues count: {}'.format(repository_info['open_issues_count']))

    print_repository_issues_info(repository_info['open_issues_info'])


def print_repositories_info(repositories_info):
    for repository_number, repository_info in enumerate(
            repositories_info, start=1):
        print('#{}'.format(repository_number))

        print_repository_info(repository_info)

        print()


def execute_get_request(url, params=None):
    try:
        response = requests.get(url, params=params)
    except ConnectionError:
        raise ResponseError(
            'Response not received. Check your Internet connection',
        )

    if not response.ok:
        raise ResponseError(
            'Response status code is {}, should be 200'.format(
                response.status_code,
            )
        )
    return response


def check_response_ok(response):
    if response is None:
        return 'Response not received. Check your Internet connection'

    if not response.ok:
        return 'Response status code is {}, should be 200'.format(
            response.status_code
        )


def add_issues_info(repositories_info):
    for repository_info in repositories_info:
        open_issues_info_response = execute_get_request(
            url=repository_info['issues_url'].rstrip('{/number}'),
        )
        repository_info['open_issues_info'] = open_issues_info_response.json()


def get_repositories_info(url, url_params, count_repositories):
    repositories_info_response = execute_get_request(
        url=url,
        params=url_params,
    )
    return repositories_info_response.json()['items'][:count_repositories]


def main():
    count_repositories = 20

    print('Getting info about top starred repositories created last week...')

    try:
        repositories_info = get_repositories_info(
            url='https://api.github.com/search/repositories',
            url_params={
                'q': 'created:>{}'.format(date.today() - timedelta(weeks=1)),
                'sort': 'stars',
                'order': 'decs',
            },
            count_repositories=count_repositories,
        )
    except ResponseError as error:
        sys.exit(error)

    print('Getting info about open issues for every repository...')

    try:
        add_issues_info(repositories_info)
    except ResponseError as error:
        sys.exit(error)

    print_repositories_info(
        repositories_info=repositories_info,
    )


if __name__ == '__main__':
    main()
