import pytest
from src.features.risks.domain.response_ref_generator import ResponseRefGenerator


class TestResponseRefGenerator:
    def test_valid_component_name(self):
        gal_ref: str = ResponseRefGenerator.generate("Gouvernace and leadership", 1)
        fra_ref: str = ResponseRefGenerator.generate("firm risk assessement process", 1)
        rer_ref: str = ResponseRefGenerator.generate("Relevant ethical requirements", 1)
        ac_ref: str = ResponseRefGenerator.generate("Acceptance and continuance", 1)
        ep_ref: str = ResponseRefGenerator.generate("Engagement performance", 1)
        r_ref: str = ResponseRefGenerator.generate("Resources", 1)
        ic_ref: str = ResponseRefGenerator.generate("information and communication", 1)
        mar_ref: str = ResponseRefGenerator.generate("Monitoring and remidation", 1)
        assert gal_ref == "GAL-1"
        assert fra_ref == "FRA-1"
        assert rer_ref == "RER-1"
        assert ac_ref == "AAC-1"
        assert ep_ref == "EP-1"
        assert r_ref == "R-1"
        assert ic_ref == "IAC-1"
        assert mar_ref == "MAR-1"
