class UsersOrm(Base):
    __tablename__= "users"
    # __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column( String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column( String(200))
