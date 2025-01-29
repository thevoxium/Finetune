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




data = CollectData()
print(len(data.get_tourist_submissions()))


