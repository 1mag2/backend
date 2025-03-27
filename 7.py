async def get_filtered_by_time(
        self, 
        date_from: date,
        date_to: date,
        location,
        title,
        limit,
        offset
    ):
        
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        ) 
        
        # Базовый запрос для фильтрации отелей
        query = select(HotelsOrm).where(HotelsOrm.id.in_(hotels_ids_to_get))
        
        # Применение фильтров по location и title
        if location:
            query = query.where(HotelsOrm.location.ilike(f"%{location}%"))
        if title:
            query = query.where(HotelsOrm.title.ilike(f"%{title}%"))
        
        # Получение общего количества отелей
        count_query = select(func.count()).select_from(query.alias("subquery"))
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Применение пагинации
        query = query.offset(offset).limit(limit)
        hotels_result = await self.session.execute(query)
        hotels = hotels_result.scalars().all()
        
        return {"data": hotels, "total": total}

@router.get("",
            summary="Получение списка отелей",
            )
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Поиск по части названия отеля"),
    location: str | None = Query(None, description="Поиск по части местоположения"),
    date_from: date = Query(example="2025-03-26", description="Дата заезда"),
    date_to: date = Query(example="2025-03-28", description="Дата выезда")
):
    per_page = pagination.per_page or 5
    offset = (pagination.page - 1) * per_page

    result = await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=offset
    )
    
    total = result["total"]
    total_pages = (total + per_page - 1) // per_page if total else 0
    
    return {
        "hotels": result["data"],
        "pagination": {
            "page": pagination.page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages
        }
    }
