# %%
from dotenv import load_dotenv

from rdagent.scenarios.general_model.scenario import GeneralModelScenario

load_dotenv(override=True)

import fire

from rdagent.components.coder.model_coder.task_loader import (
    ModelExperimentLoaderFromPDFfiles,
)
from rdagent.components.document_reader.document_reader import (
    extract_first_page_screenshot_from_pdf,
)
from rdagent.log import rdagent_logger as logger
from rdagent.scenarios.qlib.developer.model_coder import QlibModelCoSTEER


def extract_models_and_implement(
    report_file_path: str,
) -> None:
    with logger.tag("init"):
        scenario = GeneralModelScenario()
        logger.log_object(scenario, tag="scenario")
    with logger.tag("r"):
        # Save Relevant Images
        img = extract_first_page_screenshot_from_pdf(report_file_path)
        logger.log_object(img, tag="pdf_image")
        exp = ModelExperimentLoaderFromPDFfiles().load(report_file_path)
        logger.log_object(exp, tag="load_experiment")
    with logger.tag("d"):
        exp = QlibModelCoSTEER(scenario).develop(exp)
        logger.log_object(exp, tag="developed_experiment")
    return exp


if __name__ == "__main__":
    fire.Fire(extract_models_and_implement)