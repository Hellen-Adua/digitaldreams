from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
import json
import random
from datetime import timedelta

from .models import Category, Question, QuizSession, QuizQuestion, UserAnswer

def home(request):
    """Home page with category selection"""
    categories = Category.objects.all().annotate(
        question_count=Count('questions')
    )
    
    # Get recent quiz sessions for stats
    recent_sessions = QuizSession.objects.filter(
        completed_at__isnull=False
    ).order_by('-completed_at')[:5]
    
    context = {
        'categories': categories,
        'recent_sessions': recent_sessions,
        'total_questions': Question.objects.count(),
        'total_categories': categories.count(),
    }
    return render(request, 'quiz/home.html', context)

def start_quiz(request, category_id):
    """Start a category-specific quiz"""
    category = get_object_or_404(Category, id=category_id)
    
    # Get questions for this category
    questions = list(Question.objects.filter(category=category))
    
    if len(questions) < 5:
        return render(request, 'quiz/error.html', {
            'error_message': f'Not enough questions in {category.name} category. Minimum 5 questions required.'
        })
    
    # Shuffle and limit to 10-15 questions
    random.shuffle(questions)
    quiz_questions = questions[:min(15, len(questions))]
    
    # Create quiz session
    session = QuizSession.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key,
        category=category,
        is_mixed=False,
        total_questions=len(quiz_questions)
    )
    
    # Add questions to session
    for i, question in enumerate(quiz_questions):
        QuizQuestion.objects.create(
            quiz_session=session,
            question=question,
            order=i + 1
        )
    
    return redirect('quiz:quiz_question', session_id=session.id)

def start_mixed_quiz(request):
    """Start a mixed quiz with questions from all categories"""
    # Get questions from all categories
    all_questions = list(Question.objects.all())
    
    if len(all_questions) < 10:
        return render(request, 'quiz/error.html', {
            'error_message': 'Not enough questions available. Minimum 10 questions required for mixed quiz.'
        })
    
    # Shuffle and select 15 questions
    random.shuffle(all_questions)
    quiz_questions = all_questions[:15]
    
    # Create quiz session
    session = QuizSession.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key,
        category=None,
        is_mixed=True,
        total_questions=len(quiz_questions)
    )
    
    # Add questions to session
    for i, question in enumerate(quiz_questions):
        QuizQuestion.objects.create(
            quiz_session=session,
            question=question,
            order=i + 1
        )
    
    return redirect('quiz:quiz_question', session_id=session.id)

def quiz_question(request, session_id):
    """Display current quiz question"""
    session = get_object_or_404(QuizSession, id=session_id)
    
    # Get all questions for this session in order
    quiz_questions = QuizQuestion.objects.filter(
        quiz_session=session
    ).select_related('question').order_by('order')
    
    # Get answered questions
    answered_questions = UserAnswer.objects.filter(
        quiz_session=session
    ).values_list('question_id', flat=True)
    
    # Find next unanswered question
    current_quiz_question = None
    for qq in quiz_questions:
        if qq.question.id not in answered_questions:
            current_quiz_question = qq
            break
    
    # If no more questions, redirect to results
    if not current_quiz_question:
        session.completed_at = timezone.now()
        session.score = UserAnswer.objects.filter(
            quiz_session=session, 
            is_correct=True
        ).count()
        session.save()
        return redirect('quiz:quiz_results', session_id=session.id)
    
    # Calculate progress
    current_question_number = len(answered_questions) + 1
    progress_percentage = (len(answered_questions) / session.total_questions) * 100
    
    context = {
        'session': session,
        'question': current_quiz_question.question,
        'current_question_number': current_question_number,
        'total_questions': session.total_questions,
        'progress_percentage': progress_percentage,
        'time_remaining': 30,  # 30 seconds per question
    }
    
    return render(request, 'quiz/question.html', context)

