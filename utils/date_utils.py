import datetime
import time

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"


class MyDateUtils:

    # 当前毫秒数
    @staticmethod
    def cur_milis():
        return int(time.time() * 1000)


    # 当前秒数
    @staticmethod
    def cur_seconds():
        return int(time.time())


    # 当前日期 格式%Y-%m-%d %H:%M:%S
    @staticmethod
    def cur_datetime():
        return datetime.datetime.strftime(datetime.datetime.now(), DATETIME_FORMAT)


    # 当前日期 格式%Y-%m-%d
    @staticmethod
    def cur_date():
        return datetime.date.today()


    # 当前时间 格式%Y-%m-%d
    @staticmethod
    def cur_time():
        return time.strftime(TIME_FORMAT)


    # 秒转日期
    @staticmethod
    def seconds_to_datetime(seconds):
        return time.strftime(DATETIME_FORMAT, time.localtime(seconds))


    # 毫秒转日期
    @staticmethod
    def milis_to_datetime(milix):
        return time.strftime(DATETIME_FORMAT, time.localtime(milix//1000))


    # 日期转毫秒
    @staticmethod
    def datetime_to_milis(datetimestr):
        strf = time.strptime(datetimestr, DATETIME_FORMAT)
        return int(time.mktime(strf)) * 1000


    # 日期转秒
    @staticmethod
    def datetime_to_seconds(datetimestr):
        strf = time.strptime(datetimestr, DATETIME_FORMAT)
        return int(time.mktime(strf))


    # 当前年
    @staticmethod
    def cur_year():
        return datetime.datetime.now().year


    # 当前月
    @staticmethod
    def cur_month():
        return datetime.datetime.now().month


    # 当前日
    @staticmethod
    def cur_day():
        return datetime.datetime.now().day


    # 当前时
    @staticmethod
    def cur_hour():
        return datetime.datetime.now().hour


    # 当前分
    @staticmethod
    def cur_minute():
        return datetime.datetime.now().minute


    # 当前秒
    @staticmethod
    def cur_second():
        return datetime.datetime.now().second


    # 星期几
    @staticmethod
    def cur_week():
        return datetime.datetime.now().weekday()


    # 几天前的时间
    @staticmethod
    def now_days_ago(days):
        daysAgoTime = datetime.datetime.now() - datetime.timedelta(days=days)
        return time.strftime(DATETIME_FORMAT, daysAgoTime.timetuple())


    # 几天后的时间
    @staticmethod
    def now_days_after(days):
        daysAgoTime = datetime.datetime.now() + datetime.timedelta(days=days)
        return time.strftime(DATETIME_FORMAT, daysAgoTime.timetuple())


    # 某个日期几天前的时间
    @staticmethod
    def dtime_days_ago(dtimestr, days):
        daysAgoTime = datetime.datetime.strptime(dtimestr, DATETIME_FORMAT) - datetime.timedelta(days=days)
        return time.strftime(DATETIME_FORMAT, daysAgoTime.timetuple())


    # 某个日期几天前的时间
    @staticmethod
    def dtime_days_after(dtimestr, days):
        daysAgoTime = datetime.datetime.strptime(dtimestr, DATETIME_FORMAT) + datetime.timedelta(days=days)
        return time.strftime(DATETIME_FORMAT, daysAgoTime.timetuple())


def main():
    secondStamp = MyDateUtils.cur_seconds()
    print("当前秒：", secondStamp)
    milisStamp = MyDateUtils.cur_milis()
    print("当前毫秒：", milisStamp)

    curdTime = MyDateUtils.cur_datetime()
    print("当前时间：", curdTime)
    curDate = MyDateUtils.cur_date()
    print("当前日期：", curDate)
    curT = MyDateUtils.cur_time()
    print("当前时刻：", curT)

    stdtime = MyDateUtils.seconds_to_datetime(secondStamp)
    print("秒转时间：", stdtime)
    mtdtime = MyDateUtils.seconds_to_datetime(milisStamp)
    print("毫秒转时间：", mtdtime)
    dtimetm = MyDateUtils.milis_to_datetime(mtdtime)
    print("时间转毫秒：", dtimetm)
    dtimets = MyDateUtils.datetime_to_milis(mtdtime)
    print("时间转秒：", dtimets)

    year = MyDateUtils.cur_year()
    print("年：", year)
    month = MyDateUtils.cur_month()
    print("月：", month)
    day = MyDateUtils.cur_day()
    print("日：", day)
    hour = MyDateUtils.cur_hour()
    print("时：", hour)
    minute = MyDateUtils.cur_minute()
    print("分：", minute)
    second = MyDateUtils.cur_second()
    print("秒：", second)
    week = MyDateUtils.cur_week()
    print("星期：", week)



if __name__ == "__main__":
    main()