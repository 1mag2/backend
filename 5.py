from fastapi import Body, Path, Query, APIRouter
from shemas.hotels import HotelAdd
from src.repositories.rooms import RoomsRepository
from src.shemas.room import RoomAdd, RoomPatch
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine


router = APIRouter(prefix='/hotels/{hotel_id}/rooms', tags=["Номера"])


@router.get("",
            summary="Получение списка номеров",
            )
async def get_rooms(
    hotel_id: int = Path( description="ID отеля"),
    title: str | None = Query(None, description="Поиск по части названия отеля"),
    
):
    
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id = hotel_id,
            title = title)
            
  
 
@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номеров отеля")
async def get_room(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=hotel_id)

 
@router.post("",
             summary="Добавление номера в отель",
             )
async def create_rooms(room_data: RoomAdd = Body(openapi_examples={
     "1": {
         "summary": "Люкс",
         "value": {
             "title": "номер класса люкс",
             
         }
     },
     "2": {
         "summary": "стандарт",
         "value": {
             "title": "номер класса стандарт",
             
         }
     }
 })
 ):
    async with async_session_maker() as session:
        room =await  RoomsRepository(session).add(room_data)
       
        await session.commit()
    return {"status": "ok","data": room}



@router.put("/{hotel_id}/rooms/{room_id}",
           summary="Обновление данных о номере",
           description="<h1> Тут мы обновляем данные об номере полностью</h1>",
           )
async def update_room_all(
        room_id: int,
        room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "ok"}
   
    

@router.patch("/{hotel_id}/rooms/{room_id}",
           summary="Частичное обновление данных об отеле",
           description="<h1>Тут мы частично обновляем данные об номере</h1>",)
async def update_room(
        room_id: int,
        room_data: RoomPatch
        ):
 
        async with async_session_maker() as session:
            await RoomsRepository(session).edit(data=room_data, exclude_unset=True, id=room_id)
            await session.commit()
        return {"status": "ok"}

@router.delete("/{hotel_id}/rooms/{room_id}",
              summary="Удаление номера",)
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "ok"}
