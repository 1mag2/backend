@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelRepository(session).get_one_or_none(id=hotel_id)
