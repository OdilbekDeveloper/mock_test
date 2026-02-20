# from django.contrib import admin
# from .models import *
# # Register your models here.
#
# admin.site.register(User)
# admin.site.register(Listening_section)
# admin.site.register(Listening_question)
# admin.site.register(Listening_answer)
# admin.site.register(Listening_test)
# admin.site.register(Reading_section)
# admin.site.register(Reading_question)
# admin.site.register(Reading_answer)
# admin.site.register(Reading_test)
# admin.site.register(Writing_section)
# admin.site.register(Writing_test)
# admin.site.register(Writing_answer)
# admin.site.register(Speaking_test)
# admin.site.register(Speaking_section)
# admin.site.register(Full_test)
# admin.site.register(Test_Details)


from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(WebTest)
admin.site.register(WebSection)
admin.site.register(WebQuestion)
admin.site.register(WebAttempt)
admin.site.register(WebUserAnswer)
admin.site.register(WritingSubmission)
admin.site.register(SpeakingSubmission)
