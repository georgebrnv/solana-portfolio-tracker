from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def profile(request):

    if request.method == 'POST':

        user = request.user
        messages_bool = False

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']

        # Image update
        if 'image' in request.FILES:
            # Pull image from HTML input field
            image = request.FILES['image']
            # Create an instance of current user's profile_image object
            user_image = user.profile_image
            # Reassign user's image object to a new one
            user_image.image = image
            # Update DB
            user_image.save()
            messages_bool = True

        if first_name != user.first_name:
            user.first_name = first_name
            messages_bool = True

        if last_name != user.last_name:
            user.last_name = last_name
            messages_bool = True

        if username != user.username:
            user.username = username
            messages_bool = True

        if email != user.email:
            user.email = email
            messages_bool = True

        user.save()
        if messages_bool:
            messages.success(request, 'Your settings has been successfully updated.')

        return redirect('profile')

    return render(request, 'user_profile/profile.html')