
from datetime import date

import pytest
from src.shemas.bookings import BookingAdd


@pytest.mark.asyncio
async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from= date.today(),
        date_to= date.today(),
        price=100
     )
    new_booking_data = await db.bookings.add(booking_data)
    print(f"New Booking Data: {new_booking_data}")
    assert new_booking_data is not None
    
    
    # получить бронь и убедиться что она есть
    booking = await db.bookings.get_one_or_none(id=new_booking_data.id)
    print(f"Retrieved Booking: {booking}")
    assert booking is not None
    assert booking.price == 100
    
    # обновить бронь и убедиться что она обновилась
    updated_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from= date.today(),
        date_to= date.today(),
        price=200
    )
    updated_booking = await db.bookings.edit(updated_data, id=booking.id)
    print(f"Updated Booking: {updated_booking}")
    assert updated_booking is not None
    assert updated_booking.price == 200
    
    # удалить бронь
    await db.bookings.delete(booking.id)
    deleted_booking = await db.bookings.get_one_or_none(id=booking.id)
    print(f"Deleted Booking: {deleted_booking}")
    assert deleted_booking is None
    
    await db.session.rollback()
