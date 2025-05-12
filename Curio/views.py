from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.template.loader import render_to_string
from .forms import LoginForm, RegisterForm, QuestionForm, ReplyForm
from django.db.models import Q

from django.shortcuts import render
from .models import Question,Like,Reply

def questions(request):
    questions = Question.objects.all().order_by('-created_at')  # Fetch all questions, ordered by newest first
    context = {
        'questions': questions
    }
    return render(request, 'questions.html', context)

def logout_view(request):
    logout(request)
    return redirect("/")

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username  = form.cleaned_data.get("username")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            # Return an 'invalid login' error message.
            form.add_error(None, "Invalid username or password")
    return render(request, "login.html", context)


User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        username  = form.cleaned_data.get("username")
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        new_user  = User.objects.create_user(username, email, password)
        return redirect('login')

    return render(request, "register.html", context)

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = User.objects.get(id=request.user.id)  # Associate the question with the logged-in user
            question.save()
            form.save_m2m()
            # Add tags to the question
            return redirect('/')  # Redirect to the home page or question list
    else:
        form = QuestionForm()
    return render(request, 'post_question.html', {'form': form})

def tag_filter(request, tag_name):
    questions = Question.objects.filter(tags__name__in=[tag_name])
    return render(request, 'home.html', {'questions': questions, 'tag_name': tag_name})

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, user=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page or question detail page
    else:
        form = QuestionForm(instance=question)
    return render(request, 'edit_question.html', {'form': form})


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, user=request.user)
    if request.method == 'POST':
        question.delete()
        return redirect('home')  # Redirect to the home page
    return redirect('home')

@login_required
def like_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    like, created = Like.objects.get_or_create(user=request.user, question=question)

    if not created:
        # If the like already exists, remove it (unlike)
        like.delete()
        return JsonResponse({'liked': False, 'likes_count': question.likes.count()})
    
    # If the like was created, return success
    return JsonResponse({'liked': True, 'likes_count': question.likes.count()})

@login_required
def reply_to_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            # Create a reply to the question
            reply = Reply.objects.create(
                user=request.user,
                question=question,
                parent_reply=None,  # No parent reply since this is a reply to a question
                body=body
            )

            # Render the updated replies section
            replies = question.replies.all()
            replies_html = render_to_string('partials/replies.html', {'replies': replies}, request=request)
            return JsonResponse({'success': True, 'replies_html': replies_html})

    return JsonResponse({'success': False})

@login_required
def reply_to_reply(request, reply_id):
    parent_reply = get_object_or_404(Reply, id=reply_id)

    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            # Create a reply to the parent reply
            reply = Reply.objects.create(
                user=request.user,
                question=parent_reply.question,  # Use the question from the parent reply
                parent_reply=parent_reply,  # Set the parent reply
                body=body
            )

            # Render the updated child replies section
            child_replies = parent_reply.child_replies.all()
            child_replies_html = render_to_string('partials/replies.html', {'replies': child_replies}, request=request)
            return JsonResponse({'success': True, 'child_replies_html': child_replies_html})

    return JsonResponse({'success': False})

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    context = {
        'question': question,
        'replies': question.replies.all()  # Fetch all replies for the question
    }
    return render(request, 'question_detail.html', context)

@login_required
def like_reply(request, reply_id):
    item=None
    item_type=None
    try:
        # Try to fetch a Reply
        item = get_object_or_404(Reply, id=reply_id)
        item_type = 'reply'
    except:
        try:
            # If no Reply is found, try to fetch a Question
            print('item_id',item_type)
            item = get_object_or_404(Question, id=reply_id)
            item_type = 'question'
        except:
            return JsonResponse({'error': 'Item not found'}, status=404)

    # Handle the like/unlike logic
    like, created = Like.objects.get_or_create(
        user=request.user,
        reply=item if item_type == 'reply' else None,
        question=item if item_type == 'question' else None
    )

    if not created:
        # If the like already exists, remove it (unlike)
        like.delete()
        return JsonResponse({'liked': False, 'likes_count': item.likes.count()})

    # If the like was created, return success
    return JsonResponse({'liked': True, 'likes_count': item.likes.count()})


def search_questions(request):
    query = request.GET.get('q', '').strip()  # strip spaces and handle None
    results = Question.objects.all().order_by('-created_at')

    print("query:", repr(query))  # repr shows even invisible spaces

    if query:  # only search if query is not empty
        results = Question.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-created_at')

    context = {
        'questions': results,
    }

    print("context:", context)
    return render(request, 'home.html', context)