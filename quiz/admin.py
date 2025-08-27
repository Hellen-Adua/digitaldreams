from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Question, QuizSession, QuizQuestion, UserAnswer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color_class', 'get_question_count', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    readonly_fields = ['created_at']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'category', 'correct_answer', 'difficulty_level', 'created_at']
    list_filter = ['category', 'correct_answer', 'difficulty_level', 'created_at']
    search_fields = ['question_text', 'explanation']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Question Details', {
            'fields': ('category', 'question_text', 'difficulty_level')
        }),
        ('Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')
        }),
        ('Explanations', {
            'fields': ('explanation', 'explanation_a', 'explanation_b', 'explanation_c', 'explanation_d')
        }),
        ('Additional Info', {
            'fields': ('reference_link', 'created_at', 'updated_at')
        }),
    )

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 0
    readonly_fields = ['order']

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ['question', 'selected_answer', 'is_correct', 'answered_at']

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'category', 'is_mixed', 'score', 'total_questions', 'get_percentage', 'started_at', 'completed_at']
    list_filter = ['category', 'is_mixed', 'started_at', 'completed_at']
    search_fields = ['user__username', 'session_key']
    readonly_fields = ['started_at', 'get_percentage']
    inlines = [UserAnswerInline]
    
    def get_percentage(self, obj):
        return f"{obj.get_percentage()}%"
    get_percentage.short_description = 'Score %'

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_session', 'question', 'selected_answer', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'selected_answer', 'answered_at']
    search_fields = ['question__question_text']
    readonly_fields = ['answered_at']