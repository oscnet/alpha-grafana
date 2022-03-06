from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column
from sqlalchemy.types import Integer,String,Date,DateTime,Float,Text


def new_table(_table_name, _data_base):
    """hh"""

    Base = declarative_base(bind=_data_base)

    class table(Base):

        """hh"""

        __tablename__ = _table_name

        time = Column(DateTime, primary_key=True, nullable=True)
        f_usdt_balance = Column(Float, nullable=True, default="")
        account = Column(String(10), nullable=True, default="")
        initial_day = Column(DateTime, nullable=True)
        initial_cash = Column(Float, nullable=True, default="")
        hold_hour = Column(String(10), nullable=True, default="")
        max_down = Column(Float, nullable=True, default="")

    Base.metadata.create_all()

    return None
