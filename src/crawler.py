import csv
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def get_contribution_data(username: str, event_start_date: datetime):
    url = f'https://github.com/{username}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    days = soup.find_all('rect', class_='ContributionCalendar-day')

    contributions = []
    for day in days:
        if 'data-date' not in day.attrs:
            break

        date = datetime.strptime(day['data-date'], '%Y-%m-%d').date()
        if date >= event_start_date.date():
            count_text = day.get_text()
            count = extract_contribution_count(count_text)
            contributions.append({'date': date, 'count': count})

    return contributions


def extract_contribution_count(count_text: str):
    match = re.search(r'(\d+) contribution(?:s)?', count_text)
    if match:
        return int(match.group(1))
    else:
        print(count_text)
        return 0


def calculate_weekly_contributions(contributions, start_date: datetime, num_weeks: int) -> list[int]:
    weekly_contributions = [0] * num_weeks

    for contribution in contributions:
        date = contribution['date']
        count = contribution['count']
        if start_date.date() <= date:
            week_index = (date - start_date.date()).days // 7
            if week_index < num_weeks:
                weekly_contributions[week_index] += count

    return weekly_contributions


def save_daily_contributions_to_file(usernames: list[str], contribution_data: dict):
    with open('daily_contributions.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date'] + usernames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        all_dates = set()
        for daily_contributions in contribution_data.values():
            for entry in daily_contributions:
                all_dates.add(entry['date'])

        for date in sorted(all_dates):
            row = {'Date': date}
            for username in usernames:
                row[username] = 0
                for daily_contribution in contribution_data[username]:
                    if daily_contribution['date'] == date:
                        row[username] = daily_contribution['count']
                        break
            writer.writerow(row)


def fetch_members_from_organization(organization_name: str, token: str):
    api_url = f'https://api.github.com/orgs/{organization_name}/members'
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github+json'}
    usernames = []
    page = 1

    while True:
        response = requests.get(api_url, headers=headers, params={'page': page})

        if response.status_code != 200:
            print(f'Error fetching members from organization {organization_name}: {response.status_code}')
            print(response.content)
            break

        members = response.json()
        if not members:
            break

        usernames.extend([member['login'] for member in members])
        page += 1

    return usernames
