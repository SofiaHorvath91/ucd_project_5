import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Quiz, Question, Answer, Result
from books.models import Book, Category


# Daily Book Quiz Page (quiz.html)
# => Page Aim :
# Let user fill out a quiz to get her/his daily category
# and a recommended book in this category
def quiz(request):
    context = {}

    # Setting boolean values for conditional display of sections on html page
    # (by default, quiz starter section is visible)
    context['game_start'] = True
    context['game_on'] = False
    context['game_end'] = False

    # Selecting quiz from db
    quiz = Quiz.objects.filter(name='Your Daily Book').first()
    questions_count = quiz.questions.all().count()
    context['quiz'] = quiz
    context['quiz_name'] = quiz.name

    # Handling click on Start Daily Mood Quiz button
    if 'quiz_start' in request.POST:
        # Setting category points to zero
        context['crime_thriller_count'] = 0
        context['comics_manga_count'] = 0
        context['poetry_drama_count'] = 0
        context['scifi_fantasy_horror_count'] = 0

        # Setting boolean values to display quiz game section
        context['game_start'] = False
        context['game_on'] = True

        # Select first question with related answers of quiz to start
        curr_question = quiz.questions.filter(number=1).first()
        context['current_question'] = curr_question
        context['answers'] = curr_question.answers.all()

        return render(request, 'dailybook/quiz.html', context=context)

    # Handling click on Next Question button
    if 'next_question' in request.POST:
        # Setting boolean values to display quiz game section
        context['game_start'] = False

        # Getting category points so far
        crime_thriller_count = check_point_empty(request.POST['count_crime_thriller'])
        comics_manga_count = check_point_empty(request.POST['count_comics_manga'])
        poetry_drama_count = check_point_empty(request.POST['count_poetry_drama'])
        scifi_fantasy_horror_count = check_point_empty(request.POST['count_scifi_fantasy_horror'])

        # Getting category value of current answer
        # and increment related category's points
        selected_answer = request.POST.get('answers_options')
        if 'Crime-Thriller' == selected_answer:
            crime_thriller_count = add_point(crime_thriller_count)
        elif 'Comics-Manga' == selected_answer:
            comics_manga_count = add_point(comics_manga_count)
        elif 'Poetry-Drama' == selected_answer:
            poetry_drama_count = add_point(poetry_drama_count)
        else:
            scifi_fantasy_horror_count = add_point(scifi_fantasy_horror_count)

        # Setting result category values with current answer's values included
        context['crime_thriller_count'] = crime_thriller_count
        context['comics_manga_count'] = comics_manga_count
        context['poetry_drama_count'] = poetry_drama_count
        context['scifi_fantasy_horror_count'] = scifi_fantasy_horror_count

        # Get current question index
        current_index = int(request.POST['current_index'])

        # Saving result to database
        # if current question index = last question number
        if current_index == questions_count:
            # Get maximum category point and select category for final result
            category_points = {
                "Crime-Thriller": crime_thriller_count,
                "Comics-Manga": comics_manga_count,
                "Poetry-Drama": poetry_drama_count,
                "SciFi-Fantasy-Horror": scifi_fantasy_horror_count,
            }

            max_point = max(category_points.values())
            result_category = ''
            for k, v in category_points.items():
                if v == max_point:
                    result_category = k
            category = Category.objects.filter(name=result_category).first()

            # Set wording for result based on maximum category
            result_wording = ''
            if str(category) == 'Crime-Thriller':
                result_wording = "Seems like you are a bit blood-thirsty today! " \
                         "This is all right, we all have some days when darkness and mystery feels good " \
                         "- maybe the following book will fit right to your moody mood!"
            if str(category) == 'Comics-Manga':
                result_wording = "It looks like you fly as high as Superman today! " \
                         "For this colorful and dynamic mood, what else would fit better " \
                         "than a action-packed comic? Check out the following and get into the action!"
            if str(category) == 'Poetry-Drama':
                result_wording = "Feeling the spleen and the beauty today? " \
                         "As it seems you are in a poetic mood with some taste for drama, " \
                         "maybe the following book will help you dive a bit more into the depth of human soul."
            if str(category) == 'SciFi-Fantasy-Horror':
                result_wording = "It looks like you are disconnected from this world today! " \
                         "To help you get out of reality and enter a new world of dreams and monsters, " \
                         "we recommend the following book as the exit door to escape the daily routine."

            # Select random book in maximum category
            # as daily book recommendation
            books_per_category = Book.objects.filter(category=category)
            random_num = random.randint(0, (len(books_per_category) - 1))
            daily_book = books_per_category[random_num]

            # Create result object in database
            # and navigate to current result's record
            result = Result.objects.create(quiz=quiz,
                                           category=category,
                                           point=max_point,
                                           book=daily_book,
                                           user=request.user,
                                           result=result_wording)

            return redirect('result', result_id=result.id)

        # If current question index
        # != last question number, increment current question index
        index = current_index + 1
        # Set boolean values to display quiz game section
        context['game_on'] = True
        # Select next question based
        # on incremented current index with related answers
        curr_question = quiz.questions.filter(number=index).first()
        context['current_question'] = curr_question
        context['answers'] = curr_question.answers.all()

        return render(request,
                      'dailybook/quiz.html',
                      context=context)

    return render(request, 'dailybook/quiz.html', context=context)


# Daily Book Quiz's Result Page (result.html)
# => Page Aim :
# Display result of current completion of Daily Mood quiz
# => Presents daily recommended book in the daily category
@login_required
def result(request, result_id):
    context = {}

    current_result = Result.objects.filter(id=result_id).first()
    questions_count = current_result.quiz.questions.all().count()

    context['result'] = current_result
    context['questions_count'] = questions_count

    return render(request, 'dailybook/result.html', context=context)


# Helper functions


# Increment category point with one
# => Used in page view sorting
def add_point(count):
    return int(count) + 1


# Convert request.post result to number
# => Used in page view sorting
def check_point_empty(point):
    # If request.post number value is null, return 0, else converted number
    try:
        return int(point)
    except ValueError:
        return 0
