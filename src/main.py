import os
from datetime import datetime

from dotenv import load_dotenv

import crawler

load_dotenv()

if __name__ == '__main__':
    organization_name: str = 'HongikB612'  # Replace with the actual organization name
    token: str = os.getenv('GITHUB_TOKEN')
    start_date_str: str = '2023-05-03'  # Replace with the actual start date of your event
    num_weeks: int = 2

    usernames: list[str] = crawler.fetch_members_from_organization(organization_name, token)
    start_date: datetime = datetime.strptime(start_date_str, '%Y-%m-%d')
    contribution_data = {}

    for username in usernames:
        contributions = crawler.get_contribution_data(username, start_date)
        weekly_contributions = crawler.calculate_weekly_contributions(contributions, start_date, num_weeks)
        contribution_data[username] = contributions

    crawler.save_daily_contributions_to_file(usernames, contribution_data)

    for username, weekly_contributions in contribution_data.items():
        print(f'{username}: {weekly_contributions}')
