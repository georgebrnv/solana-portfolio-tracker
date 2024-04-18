from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):

    if request.method == 'POST':



        # Image update
        if 'image' in request.FILES:

            # Create instance of current user's profile_image object
            user_image = request.user.profile_image
            # Pull image from HTML input field
            new_image = request.FILES['image']
            # Reassign user's image object to a new one
            user_image.image = new_image
            # Update DB
            user_image.save()

            return redirect('profile')

    return render(request, 'user_profile/profile.html')