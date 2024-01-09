from apps.main.models import *
# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " " + str(self.amount)



