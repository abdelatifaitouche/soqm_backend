import pandas as pd
from io import BytesIO
from src.features.findings.domain.entities.rca import RootCauseCategory
from src.features.soqm_engine.application.ports import IComponentRepository


class RcaTrackerExcelParser:
    def __init__(self, isqm_repo: IComponentRepository):
        self.isqm_repo = isqm_repo

    SYNONYM_MAP = {
        # 1. Client acceptance and continuance -> Acceptance and continuance
        "client acceptance and continuance": "Acceptance and continuance",
        # 2. Governance and leadership -> Governance and leadership
        "governance and leadership": "Governance and leadership",
        # 3. Information and communication -> Information and communication
        "information and communication": "Information and communication",
        # 4. Engagement performance -> Engagement performance
        "engagement performance": "Engagement performance",
        # 5. Resources variations -> Resources
        "resources - human": "Resources",
        "resources - intellectual and technological": "Resources",
        "resources - intellectual": "Resources",
    }

    def get_normlized_isqm_name(self, excel_value: str) -> str | None:
        if not excel_value:
            return None

        normalized_key = str(excel_value).strip().lower()

        return self.SYNONYM_MAP.get(normalized_key)

    async def execute(self, file_bytes: bytes):

        print("Reading it into excel .....")
        df = pd.read_excel(BytesIO(file_bytes))

        print("Cleaning DF")
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()

        categories = {}

        print("Loading isqm refs")
        isqm_ref_map = await self.isqm_repo.list_isqm_refs()

        print(f"ISQM MAP FROM DB {isqm_ref_map}")

        for _, row in df.iterrows():
            cat_name = row["root_cause_category"]
            ind_name = row["root_cause_indicator"]
            pot_name = row["potential_root_cause"]
            isqm_name = row["isqm_component"]

            component_name = self.get_normlized_isqm_name(str(isqm_name))

            print(f"Component {component_name}")

            if not component_name:
                raise Exception("Invalid Component name")

            component_id = isqm_ref_map.get(component_name, None)

            if not component_id:
                raise Exception(
                    f"Cannot find a component with this ID {component_id}",
                )
            print(f"Component ID {component_id}")
            if cat_name not in categories:
                categories[str(cat_name)] = RootCauseCategory.create(str(cat_name))

            categories[str(cat_name)].add_indicator(
                indicator_name=ind_name,
                potential_root_cause=pot_name,
                isqm_id=component_id,
            )

        return list(categories.values())
