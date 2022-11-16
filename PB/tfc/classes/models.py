from django.db import models
from django.db.models import CASCADE
from studios.models import Studio
from accounts.models import TFCUser
import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
import dateutil.relativedelta as rd
import calendar
from .exceptions import AlreadyEnrolledException, FullCapacityException, NotSubscribedException, \
    TargetInPastException
from subscriptions.models import has_active_subscription
from django.shortcuts import get_object_or_404

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

    def delete_future_instances(self):
        today = datetime.date.today()
        class_instances = self.classinstance_set.filter(date__gte=today)
        class_instances.delete()

    def enroll_user(self, user):
        # check for subscription
        if not has_active_subscription(user.id):
            raise NotSubscribedException
        enrolled_classes = []
        # future occurrences
        today = datetime.date.today()
        future_class_instances = self.classinstance_set.filter(date__gte=today)
        for class_instance in future_class_instances:
            try:
                enrolled_class = class_instance.enroll_user(user)
                enrolled_classes.append(enrolled_class)
            except Exception:
                # ignore these
                pass
        return enrolled_classes


# https://stackoverflow.com/questions/1355150/when-saving-how-can-you-check-if-a-field-has-changed
@receiver(pre_save, sender=ClassOffering)
def handle_recursion_date_change(sender, instance, **kwargs):
    try:
        old_obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Object is new, so we do nothing
        return
    if not old_obj.end_recursion_date == instance.end_recursion_date:
        # field has changed
        old_recursion_date = old_obj.end_recursion_date
        new_recursion_date = instance.end_recursion_date
        if new_recursion_date > old_recursion_date:
            # gen new class instances
            for time_interval in instance.timeinterval_set.all():
                earliest_new_instance_date = old_recursion_date + rd.relativedelta(days=1)
                time_interval.generate_future_class_instances(earliest_new_instance_date)
            pass
        elif new_recursion_date < old_recursion_date:
            for time_interval in instance.timeinterval_set.all():
                time_interval.delete_instances_after_date(new_recursion_date)


class TimeInterval(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE)

    def delete_instances_after_date(self, exclusive_date):
        """

        Args:
            exclusive_date:  EXCLUSIVE date to delete after


        """

        self.classinstance_set.filter(date__gt=exclusive_date).delete()

    def generate_future_class_instances(self, start_date):
        """

        Args:
            start_date: INCLUSIVE start date (if time is correct) to start generating future class instances from

        Returns:

        """
        offering = self.class_offering
        end_recursion_date = offering.end_recursion_date
        next_class_date = get_next_weekday(start_date, self.day)
        class_instances = []
        while next_class_date <= end_recursion_date:
            class_instance = ClassInstance(date=next_class_date, class_offering=offering,
                                           time_interval=self)
            class_instances.append(class_instance)
            next_class_date += rd.relativedelta(days=7)
        ClassInstance.objects.bulk_create(class_instances)

    def clear_class_instances(self):
        self.classinstance_set.all().delete()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.clear_class_instances()
        self.generate_future_class_instances(datetime.date.today())


# https://stackoverflow.com/questions/13014411/django-post-save-signal-implementation


class Keyword(models.Model):
    keyword = models.CharField(max_length=200, null=False)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE)


class ClassInstance(models.Model):
    date = models.DateField()
    capacity_count = models.PositiveIntegerField(default=0, null=False)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE)
    time_interval = models.ForeignKey(to=TimeInterval, on_delete=CASCADE)

    def __str__(self):
        return f"pk: {self.pk}, date: {self.date}, capacity: {self.capacity_count}"

    def user_enrolled(self, user):
        return self.userenroll_set.filter(user=user).exists()

    def enroll_user(self, user):
        # check that it is in the future
        if self.date <= datetime.date.today():
            raise TargetInPastException
        # check for subscription
        if not has_active_subscription(user.id):
            raise NotSubscribedException
        if self.capacity_count == self.class_offering.capacity:
            raise FullCapacityException
        if self.user_enrolled(user):
            raise AlreadyEnrolledException
        self.capacity_count += 1
        user_enroll = UserEnroll.objects.create(class_instance=self,
                                                class_offering=self.class_offering, user=user)
        user_enroll.save()
        self.save()

        return self


class UserEnroll(models.Model):
    class_instance = models.ForeignKey(to=ClassInstance, on_delete=CASCADE)
    class_offering = models.ForeignKey(to=ClassOffering, on_delete=CASCADE)
    user = models.ForeignKey(to=TFCUser, on_delete=CASCADE)

    def unenroll(self):
        """

        Returns: True if successfully unenrolled, false if the capacity is already at 0

        """

        if self.class_offering.capacity == 0:
            return False
        self.class_instance.capacity -= 1
        self.class_instance.save()
        self.delete()
