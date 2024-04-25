import logging

from fastapi import APIRouter

from fastapi_service.services.model_infer import model_infer, model_knn_infer
from pydantic import BaseModel


logger = logging.getLogger()
router = APIRouter()



class CSV(BaseModel):
    resume_csv: str
    vacancy_csv: str

class Resume(BaseModel):
    text: str = ""
    job: str = ""
    url: str = ""
    number: int = 0

class Vacancy(BaseModel):
    vacancy: str = ""
#
@router.post("/predict_item")
async def predict_vac_res(items: CSV):

    vacancy = items.vacancy_csv
    resume = items.resume_csv
    result = model_infer(vacancy, resume)[0] * 100

    return f'{result: .2f} '


@router.post("/kneighbors")
async def predict_resumes(vacancy: Vacancy):

    result = model_knn_infer(vacancy.vacancy)

    return result
