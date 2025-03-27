
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

# Добавляем методы в репозиторий rooms_facilities
class RoomsFacilitiesRepository:
    async def get_facilities_by_room(self, room_id: int) -> list[int]:
        result = await self.session.execute(
            select(self.model.facility_id).where(self.model.room_id == room_id)
        )
        return list(result.scalars())

    async def delete_by_room_and_facilities(self, room_id: int, facility_ids: list[int]):
        if not facility_ids:
            return
        stmt = delete(self.model).where(
            self.model.room_id == room_id,
            self.model.facility_id.in_(facility_ids)
        )
        await self.session.execute(stmt)

# Обновляем обработчики
@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room_all(...):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    
    # Синхронизация удобств
    current_ids = await db.rooms_facilities.get_facilities_by_room(room_id)
    new_ids = room_data.facilities_ids
    
    to_remove = list(set(current_ids) - set(new_ids))
    to_add = list(set(new_ids) - set(current_ids))
    
    if to_remove:
        await db.rooms_facilities.delete_by_room_and_facilities(room_id, to_remove)
    if to_add:
        facilities_data = [RoomFacilityAdd(room_id=room_id, facility_id=fid) for fid in to_add]
        await db.rooms_facilities.add_bulk(facilities_data)
    
    await db.commit()
    return {"status": "ok"}

@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_room(...):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(...)
    
    if hasattr(room_data, 'facilities_ids') and room_data.facilities_ids is not None:
        current_ids = await db.rooms_facilities.get_facilities_by_room(room_id)
        new_ids = room_data.facilities_ids
        
        to_remove = list(set(current_ids) - set(new_ids))
        to_add = list(set(new_ids) - set(current_ids))
        
        if to_remove:
            await db.rooms_facilities.delete_by_room_and_facilities(room_id, to_remove)
        if to_add:
            facilities_data = [RoomFacilityAdd(room_id=room_id, facility_id=fid) for fid in to_add]
            await db.rooms_facilities.add_bulk(facilities_data)
    
    await db.commit()
    return {"status": "ok"}


   
    async def get_one_or_none_with_rels(self, **filter_by):
        query = (
             select(self.model)
             .options(selectinload(self.model.facilities))
             .filter_by(**filter_by)
         )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
                return None
        return  RoomWithRels.model_validate(model, from_attributes=True)
