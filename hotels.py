from fastapi import Body, Query, APIRouter
from shemas.hotels import Hotel, HotelPatch



router = APIRouter(prefix='/hotels', tags=["Отели"])


hotels = [
     {"id": 1, "title": "Sochi", "name": "sochi"},
     {"id": 2, "title": "Дубай", "name": "dubai"},
     {"id": 3, "title": "Мальдивы", "name": "maldivi"},
     {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
     {"id": 5, "title": "Москва", "name": "moscow"},
     {"id": 6, "title": "Казань", "name": "kazan"},
     {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
 ]


@router.get("",
            summary="Получение списка отелей",
            )
def get_hotels(
         id: int | None = Query(None, description="Айдишник"),
         title: str | None = Query(None, description="Название отеля"),
         page: int  = Query(1, description="Номер страницы"),
         per_page: int = Query(3, description="Количество отелей на странице"),
 ):
     hotels_ = []
     for hotel in hotels:
         if id and hotel["id"] != id:
             continue
         if title and hotel["title"] != title:
             continue
         hotels_.append(hotel)
     if page < 1:
         page = 1
     if per_page < 1:
         per_page = 3
     start = (page - 1) * per_page
     end = start + per_page
     return hotels_[start:end]

 

 
@router.post("",
             summary="Добавление отеля",
             )
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
     "1": {
         "summary": "Сочи",
         "value": {
             "title": "Отель Сочи 5 звезд у моря",
             "name": "sochi_u_morya",
         }
     },
     "2": {
         "summary": "Дубай",
         "value": {
             "title": "Отель Дубай У фонтана",
             "name": "dubai_fountain",
         }
     }
 })
 ):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            
            "title": hotel_data.title,
            "name": hotel_data.name
        }
    )
 
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
    
    