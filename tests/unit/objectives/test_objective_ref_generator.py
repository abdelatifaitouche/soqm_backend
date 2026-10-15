import logging

from src.features.soqm_engine.domain.services.objective_ref_generator import (
    ObjectiveRefGenerator,
)

logger = logging.getLogger()


class TestObjectiveReferenceGenerator:
    def test_basic_generation(self):

        for i in range(1, 100):
            ref = ObjectiveRefGenerator.generate_objective_ref(1, i)
            logger.info(ref)
