from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserProfileForm

from checkout.models import Order
from feedback.models import Feedback, Recommendation

@login_required
def profile(request):
    context = {}
    profile = get_object_or_404(Profile, user=request.user)
    orders = profile.orders.all()
    context['orders'] = orders
    context['on_profile_page'] = True

    if request.user.is_superuser:
        # If user is admin (superuser), show all feedbacks
        # and all recommendations with Pending status, regardless of owner
        context['feedbacks'] = Feedback.objects.all()
        context['recommendations'] = Recommendation.objects.all()
    else:
        # If user is standard user, show own feedbacks and recommendations
        context['feedbacks'] = Feedback.objects.filter(user=request.user)
        context['recommendations'] = Recommendation.objects.filter(user=request.user)

    if request.POST.get('profile-update-form'):
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
        context['form'] = form

        # Delete object records
        # Delete a feedback, allowed for feedback owner / request user and admin / superuser
        if request.POST.get('myfeedback-to-delete'):
            feedback = Feedback.objects.filter(id=request.POST['myfeedback-to-delete']).first()
            feedback.delete()
            messages.success(request, 'Feedback was deleted.')
            return render(request, 'profiles/profile.html', context=context)
        # Delete a recommendation, allowed only for recommendation owner
        if request.POST.get('myrecommendations-to-delete'):
            recommendation = Recommendation.objects.filter(id=request.POST['myrecommendations-to-delete']).first()
            recommendation.delete()
            messages.success(request, 'Recommendation was deleted.')
            return render(request, 'profiles/profile.html', context=context)
        # Approve recommendation, allowed only for admin / superuser
        if request.POST.get('recommendations-to-approve') and request.user.is_superuser:
            recommendation = Recommendation.objects.filter(id=request.POST['recommendations-to-approve']).first()
            recommendation.status = 'Approved'
            recommendation.save()
            messages.success(request, 'You approved the recommendation.')
            return render(request, 'profiles/profile.html', context=context)
        # Reject recommendation, allowed only for admin / superuser
        if request.POST.get('recommendations-to-reject') and request.user.is_superuser:
            recommendation = Recommendation.objects.filter(id=request.POST['recommendations-to-reject']).first()
            recommendation.status = 'Rejected'
            recommendation.save()
            messages.success(request, 'You rejected the recommendation.')
            return render(request, 'profiles/profile.html', context=context)

    return render(request, 'profiles/profile.html', context)


def order_history(request, order_number):
    context = {}
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    context['order'] = order
    context['from_profile'] = True

    return render(request, 'checkout/checkout_success.html', context)