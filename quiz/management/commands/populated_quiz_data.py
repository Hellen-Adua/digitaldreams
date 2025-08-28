import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from quiz.models import Category, Question


class Command(BaseCommand):
    help = 'Populate quiz data with nested categories from CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to CSV file',
            default=os.path.join(settings.BASE_DIR, 'quiz_data.csv')
        )

    def handle(self, *args, **options):
        csv_file = options['file']

        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file}"))
            return

        self.stdout.write(f'Loading quiz data from {csv_file}...')

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Build nested categories
                category_path = row['category_path'].split('/')
                parent = None
                for cat_name in category_path:
                    category, _ = Category.objects.get_or_create(
                        name=cat_name.strip(),
                        parent=parent  # <-- assumes Category model has parent = ForeignKey("self", null=True, blank=True)
                    )
                    parent = category  # next level down

                # At this point, `parent` is the deepest category
                category = parent

                # Create Question
                question, created = Question.objects.get_or_create(
                    category=category,
                    question_text=row['question_text'],
                    defaults={
                        'option_a': row['option_a'],
                        'option_b': row['option_b'],
                        'option_c': row['option_c'],
                        'option_d': row['option_d'],
                        'correct_answer': row['correct_answer'],
                        'explanation': row['explanation'],
                        'explanation_a': row['explanation_a'],
                        'explanation_b': row['explanation_b'],
                        'explanation_c': row['explanation_c'],
                        'explanation_d': row['explanation_d'],
                        'reference_link': row['reference_link'],
                        'difficulty_level': row['difficulty_level'],
                    }
                )

                if created:
                    self.stdout.write(f"✓ Added question: {question.question_text[:60]}...")
                else:
                    self.stdout.write(f"- Skipped existing: {question.question_text[:60]}...")

        self.stdout.write(self.style.SUCCESS('Successfully populated quiz data!'))
        self.stdout.write(f'Total categories: {Category.objects.count()}')
        self.stdout.write(f'Total questions: {Question.objects.count()}')
