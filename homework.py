from __future__ import annotations
import datetime as dt
from typing import List


class Record:
    """Запись для калькулятора."""

    def __init__(self, amount: int, comment: str, date=None) -> None:
        self.amount = amount
        self.comment = comment
        if date:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.datetime.today().date()


class Calculator(Record):
    """Базовый класс калькулятора."""

    def __init__(self, limit) -> None:
        self.limit = limit
        self.records = []  #type:List

    def add_record(self, record):
        self.records.append(record)

    def date_count(self) -> int:
        date_cnt = []
        for record in self.records:
            date_cnt.append(record)
            date_counted = len(date_cnt)
        return date_counted

    def get_today_stats(self):
        sum_today = []
        today = dt.datetime.today().date()
        for record in self.records:
            if record.date == today:
                sum_today.append(record.amount)
        return sum(sum_today)

    def remained(self):
        remain = self.limit - self.get_today_stats()
        return remain

    def get_week_stats(self):
        week_stats = []
        week_ago = dt.datetime.today().date() - dt.timedelta(days=7)
        for record in self.records:
            if week_ago <= record.date <= dt.datetime.today().date():
                week_stats.append(record.amount)
        return sum(week_stats)


class CashCalculator(Calculator):
    EURO_RATE = 70.0
    RUB_RATE = 1
    USD_RATE = 60.0

    def get_today_cash_remained(self, currency):

        cur_dic = {
            'rub': [CashCalculator.RUB_RATE, 'руб'],
            'usd': [CashCalculator.USD_RATE, 'USD'],
            'eur': [CashCalculator.EURO_RATE, 'Euro'], }
        today_calc_list = []
        for record in self.records:
            if record.date == dt.date.today():
                today_calc_list.append(record.amount)
        if sum(today_calc_list) < self.limit:
            today_calc = self.limit - sum(today_calc_list)
            today_calc = round((today_calc / cur_dic[currency][0]), 2)
            return f'На сегодня осталось {today_calc} {cur_dic[currency][1]}'
        elif sum(today_calc_list) == self.limit:
            return 'Денег нет, держись'
        else:
            today_calc = sum(today_calc_list) - self.limit
            today_calc = round((today_calc / cur_dic[currency][0]), 2)
            return (f'Денег нет, держись: твой долг - '
                    f'{today_calc} {cur_dic[currency][1]}')


class CaloriesCalculator(Calculator):

    def __init__(self, limit: float):
        super().__init__(limit)

    def get_calories_remained(self):
        calories_remained = self.remained()
        if calories_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_remained} кКал')
        return 'Хватит есть!'


cash_calculator = CashCalculator(1000)

# дата в параметрах не указана, так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=100, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=200, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('rub'))
print(cash_calculator.get_today_stats())
print(cash_calculator.get_week_stats())
# должно напечататься.
# На сегодня осталось 555 руб.
