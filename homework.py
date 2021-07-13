import datetime as dt

date_format = '%d.%m.%Y'


class Record:
    """Запись для калькулятора."""

    def __init__(self, amount: int, comment: str, date=None) -> None:
        self.amount = amount
        self.comment = comment
        if date:
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            self.date = dt.datetime.today().date()


class Calculator(Record):
    """Базовый класс калькулятора."""

    def __init__(self, limit) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.datetime.today().date()
        return sum(record.amount for record in self.records
                   if record.date == today
                   )

    def remained(self):
        remain = self.limit - self.get_today_stats()
        return remain

    def get_week_stats(self):
        week_ago = dt.datetime.today().date() - dt.timedelta(days=7)
        today = dt.datetime.today().date()
        return sum(
                  record.amount for record in self.records
                  if week_ago <= record.date <= today
                  )


class CashCalculator(Calculator):
    EURO_RATE = 70.0
    RUB_RATE = 1
    USD_RATE = 60.0
    CUR_DIC = {
              'rub': (RUB_RATE, 'руб'),
              'usd': (USD_RATE, 'USD'),
              'eur': (EURO_RATE, 'Euro'), }

    def get_today_cash_remained(self, currency):
        rate, name = CashCalculator.CUR_DIC[currency]
        if self.get_today_stats() < self.limit:
            today_calc = self.limit - self.get_today_stats()
            today_calc = round(
                              (today_calc / rate), 2)
            return (f'На сегодня осталось '
                    f'{today_calc} {name}')
        elif self.get_today_stats() == self.limit:
            return 'Денег нет, держись'
        today_calc = self.get_today_stats() - self.limit
        today_calc = round(
                          (today_calc / rate), 2)
        return (
               'Денег нет, держись: твой долг - '
               f'{today_calc} {name}'
               )


class CaloriesCalculator(Calculator):

    def __init__(self, limit: float):
        super().__init__(limit)

    def get_calories_remained(self):
        calories_remained = self.remained()
        if calories_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_remained} кКал')
        return 'Хватит есть!'
