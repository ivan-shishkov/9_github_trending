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


def print_repositories_info(repositories_info, title):
    print()
    print(title)
    print()

    for repository_number, repository_info in enumerate(
            repositories_info, start=1):
        print('#{}'.format(repository_number))

        print_repository_info(repository_info)

        print()


def execute_get_request(url, params=None):
    try:
        response = requests.get(url, params=params)
    except ConnectionError:
        return None

    return response.json() if response.ok else None


def add_issues_info(repositories_info):
    for repository_info in repositories_info:
        open_issues_info = execute_get_request(
            url=repository_info['issues_url'].rstrip('{/number}'),
        )
        if open_issues_info is None:
            return False

        repository_info['open_issues_info'] = open_issues_info

    return True


def get_repositories_info(url, url_params, count_repositories):
    repositories_info = execute_get_request(
        url=url,
        params=url_params,
    )
    if repositories_info is None:
        return None

    return repositories_info['items'][:count_repositories]


def main():
    count_repositories = 20

    print('Getting info about top starred repositories created last week...')

    repositories_info = get_repositories_info(
        url='https://api.github.com/search/repositories',
        url_params={
            'q': 'created:>{}'.format(date.today() - timedelta(weeks=1)),
            'sort': 'stars',
            'order': 'decs',
        },
        count_repositories=count_repositories,
    )

    if repositories_info is None:
        sys.exit('Could not get info about repositories')

    print('Getting info about open issues for every repository...')

    if not add_issues_info(repositories_info):
        sys.exit('Could not get info about open issues of repositories')

    print_repositories_info(
        repositories_info=repositories_info,
        title='Top {} Most Starred Repositories Created Last Week'.format(
            len(repositories_info)
        ),
    )


if __name__ == '__main__':
    main()
