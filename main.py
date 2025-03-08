from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn
 
app = FastAPI()
 
hotels = [
     {"id": 1, "title": "Sochi", "name": "sochi"},
     {"id": 2, "title": "Дубай", "name": "dubai"},
 ]


@app.get("/hotels")
def get_hotels(
         id: int | None = Query(None, description="Айдишник"),
         title: str | None = Query(None, description="Название отеля"),
 ):
     hotels_ = []
     for hotel in hotels:
         if id and hotel["id"] != id:
             continue
         if title and hotel["title"] != title:
             continue
         hotels_.append(hotel)
     return hotels_
 
@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True, description="Название отеля"),
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": title
        }
    )
 
@app.put("/hotels/{hotel_id}")
def update_hotel_all(
        hotel_id: int,
        title: str = Body(embed=True, description="Название отеля"),
        name: str = Body(embed=True)
        ):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
        else:
            return {"Отель не найден"}
    return {"status": "ok"}
   
    

@app.patch("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        title: str | None = Query(None, description="Название отеля"),
        name: str | None = Query(None)
        ):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
        else:
            return {"Отель не найден"}
    return {"status": "ok"}

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}
    
    

if __name__ == "__main__":
    
    uvicorn.run( 'main:app', reload= True, host="127.0.0.1", port=8000)