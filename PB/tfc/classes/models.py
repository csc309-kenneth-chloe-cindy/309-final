from django.db import models
from django.db.models import CASCADE
from studios.models import Studio
from accounts.models import TFCUser
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
import dateutil.relativedelta as rd
import calendar

# based on https://stackoverflow.com/questions/5966629/django-days-of-week-representation-in-model
DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


def get_next_weekday(date, day_num):
    """

    Args:
        date:
        day_num: Expects the day field from the DB


    """
    relativedelta = None
    match day_num:
        case 0:
            relativedelta = rd.relativedelta(days=0, weekday=calendar.MONDAY)
        case 1:
            relativedelta = rd.relativedelta(days=0, weekday=calendar.TUESDAY)
        case 2:
            relativedelta = rd.relativedelta(days=0, weekday=calendar.WEDNESDAY)
        case 3:
            relativedelta = rd.relativedelta(days=0, weekday=calendar.THURSDAY)
        case 4:
            relativedelta = rd.relativedelta(days=0, weekday=calendar.FRIDAY)
        case 5:
            relativedelta = rd.relativedelta(days=0, weekday=calendar.SATURDAY)
        case 6:
            relativedelta = rd.relativedelta(days=0, weekday=calendar.FRIDAY)
    return date + relativedelta


class DateTimeInterval():
    def __init__(self, date, start, end):
        self.date = date
        self.start = start
        self.end = end

    def __str__(self):
        return f"date is: {self.date}, start time is {self.start}, end time is {self.end}"


class ClassOffering(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=False)
    coach = models.CharField(max_length=200, null=False)
    capacity = models.PositiveIntegerField(null=False)
    end_recursion_date = models.DateField()
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE)

    def _get_offset_by_weekday(self, day):
        # TODO: delete
        # This is just to make the relation explicit
        return day

    def _get_class_dates_for_this_week(self) -> list[DateTimeInterval]:
        # TODO: delete
        time_intervals = self.timeinterval_set.all()
        print(time_intervals)
        today = datetime.date.today()
        start = today - datetime.timedelta(days=today.weekday())
        end = start + datetime.timedelta(days=6)

        date_time_intervals = []

        for time_interval in time_intervals:
            date = start + datetime.timedelta(days=self._get_offset_by_weekday(time_interval.day))
            date_time_intervals.append(
                DateTimeInterval(date, time_interval.start_time, time_interval.end_time))
        return date_time_intervals

    def generate_initial_class_instances(self):
        # TODO: delete
        print("RUNNING GENERATE INITIAL")
        date_time_intervals = self._get_class_dates_for_this_week()
        end_recursion_date = self.end_recursion_date
        today = datetime.date.today()
        now = datetime.datetime.now().time()
        for date_time_interval in date_time_intervals:
            print(date_time_interval)
        generate = False

        class_instances = []

        while generate:
            for date_time_interval in date_time_intervals:
                class_instance = None
                if date_time_interval > end_recursion_date:
                    generate = False
                    continue
                if today == date_time_interval:
                    if date_time_interval.start > now:
                        class_instance = ClassInstance(date=date_time_interval.date,
                                                       class_offering=self)
                elif today < date_time_interval.date:
                    class_instance = ClassInstance(date=date_time_interval.date,
                                                   class_offering=self)
                class_instances.append(class_instance)
                date_time_interval.date = date_time_interval.date + datetime.timedelta(days=7)
        ClassInstance.objects.bulk_create(class_instances)


class TimeInterval(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE)

    def generate_future_class_instances(self, start_date):
        offering = self.class_offering
        end_recursion_date = offering.end_recursion_date
        next_class_date = get_next_weekday(start_date, self.day)
        class_instances = []
        while next_class_date <= end_recursion_date:
            class_instance = ClassInstance(date=next_class_date, class_offering=offering)
            class_instances.append(class_instance)
            next_class_date += rd.relativedelta(days=7)
        ClassInstance.objects.bulk_create(class_instances)


# https://stackoverflow.com/questions/13014411/django-post-save-signal-implementation

@receiver(post_save, sender=TimeInterval)
def create_instances(sender, instance, **kwargs):
    print("RUNNING ON MODEL LEVEL")
    instance.generate_future_class_instances(datetime.date.today())


class Keyword(models.Model):
    keyword = models.CharField(max_length=200, null=False)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE)


class ClassInstance(models.Model):
    date = models.DateField()
    capacity_count = models.PositiveIntegerField(default=0, null=False)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE,
                                       related_name='class_offering')

    def __str__(self):
        return f"pk: {self.pk}, date: {self.date}, capacity: {self.capacity_count}"


class UserEnroll(models.Model):
    class_instance = models.ForeignKey(to=ClassInstance, on_delete=CASCADE)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE)
    user = models.ForeignKey(to=TFCUser, on_delete=CASCADE)
