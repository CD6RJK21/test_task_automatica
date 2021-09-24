from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlalchemy
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import json
import pymysql.cursors
from sqlalchemy.sql.expression import update


'''
программа читает конфиги, если файл конфигурации присутствует 
или создаёт его со значениями по умолчанию в противном случае
'''
if os.path.exists('config.json'):
    with open('config.json', encoding='utf-8') as config_file:
        config = json.load(config_file)
else:
    config = {'API_TOKEN': "2038454997:AAHeUbpr3Y-13U9LJh5obGtyqkwhaZsF_rg",
     'how_old_question': 'сколько лет?', 'place_of_birth_question': 'где родился?',
     'advice_start': 'чтобы начать сначала нажми /start', 'mysql_username': 'root',
     'mysql_password': '1234'}
    with open('config.json', 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=4)

# инициализация бота
API_TOKEN = config['API_TOKEN']
bot = Bot(token=API_TOKEN, timeout=100)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# подключение к базе данных MySQL
try:
    engine = sqlalchemy.create_engine('mysql+pymysql://{}:{}@127.0.0.1/test_base'.format(config['mysql_username'], config['mysql_password']), echo=True)
    engine.connect()
    base = declarative_base()
except sqlalchemy.exc.OperationalError as oe:
    connection = pymysql.connect(host='localhost',
                             user=config['mysql_username'],
                             password=config['mysql_password'])

    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute('create database test_base')

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    engine = sqlalchemy.create_engine('mysql+pymysql://{}:{}@127.0.0.1/test_base'.format(config['mysql_username'], config['mysql_password']), echo=True)
    engine.connect()
    base = declarative_base()


class TestUsers(base):
    __tablename__ = 'test_base'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.Integer)
    address = sqlalchemy.Column(sqlalchemy.Text)


    def __init__(self, user_id, date, address):
        self.user_id = user_id
        self.date = date
        self.address = address

    def __repr__(self):
        return '{}|{}|{}'.format(str(self.user_id), self.date, self.address)


Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
base.metadata.create_all(engine)
session.commit()


class CreateUser(StatesGroup):
    waiting_for_date = State()
    waiting_for_address = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await CreateUser.waiting_for_date.set()
    await message.answer(config['how_old_question'])
    


@dp.message_handler(state=CreateUser.waiting_for_date)
async def process_date(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        state = dp.get_current().current_state()
        await state.update_data(date=int(message.text))
        await CreateUser.next()
        await message.answer(config['place_of_birth_question'])
    else:
        await message.answer('Возраст - это натуральное число!')
    


@dp.message_handler(state=CreateUser.waiting_for_address)
async def process_address(message: types.Message, state: FSMContext):
    state = dp.get_current().current_state()
    user_data = await state.get_data()
    print(user_data.get('date'))
    if session.query(TestUsers).filter_by(user_id=message.chat.id).first() is None:
            session.add(TestUsers(message.chat.id, user_data.get('date'), message.text))
            session.commit()
    else:
        session.execute(update(TestUsers).where(TestUsers.user_id == message.chat.id).values(date=user_data.get('date'), address=message.text))
        session.commit()
    await state.finish()
    await advice_start(message)


@dp.message_handler(lambda message: message.text)
async def advice_start(message: types.Message):
    await message.answer(config['advice_start'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, timeout=100)