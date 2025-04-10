@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    with open("tests/mock_hotels.json", "r", encoding="utf-8") as file:
            hotels_data = json.load(file)  

    async with async_session_maker_null_pool() as session:
            hotels = [
                HotelsOrm(
                    title=hotel["title"],
                    location=hotel["location"]
                )
                for hotel in hotels_data
            ]
            
            session.add_all(hotels)
            await session.commit()
            
    with open("tests/mock_rooms.json", "r", encoding="utf-8") as file:
            rooms_data = json.load(file)  

    async with async_session_maker_null_pool() as session:
            rooms = [
                RoomsOrm(
                     hotel_id=room["hotel_id"],
                     title = room["title"],
                     description = room["description"],
                     price = room["price"],
                     quantity = room["quantity"]
                )
                for room in rooms_data
            ]
            
            session.add_all(rooms)
            await session.commit()
