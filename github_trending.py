from datetime import date, timedelta
import sys

import requests
from requests.exceptions import ConnectionError


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


def execute_get_request(request_string):
    try:
        response = requests.get(request_string)
        return response
    except ConnectionError:
        return None


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
            repository_info['issues_url'].rstrip('{/number}')
        )
        error_message = check_response_ok(open_issues_info_response)

        if error_message:
            return error_message

        repository_info['open_issues_info'] = open_issues_info_response.json()


def main():
    count_repositories = 20

    date_week_ago = date.today() - timedelta(weeks=1)

    repositories_info_request = '{}?q=created:>{}&{}&{}'.format(
        'https://api.github.com/search/repositories',
        date_week_ago,
        'sort=stars',
        'order=desc',
    )

    print('Getting info about top starred repositories created last week...')

    repositories_info_response = execute_get_request(repositories_info_request)

    error_message = check_response_ok(repositories_info_response)

    if error_message:
        sys.exit(error_message)

    print('Getting info about open issues for every repository...')

    repositories_info = repositories_info_response.json()['items'][
                        :count_repositories]

    error_message = add_issues_info(repositories_info)

    if error_message:
        sys.exit(error_message)

    print()
    print('Top {} Most Starred Repositories Created Last Week'.format(
        count_repositories
    ))
    print()

    print_repositories_info(
        repositories_info=repositories_info,
    )


if __name__ == '__main__':
    main()
