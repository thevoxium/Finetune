import requests
from bs4 import BeautifulSoup
import json
import time 
import random


class CollectData:
    def __init__(self):
        self.base_url = "https://codeforces.com"
        self.api_url = "https://codeforces.com/api"
        self.handle = "tourist"

    def get_tourist_submissions(self, count = 0):
        url = f"{self.api_url}/user.status?handle={self.handle}"
        response = requests.get(url)
        if response.status_code != 200:
            print("Unable to fetch the submissions")
            return []

        submissions = response.json()['result']

        accepted_submissions = [sub for sub in submissions if sub['verdict'] == 'OK']

        seen_problems = set()
        unique_submissions = []
        for sub in accepted_submissions:
            problem_key = (sub['problem']['contestId'], sub['problem']['index'])
            if problem_key not in seen_problems:
                seen_problems.add(problem_key)
                unique_submissions.append(sub)

        if count:
            unique_submissions = unique_submissions[:count]

        return unique_submissions

    def collect_tourist_data(self, num_problems = None):
        print("Creating Tourist Submissions Data!")

        submissions = self.get_tourist_submissions(count = num_problems)
        dataset = []

        for idx, submission in enumerate(submissions):
            contest_id = submission['problem']['contestId']
            problem_index = submission['problem']['index']
            submission_id = submission['id']

            print(f"Processing problem {idx+1}/{len(submissions)}: Contest {contest_id}, Problem {problem_index}")

            problem_data = self.get_problem_data(contest_id, problem_index)
            if not problem_data:
                print(f"Skipping problem {contest_id}{problem_index} - couldn't fetch problem data")
                continue

            solution = self.get_submission_code(contest_id, submission_id)
            if not solution:
                print(f"Skipping problem {contest_id}{problem_index} - couldn't fetch solution")
                continue

            problem_data.update({
                'contest_id': contest_id,
                'problem_index': problem_index,
                'submission_id': submission_id,
                'solution': solution,
                'tags': submission['problem'].get('tags', []),
                'rating': submission['problem'].get('rating'),
                'submission_time': submission['creationTimeSeconds']
            })

            dataset.append(problem_data)
            time.sleep(1)

        return dataset






data = CollectData()
print(len(data.get_tourist_submissions()))


