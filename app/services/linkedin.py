import pandas as pd
from app.models.user_data import UserData
from app.models.projetcs import Project  
from app.services.techs import ALL_TECH_KEYWORDS

class LinkedIn:

    @staticmethod
    def get_user_data_from_csv(csv_path: str) -> UserData:
        df = pd.read_csv(csv_path)

        row = df.iloc[0]

        name = f"{row.get('First Name', '')} {row.get('Last Name', '')}".strip()

        bio = str(row.get("Summary", "")).strip()

        headline = str(row.get("Headline", "")).strip()

        location = str(row.get("Geo Location", "")).strip()

        skills = [kw for kw in ALL_TECH_KEYWORDS if kw.lower() in headline.lower()]

        user_data = UserData(
            name=name,
            photo= "",
            email="",  
            github_url="",
            bio=f"{bio}\n\n{headline}" if bio else headline,
            skills=skills,
            location = location,
            projects=[]  
        )

        return user_data