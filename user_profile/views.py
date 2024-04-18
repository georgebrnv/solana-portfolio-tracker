from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):

    if request.method == 'POST':

        user = request.user

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

        if first_name != user.first_name:
            user.first_name = first_name

        if last_name != user.last_name:
            user.last_name = last_name

        if username != user.username:
            user.username = username

        if email != user.email:
            user.email = email

        user.save()

        return redirect('profile')

    return render(request, 'user_profile/profile.html')