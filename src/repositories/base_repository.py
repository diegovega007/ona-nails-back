from sqlmodel import SQLModel, Session, select, update, delete

class BaseRepository:
    def __init__(self, model: SQLModel, session: Session):
        self.model = model
        self.session = session

    def create(self, data: SQLModel) -> SQLModel:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def get_by_id(self, id: int) -> SQLModel:
        return self.session.get(self.model, id)

    def get_all(self) -> list[SQLModel]:
        return self.session.exec(select(self.model)).all()

    def update(self, data: SQLModel) -> SQLModel:
        data_dict = data.model_dump(exclude_unset=True)
        self.session.exec(
            update(self.model).where(self.model.id == data.id).values(**data_dict)
        )
        self.session.commit()
        return self.session.get(self.model, data.id)

    def delete(self, id: int) -> bool:
        self.session.exec(delete(self.model).where(self.model.id == id))
        self.session.commit()        
        return True