from lib import BaseService
from lib.base_database import Session

from database_models.user import User


class UserService(BaseService):

    __session = Session()

    async def get_user(self) -> list[dict[str, str | bool | int]] | int:
        try:
            query = self.__session.query(User).all()
            content = []
            for result in query:
                content.append({
                    "id": result.id,
                    "name": result.name,
                    "last_session": result.last_session,
                    "os": result.os,
                    "device": result.device
                })
            self.__session.close()
            return content
        except Exception as error:
            print(error)
            return 400

    async def set_user(self, request) -> int:
        try:
            data = request
            old_user = self.__session.query(User).filter_by(id=1).first()
            if old_user:
                old_user.last_session = data["last_session"]
            else:
                new_user = User(
                    id=data["id"], 
                    name=data["name"], 
                    last_session=data["last_session"], 
                    os=data["os"], 
                    device=data["device"]
                )
                self.__session.add(new_user)
            self.__session.commit()
            self.__session.close()
            return 200
        except Exception as error:
            print(error)
            return 400