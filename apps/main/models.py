from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    balance = models.IntegerField(default=19990)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    type_choices = (
        (1, 'User'),
        (2, 'Owner'),
        (3, 'Speaking admin'),
        (4, 'Writing admin'),
    )
    type = models.IntegerField(choices=type_choices, default=1)
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)


    status_choices = (
        (1, 'Free'),
        (2, 'Testing'),
        (3, 'Speaking'),
    )
    status = models.IntegerField(choices=status_choices, default=1)
    is_active = models.BooleanField(default=True)
    referrals = models.IntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    # Add a related_name argument to the groups field to resolve the clash
    groups = models.ManyToManyField(Group, related_name='users', blank=True,
                                    help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.")

    # Add a related_name argument to the user_permissions field to resolve the clash
    user_permissions = models.ManyToManyField(
        Permission, related_name='users', blank=True, help_text='Specific permissions for this user.')


    def __str__(self):
        return self.first_name


class Listening_section(models.Model):
    img = models.ImageField(upload_to='test/sections/listening/')
    img2 = models.ImageField(upload_to='test/sections/listening/', null=True, blank=True)
    img3 = models.ImageField(upload_to='test/sections/listening/', null=True, blank=True)
    question_numbers = models.IntegerField()
    questions = models.ManyToManyField('Listening_question')
    audio = models.FileField(upload_to='test/sections/listening/')

    part_choices = (
        (1, 'Part 1'),
        (2, 'Part 2'),
        (3, 'Part 3'),
        (4, 'Part 4'),
    )
    part = models.IntegerField(choices=part_choices)


class Listening_question(models.Model):
    order = models.IntegerField()
    right_answer = models.CharField(max_length=255)
    right_answer2 = models.CharField(max_length=255, blank=True, null=True)
    right_answer3 = models.CharField(max_length=255, blank=True, null=True)
    right_answer4 = models.CharField(max_length=255, blank=True, null=True)
    right_answer5 = models.CharField(max_length=255, blank=True, null=True)

    type_choices = (
        (1, 'Multiple choice'),
        (2, 'Matching'),
        (3, 'Map'),
        (4, 'Filling blank'),
        (5, 'Sentence completion'),
    )
    type = models.IntegerField(choices=type_choices)


class Listening_answer(models.Model):
    question = models.ForeignKey(Listening_question, on_delete=models.PROTECT)
    user_answer = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_checked = models.BooleanField(default=False)


class Listening_test(models.Model):
    test_section = models.ManyToManyField(Listening_section)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, null=True, blank=True)
    band_score = models.IntegerField()


class Reading_section(models.Model):
    img = models.ImageField(upload_to='test/sections/reading/')
    img2 = models.ImageField(upload_to='test/sections/reading/', null=True, blank=True)
    img3 = models.ImageField(upload_to='test/sections/reading/', null=True, blank=True)
    img4 = models.ImageField(upload_to='test/sections/reading/', null=True, blank=True)
    img5 = models.ImageField(upload_to='test/sections/reading/', null=True, blank=True)
    question_numbers = models.IntegerField()
    questions = models.ManyToManyField('Reading_question')
    part_choices = (
        (1, 'Part 1'),
        (2, 'Part 2'),
        (3, 'Part 3'),
    )
    part = models.IntegerField(choices=part_choices)


class Reading_question(models.Model):
    order = models.IntegerField()
    right_answer = models.CharField(max_length=255)
    right_answer2 = models.CharField(max_length=255, blank=True, null=True)
    right_answer3 = models.CharField(max_length=255, blank=True, null=True)
    right_answer4 = models.CharField(max_length=255, blank=True, null=True)
    right_answer5 = models.CharField(max_length=255, blank=True, null=True)

    type_choices = (
        (1, 'Multiple choice'),
        (2, 'Matching'),
        (3, 'Map'),
        (4, 'Filling blank'),
        (5, 'Sentence completion'),
        (6, 'Yes_no'),
        (7, 'True_false'),
    )
    type = models.IntegerField(choices=type_choices)


class Reading_answer(models.Model):
    question = models.ForeignKey(Reading_question, on_delete=models.PROTECT)
    user_answer = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_checked = models.BooleanField(default=False)



class Reading_test(models.Model):
    test_section = models.ManyToManyField(Reading_section)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, null=True, blank=True)
    band_score = models.FloatField()


class Writing_section(models.Model):
    img = models.ImageField(upload_to='writing/imgs/')
    # question = models.CharField(max_length=255)

    type_choices = (
        (1, 'Task 1'),
        (2, 'Task 2'),
    )
    type = models.IntegerField(choices=type_choices)


class Writing_answer(models.Model):
    question = models.ForeignKey(Writing_section, on_delete=models.PROTECT)
    user_answer = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_checked = models.BooleanField(default=False)


class Writing_test(models.Model):
    live_section = models.ManyToManyField(Writing_section)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, null=True, blank=True)
    band_score = models.FloatField()
    is_sent = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


class Speaking_section(models.Model):
    img = models.ImageField(upload_to='speaking/imgs/')
    # question = models.CharField(max_length=255)

    type_choices = (
        (1, 'Part 1'),
        (2, 'Part 2'),
        (3, 'Part 3'),
    )   
    type = models.IntegerField(choices=type_choices)


class Speaking_test(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, null=True, blank=True)
    audio = models.FileField(upload_to='test/speaking/')
    band_score = models.FloatField()
    is_sent = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


class Full_test(models.Model):
    listening = models.ForeignKey(Listening_test, on_delete=models.PROTECT)
    reading = models.ForeignKey(Reading_test, on_delete=models.PROTECT)
    writing = models.ForeignKey(Writing_test, on_delete=models.PROTECT)
    speaking = models.ForeignKey(Speaking_test, on_delete=models.PROTECT)
    band_score = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    date_joined = models.DateTimeField(auto_now_add=True)



class Result(models.Model):
    full_test = models.ForeignKey(Full_test, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    band_score = models.FloatField()


class Test_Details(models.Model):
    price1 = models.IntegerField()
    price2 = models.IntegerField()
    price4 = models.IntegerField()
    price10 = models.IntegerField()
    ref_price = models.IntegerField()
    bot_token = models.CharField(max_length=255)