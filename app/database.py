import aiosqlite
import asyncio


class AsyncDB:
    def __init__(self, db_path):
        self.db_path = db_path

    async def do(self, query, params=None):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.cursor() as cursor:
                if params:
                    await cursor.execute(query, params)
                else:
                    await cursor.execute(query)
                await db.commit()

    async def read(self, query, params=None, fetchone=False):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.cursor() as cursor:
                if params:
                    await cursor.execute(query, params)
                else:
                    await cursor.execute(query)

                if fetchone:
                    result = await cursor.fetchone()
                else:
                    result = await cursor.fetchall()

                return result


class RegexDB(AsyncDB):
    def __init__(self, db_path):
        super().__init__(db_path)
        asyncio.run(self.create_db())

    async def create_db(self):
        await self.do(""" 
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                lang TEXT NOT NULL,
                name TEXT NOT NULL,
                registration_date TEXT NOT NULL
            );""")
        await self.do("""
            CREATE TABLE IF NOT EXISTS pattern(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT NOT NULL,
                flag TEXT NOT NULL DEFAULT 'default',
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id)
            );""")

    # region user
    async def add_user(self, user_id, name, lang, registration_date):
        await self.do(
            "INSERT INTO user (id, name, lang, registration_date) VALUES (?, ?, ?, ?)",
            (user_id, name, lang, registration_date),
        )

    async def user_exists(self, user_id):
        return bool(
            await self.read(
                "SELECT * FROM user WHERE id = ?", (user_id,), fetchone=True
            )
        )

    async def get_lang(self, user_id):
        return (
            await self.read(
                "SELECT lang FROM user WHERE id = ?", (user_id,), fetchone=True
            )
        )[0]

    async def change_lang(self, user_id, lang):
        await self.do("UPDATE user SET lang = ? WHERE id = ?", (lang, user_id))

    # endregion
    # region pattern
    async def add_pattern(self, pattern, user_id):
        await self.do(
            "INSERT INTO pattern (pattern, user_id) VALUES (?, ?)",
            (pattern, user_id),
        )

    async def delete_pattern(self, pattern_id):
        await self.do("DELETE FROM pattern WHERE id = ?", (pattern_id,))

    async def add_flag(self, pattern_id, flag):
        await self.do("UPDATE pattern SET flag = ? WHERE id = ?", (flag, pattern_id))

    async def get_flag(self, pattern_id):
        return (
            await self.read(
                "SELECT flag FROM pattern WHERE id = ?", (pattern_id,), fetchone=True
            )
        )[0]

    async def get_patterns(self, user_id):
        return await self.read(
            "SELECT pattern, id FROM pattern WHERE user_id = ?", (user_id,)
        )

    async def get_pattern(self, pattern_id):
        return (
            await self.read(
                "SELECT pattern FROM pattern WHERE id = ?",
                (pattern_id,),
                fetchone=True,
            )
        )[0]

    # endregion
