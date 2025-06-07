from app.services.github import GitHub
from app.models.user_data import UserData
from app.services.linkedin import LinkedIn
from app.services.gemini import Gemini
from jinja2 import Template
from weasyprint import HTML
from app import gemini
from flask import url_for, render_template
import os
import shutil

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


def pdf_generator(user_data: UserData, template: str):
    template_path = os.path.join(os.path.dirname(__file__), 'templates', f"{template}.html")

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template '{template}.html' não encontrado.")

    try:
        with open(template_path, encoding='utf-8') as file:
            html_content = file.read()
    except Exception as e:
        print(f"[ERRO] Falha ao ler template: {e}")

    try:
        template_render = Template(html_content)
        rendered_html = template_render.render(user=user_data)
    except Exception as e:
        print(f"[ERRO] Falha ao renderizar template: {e}")
        raise

    output_dir = "output"
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        print(f"[ERRO] Falha ao criar diretório de saída: {e}")
        raise
    output_path = os.path.join(output_dir, "cv_output.pdf")
    try:
        HTML(string=rendered_html).write_pdf(output_path)
    except Exception as e:
        print(f"[ERRO] Falha ao gerar PDF: {e}")
        raise

    static_dir = os.path.join("app", "static")
    static_pdf_path = os.path.join(static_dir, "cv.pdf")
    try:
        os.makedirs(static_dir, exist_ok=True)
    except Exception as e:
        print(f"[ERRO] Falha ao criar diretório static: {e}")
        raise
    try:
        shutil.copyfile(output_path, static_pdf_path)
    except Exception as e:
        print(f"[ERRO] Falha ao copiar PDF para static: {e}")
        raise

    return output_path