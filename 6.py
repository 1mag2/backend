from fastapi import  APIRouter
from src.shemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependencies import DBDep, UserIdDep



router = APIRouter(prefix='/bookings', tags=["Бронирование"])

@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        bookking_data: BookingAddRequest
):  
    room = await db.rooms.get_one_or_none(id = bookking_data.room_id)
    room_price = room.price
    
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **bookking_data.model_dump()
)
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "ok", "data": booking}
