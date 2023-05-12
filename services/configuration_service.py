from lib import BaseService
from lib.base_database import Session

from database_models.configuration import Configuration


class ConfigurationService(BaseService):
    
    __session = Session()

    async def get_configurations(self) -> list[dict[str, str | bool | int]] | int:
        try:
            query = self.__session.query(Configuration).all()
            content = []
            for result in query:
                content.append({
                    "id": result.id,
                    "id_user": result.id_user,
                    "active": result.active,
                    "clean_recycle_bin": result.clean_recycle_bin,
                    "clean_temp": result.clean_temp,
                    "clean_browsers": result.clean_browsers
                })
            return content
        except Exception as error:
            return 400

    async def set_configuration(self, request) -> int:
        try:
            data = request
            old_configuration = self.__session.query(Configuration).filter_by(id=1).first()
            if old_configuration:
                old_configuration.active = data["active"]
                old_configuration.clean_recycle_bin = data["clean_recycle_bin"]
                old_configuration.clean_temp = data["clean_temp"]
                old_configuration.clean_browsers = data["clean_browsers"]
            else:
                new_configuration = Configuration(
                    id=data["id"],
                    id_user=1,
                    active=data["active"],
                    clean_recycle_bin=data["clean_recycle_bin"],
                    clean_temp=data["clean_temp"],
                    clean_browsers=data["clean_browsers"]
                )
                self.__session.add(new_configuration)
            self.__session.commit()
            self.__session.close()
            return 200
        except Exception as error:
            return 400