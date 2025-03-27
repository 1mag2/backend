
from fastapi import Body, APIRouter, Query
from src.shemas.facilities import FacilityAdd
from src.api.dependencies import DBDep

from shemas.rooms import RoomAdd, RoomAddRequest


router = APIRouter(prefix='/facilities', tags=["Удобства"])

@router.get("",
            summary="Получение списка удобств",
            )
async def get_facilities(
    db: DBDep,
):
    return await db.facilities.get_all()
        
 
 
@router.post("",
             summary="Добавление удобств",
             )
async def create_facilities(db: DBDep, facilitiy_data: FacilityAdd = Body()):
    facilitiy =await db.facilities.add(facilitiy_data)
    await db.commit()
    return {"status": "ok","data": facilitiy}
