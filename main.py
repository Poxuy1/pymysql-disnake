import disnake
from disnake.ext import commands
import datetime
import pytz
import pymysql
import sys

host = 'localhost'
user = 'root'
password = 'root'
db_name = 'dbname'

bot = commands.Bot(command_prefix='!', help_command=None, intents=disnake.Intents.all())

@bot.event
async def on_ready():
	global connection, cs
	try:
		connection = pymysql.connect(
			host=host,
			port=3306,
			user=user,
			password=password,
			database=db_name,
			cursorclass=pymysql.cursors.DictCursor
		)
		cs = connection.cursor()

	except Exception as ex:
		print(f'Database {db_name} given error. Close connection...\n{ex}')
		
		print('Connection close.')

		sys.exit()

	createtable = "CREATE TABLE IF NOT EXISTS `users`(ownerid BIGINT, lvl INT, xp INT, balance INT)"
	cs.execute(createtable)

	connection.commit()

	try:
		for guild in bot.guilds:
			for member in guild.members:
				if member.bot:
					pass
				elif cs.execute(f'SELECT ownerid FROM `users` WHERE ownerid = {member.id}') == 0:
					cs.execute(f"INSERT INTO `users` (`ownerid`, `lvl`, `xp`, `balance`) VALUES ('{member.id}', '1', '0', '0')")
					connection.commit()
				else:
					pass


		print('Database is connection.')
		pctime = datetime.datetime.today().replace(microsecond=0)
		print(f'Local pc/host time: {pctime}')
		tzmoscow = pytz.timezone('Europe/Moscow')
		moscowtime = datetime.datetime.now(tzmoscow).replace(tzinfo=None, microsecond=0)
		print(f'Europe, Moscow time - {moscowtime}')

		print(f'\/ discord \/ bot \/ \nfull ready for work.')
	except Exception as ex:
		print(f'Error.\n{ex}')

		print('Close db, progam...')

		connection.close()

		await bot.close()

		sys.exit()

bot.run("yourtoken")