import sqlite3 as sq
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect("test_db.db")
    cur = base.cursor()
    if base:
        print("база подключена")
    base.execute("CREATE TABLE IF NOT EXISTS data(img TEXT, name TEXT PRIMARY KEY)")
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO data VALUES (?, ?)", tuple(data.values()))
        base.commit()


async def test_zag_pol(message):
    for ret in cur.execute("SELECT * FROM data").fetchall():
        await bot.send_photo(message.chat.id, ret[0], f"Что я написал к этой картинке: {ret[1]}")


async def sql_read2():
    return cur.execute("SELECT * from data").fetchall()


async def sql_delete_command(data):
    cur.execute("DELETE FROM data WHERE name == ?", (data,))
    base.commit()
