import aiomysql

import constants

from log import logger


class Manager:
    db_poll = None

    @classmethod
    async def get_pool(cls):
        return await aiomysql.create_pool(**constants.db_config)

    @classmethod
    async def start(cls):
        cls.db_poll = await cls.get_pool()

    @classmethod
    async def machine(cls, place, start_date, end_date, login):
        conn = await cls.db_poll.acquire()
        logger.debug(f"conn: {conn}")

        try:
            pre_sql = f"USE {constants.db_name}"
            sql = f"""
                    SELECT m.timestamp, m.value, m.kind, u.login, p.place, m.id
                    FROM movement m
                    LEFT JOIN user u ON m.id_user = u.id
                    LEFT JOIN place p ON m.id_user = p.id_user
                    WHERE p.place = %s
                    AND u.login = %s
                    AND m.timestamp BETWEEN %s AND %s
                    ORDER BY m.timestamp DESC;
                """

            cursor = await conn.cursor()
            await cursor.execute(pre_sql)

            await cursor.execute(sql, (place, login, start_date, end_date))
            records = await cursor.fetchall()

        finally:
            cls.db_poll.release(conn)

        return records

    @classmethod
    async def move(cls, place, start_date, end_date, login):
        conn = await cls.db_poll.acquire()
        logger.debug(f"conn: {conn}")

        try:
            pre_sql = f"USE {constants.db_name}"
            sql = f"""
                        SELECT b.timestamp,b.id_match,b.id_game,b.credit, b.value, b.kind, u.login,u.counter_in,u.counter_out
                        FROM balance b
                        JOIN place p ON b.id_user = p.id_user
                        JOIN user u ON b.id_user = u.id
                        WHERE u.login = %s
                        AND b.timestamp BETWEEN %s AND %s
                        AND p.place = %s
                        ORDER BY b.timestamp DESC;
                   """

            cursor = await conn.cursor()
            await cursor.execute(pre_sql)

            await cursor.execute(sql, (login, start_date, end_date, place))
            records = await cursor.fetchall()

        finally:
            cls.db_poll.release(conn)

        return records


