from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import json

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='📚')
    color_class = models.CharField(max_length=50, default='bg-blue-500')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_question_count(self):
        return self.questions.count()

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    explanation = models.TextField(help_text="General explanation for the correct answer")
    explanation_a = models.TextField(blank=True, help_text="Why option A is correct/incorrect")
    explanation_b = models.TextField(blank=True, help_text="Why option B is correct/incorrect")
    explanation_c = models.TextField(blank=True, help_text="Why option C is correct/incorrect")
    explanation_d = models.TextField(blank=True, help_text="Why option D is correct/incorrect")
    reference_link = models.URLField(blank=True, help_text="Optional reference link for additional learning")
    difficulty_level = models.CharField(max_length=10, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.category.name}: {self.question_text[:50]}..."
    
    def get_options(self):
        return {
            'A': self.option_a,
            'B': self.option_b,
            'C': self.option_c,
            'D': self.option_d,
        }
    
    def get_explanations(self):
        return {
            'A': self.explanation_a,
            'B': self.explanation_b,
            'C': self.explanation_c,
            'D': self.explanation_d,
        }

class QuizSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_mixed = models.BooleanField(default=False)
    questions = models.ManyToManyField(Question, through='QuizQuestion')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    time_taken = models.DurationField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        category_name = self.category.name if self.category else "Mixed Quiz"
        return f"Quiz Session - {category_name} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_percentage(self):
        if self.total_questions == 0:
            return 0
        return round((self.score / self.total_questions) * 100)
    
    def get_performance_message(self):
        percentage = self.get_percentage()
        if percentage >= 90:
            return "Outstanding! You're a quiz master! 🏆"
        elif percentage >= 80:
            return "Excellent work! You know your stuff! 🌟"
        elif percentage >= 70:
            return "Great job! You did really well! 👏"
        elif percentage >= 60:
            return "Good effort! Room for improvement! 👍"
        else:
            return "Keep studying and try again! You've got this! 💪"

class QuizQuestion(models.Model):
    quiz_session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']
        unique_together = ['quiz_session', 'question']

class UserAnswer(models.Model):
    quiz_session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.DurationField(null=True, blank=True)
    
    class Meta:
        unique_together = ['quiz_session', 'question']
        ordering = ['answered_at']
    
    def __str__(self):
        return f"Answer for {self.question.question_text[:30]}... - {self.selected_answer}"