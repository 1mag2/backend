    # src/repositories/hotels.py
    async def add(self, hotel_data: HotelsOrm):
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await self.session.execute(add_hotel_stmt)
        return hotel_data

# src/api/hotels.py
    async with async_session_maker() as session:
        hotel =await HotelRepository(session).add(hotel_data)
       
        await session.commit()
    return {"status": "ok","data": hotel}
