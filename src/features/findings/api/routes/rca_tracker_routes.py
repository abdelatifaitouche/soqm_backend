from fastapi import APIRouter, UploadFile, File, Depends, status, HTTPException
from src.features.findings.infra.inbound.excel_parser import RcaTrackerExcelParser
from src.features.soqm_engine.infra.repositories.component_repository import (
    ComponentRepository,
)
from src.api.deps.db_session import get_db
from src.features.findings.application.usecases import RcaTrackerUC
from src.infra.db.unit_of_work import UnitOfWork
from src.features.findings.infra.repositories import RcaTrackerRepository
from sqlalchemy.ext.asyncio import AsyncSession
import filetype

router = APIRouter(prefix="/rca_tracker")


async def get_rca_tracker_uc(db: AsyncSession = Depends(get_db)):
    uow = UnitOfWork(db)
    repo = RcaTrackerRepository(db)

    return RcaTrackerUC(uow, repo)


async def get_excel_parser(db: AsyncSession = Depends(get_db)):
    comp_repo = ComponentRepository(db)
    return RcaTrackerExcelParser(comp_repo)


VALID_EXCEL_MIMES = {
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # Official .xlsx
    "application/vnd.ms-excel",  # Official .xls
    "application/zip",  # Zipped archive overlap
    "application/octet-stream",  # Binary stream fallback
}


@router.post("/seed", status_code=status.HTTP_201_CREATED)
async def seed_db(
    file: UploadFile = File(...),
    parser: RcaTrackerExcelParser = Depends(get_excel_parser),
    uc: RcaTrackerUC = Depends(get_rca_tracker_uc),
):
    """
    this endpoint needs to be updated once we add the blob storage
    the upload will block the app
    """

    try:
        file_bytes: bytes = await file.read()

        if len(file_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file uploaded",
            )
        data_parsed = await parser.execute(file_bytes)

        await uc.inject_data(data_parsed)

        return {
            "success": True,
            "message": "Database Taxomony seeded",
        }
    finally:
        await file.close()
