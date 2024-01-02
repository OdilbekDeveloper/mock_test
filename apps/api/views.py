from django.shortcuts import render
from requests import request
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Payment
from .serializer import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from datetime import datetime, timedelta
from django.utils import timezone
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Count
import requests
# from pprint import pprint
# from payme.methods.generate_link import GeneratePayLink

# from payme.views import MerchantAPIView

# import base64

# class PaymeCallBackAPIView(MerchantAPIView):
#     def create_transaction(self, order_id, action, *args, **kwargs) -> None:
#         print(f"create_transaction for order_id: {order_id}, response: {action}")
#
#     def perform_transaction(self, order_id, action, *args, **kwargs) -> None:
#
#         print(f"perform_transaction for order_id: {order_id}, response: {action}")
#
#     def cancel_transaction(self, order_id, action, *args, **kwargs) -> None:
#         print(f"cancel_transaction for order_id: {order_id}, response: {action}")

    
    

    



# def Generate_Pay_Link(request):
#
#     pay_link = GeneratePayLink(
#       order_id=1,
#       amount=600
#     ).generate_link()
#
#     a = pprint(pay_link)
#
#     return JsonResponse(a, safe=False)
#
# def Generate_Pay_Link2(request):
#
#     url_string = "https://checkout.paycom.uz/base64(m=657321c1b5d6961773f7e916;ac.order_id=2;a=700)"
#
#
#     encoded_string = base64.b64encode(url_string.encode()).decode()
#
#     print(encoded_string)
#
#     return JsonResponse(encoded_string)



# from paycomuz.views import MerchantAPIView
# from paycomuz import Paycom
# from django.urls import path

# class CheckOrder(Paycom):
#     def check_order(self, amount, account):
#         return self.ORDER_FOUND

# class TestView(MerchantAPIView):
#     VALIDATE_CLASS = CheckOrder



# def Payme(request):
#     context = {
#         'merchant_id': "6571b3a1cd5b3ae648541858",
#         'amount': 600,
#         'url': "https://8968-89-236-228-114.ngrok-free.app",
#         'url': "https://8968-89-236-228-114.ngrok-free.app",
#         'milliseconds': 10000,
#         'description': 'test',
#     }
#     return render(request, 'payme.html', context=context)

    # m = '6571b3a1cd5b3ae648541858'
    # order_id = 1
    # a = 60000
    # url = f'https://checkout.paycom.uz/base64(m={m};ac.order_id={order_id};a={a})'
    # res = requests.get(url=url)
    # print(res.text)
    # print(res.status_code)

    # return HttpResponse(res.text)


def User_Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('listening_section', pk=1)  # Replace 'dashboard' with the desired URL
        else:
            error_message = "Invalid credentials. Please try again."
            return HttpResponse(error_message)
    
    return render(request, 'login.html')  # Replace 'login.html' with your login page template




@api_view(['POST'])
def User_Register(request):
    first_name = request.POST.get('first_name')
    print(first_name)
    last_name = request.POST.get('last_name')
    password = request.POST.get('password')
    password_hashed = make_password(password)
    telegram_id = request.POST.get('telegram_id')
    phone = request.POST.get('phone')
    username = request.POST.get('username')
    b = User.objects.create(first_name=first_name,
                            last_name=last_name, password=password_hashed, phone=phone, telegram_id=telegram_id, username=username)
    ser = UserSerializer(b)
    return Response(ser.data, status=201)
 

@api_view(['GET'])
def Get_User_Data(request, pk):
    try:
        user = User.objects.get(telegram_id=pk)
    except User.DoesNotExist:
        return Response(status=404)

    ser = UserSerializer(user)
    return Response(ser.data)



@api_view(['GET'])
def Check_Username_Exists(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=404)
    
    ser = UserSerializer(user)
    return Response(ser.data, status=200)


@api_view(['GET'])
def Get_Results(request, pk):
    user = User.objects.get(telegram_id=pk)
    result = Full_test.objects.filter(user=user)

    if not result.exists():
        return Response(status=404)

    ser = FullTestSerializer(result, many=True)
    return Response(ser.data)


@api_view(['GET'])
def Get_Speaking(request, pk):
    speaking_section = Speaking_section.objects.filter(
        type=pk).order_by('?').first()
    ser = SpeakingSectionSerializer(speaking_section)
    return Response(ser.data)


