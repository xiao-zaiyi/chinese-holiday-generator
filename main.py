import uuid
import datetime
from datetime import timedelta


def get_holiday_status(date_str, holidays_data):
    """
    获取日期的假期状态
    返回:
        0 - 工作日
        1 - 周末
        2 - 补班日
        3 - 法定节假日
    """
    # 检查是否在节假日数据中
    for day in holidays_data['days']:
        if day['date'] == date_str:
            return 2 if not day['isOffDay'] else 3
    return None


def print_special_days(holidays_data):
    print("\n补班日期（status=2）：")
    for day in holidays_data['days']:
        if not day['isOffDay']:
            print(f"{day['date']} ({day['name']}补班)")

    print("\n法定节假日（status=3）：")
    for day in holidays_data['days']:
        if day['isOffDay']:
            print(f"{day['date']} ({day['name']})")


def generate_calendar_2025():
    # https://github.com/NateScarlet/holiday-cn/blob/master/2025.json
    # 节假日数据
    holidays_data = {
        "year": 2025,
        "days": [
            {"name": "元旦", "date": "2025-01-01", "isOffDay": True},
            {"name": "春节", "date": "2025-01-26", "isOffDay": False},
            {"name": "春节", "date": "2025-01-28", "isOffDay": True},
            {"name": "春节", "date": "2025-01-29", "isOffDay": True},
            {"name": "春节", "date": "2025-01-30", "isOffDay": True},
            {"name": "春节", "date": "2025-01-31", "isOffDay": True},
            {"name": "春节", "date": "2025-02-01", "isOffDay": True},
            {"name": "春节", "date": "2025-02-02", "isOffDay": True},
            {"name": "春节", "date": "2025-02-03", "isOffDay": True},
            {"name": "春节", "date": "2025-02-04", "isOffDay": True},
            {"name": "春节", "date": "2025-02-08", "isOffDay": False},
            {"name": "清明节", "date": "2025-04-04", "isOffDay": True},
            {"name": "清明节", "date": "2025-04-05", "isOffDay": True},
            {"name": "清明节", "date": "2025-04-06", "isOffDay": True},
            {"name": "劳动节", "date": "2025-04-27", "isOffDay": False},
            {"name": "劳动节", "date": "2025-05-01", "isOffDay": True},
            {"name": "劳动节", "date": "2025-05-02", "isOffDay": True},
            {"name": "劳动节", "date": "2025-05-03", "isOffDay": True},
            {"name": "劳动节", "date": "2025-05-04", "isOffDay": True},
            {"name": "劳动节", "date": "2025-05-05", "isOffDay": True},
            {"name": "端午节", "date": "2025-05-31", "isOffDay": True},
            {"name": "端午节", "date": "2025-06-01", "isOffDay": True},
            {"name": "端午节", "date": "2025-06-02", "isOffDay": True},
            {"name": "国庆节、中秋节", "date": "2025-09-28", "isOffDay": False},
            {"name": "国庆节、中秋节", "date": "2025-10-01", "isOffDay": True},
            {"name": "国庆节、中秋节", "date": "2025-10-02", "isOffDay": True},
            {"name": "国庆节、中秋节", "date": "2025-10-03", "isOffDay": True},
            {"name": "国庆节、中秋节", "date": "2025-10-04", "isOffDay": True},
            {"name": "国庆节、中秋节", "date": "2025-10-05", "isOffDay": True},
            {"name": "国庆节、中秋节", "date": "2025-10-06", "isOffDay": True},
            {"name": "国庆节、中秋节", "date": "2025-10-07", "isOffDay": True},
            {"name": "国庆节、中秋节", "date": "2025-10-08", "isOffDay": True},
            {"name": "国庆节、中秋节", "date": "2025-10-11", "isOffDay": False}
        ]
    }

    # 先打印特殊日期
    print_special_days(holidays_data)

    start_date = datetime.date(2025, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    current_date = start_date

    sql_statements = []

    while current_date <= end_date:
        id = str(uuid.uuid4()).replace('-', '')[:19]
        year = current_date.year
        month = current_date.month
        day = current_date.day
        week = current_date.isoweekday()
        date_str = current_date.strftime('%Y-%m-%d')

        # 获取假期状态
        holiday_status = get_holiday_status(date_str, holidays_data)
        if holiday_status is not None:
            status = holiday_status
        else:
            # 如果不是特殊节假日，则判断是否为周末
            status = 1 if week in [6, 7] else 0

        sql = f"INSERT INTO tb_calendar VALUES ('{id}', '{date_str}', {year}, {month}, {day}, {status}, {week});"
        sql_statements.append(sql)

        current_date += timedelta(days=1)

    with open('calendar_2025.sql', 'w', encoding='utf-8') as f:
        for sql in sql_statements:
            f.write(sql + '\n')


if __name__ == '__main__':
    generate_calendar_2025()
    print("\n数据生成完成，已保存到 calendar_2025.sql")