from app.services.github import GitHub
from app.models.user_data import UserData
from app.services.linkedin import LinkedIn
from app.services.gemini import Gemini
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from app import gemini
from flask import url_for
import os

def join_user_data(csv_path: str, github_username: str) -> UserData:
    linkedin_data = LinkedIn.get_user_data_from_csv(csv_path)
    github_data = GitHub.get_data(github_username)

    bio_link = linkedin_data.bio
    bio_git = github_data.bio
    biograph = gemini.prof_bio(bio_link, bio_git)

    join_info = UserData(
        name=linkedin_data.name or github_data.name,
        photo=github_data.photo,
        email=linkedin_data.email or '',
        github_url=github_data.github_url,
        bio=biograph,
        skills=list(set(linkedin_data.skills)),
        location=linkedin_data.location,
        projects=github_data.projects
    )

    return join_info


def pdf_generator(user_data: UserData, output: str = "output/cv.pdf"):
    os.makedirs(os.path.dirname(output), exist_ok=True)

    env = Environment(loader=FileSystemLoader("app/templates"))
    env.globals['url_for'] = url_for
    template = env.get_template("cv_template.html")
    html = template.render(user=user_data)

    HTML(string=html).write_pdf(output)
    return output