# 잔디심기 농부
B612의 잔디심기 이벤트 진행을 위한 웹 크롤러입니다.

## How to use
B612 뿐만 아니라 코드를 수정한다면 어떤 Organization에서도 사용할 수 있습니다.

1. git clone하기
```bash
$ git clone https://github.com/HongikB612/jandi-counter.git
```

2. `main.py` 수정
src/main.py를 수정합니다.
```python
organization_name: str = 'HongikB612'  # Replace with the actual organization name
token: str = os.getenv('GITHUB_TOKEN')
start_date_str: str = '2023-05-03'  # Replace with the actual start date of your event
num_weeks: int = 2
```

`organization_name`에 자신의 organization 이름을 추가하면, 해당 Organization의 member들이 git contribution를 추적할 수 있습니다.
`token`에는 깃허브의 API 토큰을 추가해야 합니다. 
우선 [https://github.com/settings/tokens](https://github.com/settings/tokens)으로 이동하여 토큰을 발급받습니다.
이때 토큰의 권한에 **"read:org"** 권한이 반드시 체크되어 있어야 합니다. 토큰의 사용 용도(이름)와 만료 기한을 적절히 정하고, 완료하여 토큰을 발급받습니다.
이 토큰을 복사하여 붙여넣습니다.
이때 `token = 2932r09fklsdfe...` 이런 식으로 붙여넣어도 되고, `.env` 파일을 만들어 붙여넣어도 됩니다. 나는 `.env` 파일 이용함.
`start_date_str`은 시작 날짜입니다. 통계의 집계 시작 날짜를 집어넣어주시면 됩니다.
`num_weeks`는 이벤트 기간으로 2면 2주일을 뜻함.

3. 실행하기
```bash
$ cd src
$ python3 main.py
```

4. Output
`daily_contributions.csv` 에서 결과를 확인할 수 있습니다.

## API document
### Overview

This Python module provides functionality to fetch user contribution information from a specified GitHub organization and calculate weekly contributions. Additionally, it can save daily contribution information to a CSV file.

### Functions
#### `get_contribution_data(username: str, event_start_date: datetime)`

Fetches daily contribution data for a specified GitHub user, starting from the given `event_start_date`.

**Arguments:**

- `username` (str): GitHub username.
- `event_start_date` (datetime): Starting date for fetching contribution information.

**Returns:**

- A list of dictionaries containing the number of contributions for each date.

---

#### `extract_contribution_count(count_text: str)`

Extracts the contribution count from the given text.

**Arguments:**

- `count_text` (str): Text containing the contribution count.

**Returns:**

- The count of contributions as an integer.

---
#### `calculate_weekly_contributions(contributions, start_date: datetime, num_weeks: int)`

Calculates the weekly contributions for a specified user.

**Arguments:**

- `contributions` (list): A list of dictionaries containing daily contribution data.
- `start_date` (datetime): Starting date for calculating weekly contributions.
- `num_weeks` (int): The number of weeks to calculate contributions for.

**Returns:**

- A list of integers representing the weekly contributions.

---

#### `save_daily_contributions_to_file(usernames: list[str], contribution_data: dict)`

Saves daily contribution information for a list of users to a CSV file.

**Arguments:**

- `usernames` (list[str]): A list of GitHub usernames.
- `contribution_data` (dict): A dictionary containing daily contribution information for each user.

---

#### `fetch_members_from_organization(organization_name: str, token: str)`

Fetches a list of GitHub usernames for members of the specified organization.

**Arguments:**

- `organization_name` (str): GitHub organization name.
- `token` (str): A valid GitHub API token.

**Returns:**

- A list of GitHub usernames for the organization members.

## License
This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.
