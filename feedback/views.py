from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages

from .models import Feedback, Recommendation

from django.contrib.auth import get_user_model
User = get_user_model()


# Feedback Page (feedback.html)
# => Page Aim :
# Give ability to users to provide feedback and recommend book
def feedback(request):
    context = {}

    # Pass all existing feedbacks to show them as list
    context['feedbacks'] = Feedback.objects.all()

    # Get star-based rating and/or text-based comment from user
    # (Click on Send Feedback button)
    if request.method == "POST" and request.POST.get('feedback') or request.POST.get('rating'):
        rating = request.POST.get('rating').split('_')[0]
        rating_desc = request.POST.get('rating').split('_')[1]
        content = request.POST['feedback']

        # Create feedback only if either star-based rating,
        # either text-based comment, either both were provided
        if content or (rating != '0'):
            user = request.user
            feedback = Feedback.objects.create(rating_point=rating,
                                               rating_description=rating_desc,
                                               content=content,
                                               user=user)
            feedback.save()
            messages.success(request, 'Feedback #' + str(feedback.id) + ' created, thank you!')
            return render(request, 'feedback/feedback.html', context=context)
        else:
            messages.error(request, 'Please share your feedback or rating!')
            return render(request, 'feedback/feedback.html', context=context)

    # Allow feedback owner or admin user (superuser) to delete feedback from list
    # (Click on Delete button of a feedback)
    if request.method == "POST" and request.POST.get('feedback-to-delete'):
        feedback = Feedback.objects.filter(id=request.POST['feedback-to-delete']).first()
        feedback.delete()
        messages.success(request, 'Feedback was deleted.')
        return render(request, 'feedback/feedback.html', context=context)

    # Get recommended item from user (Click on Recommend Item button)
    if request.method == "POST" and request.POST.get('book_title'):
        user = request.user
        title = request.POST['book_title']
        author = request.POST['book_author']
        category = request.POST['book_category']

        # Create recommendation for admin approval
        recommendation = Recommendation.objects.create(user=user,
                                                       title=title,
                                                       author=author,
                                                       category=category,
                                                       status='Pending')
        recommendation.save()
        messages.success(request, 'Recommendation #' + str(recommendation.id) + ' created, thank you!')
        return render(request, 'feedback/feedback.html', context=context)

    return render(request, 'feedback/feedback.html', context=context)