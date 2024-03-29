from lib import BaseService
from lib.base_database import Session

from models.history import History


class HistoryService(BaseService):

    __session = Session()

    async def get_history(self) -> list[dict[str, str | bool | int]] | int:
        try:
            query = self.__session.query(History).all()
            content = []
            for result in query:
                content.append({
                    "id": result.id,
                    "id_configuration": result.id_configuration,
                    "deleted": result.deleted,
                    "state": result.state,
                    "message_error": result.message_error,
                    "date": result.date
                }
            )
            return content

        except Exception:
            return 400

    async def set_history(self, data):
        old_history = self.__session.query(History).filter_by(id=1).first()
        if old_history:
            pass
        else:
            new_History = History(
            id_configuration=1,
            deleted=data["deleted"],
            state=data["state"],
            message_error=data["message_error"],
            date=data["date"]
        )
            self.__session.add(new_History)
        self.__session.commit()
        self.__session.close()
