import requests
from app import gemini
from app.models.user_data import UserData
from app.models.projetcs import Project

GITHUB_URL = "https://api.github.com/users"

class GitHub:
    @staticmethod
    def get_data(username) -> UserData:
        user_url = f"{GITHUB_URL}/{username}"
        repo_url = f'{user_url}/repos'

        user_response = requests.get(user_url)
        if user_response.status_code != 200:
            raise Exception(f'Error fetching data: {user_response.text}')
        user_info = user_response.json()

        repo_response = requests.get(repo_url)
        if repo_response.status_code != 200:
            raise Exception(f'Error fetching data: {repo_response.text}')
        repos_info = repo_response.json()

        projects = []
        for repo in repos_info:
            if not repo.get('fork') and repo.get('description'):
                project = Project(
                    name=repo.get("name"),
                    description=gemini.proj_description(repo.get("description")),
                    url=repo.get('html_url'),
                    tech_stack=[repo.get('language')] if repo.get('language') else []
                )
                projects.append(project)

        user_data = UserData(
            name = user_info.get('name') or user_info.get('login'),
            photo= user_info.get('avatar_url'),
            email = '',
            github_url = user_info.get('html_url'),
            bio = user_info.get('bio') or "",
            skills=[],
            location= "",
            projects=projects
        )

        return user_data