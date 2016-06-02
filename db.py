from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Time

metadata = MetaData()

table_today = Table(
    'today', metadata,
    Column('id', Integer, primary_key=True),
    Column('timestamp', Integer),
    Column('date', Date),
    Column('time', Time),
    Column('host', String(length=255)),
    Column('customer', String(length=255)),
    Column('service', String(length=255)),
    Column('target', String(length=255)),
    Column('result', String(length=255)),
    Column('message', String(length=255)),
)

table_archive = Table(
    'archive', metadata,
    Column('id', Integer, primary_key=True),
    Column('timestamp', Integer),
    Column('date', Date),
    Column('time', Time),
    Column('host', String(length=255)),
    Column('customer', String(length=255)),
    Column('service', String(length=255)),
    Column('target', String(length=255)),
    Column('result', String(length=255)),
    Column('message', String(length=255)),
)