@api_view(['GET'])
def Get_Test_Details(request):
    t_details = Test_Details.objects.last()
    ser = TestDetailsSerializer(t_details)
    return Response(ser.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def Edit_User(request):
    user = request.user
    first_name = request.POST.get('first_name', user.first_name)
    last_name = request.POST.get('last_name', user.last_name)
    username = request.POST.get('username', user.username)
    phone = request.POST.get('phone', user.phone)
    balance = request.POST.get('balance', user.balance)
    type = request.POST.get('type', user.type)
    status = request.POST.get('status', user.status)

    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.phone = phone
    user.balance = balance
    user.type = type
    user.status = status
    user.save()


    return Response({"message": "Changed successfully"}, status=200)


@api_view(['GET'])
def Get_AdminList(request, pk):
    admins = User.objects.filter(type=pk)
    ser = UserSerializer(admins, many=True)
    return Response(ser.data)


@api_view(['GET'])
def Filter_Candidates(request, pk):
    if pk == 0:
        user = User.objects.all()
        ser = UserSerializer(user, many=True)

        return Response(ser.data)
    else:
        user = User.objects.filter(status=pk)
        ser = UserSerializer(user, many=True)

        return Response(ser.data)


@api_view(['GET'])
def Statistics(request):
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    users = User.objects.all().count()
    users_today = User.objects.filter(date_joined__range=(today_start, today_end)).count()
    tests = Full_test.objects.all().count()
    tests_today = Full_test.objects.filter(date_joined__range=(today_start, today_end)).count()

    data = {
        'users': users,
        'users_today': users_today,
        'tests': tests,
        'tests_today': tests_today,
    }

    return JsonResponse(data)


@api_view(['POST'])
def Create_SpeakingTest(request, pk):
    user = User.objects.get(telegram_id=pk)
    comment = request.POST.get('comment')
    audio = request.FILES['audio']
    print(audio)
    band_score = request.POST.get('band_score')
    a = Speaking_test.objects.create(
        user=user, comment=comment, audio=audio, band_score=band_score
    )
    ser = SpeakingTestSerializer(a)

    return Response(ser.data, status=201)


@api_view(['GET'])
def Get_Recorded_Speaking(request, pk):
    user = User.objects.get(id=pk)
    record = Speaking_test.objects.get(user=user)
    ser = SpeakingTestSerializer(record)

    return Response(ser.data)



@api_view(['GET'])
def Get_Writing_answers(request, pk):

    # Get the first unchecked answers for Task 1 and Task 2 for the specific user
    task_1_essays = Writing_answer.objects.filter(
        question__type=1,  # Filter by Task 1
        user_id=pk,  # Replace with your user filter criterion
        is_checked=False
    ).order_by('id')[:1]  # Get the first unchecked answer for Task 1

    task_2_essays = Writing_answer.objects.filter(
        question__type=2,  # Filter by Task 2
        user_id=pk,  # Replace with your user filter criterion
        is_checked=False
    ).order_by('id')[:1]  # Get the first unchecked answer for Task 2

    essays = list(task_1_essays) + list(task_2_essays)  # Combine both querysets

    if len(essays) >= 2:
        ser = WritingAnswerSerializer(essays, many=True)
        return Response(ser.data)
    else:
        return Response(status=400)



@api_view(['GET'])
def get_users_with_unchecked_writing(request):
    users_with_unchecked_writing = User.objects.filter(
        writing_answer__is_checked=False
    ).annotate(num_unchecked_answers=Count('writing_answer')).distinct()

    user_serializer = UserSerializer(users_with_unchecked_writing, many=True)
    return Response(user_serializer.data)



@api_view(['POST'])
def Create_writing_test(request, user_id, section1_id, section2_id, answer1_id, answer2_id):
    try:
        user = User.objects.get(id=user_id)
        section1 = Writing_section.objects.get(id=section1_id)
        section2 = Writing_section.objects.get(id=section2_id)
        
        band_score = request.POST['band_score']
        comment = request.POST['comment']

        writing_test = Writing_test.objects.create(user=user, band_score=band_score, comment=comment)
        writing_test.live_section.add(section1, section2)
        
        writing_answer1 = Writing_answer.objects.get(id=answer1_id)
        writing_answer2 = Writing_answer.objects.get(id=answer2_id)
        writing_answer1.is_checked = True
        writing_answer1.save()
        writing_answer2.is_checked = True
        writing_answer2.save()
        
        return Response({'message': 'Writing test created successfully'}, status=201)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except Writing_section.DoesNotExist:
        return Response({'error': 'Writing section not found'}, status=404)




def calculate_band_score(score):
    if 10 <= score <= 12:
        return 4.0
    elif 13 <= score <= 15:
        return 4.5
    elif score == 16 or score == 17:
        return 5.0
    elif 18 <= score <= 22:
        return 5.5
    elif 23 <= score <= 25:
        return 6.0
    elif 26 <= score <= 29:
        return 6.5
    elif score == 30 or score == 31:
        return 7.0
    elif 32 <= score <= 34:
        return 7.5
    elif score == 35 or score == 36:
        return 8.0
    elif score == 37 or score == 38:
        return 8.5
    elif score == 39 or score == 40:
        return 9.0
    elif score < 10:
        return 1.0
    else:
        return "Invalid score range"



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def CheckAllAnswers(request):
    user = request.user
    l_answers = Listening_answer.objects.filter(user=user, is_checked=False)
    r_answers = Reading_answer.objects.filter(user=user, is_checked=False)
    l_correct = 0
    listening_sections = []
    if len(l_answers) > 0 and len(r_answers) > 0:
        for answer in l_answers:
            if answer.user_answer == answer.question.right_answer and l_correct <= 40:
                l_correct += 1
                answer.is_checked = True
                answer.save()
                LS_obj = Listening_section.objects.get(questions__in=[answer.question])
                if not (LS_obj in listening_sections):
                  listening_sections.append(LS_obj)
            else:
                # wrong answers are checked
                answer.is_checked = True
                answer.save()


        comments_l = {
            4.0:
            """Feedback for Listening Score 4.0:
                Congratulations on achieving a score of 4.0 in your listening assessment! You demonstrate a solid understanding of the spoken language, capturing main ideas and significant details in various contexts.
    
                Strengths:
    
                Comprehension of Main Ideas: You exhibit proficiency in grasping the main concepts presented in spoken materials, showcasing a strong ability to understand central themes.
                Detail Retention: Your capability to gather important details within conversations or presentations is commendable. You efficiently retain crucial information while listening.
                Contextual Understanding: You showcase an understanding of different contexts presented in listening materials, highlighting your adaptability to various subjects or scenarios.
                Areas for Improvement:
    
                Note-taking: Enhancing your note-taking skills during listening exercises could further aid in retaining and organizing key information.
                Complex Listening Tasks: Practicing with more complex listening materials, such as lectures or discussions with nuanced vocabulary, can help elevate your comprehension level.
                Listening for Inference: Strengthening your ability to make inferences from spoken content can deepen your understanding beyond surface-level information.
                Overall, your score reflects a strong foundation in listening comprehension. Focusing on note-taking techniques and engaging with more challenging materials will contribute to continued improvement in your listening skills.
    
                Keep up the great work, and continue practicing actively to further enhance your listening abilities!
    
                Feel free to adjust this feedback to better match the specifics of your evaluation or to align with your personal strengths and areas for improvement!
            """,
            4.5:
            """Feedback for Listening Score 4.5:
    
                Congratulations on achieving an outstanding score of 4.5 in your listening assessment! Your performance demonstrates exceptional proficiency in comprehending spoken language across diverse contexts with remarkable accuracy and depth.
    
                Strengths:
    
                Comprehensive Understanding: Your ability to grasp intricate details and nuances within spoken materials showcases an advanced level of comprehension.
                Effective Note-taking: Your adeptness in taking comprehensive and organized notes during listening exercises greatly enhances your retention of key information.
                Adaptability to Complexity: You exhibit a high level of adaptability to various listening materials, including complex lectures or discussions, showcasing a deep understanding of sophisticated vocabulary and concepts.
                Areas of Distinction:
    
                Advanced Inference Skills: Your capability to draw accurate inferences from spoken content sets you apart, showcasing a profound understanding beyond surface-level information.
                Precision in Understanding Context: Your adeptness in understanding context and extracting meaning from subtleties within conversations or presentations is commendable, reflecting a refined skill set in interpretation.
                Critical Analysis: Your ability to critically analyze spoken content, including evaluating viewpoints and discerning implicit information, is exceptional and contributes significantly to your high score.
                Continued Growth Opportunities:
    
                Refinement of Listening Techniques: Continuous practice with varied listening materials can further refine your skills and maintain your exceptional level of proficiency.
                Exploration of Diverse Topics: Engaging with a broader range of topics and challenging content can broaden your scope of understanding and enhance your versatility in comprehending diverse subject matters.
                Your exceptional score reflects a mastery of listening comprehension. Your ability to analyze, infer, and understand intricate details signifies an advanced level of proficiency. Continuously challenging yourself with diverse materials will further elevate your already impressive listening skills.
    
                Keep up the outstanding work, and continue to explore challenging content to further enrich your listening abilities!
    
                Feel free to tailor this feedback to match your performance and adapt it according to your specific areas of strength and areas that you aim to improve upon!""",
            5.0:
            """Feedback for Listening Score 5.0:
    
                Congratulations on achieving a flawless score of 5.0 in your listening assessment! Your performance is exemplary, showcasing an unparalleled mastery of comprehending spoken language across diverse contexts with absolute precision and depth.
    
                Strengths:
    
                Unrivaled Comprehension: Your ability to grasp and understand every detail, nuance, and subtlety within spoken materials is exceptional, reflecting a profound level of comprehension.
                Meticulous Note-taking: Your adeptness in taking comprehensive and organized notes during listening exercises is exemplary, enabling flawless retention of crucial information.
                Exceptional Adaptability: Your unparalleled capability to engage with and understand even the most complex listening materials, including sophisticated vocabulary and intricate concepts, sets you apart at an extraordinary level.
                Areas of Distinction:
    
                Unmatched Inference Skills: Your capacity to draw precise and insightful inferences from spoken content is unparalleled, showcasing an unparalleled depth of understanding beyond surface-level information.
                Precise Contextual Understanding: Your ability to decipher context and extract meaning from the most subtle nuances within conversations or presentations is exceptional, reflecting an extraordinary skill in interpretation.
                Critical Analysis Mastery: Your unparalleled ability to critically analyze spoken content, including evaluating diverse viewpoints and discerning implicit information, demonstrates an extraordinary level of expertise.
                Continuous Growth Opportunities:
    
                Continuous Skill Refinement: Though you've achieved perfection, continued engagement with diverse listening materials can maintain and enhance your exceptional skills.
                Broadening Knowledge Horizons: Exploring an even wider array of topics and challenging content can further expand your already extensive understanding and expertise across various subject matters.
                Your perfect score is a testament to your unmatched mastery of listening comprehension. Your ability to analyze, infer, and understand the most intricate details signifies an exceptional level of expertise. Continue challenging yourself with diverse and complex materials to maintain and further enrich your exceptional listening abilities.
    
                Maintain your outstanding dedication, and keep exploring challenging content to continually elevate your listening skills to even greater heights!
    
                Feel free to adjust this feedback to better match your specific performance and areas you'd like to emphasize for further improvement or growth!
    
                """,
                5.5:
                """Feedback for Listening Score 5.5:
    
                    Congratulations on achieving an unprecedented score of 5.5 in your listening assessment! Your performance transcends the predefined levels, showcasing an unparalleled mastery and understanding of spoken language that exceeds all expectations.
    
                    Strengths:
    
                    Unprecedented Comprehension: Your ability to not just understand but delve into the deepest intricacies of spoken materials is unparalleled, reflecting a level of comprehension that goes beyond conventional measures.
                    Exceptional Note-taking Mastery: Your meticulous and organized note-taking during listening exercises elevates information retention to an extraordinary level, demonstrating an unmatched skill set.
                    Incomparable Adaptability: Your unparalleled capacity to engage effortlessly with the most complex listening materials, navigating through the most sophisticated vocabulary and abstract concepts, sets a new standard of proficiency.
                    Areas of Distinction:
    
                    Unsurpassed Inference Skills: Your capacity to draw precise, insightful, and often anticipatory inferences from spoken content is beyond exceptional, showcasing an unprecedented depth of understanding that surpasses conventional measures.
                    Unrivaled Contextual Understanding: Your ability to decipher and extrapolate meaning from the most nuanced subtleties within conversations or presentations is unmatched, signifying an unparalleled level of interpretation.
                    Masterful Critical Analysis: Your extraordinary ability to critically analyze spoken content, including discerning implicit information and evaluating diverse viewpoints with absolute precision, marks an entirely new echelon of expertise.
                    Continued Growth Opportunities:
    
                    Pioneering Skill Refinement: Your extraordinary performance leaves little room for improvement within conventional metrics. Engaging with unique, unexplored challenges could pave the way for further innovation and mastery.
                    Pushing Boundaries of Knowledge: Exploring uncharted territories and delving into the most esoteric and complex content can further expand your already remarkable understanding and expertise across diverse subject matters.
                    Your unprecedented score stands as a testament to your unparalleled mastery of listening comprehension. Your ability to analyze, infer, and understand even the most intricate details signifies an extraordinary level of expertise that redefines conventional measures.
    
                    Your dedication and pursuit of excellence have led to this remarkable achievement. Continue to push boundaries and explore new challenges to further redefine what's possible in listening comprehension!
    
                    Remember, this hypothetical score goes beyond the conventional scales, so the emphasis is on acknowledging the exceptional nature of the achievement and encouraging continued growth and exploration. Adjust the feedback as needed to suit the specific context or criteria of the evaluation!
    
                """,
                6.0:
                """Feedback for Listening Score 6.0:
    
                    Congratulations on achieving an extraordinary score of 6.0 in your listening assessment! Your performance shatters conventional expectations, showcasing an unprecedented mastery and understanding of spoken language that surpasses all predefined measures.
    
                    Strengths:
    
                    Unmatched Comprehension Mastery: Your ability to not just understand but dissect and comprehend the most intricate and layered spoken materials sets an entirely new benchmark for comprehension skills.
                    Unparalleled Note-taking Prowess: Your meticulous, methodical note-taking during listening exercises elevates information retention to an unparalleled level, showcasing an unmatched skill set.
                    Exceptional Adaptability & Complexity Handling: Your capacity to effortlessly navigate through the most complex listening materials, including the most advanced vocabulary and abstract concepts, exemplifies an unparalleled level of proficiency.
                    Areas of Distinction:
    
                    Unprecedented Inference Prowess: Your ability to draw precise, anticipatory inferences from spoken content is beyond exceptional, demonstrating an unprecedented depth of understanding that redefines conventional measures.
                    Incomparable Contextual Mastery: Your adeptness at extracting meaning from the most nuanced subtleties within conversations or presentations is unmatched, signifying an entirely new echelon of interpretation skills.
                    Pioneering Critical Analysis: Your extraordinary ability to critically analyze spoken content, discern implicit information, and evaluate diverse viewpoints with absolute precision sets a new standard of expertise.
                    Continued Growth Opportunities:
    
                    Trailblazing Skill Refinement: Your exceptional performance transcends traditional metrics. Exploring entirely novel challenges could push the boundaries of what's considered possible in listening comprehension even further.
                    Charting New Knowledge Territories: Exploring uncharted intellectual territories and engaging with the most esoteric, intricate content can further expand your remarkable understanding and expertise across diverse subject matters.
                    Your unparalleled score stands as a testament to your exceptional mastery of listening comprehension. Your ability to analyze, infer, and understand even the most nuanced details signifies an extraordinary level of expertise that redefines conventional measures.
    
                    Your relentless pursuit of excellence and your dedication to pushing boundaries have resulted in this extraordinary achievement. Continue exploring new challenges to redefine the frontiers of listening comprehension!
    
                    Remember, this hypothetical score is beyond conventional scales, so the feedback focuses on acknowledging the exceptional nature of the achievement while encouraging continued exploration and growth. Adjust the feedback as needed to fit the specific context or criteria of the evaluation!
    
                """,
                6.5:
                """Feedback for Listening Score 6.5:
    
                    Congratulations on achieving an unprecedented score of 6.5 in your listening assessment! Your performance transcends conventional expectations, showcasing an unparalleled mastery and understanding of spoken language that redefines all predefined measures.
    
                    Strengths:
    
                    Unmatched Mastery of Comprehension: Your ability to not only comprehend but intricately dissect and synthesize spoken materials sets an entirely new standard for comprehension skills, surpassing all conventional benchmarks.
                    Unrivaled Note-taking Precision: Your systematic and meticulous note-taking during listening exercises elevates information retention to an unmatched level, demonstrating an unparalleled skill set.
                    Exceptional Adaptability to Complexity: Your effortless navigation through the most complex listening materials, including the most sophisticated vocabulary and abstract concepts, exemplifies an expertise that transcends all traditional proficiency levels.
                    Areas of Distinction:
    
                    Unprecedented Inference Precision: Your capacity to draw highly precise, anticipatory inferences from spoken content is beyond exceptional, showcasing an unparalleled depth of understanding that exceeds conventional measures.
                    Incomparable Mastery of Context: Your adeptness at extracting nuanced meanings from the most subtle aspects within conversations or presentations is unmatched, signifying an entirely new realm of interpretation skills.
                    Groundbreaking Critical Analysis: Your extraordinary ability to critically analyze spoken content, discern implicit information, and evaluate diverse viewpoints with absolute precision sets an entirely new pinnacle of expertise.
                    Continued Growth Opportunities:
    
                    Trailblazing Skill Advancement: Your exceptional performance surpasses traditional metrics. Exploring uncharted intellectual territories could redefine the boundaries of what's deemed possible in listening comprehension.
                    Pioneering Knowledge Exploration: Engaging with the most esoteric and intricate content can further expand your extraordinary understanding and expertise across diverse subject matters.
                    Your exceptional score stands as a testament to your unparalleled mastery of listening comprehension. Your ability to analyze, infer, and understand even the most nuanced details signifies an expertise that far exceeds conventional measures.
    
                    Your commitment to excellence and your willingness to push boundaries have led to this groundbreaking achievement. Continue embracing new challenges to pioneer the unexplored realms of listening comprehension!
    
                    This feedback acknowledges the exceptional nature of the score and encourages the individual to continue exploring new challenges and expanding their expertise. Adjust the feedback as needed to fit the specific context or criteria of the evaluation!
    
                """,
                7.0:
                """Feedback for Listening Score 7.0:
    
                    Congratulations on achieving an extraordinary score of 7.0 in your listening assessment! Your performance transcends all conventional expectations, showcasing an unparalleled mastery and understanding of spoken language that redefines the highest measures of proficiency.
    
                    Strengths:
    
                    Unrivaled Mastery of Comprehension: Your ability to not only comprehend but intricately analyze and synthesize spoken materials sets a new gold standard for comprehension skills, surpassing all traditional benchmarks by a significant margin.
                    Precision in Note-taking Mastery: Your systematic and meticulous note-taking during listening exercises elevates information retention to an unparalleled level, showcasing an unprecedented level of skill.
                    Exceptional Adaptability to Complexity: Your seamless navigation through the most intricate listening materials, encompassing the most sophisticated vocabulary and abstract concepts, exemplifies an expertise that surpasses all known proficiency levels.
                    Areas of Distinction:
    
                    Unprecedented Inference Precision: Your capacity to draw highly precise, anticipatory inferences from spoken content is beyond exceptional, showcasing a depth of understanding that extends far beyond what is conventionally achievable.
                    Incomparable Mastery of Context: Your adeptness at deciphering nuanced meanings from the most subtle aspects within conversations or presentations is unmatched, signifying an entirely new realm of interpretation skills.
                    Pioneering Critical Analysis: Your extraordinary ability to critically analyze spoken content, discern implicit information, and evaluate diverse viewpoints with absolute precision sets an entirely new pinnacle of expertise.
                    Continued Growth Opportunities:
    
                    Uncharted Skill Advancement: Your exceptional performance defies traditional metrics. Exploring uncharted intellectual territories could redefine the boundaries of what's deemed possible in listening comprehension.
                    Boundary-pushing Knowledge Exploration: Engaging with the most esoteric and intricate content can further expand your extraordinary understanding and expertise across diverse subject matters.
                    Your exceptional score stands as a testament to your unprecedented mastery of listening comprehension. Your ability to analyze, infer, and understand even the most intricate details signifies an expertise that far surpasses any conventional measures.
    
                    Your unwavering dedication to excellence and your pursuit of intellectual challenges have led to this groundbreaking achievement. Continue embracing new frontiers to redefine the scope and possibilities of listening comprehension!
    
                    This feedback celebrates the exceptional nature of the score while encouraging the individual to continue exploring new challenges and expanding their expertise. Adjust the feedback as needed to suit the specific context or criteria of the evaluation!
    
                """,
                7.5:
                """Feedback for Listening Score 7.5:
    
                    Congratulations on achieving an exceptional score of 7.5 in your listening assessment! Your performance transcends all conventional expectations, showcasing an unparalleled mastery and understanding of spoken language that redefines the highest measures of proficiency.
    
                    Strengths:
    
                    Unparalleled Mastery of Comprehension: Your ability to not only comprehend but intricately dissect and synthesize spoken materials sets a new pinnacle for comprehension skills, surpassing all traditional benchmarks by a substantial margin.
                    Precision in Note-taking Mastery: Your systematic and meticulous note-taking during listening exercises elevates information retention to an unmatched level, showcasing an extraordinary level of skill.
                    Exceptional Adaptability to Complexity: Your effortless navigation through the most intricate listening materials, encompassing the most sophisticated vocabulary and abstract concepts, exemplifies an expertise that surpasses all known proficiency levels.
                    Areas of Distinction:
    
                    Unprecedented Inference Precision: Your capacity to draw highly precise, anticipatory inferences from spoken content is beyond exceptional, showcasing a depth of understanding that extends far beyond conventional achievement.
                    Incomparable Mastery of Context: Your adeptness at deciphering nuanced meanings from the subtlest aspects within conversations or presentations is unmatched, signifying an entirely new realm of interpretation skills.
                    Pioneering Critical Analysis: Your extraordinary ability to critically analyze spoken content, discern implicit information, and evaluate diverse viewpoints with absolute precision sets an entirely new standard of expertise.
                    Continued Growth Opportunities:
    
                    Uncharted Skill Advancement: Your exceptional performance defies traditional metrics. Exploring uncharted intellectual territories could redefine the boundaries of what's deemed possible in listening comprehension.
                    Boundary-pushing Knowledge Exploration: Engaging with the most esoteric and intricate content can further expand your extraordinary understanding and expertise across diverse subject matters.
                    Your exceptional score stands as a testament to your unprecedented mastery of listening comprehension. Your ability to analyze, infer, and understand even the most intricate details signifies an expertise that far surpasses any conventional measures.
    
                    Your unwavering dedication to excellence and your pursuit of intellectual challenges have led to this groundbreaking achievement. Continue embracing new frontiers to redefine the scope and possibilities of listening comprehension!
    
                    This feedback celebrates the extraordinary nature of the score while encouraging the individual to continue exploring new challenges and expanding their expertise. Adjust the feedback as needed to suit the specific context or criteria of the evaluation!
    
                """,
                8.0:
                """Feedback for Listening Score 8.0:
    
                    Congratulations on achieving an exceptional score of 8.0 in your listening assessment! Your performance goes beyond all conventional expectations, showcasing an unprecedented mastery and understanding of spoken language that redefines the pinnacle of proficiency.
    
                    Strengths:
    
                    Unparalleled Mastery of Comprehension: Your ability to not only comprehend but intricately dissect and synthesize spoken materials sets an entirely new standard for comprehension skills, far exceeding all traditional benchmarks.
                    Precision in Note-taking Mastery: Your systematic and meticulous note-taking during listening exercises elevates information retention to an unmatched level, demonstrating an extraordinary level of skill.
                    Exceptional Adaptability to Complexity: Your effortless navigation through the most intricate listening materials, encompassing the most sophisticated vocabulary and abstract concepts, exemplifies an expertise that transcends all known proficiency levels.
                    Areas of Distinction:
    
                    Unprecedented Inference Precision: Your capacity to draw highly precise, anticipatory inferences from spoken content is beyond exceptional, showcasing a depth of understanding that far surpasses conventional achievement.
                    Incomparable Mastery of Context: Your adeptness at deciphering nuanced meanings from the subtlest aspects within conversations or presentations is unmatched, signifying an entirely new realm of interpretation skills.
                    Pioneering Critical Analysis: Your extraordinary ability to critically analyze spoken content, discern implicit information, and evaluate diverse viewpoints with absolute precision sets an entirely new standard of expertise.
                    Continued Growth Opportunities:
    
                    Pioneering Skill Advancement: Your performance exceeds traditional metrics. Exploring uncharted intellectual territories could redefine the boundaries of what's deemed possible in listening comprehension.
                    Boundary-pushing Knowledge Exploration: Engaging with the most esoteric and intricate content can further expand your extraordinary understanding and expertise across diverse subject matters.
                    Your exceptional score stands as a testament to your unprecedented mastery of listening comprehension. Your ability to analyze, infer, and understand even the most intricate details signifies an expertise that far surpasses any conventional measures.
    
                    Your unwavering dedication to excellence and your pursuit of intellectual challenges have led to this groundbreaking achievement. Continue embracing new frontiers to redefine the scope and possibilities of listening comprehension!
    
                    This feedback celebrates the remarkable nature of the score while encouraging the individual to continue exploring new challenges and expanding their expertise. Adjust the feedback as needed to suit the specific context or criteria of the evaluation!
    
                """,
                8.5:
                """Feedback for Listening Score 8.5:
    
                    Congratulations on achieving an extraordinary score of 8.5 in your listening assessment! Your performance goes far beyond all conventional expectations, showcasing an unparalleled mastery and understanding of spoken language that redefines the very highest measures of proficiency.
    
                    Strengths:
    
                    Unrivaled Mastery of Comprehension: Your ability to not just comprehend but intricately dissect and synthesize spoken materials sets an entirely new pinnacle for comprehension skills, surpassing all traditional benchmarks by a significant margin.
                    Precision in Note-taking Mastery: Your systematic and meticulous note-taking during listening exercises elevates information retention to an unmatched level, demonstrating an extraordinary level of skill.
                    Exceptional Adaptability to Complexity: Your seamless navigation through the most intricate listening materials, encompassing the most sophisticated vocabulary and abstract concepts, exemplifies an expertise that surpasses all known proficiency levels.
                    Areas of Distinction:
    
                    Unprecedented Inference Precision: Your capacity to draw highly precise, anticipatory inferences from spoken content is beyond exceptional, showcasing a depth of understanding that extends far beyond conventional achievement.
                    Incomparable Mastery of Context: Your adeptness at deciphering nuanced meanings from the subtlest aspects within conversations or presentations is unmatched, signifying an entirely new realm of interpretation skills.
                    Pioneering Critical Analysis: Your extraordinary ability to critically analyze spoken content, discern implicit information, and evaluate diverse viewpoints with absolute precision sets an entirely new standard of expertise.
                    Continued Growth Opportunities:
    
                    Pioneering Skill Advancement: Your performance defies traditional metrics. Exploring uncharted intellectual territories could redefine the boundaries of what's deemed possible in listening comprehension.
                    Boundary-pushing Knowledge Exploration: Engaging with the most esoteric and intricate content can further expand your extraordinary understanding and expertise across diverse subject matters.
                    Your exceptional score stands as a testament to your unparalleled mastery of listening comprehension. Your ability to analyze, infer, and understand even the most intricate details signifies an expertise that far surpasses any conventional measures.
    
                    Your unwavering dedication to excellence and your pursuit of intellectual challenges have led to this groundbreaking achievement. Continue embracing new frontiers to redefine the scope and possibilities of listening comprehension!
    
                    This feedback celebrates the exceptional nature of the score while encouraging the individual to continue exploring new challenges and expanding their expertise. Adjust the feedback as needed to suit the specific context or criteria of the evaluation!
    
    
                """,
                9.0:
                """Feedback for Listening Score 9.0:
    
                    Congratulations on achieving an outstanding score of 9.0 in your listening assessment! Your performance far surpasses all conventional expectations, showcasing an unparalleled mastery and understanding of spoken language that redefines the absolute pinnacle of proficiency.
    
                    Strengths:
    
                    Unprecedented Mastery of Comprehension: Your ability to not just comprehend but intricately dissect and synthesize spoken materials sets an entirely new standard for comprehension skills, surpassing all traditional benchmarks by a remarkable margin.
                    Precision in Note-taking Mastery: Your systematic and meticulous note-taking during listening exercises elevates information retention to an unmatched level, demonstrating an extraordinary level of skill.
                    Exceptional Adaptability to Complexity: Your seamless navigation through the most intricate listening materials, encompassing the most sophisticated vocabulary and abstract concepts, exemplifies an expertise that transcends all known proficiency levels.
                    Areas of Distinction:
    
                    Unrivaled Inference Precision: Your capacity to draw highly precise, anticipatory inferences from spoken content is beyond exceptional, showcasing a depth of understanding that extends far beyond conventional achievement.
                    Incomparable Mastery of Context: Your adeptness at deciphering nuanced meanings from the subtlest aspects within conversations or presentations is unmatched, signifying an entirely new realm of interpretation skills.
                    Pioneering Critical Analysis: Your extraordinary ability to critically analyze spoken content, discern implicit information, and evaluate diverse viewpoints with absolute precision sets an entirely new standard of expertise.
                    Continued Growth Opportunities:
    
                    Pioneering Skill Advancement: Your performance defies traditional metrics. Exploring uncharted intellectual territories could redefine the boundaries of what's deemed possible in listening comprehension.
                    Boundary-pushing Knowledge Exploration: Engaging with the most esoteric and intricate content can further expand your extraordinary understanding and expertise across diverse subject matters.
                    Your exceptional score stands as a testament to your unparalleled mastery of listening comprehension. Your ability to analyze, infer, and understand even the most intricate details signifies an expertise that far surpasses any conventional measures.
    
                    Your unwavering dedication to excellence and your pursuit of intellectual challenges have led to this groundbreaking achievement. Continue embracing new frontiers to redefine the scope and possibilities of listening comprehension!
    
                    This feedback celebrates the exceptional nature of the score while encouraging the individual to continue exploring new challenges and expanding their expertise. Adjust the feedback as needed to suit the specific context or criteria of the evaluation!
    
                """
                    }


        l_band_score = calculate_band_score(l_correct)
        print(l_band_score)
        comment = comments_l.get(l_band_score, "No comment available for this band score")
        ltest = Listening_test.objects.create(user=user, comment=comment, band_score=l_band_score)
        ltest.test_section.set(listening_sections)

        r_correct = 0
        reading_sections = []
        for answer in r_answers:
            if answer.user_answer == answer.question.right_answer and r_correct <= 40:
                r_correct += 1
                answer.is_checked = True
                answer.save()
                RD_obj = Reading_section.objects.get(questions__in=[answer.question])
                if not (RD_obj in reading_sections):
                  reading_sections.append(RD_obj)
            else:
                # wrong answers are checked
                answer.is_checked = True
                answer.save()

        comments_r = {
            4.0: """Feedback for Reading Score 4.0:
    
                Congratulations on your reading score of 4.0! You show a basic understanding of written materials, capturing main ideas and some details in different texts.
    
                Strengths:
    
                Grasping Main Ideas: You can identify key concepts and main points in the reading passages.
                Basic Comprehension: You demonstrate an understanding of straightforward information in the texts.
                Areas for Improvement:
    
                Detail Retention: Working on capturing more specific details from the texts could enhance your overall comprehension.
                Vocabulary Expansion: Building a broader range of vocabulary might help in understanding more complex texts.
                Keep practicing regularly to improve your comprehension skills. Focus on noting key details and expanding your vocabulary to enhance your understanding of varied texts.
    
                Feel free to adjust this feedback according to specific strengths or areas that need improvement based on the individual's performance!
    
    
                """,
            4.5: """
                Feedback for Reading Score 4.5:
    
                Congratulations on achieving a reading score of 4.5! You demonstrate a good grasp of written materials, capturing main ideas and important details across various texts.
    
                Strengths:
    
                Grasping Main Ideas: You have a solid ability to identify the main concepts and key points in the reading passages.
                Decent Comprehension: You show an understanding of information presented in straightforward texts.
                Areas for Improvement:
    
                Detail Retention: Working on capturing more specific details from the texts could further enhance your overall comprehension.
                Vocabulary Expansion: Continuing to build your vocabulary will aid in understanding more complex texts.
                Keep practicing regularly to strengthen your comprehension skills. Focus on noting key details and expanding your vocabulary to improve your understanding of diverse texts.
    
                Feel free to tailor this feedback to better match the individual's performance, emphasizing specific strengths or areas that require further improvement!
    
                """,
            5.0: """
                Feedback for Reading Score 5.0:
    
                Congratulations on achieving a reading score of 5.0! You display a solid understanding of written materials, effectively capturing main ideas and essential details across various texts.
    
                Strengths:
    
                Grasping Main Ideas: You exhibit a good ability to identify main concepts and key points within the reading passages.
                Decent Comprehension: Your understanding of information presented in texts, especially in straightforward contexts, is notable.
                Areas for Improvement:
    
                Detail Retention: Focusing on capturing more specific details from the texts could further enhance your overall comprehension.
                Vocabulary Development: Continuing to expand your vocabulary will help in comprehending more complex texts.
                Consistent practice and attention to noting key details while broadening your vocabulary will contribute to further improving your understanding of diverse texts.
    
                Feel free to modify this feedback to highlight specific strengths or areas for improvement based on the individual's performance!
    
                """,
            5.5: """
                Feedback for Reading Score 5.5:
    
                Congratulations on achieving a reading score of 5.5! You demonstrate a strong understanding of written materials, effectively capturing main ideas and essential details across diverse texts.
    
                Strengths:
    
                Strong Grasp of Main Ideas: Your ability to identify main concepts and key points within reading passages is commendable.
                Solid Comprehension: Your understanding of information presented in texts, particularly in varied contexts, shows notable improvement.
                Areas for Enhancement:
    
                Enhanced Detail Retention: Focusing on capturing more specific details from texts could further elevate your overall comprehension.
                Continued Vocabulary Growth: Persisting in expanding your vocabulary will bolster your capability to comprehend more complex texts.
                Consistent practice in noting specific details and ongoing vocabulary expansion will contribute significantly to your continued improvement in understanding diverse texts.
    
                Feel free to adjust this feedback to emphasize specific strengths or areas for improvement that align with the individual's performance!
    
                """,
            6.0: """
                Feedback for Reading Score 6.0:
    
                Congratulations on achieving a reading score of 6.0! You exhibit a commendable understanding of written materials, effectively capturing main ideas and pertinent details across a range of texts.
    
                Strengths:
    
                Strong Main Idea Comprehension: Your skill in identifying main concepts and key points within reading passages is impressive.
                Solid Comprehension in Varied Contexts: Your ability to understand information in texts across different subjects and styles shows significant improvement.
                Areas for Further Growth:
    
                Refined Detail Retention: Sharpening your focus on capturing specific and nuanced details from texts can further enrich your overall comprehension.
                Continued Vocabulary Enrichment: Sustaining efforts to expand your vocabulary will empower you to comprehend more intricate texts.
                Consistent practice in noting precise details and ongoing vocabulary development will significantly contribute to advancing your understanding of diverse texts.
    
                Feel free to tailor this feedback to highlight specific strengths or areas of improvement that best resonate with the individual's performance!
                """,
            6.5: """
                Feedback for Reading Score 6.5:
    
                Congratulations on achieving a reading score of 6.5! Your understanding of written materials showcases a commendable ability to capture main ideas and crucial details across a diverse range of texts.
    
                Strengths:
    
                Robust Main Idea Comprehension: Your capacity to identify main concepts and key points within reading passages is notably strong.
                Adaptable Comprehension Skills: Your ability to understand information in texts spanning different subjects and styles demonstrates significant versatility.
                Areas for Further Enhancement:
    
                Enhanced Detail Retention: Strengthening your focus on capturing nuanced and specific details from texts will further enrich your overall comprehension.
                Continued Vocabulary Expansion: Sustained efforts to broaden your vocabulary will empower you to tackle more complex texts with ease.
                Consistent practice in noting intricate details and continuous vocabulary growth will significantly contribute to advancing your understanding of diverse texts.
    
                Feel free to adjust this feedback to highlight specific strengths or areas that require more attention based on the individual's performance!
                """,
            7.0: """
                Feedback for Reading Score 7.0:
    
                Congratulations on achieving a reading score of 7.0! Your understanding of written materials reflects a strong ability to grasp main ideas and essential details across various texts.
    
                Strengths:
    
                Exceptional Main Idea Comprehension: Your adeptness at identifying main concepts and key points within reading passages is highly impressive.
                Versatile Comprehension Skills: Your capability to comprehend information in diverse texts, spanning different subjects and styles, demonstrates remarkable adaptability.
                Areas for Further Development:
    
                Fine-tuning Detail Retention: Strengthening your focus on capturing nuanced and specific details from texts will further enhance your overall comprehension.
                Continued Vocabulary Growth: Persisting in expanding your vocabulary will equip you to navigate through more complex texts effectively.
                Consistent practice in capturing intricate details and ongoing vocabulary enrichment will significantly contribute to advancing your understanding of diverse texts.
    
                Feel free to modify this feedback to emphasize particular strengths or areas for improvement based on the individual's performance!
                """,
            7.5: """
                Feedback for Reading Score 7.5:
    
                Congratulations on achieving a reading score of 7.5! Your understanding of written materials showcases an impressive ability to grasp main ideas and essential details across a wide array of texts.
    
                Strengths:
    
                Outstanding Main Idea Comprehension: Your proficiency in identifying main concepts and key points within reading passages is notably strong.
                Adaptable Comprehension Skills: Your capacity to comprehend information in diverse texts, spanning various subjects and styles, demonstrates exceptional adaptability.
                Areas for Further Refinement:
    
                Fine-tuning Detail Retention: Strengthening your focus on capturing nuanced and specific details from texts will further enrich your overall comprehension.
                Continuous Vocabulary Expansion: Sustained efforts in expanding your vocabulary will empower you to navigate through more complex texts effortlessly.
                Consistent practice in capturing intricate details and ongoing efforts in vocabulary enhancement will significantly contribute to advancing your understanding of diverse texts.
    
                Feel free to adjust this feedback to highlight specific strengths or areas requiring more attention based on the individual's performance!
    
                """,
            8.0: """
                Feedback for Reading Score 8.0:
    
                Congratulations on achieving a reading score of 8.0! Your understanding of written materials demonstrates an exceptional ability to grasp main ideas and intricate details across a diverse range of texts.
    
                Strengths:
    
                Exceptional Main Idea Comprehension: Your proficiency in identifying main concepts and key points within reading passages is highly commendable.
                Adaptable Comprehension Skills: Your capability to comprehend information in texts across varied subjects and styles showcases remarkable adaptability.
                Areas for Further Development:
    
                Fine-tuning Detail Retention: Continuously focusing on capturing nuanced and specific details from texts will further elevate your overall comprehension.
                Sustained Vocabulary Growth: Persisting in expanding your vocabulary will enable you to navigate through more complex texts with ease.
                Consistent practice in capturing intricate details and continuous vocabulary enrichment will significantly contribute to advancing your understanding of diverse texts.
    
                Feel free to modify this feedback to highlight specific strengths or areas that might require more attention based on the individual's performance!
    
                """,
            8.5: """
                Feedback for Reading Score 8.5:
    
                Congratulations on achieving a reading score of 8.5! Your understanding of written materials demonstrates an exceptional ability to comprehend main ideas and intricate details across diverse and complex texts.
    
                Strengths:
    
                Exceptional Main Idea Comprehension: Your proficiency in identifying main concepts and key points within reading passages is outstanding.
                Versatile Comprehension Skills: Your capability to comprehend information in texts across various subjects and styles showcases remarkable adaptability.
                Areas for Further Refinement:
    
                Fine-tuning Detail Retention: Continuously focusing on capturing nuanced and specific details from texts will further elevate your overall comprehension.
                Sustained Vocabulary Expansion: Persisting in expanding your vocabulary will empower you to navigate through even more complex texts effortlessly.
                Consistent practice in capturing intricate details and ongoing vocabulary enrichment will significantly contribute to advancing your understanding of diverse texts.
    
                Feel free to adjust this feedback to emphasize specific strengths or areas that may require more attention based on the individual's performance!
    
                """,
            9.0: """
                Feedback for Reading Score 9.0:
    
                Congratulations on achieving a reading score of 9.0! Your understanding of written materials demonstrates an exceptional ability to grasp main ideas and intricate details across a broad spectrum of complex texts.
    
                Strengths:
    
                Exceptional Main Idea Comprehension: Your proficiency in identifying main concepts and key points within reading passages is outstanding.
                Versatile Comprehension Skills: Your capability to comprehend information in texts across diverse subjects and styles showcases remarkable adaptability.
                Areas for Further Development:
    
                Continued Detail Mastery: Continuously focusing on capturing nuanced and specific details from texts will further elevate your already exceptional comprehension.
                Sustained Vocabulary Growth: Persisting in expanding your vocabulary will further enhance your ability to navigate through complex texts effortlessly.
                Consistent practice in capturing intricate details and ongoing vocabulary enrichment will continue to elevate your understanding of diverse texts to even higher levels.
    
                Feel free to modify this feedback to highlight specific strengths or areas that might require more attention based on the individual's performance!
    
                """

        }

        r_band_score = calculate_band_score(r_correct)
        comment = comments_r.get(r_band_score, "No comment available for this band score")
        rtest = Reading_test.objects.create(user=user, comment=comment, band_score=r_band_score)
        rtest.test_section.set(reading_sections)
        wtest = Writing_test.objects.get(is_sent=False, user=user)
        stest = Speaking_test.objects.get(is_sent=False, user=user)

        wtest.is_sent = True
        wtest.save()
        stest.is_sent = True
        stest.save()
        overall_band = (l_band_score + r_band_score + wtest.band_score + stest.band_score) / 4

        ftest = Full_test.objects.create(listening=ltest, reading=rtest, writing=wtest, speaking=stest, band_score=overall_band, user=user)

        ser = FullTestSerializer(ftest)
        return Response(ser.data)
    else:
        my_data = {'message': 'Your result has not released yet'}
        return Response(my_data, status=404)




import requests
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def Send_Message(request):
    text = request.POST['text']
    users = User.objects.all()  
    for user in users:
        test_detail = Test_Details.objects.last()
        token = test_detail.bot_token
        # token = '6384054823:AAH3QEHqITPdRWMJmM6j-ZFaY16CikvSSrw'
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id='
        try:
            response = requests.get(url + str(user.telegram_id) + '&text=' + text)
            if response.status_code != 200 or not response.json().get('ok'):
                # If there's an error in the response
                if response.json().get('error_code') == 403:
                    user.is_active = False
                    user.save()
        except requests.RequestException as e:
            # RequestException covers any exception raised during the request
            # Handle or log the exception accordingly
            print(f"Error sending message to user {user.telegram_id}: {e}")
            # Optionally, mark the user as inactive or handle the error in another way
    
    return Response("Messages sent", status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def Add_Payment(request):
    amount_f = float(request.POST['amount'])
    amount = int(amount_f)
    user = request.user

    new_payment = Payment.objects.create(user=user, amount=amount)

    ser = PaymentSerializer(new_payment)
    user.balance += int(amount)
    user.save()

    return  Response(ser.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def Add_refferal(request, pk):
    user = User.objects.get(telegram_id=pk)
    prices = Test_Details.objects.last()
    user.balance += prices.ref_price
    user.referrals += 1
    user.save()

    ser = UserSerializer(user)
    return Response(ser.data, status=200)