@csrf_exempt
def submit_answer(request):
    """Submit answer via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            question_id = data.get('question_id')
            selected_answer = data.get('selected_answer')
            time_taken = data.get('time_taken', 0)
            
            session = get_object_or_404(QuizSession, id=session_id)
            question = get_object_or_404(Question, id=question_id)
            
            is_correct = selected_answer == question.correct_answer
            
            # Save user answer
            UserAnswer.objects.create(
                quiz_session=session,
                question=question,
                selected_answer=selected_answer,
                is_correct=is_correct,
                time_taken=timedelta(seconds=time_taken)
            )
            
            return JsonResponse({
                'success': True,
                'is_correct': is_correct,
                'correct_answer': question.correct_answer,
                'explanation': question.explanation
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def quiz_results(request, session_id):
    """Display quiz results"""
    session = get_object_or_404(QuizSession, id=session_id)
    answers = UserAnswer.objects.filter(
        quiz_session=session
    ).select_related('question').order_by('answered_at')
    
    # Calculate statistics
    correct_count = answers.filter(is_correct=True).count()
    incorrect_count = answers.filter(is_correct=False).count()
    percentage = session.get_percentage()
    
    # Category breakdown for mixed quiz
    category_stats = {}
    if session.is_mixed:
        for answer in answers:
            cat_name = answer.question.category.name
            if cat_name not in category_stats:
                category_stats[cat_name] = {'correct': 0, 'total': 0, 'half_total': 0,}
            category_stats[cat_name]['total'] += 1
            if answer.is_correct:
                category_stats[cat_name]['correct'] += 1
    
        for cat, stats in category_stats.items():
            stats['half_total'] = stats['total'] / 2

    context = {
        'session': session,
        'answers': answers,
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'percentage': percentage,
        'performance_message': session.get_performance_message(),
        'category_stats': category_stats,
    }
    
    return render(request, 'quiz/results.html', context)

def revision_mode(request, session_id):
    """Review mode with detailed explanations"""
    session = get_object_or_404(QuizSession, id=session_id)
    answers = UserAnswer.objects.filter(
        quiz_session=session
    ).select_related('question', 'question__category').order_by('answered_at')
    
    # Add additional data for each answer
    for answer in answers:
        answer.options = answer.question.get_options()
        answer.explanations = answer.question.get_explanations()
    
    context = {
        'session': session,
        'answers': answers,
    }
    
    return render(request, 'quiz/revision.html', context)

def get_question_details(request, question_id):
    """API endpoint for question details (for modals)"""
    question = get_object_or_404(Question, id=question_id)
    
    # Get user's answer if available
    user_answer = None
    if request.GET.get('session_id'):
        try:
            session_id = int(request.GET.get('session_id'))
            answer = UserAnswer.objects.get(
                quiz_session_id=session_id,
                question=question
            )
            user_answer = answer.selected_answer
        except (UserAnswer.DoesNotExist, ValueError):
            pass
    
    return JsonResponse({
        'id': question.id,
        'question': question.question_text,
        'options': question.get_options(),
        'correct_answer': question.correct_answer,
        'explanation': question.explanation,
        'explanations': question.get_explanations(),
        'reference_link': question.reference_link,
        'user_answer': user_answer,
        'category': question.category.name,
        'difficulty': question.difficulty_level,
    })

def leaderboard(request):
    """Display leaderboard of top performers"""
    # Get top sessions by percentage
    top_sessions = QuizSession.objects.filter(
        completed_at__isnull=False,
        total_questions__gt=0
    ).extra(
        select={'percentage': '(score * 100.0 / total_questions)'}
    ).order_by('-percentage', '-score', 'started_at')[:20]
    
    context = {
        'top_sessions': top_sessions,
    }
    
    return render(request, 'quiz/leaderboard.html', context)

@login_required
def user_stats(request):
    """Display user statistics"""
    user_sessions = QuizSession.objects.filter(
        user=request.user,
        completed_at__isnull=False
    ).order_by('-started_at')
    
    # Calculate statistics
    total_sessions = user_sessions.count()
    if total_sessions > 0:
        avg_score = sum(s.get_percentage() for s in user_sessions) / total_sessions
        best_score = max(s.get_percentage() for s in user_sessions)
        total_questions_answered = sum(s.total_questions for s in user_sessions)
        total_correct = sum(s.score for s in user_sessions)
    else:
        avg_score = best_score = total_questions_answered = total_correct = 0
    
    # Category performance
    category_performance = {}
    for session in user_sessions:
        if session.category:
            cat_name = session.category.name
            if cat_name not in category_performance:
                category_performance[cat_name] = {'sessions': 0, 'total_score': 0, 'total_questions': 0}
            category_performance[cat_name]['sessions'] += 1
            category_performance[cat_name]['total_score'] += session.score
            category_performance[cat_name]['total_questions'] += session.total_questions
    
    # Calculate percentages for categories
    for cat_data in category_performance.values():
        if cat_data['total_questions'] > 0:
            cat_data['percentage'] = round((cat_data['total_score'] / cat_data['total_questions']) * 100)
        else:
            cat_data['percentage'] = 0
    
    context = {
        'user_sessions': user_sessions[:10],  # Recent 10 sessions
        'total_sessions': total_sessions,
        'avg_score': round(avg_score, 1),
        'best_score': best_score,
        'total_questions_answered': total_questions_answered,
        'total_correct': total_correct,
        'category_performance': category_performance,
    }
    
    return render(request, 'quiz/user_stats.html', context)