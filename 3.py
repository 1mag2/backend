async def edit(self, data: BaseModel, **filter_by) -> None:
        count = await self.session.scalar(
        select(func.count())
        .select_from(self.model)
        .filter_by(**filter_by)
    )
    
        if count == 0:
            raise HTTPException(status_code=404, detail="Ничего не найдено")
        elif count > 1:
            raise HTTPException(status_code=400, detail="Найдено больше одного объекта")
        
        
        edit_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump())
        await self.session.execute(edit_stmt)
        
        
    async def delete(self, **filter_by) -> None:
        count = await self.session.scalar(
        select(func.count())
        .select_from(self.model)
        .filter_by(**filter_by)
    )
    
        if count == 0:
            raise HTTPException(status_code=404, detail="Ничего не найдено")
        elif count > 1:
            raise HTTPException(status_code=400, detail="Найдено больше одного объекта")
        
        
        del_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(del_stmt)





@router.put("/{hotel_id}",
           summary="Обновление данных об отеле",
           description="<h1> Тут мы обновляем данные об отеле полностью</h1>",
           )
async def update_hotel_all(
        hotel_id: int,
        hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "ok"}

    @router.delete("/{hotel_id}",
              summary="Удаление отеля",)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "ok"}
