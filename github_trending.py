from datetime import date, timedelta

import requests


def main():
    date_week_ago = date.today() - timedelta(weeks=1)

    request_string = '{}?q=created:>{}&{}&{}'.format(
        'https://api.github.com/search/repositories',
        date_week_ago,
        'sort=stars',
        'order=desc',
    )

    github_response = requests.get(request_string)


if __name__ == '__main__':
    main()
