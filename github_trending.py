from datetime import date, timedelta
import sys

import requests
from requests.exceptions import ConnectionError


def main():
    date_week_ago = date.today() - timedelta(weeks=1)

    request_string = '{}?q=created:>{}&{}&{}'.format(
        'https://api.github.com/search/repositories',
        date_week_ago,
        'sort=stars',
        'order=desc',
    )

    try:
        github_response = requests.get(request_string)
    except ConnectionError:
        sys.exit('Could not connect to GitHub. Check your Internet connection')


if __name__ == '__main__':
    main()
