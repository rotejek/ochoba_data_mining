import json

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper


class ParseUserData:
    def __init__(self):
        config = ConfigLoader.load()
        self.db = DataBaseWrapper(config["db"])

    def parse(self):
        page_size = 500
        page = 0
        while True:
            print("Fetch page #{0} ({1})".format(page, page_size * page))
            result = self.db.execute_select(
                """
                    select json from users
                        order by id
                        limit %s offset %s
                """,
                (page_size, page_size * page)
            )
            if len(result) == 0:
                break

            for row in result:
                user_data = json.loads(row[0])["result"]
                self.db.execute_update(
                    """
                        update users
                            set
                                created = to_timestamp(%s),
                                name = %s,
                                type = %s,
                                karma = %s,
                                is_plus = %s,
                                is_verified = %s,
                                is_available_for_messenger = %s,
                                entries_count = %s,
                                comments_count = %s,
                                favorites_count = %s,
                                subscribers_count = %s
                            where id = %s
                    """,
                    (user_data["created"], user_data["name"], user_data["type"], user_data["karma"],
                     user_data["is_plus"], user_data["is_verified"], user_data["isAvailableForMessenger"],
                     user_data["counters"]["entries"], user_data["counters"]["comments"],
                     user_data["counters"]["favorites"], user_data["subscribers_count"],
                     user_data["id"])
                )

            page += 1
            self.db.commit()


if __name__ == "__main__":
    ParseUserData().parse()
