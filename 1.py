from fastapi import Body, Query, APIRouter
from models.hotels import HotelsOrm
from src.shemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from sqlalchemy import insert, select

router = APIRouter(prefix='/hotels', tags=["Отели"])


@router.get("",
            summary="Получение списка отелей",
            )
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Поиск по части названия отеля"),
    location: str | None = Query(None, description="Поиск по части местоположения"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))  # Поиск по вхождению в title
        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))  # Поиск по вхождению в location
            
        query = query.limit(per_page).offset((pagination.page - 1) * per_page)
        
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels
 
 

 

 
@router.post("",
             summary="Добавление отеля",
             )
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
     "1": {
         "summary": "Сочи",
         "value": {
             "title": "Отель  Rich 5 звезд у моря",
             "location": "Сочи, ул. Моря, 1",
         }
     },
     "2": {
         "summary": "Дубай",
         "value": {
             "title": "Отель Deluxe У фонтана",
             "location": "Дубай, ул. Шейха, 2",
         }
     }
 })
 ):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "ok"}



@router.put("/{hotel_id}",
           summary="Обновление данных об отеле",
           description="<h1> Тут мы обновляем данные об отеле полностью</h1>",
           )
def update_hotel_all(
        hotel_id: int,
        hotel_data: Hotel
        ):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
                hotel["title"] = hotel_data.title
                hotel["name"] = hotel_data.name
 
    return {"status": "ok"}
   
    

@router.patch("/{hotel_id}",
           summary="Частичное обновление данных об отеле",
           description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",)
def update_hotel(
        hotel_id: int,
        hotel_data: HotelPatch
        ):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
 
    return {"status": "ok"}

@router.delete("/{hotel_id}",
              summary="Удаление отеля",)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}
    
    
