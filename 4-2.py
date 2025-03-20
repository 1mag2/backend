@router.get("/only_auth")
async def only_auth(
    request: Request
):
    access_token = request.cookies.get("access_token") or None
    return {"access_token": access_token}
    


@router.post("/logout")
async def logout(response: Response):
    # Удаляем куку с access_token
    response.delete_cookie("access_token")
