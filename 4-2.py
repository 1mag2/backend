@router.get("/only_auth")
async def only_auth(
    request: Request
):
    access_token = request.cookies.get("access_token") or None
    return {"access_token": access_token}
    
