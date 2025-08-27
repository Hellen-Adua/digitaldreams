from django.core.management.base import BaseCommand
from quiz.models import Category, Question

class Command(BaseCommand):
    help = 'Populate the database with sample quiz data'

    def handle(self, *args, **options):
        self.stdout.write('Populating quiz data...')
        
        # Create categories
        categories_data = [
            {
                'name': 'Science & Technology',
                'description': 'Questions about scientific discoveries, technology, and innovations',
                'icon': '🔬',
                'color_class': 'bg-blue-500'
            },
            {
                'name': 'History & Culture',
                'description': 'Historical events, cultural knowledge, and world civilizations',
                'icon': '🏛️',
                'color_class': 'bg-emerald-500'
            },
            {
                'name': 'Geography & Nature',
                'description': 'World geography, natural phenomena, and environmental science',
                'icon': '🌍',
                'color_class': 'bg-amber-500'
            },
            {
                'name': 'Literature & Arts',
                'description': 'Literature, fine arts, music, and creative expressions',
                'icon': '📚',
                'color_class': 'bg-purple-500'
            },
            {
                'name': 'Sports & Entertainment',
                'description': 'Sports trivia, entertainment industry, and popular culture',
                'icon': '⚽',
                'color_class': 'bg-red-500'
            },
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'✓ Created category: {category.name}')

        # Science & Technology Questions
        science_questions = [
            {
                'question_text': 'What is the chemical symbol for gold?',
                'option_a': 'Go',
                'option_b': 'Gd',
                'option_c': 'Au',
                'option_d': 'Ag',
                'correct_answer': 'C',
                'explanation': 'Gold\'s chemical symbol is Au, derived from the Latin word "aurum" meaning gold.',
                'explanation_a': 'Go is not a recognized chemical symbol in the periodic table.',
                'explanation_b': 'Gd is the symbol for Gadolinium, a rare earth element.',
                'explanation_c': 'Correct! Au comes from the Latin "aurum" meaning gold.',
                'explanation_d': 'Ag is the symbol for Silver, from Latin "argentum".',
                'reference_link': 'https://en.wikipedia.org/wiki/Gold',
                'difficulty_level': 'easy'
            },
            {
                'question_text': 'Which planet is known as the "Red Planet"?',
                'option_a': 'Venus',
                'option_b': 'Mars',
                'option_c': 'Jupiter',
                'option_d': 'Saturn',
                'correct_answer': 'B',
                'explanation': 'Mars is called the "Red Planet" due to iron oxide (rust) on its surface, giving it a reddish appearance.',
                'explanation_a': 'Venus is known as the "Morning Star" or "Evening Star" due to its brightness.',
                'explanation_b': 'Correct! Mars appears red due to iron oxide on its surface.',
                'explanation_c': 'Jupiter is the largest planet and is known for its Great Red Spot.',
                'explanation_d': 'Saturn is famous for its prominent ring system.',
                'reference_link': 'https://en.wikipedia.org/wiki/Mars',
                'difficulty_level': 'easy'
            },
            {
                'question_text': 'What does DNA stand for?',
                'option_a': 'Deoxyribonucleic Acid',
                'option_b': 'Dinitrogen Acid',
                'option_c': 'Diacetyl Nucleic Acid',
                'option_d': 'Deoxyribose Nitrate Acid',
                'correct_answer': 'A',
                'explanation': 'DNA stands for Deoxyribonucleic Acid, the molecule that carries genetic instructions in living organisms.',
                'explanation_a': 'Correct! DNA is Deoxyribonucleic Acid, containing genetic information.',
                'explanation_b': 'Dinitrogen Acid is not a real compound related to genetics.',
                'explanation_c': 'This is not a real biological molecule.',
                'explanation_d': 'This is not the correct expansion of DNA.',
                'reference_link': 'https://en.wikipedia.org/wiki/DNA',
                'difficulty_level': 'medium'
            },
            {
                'question_text': 'Who invented the World Wide Web?',
                'option_a': 'Bill Gates',
                'option_b': 'Steve Jobs',
                'option_c': 'Tim Berners-Lee',
                'option_d': 'Mark Zuckerberg',
                'correct_answer': 'C',
                'explanation': 'Tim Berners-Lee invented the World Wide Web in 1989 while working at CERN.',
                'explanation_a': 'Bill Gates co-founded Microsoft but did not invent the World Wide Web.',
                'explanation_b': 'Steve Jobs co-founded Apple but did not invent the World Wide Web.',
                'explanation_c': 'Correct! Tim Berners-Lee created the first web browser and web server.',
                'explanation_d': 'Mark Zuckerberg founded Facebook, which came much later.',
                'reference_link': 'https://en.wikipedia.org/wiki/Tim_Berners-Lee',
                'difficulty_level': 'medium'
            },
            {
                'question_text': 'What is the speed of light in vacuum?',
                'option_a': '299,792,458 meters per second',
                'option_b': '300,000,000 meters per second',
                'option_c': '186,000 miles per second',
                'option_d': '299,792,458 kilometers per second',
                'correct_answer': 'A',
                'explanation': 'The speed of light in vacuum is exactly 299,792,458 meters per second.',
                'explanation_a': 'Correct! This is the exact value defined by international standards.',
                'explanation_b': 'This is an approximation, but not the exact value.',
                'explanation_c': 'This is approximately correct in miles per second, but the question asks for the standard unit.',
                'explanation_d': 'This would be much faster than the actual speed of light.',
                'reference_link': 'https://en.wikipedia.org/wiki/Speed_of_light',
                'difficulty_level': 'hard'
            },
        ]

        # History & Culture Questions
        history_questions = [
            {
                'question_text': 'In which year did World War II end?',
                'option_a': '1944',
                'option_b': '1945',
                'option_c': '1946',
                'option_d': '1947',
                'correct_answer': 'B',
                'explanation': 'World War II ended in 1945 with Japan\'s surrender on September 2, 1945.',
                'explanation_a': '1944 was still during active warfare, including D-Day landings.',
                'explanation_b': 'Correct! WWII ended in 1945 with Japan\'s surrender in September.',
                'explanation_c': '1946 was the post-war period, with trials and reconstruction beginning.',
                'explanation_d': '1947 was well into the post-war era and Cold War tensions.',
                'reference_link': 'https://en.wikipedia.org/wiki/World_War_II',
                'difficulty_level': 'easy'
            },
            {
                'question_text': 'Who was the first person to walk on the moon?',
                'option_a': 'Buzz Aldrin',
                'option_b': 'Neil Armstrong',
                'option_c': 'Michael Collins',
                'option_d': 'John Glenn',
                'correct_answer': 'B',
                'explanation': 'Neil Armstrong was the first human to walk on the moon on July 20, 1969.',
                'explanation_a': 'Buzz Aldrin was the second person to walk on the moon.',
                'explanation_b': 'Correct! Neil Armstrong was first to step onto the lunar surface.',
                'explanation_c': 'Michael Collins was the command module pilot who stayed in orbit.',
                'explanation_d': 'John Glenn was the first American to orbit Earth, but never went to the moon.',
                'reference_link': 'https://en.wikipedia.org/wiki/Neil_Armstrong',
                'difficulty_level': 'easy'
            },
            {
                'question_text': 'Which ancient wonder was located in Alexandria?',
                'option_a': 'Colossus of Rhodes',
                'option_b': 'Lighthouse of Alexandria',
                'option_c': 'Hanging Gardens',
                'option_d': 'Temple of Artemis',
                'correct_answer': 'B',
                'explanation': 'The Lighthouse of Alexandria (Pharos) was one of the Seven Wonders of the Ancient World.',
                'explanation_a': 'The Colossus of Rhodes was located on the Greek island of Rhodes.',
                'explanation_b': 'Correct! The Pharos lighthouse was in Alexandria, Egypt.',
                'explanation_c': 'The Hanging Gardens were allegedly in Babylon (modern-day Iraq).',
                'explanation_d': 'The Temple of Artemis was located in Ephesus (modern-day Turkey).',
                'reference_link': 'https://en.wikipedia.org/wiki/Lighthouse_of_Alexandria',
                'difficulty_level': 'medium'
            },
            {
                'question_text': 'Who painted the ceiling of the Sistine Chapel?',
                'option_a': 'Leonardo da Vinci',
                'option_b': 'Raphael',
                'option_c': 'Michelangelo',
                'option_d': 'Donatello',
                'correct_answer': 'C',
                'explanation': 'Michelangelo painted the ceiling of the Sistine Chapel between 1508 and 1512.',
                'explanation_a': 'Leonardo da Vinci was a contemporary but did not paint the Sistine Chapel.',
                'explanation_b': 'Raphael painted other parts of the Vatican but not the Sistine Chapel ceiling.',
                'explanation_c': 'Correct! Michelangelo spent four years painting this masterpiece.',
                'explanation_d': 'Donatello was primarily a sculptor, not a painter.',
                'reference_link': 'https://en.wikipedia.org/wiki/Sistine_Chapel_ceiling',
                'difficulty_level': 'medium'
            },
            {
                'question_text': 'The Rosetta Stone was crucial for deciphering which ancient script?',
                'option_a': 'Cuneiform',
                'option_b': 'Hieroglyphics',
                'option_c': 'Linear B',
                'option_d': 'Sanskrit',
                'correct_answer': 'B',
                'explanation': 'The Rosetta Stone was key to understanding Egyptian hieroglyphics.',
                'explanation_a': 'Cuneiform was deciphered through other means, primarily Mesopotamian tablets.',
                'explanation_b': 'Correct! The stone contained the same text in hieroglyphics, Demotic, and Greek.',
                'explanation_c': 'Linear B was deciphered by Michael Ventris without the Rosetta Stone.',
                'explanation_d': 'Sanskrit was never lost and didn\'t need deciphering like hieroglyphics.',
                'reference_link': 'https://en.wikipedia.org/wiki/Rosetta_Stone',
                'difficulty_level': 'hard'
            },
        ]

        # Geography & Nature Questions
        geography_questions = [
            {
                'question_text': 'What is the longest river in the world?',
                'option_a': 'Amazon River',
                'option_b': 'Nile River',
                'option_c': 'Yangtze River',
                'option_d': 'Mississippi River',
                'correct_answer': 'B',
                'explanation': 'The Nile River is the longest river in the world at approximately 6,650 kilometers.',
                'explanation_a': 'The Amazon is the largest by volume and second longest river.',
                'explanation_b': 'Correct! The Nile is the longest river at about 6,650 km.',
                'explanation_c': 'The Yangtze is the longest river in Asia and third longest globally.',
                'explanation_d': 'The Mississippi is the longest river system in North America.',
                'reference_link': 'https://en.wikipedia.org/wiki/Nile',
                'difficulty_level': 'easy'
            },
            {
                'question_text': 'Which mountain range contains Mount Everest?',
                'option_a': 'Andes',
                'option_b': 'Rockies',
                'option_c': 'Alps',
                'option_d': 'Himalayas',
                'correct_answer': 'D',
                'explanation': 'Mount Everest is located in the Himalayas, on the border between Nepal and Tibet.',
                'explanation_a': 'The Andes are in South America, containing peaks like Aconcagua.',
                'explanation_b': 'The Rockies are in North America, with peaks like Mount Elbert.',
                'explanation_c': 'The Alps are in Europe, with famous peaks like Mont Blanc.',
                'explanation_d': 'Correct! The Himalayas contain Everest and many of the world\'s highest peaks.',
                'reference_link': 'https://en.wikipedia.org/wiki/Mount_Everest',
                'difficulty_level': 'easy'
            },
            {
                'question_text': 'What is the largest desert in the world?',
                'option_a': 'Sahara Desert',
                'option_b': 'Gobi Desert',
                'option_c': 'Antarctica',
                'option_d': 'Arabian Desert',
                'correct_answer': 'C',
                'explanation': 'Antarctica is technically the largest desert in the world, being a cold desert.',
                'explanation_a': 'The Sahara is the largest hot desert, but not the largest overall.',
                'explanation_b': 'The Gobi is a large desert but much smaller than Antarctica.',
                'explanation_c': 'Correct! Antarctica is classified as a polar desert and is the largest.',
                'explanation_d': 'The Arabian Desert is large but much smaller than Antarctica.',
                'reference_link': 'https://en.wikipedia.org/wiki/Desert',
                'difficulty_level': 'hard'
            },
            {
                'question_text': 'Which country has the most time zones?',
                'option_a': 'Russia',
                'option_b': 'United States',
                'option_c': 'China',
                'option_d': 'France',
                'correct_answer': 'D',
                'explanation': 'France has 12 time zones due to its overseas territories, more than any other country.',
                'explanation_a': 'Russia has 11 time zones, making it second.',
                'explanation_b': 'The United States has 6 time zones in its main territory.',
                'explanation_c': 'China uses only one time zone despite its large size.',
                'explanation_d': 'Correct! France has 12 time zones including its overseas territories.',
                'reference_link': 'https://en.wikipedia.org/wiki/Time_zone',
                'difficulty_level': 'hard'
            },
            {
                'question_text': 'What is the deepest point in the ocean?',
                'option_a': 'Puerto Rico Trench',
                'option_b': 'Java Trench',
                'option_c': 'Mariana Trench',
                'option_d': 'Peru-Chile Trench',
                'correct_answer': 'C',
                'explanation': 'The Mariana Trench in the Pacific Ocean is the deepest part of the world\'s oceans.',
                'explanation_a': 'The Puerto Rico Trench is deep but not the deepest.',
                'explanation_b': 'The Java Trench is in the Indian Ocean but not the deepest.',
                'explanation_c': 'Correct! The Mariana Trench reaches depths of over 11,000 meters.',
                'explanation_d': 'The Peru-Chile Trench is deep but not the deepest.',
                'reference_link': 'https://en.wikipedia.org/wiki/Mariana_Trench',
                'difficulty_level': 'medium'
            },
        ]

        # Literature & Arts Questions
        literature_questions = [
            {
                'question_text': 'Who wrote "Pride and Prejudice"?',
                'option_a': 'Charlotte Brontë',
                'option_b': 'Emily Dickinson',
                'option_c': 'Jane Austen',
                'option_d': 'Virginia Woolf',
                'correct_answer': 'C',
                'explanation': 'Jane Austen wrote "Pride and Prejudice" in 1813, one of her most famous novels.',
                'explanation_a': 'Charlotte Brontë wrote "Jane Eyre" and "Villette".',
                'explanation_b': 'Emily Dickinson was an American poet known for her reclusive life.',
                'explanation_c': 'Correct! Jane Austen authored this beloved 1813 novel.',
                'explanation_d': 'Virginia Woolf wrote "Mrs. Dalloway" and "To the Lighthouse".',
                'reference_link': 'https://en.wikipedia.org/wiki/Pride_and_Prejudice',
                'difficulty_level': 'easy'
            },
            {
                'question_text': 'Which artist painted "The Starry Night"?',
                'option_a': 'Pablo Picasso',
                'option_b': 'Vincent van Gogh',
                'option_c': 'Claude Monet',
                'option_d': 'Leonardo da Vinci',
                'correct_answer': 'B',
                'explanation': '"The Starry Night" was painted by Vincent van Gogh in 1889.',
                'explanation_a': 'Picasso was a pioneer of Cubism, known for works like "Guernica".',
                'explanation_b': 'Correct! Van Gogh painted this masterpiece in 1889.',
                'explanation_c': 'Monet was an Impressionist known for his "Water Lilies" series.',
                'explanation_d': 'Da Vinci painted "Mona Lisa" and "The Last Supper".',
                'reference_link': 'https://en.wikipedia.org/wiki/The_Starry_Night',
                'difficulty_level': 'easy'
            },
            {
                'question_text': 'Who wrote the novel "1984"?',
                'option_a': 'Aldous Huxley',
                'option_b': 'George Orwell',
                'option_c': 'Ray Bradbury',
                'option_d': 'H.G. Wells',
                'correct_answer': 'B',
                'explanation': 'George Orwell wrote "1984", published in 1949, a dystopian novel about totalitarian surveillance.',
                'explanation_a': 'Aldous Huxley wrote "Brave New World", another famous dystopian novel.',
                'explanation_b': 'Correct! Orwell\'s "1984" introduced concepts like Big Brother and thoughtcrime.',
                'explanation_c': 'Ray Bradbury wrote "Fahrenheit 451", a dystopian novel about book burning.',
                'explanation_d': 'H.G. Wells wrote science fiction novels like "The Time Machine".',
                'reference_link': 'https://en.wikipedia.org/wiki/Nineteen_Eighty-Four',
                'difficulty_level': 'medium'
            },
            {
                'question_text': 'Which Shakespeare play features the line "To be or not to be"?',
                'option_a': 'Macbeth',
                'option_b': 'Romeo and Juliet',
                'option_c': 'Hamlet',
                'option_d': 'Othello',
                'correct_answer': 'C',
                'explanation': 'This famous soliloquy is from Hamlet, spoken by the title character.',
                'explanation_a': 'Macbeth has famous lines like "Out, damned spot!" but not this one.',
                'explanation_b': 'Romeo and Juliet has "Romeo, Romeo, wherefore art thou Romeo?" among others.',
                'explanation_c': 'Correct! This is from Hamlet\'s famous soliloquy in Act 3, Scene 1.',
                'explanation_d': 'Othello has its own memorable quotes but not this particular line.',
                'reference_link': 'https://en.wikipedia.org/wiki/To_be,_or_not_to_be',
                'difficulty_level': 'medium'
            },
            {
                'question_text': 'Who composed "The Four Seasons"?',
                'option_a': 'Johann Sebastian Bach',
                'option_b': 'Wolfgang Amadeus Mozart',
                'option_c': 'Antonio Vivaldi',
                'option_d': 'Ludwig van Beethoven',
                'correct_answer': 'C',
                'explanation': 'Antonio Vivaldi composed "The Four Seasons" around 1720.',
                'explanation_a': 'Bach composed many famous works but not "The Four Seasons".',
                'explanation_b': 'Mozart was a later composer and did not write "The Four Seasons".',
                'explanation_c': 'Correct! Vivaldi\'s "The Four Seasons" is a set of four violin concertos.',
                'explanation_d': 'Beethoven came after Vivaldi and did not compose "The Four Seasons".',
                'reference_link': 'https://en.wikipedia.org/wiki/The_Four_Seasons_(Vivaldi)',
                'difficulty_level': 'hard'
            },
        ]

        # Sports & Entertainment Questions
        sports_questions = [
            {
                'question_text': 'How many players are on a basketball team on the court at one time?',
                'option_a': '4',
                'option_b': '5',
                'option_c': '6',
                'option_d': '7',
                'correct_answer': 'B',
                'explanation': 'In basketball, each team has 5 players on the court at any given time.',
                'explanation_a': '4 players would be missing one position on the court.',
                'explanation_b': 'Correct! Basketball teams have 5 players on court per team.',
                'explanation_c': '6 players would result in a technical foul for too many players.',
                'explanation_d': '7 players is far too many for a basketball court.',
                'reference_link': 'https://en.wikipedia.org/wiki/Basketball',
                'difficulty_level': 'easy'
            },
            {
                'question_text': 'In which sport would you perform a slam dunk?',
                'option_a': 'Tennis',
                'option_b': 'Volleyball',
                'option_c': 'Basketball',
                'option_d': 'Soccer',
                'correct_answer': 'C',
                'explanation': 'A slam dunk is a basketball move where a player jumps and forcefully puts the ball through the hoop.',
                'explanation_a': 'Tennis involves hitting a ball over a net with a racket.',
                'explanation_b': 'Volleyball involves spiking a ball over a net, but not dunking.',
                'explanation_c': 'Correct! Slam dunks are a signature move in basketball.',
                'explanation_d': 'Soccer involves kicking a ball, with no hoops or dunking.',
                'reference_link': 'https://en.wikipedia.org/wiki/Slam_dunk',
                'difficulty_level': 'easy'
            },
            {
                'question_text': 'Which movie won the Academy Award for Best Picture in 2020?',
                'option_a': '1917',
                'option_b': 'Joker',
                'option_c': 'Parasite',
                'option_d': 'Once Upon a Time in Hollywood',
                'correct_answer': 'C',
                'explanation': 'Parasite won Best Picture at the 2020 Academy Awards, making history as the first non-English language film to win.',
                'explanation_a': '1917 was nominated and won several technical awards but not Best Picture.',
                'explanation_b': 'Joker was nominated and Joaquin Phoenix won Best Actor, but it didn\'t win Best Picture.',
                'explanation_c': 'Correct! Parasite made history as the first non-English Best Picture winner.',
                'explanation_d': 'Once Upon a Time in Hollywood was nominated but didn\'t win Best Picture.',
                'reference_link': 'https://en.wikipedia.org/wiki/92nd_Academy_Awards',
                'difficulty_level': 'medium'
            },
            {
                'question_text': 'How many holes are there in a standard round of golf?',
                'option_a': '16',
                'option_b': '18',
                'option_c': '20',
                'option_d': '24',
                'correct_answer': 'B',
                'explanation': 'A standard round of golf consists of 18 holes.',
                'explanation_a': '16 holes would be less than a standard round.',
                'explanation_b': 'Correct! Golf courses have 18 holes for a complete round.',
                'explanation_c': '20 holes would be more than a standard round.',
                'explanation_d': '24 holes would be much more than a standard round.',
                'reference_link': 'https://en.wikipedia.org/wiki/Golf',
                'difficulty_level': 'easy'
            },
            {
                'question_text': 'Which band released the album "Abbey Road"?',
                'option_a': 'The Rolling Stones',
                'option_b': 'Led Zeppelin',
                'option_c': 'The Beatles',
                'option_d': 'Pink Floyd',
                'correct_answer': 'C',
                'explanation': 'The Beatles released "Abbey Road" in 1969, their final recorded album.',
                'explanation_a': 'The Rolling Stones had many famous albums but not "Abbey Road".',
                'explanation_b': 'Led Zeppelin released albums like "Led Zeppelin IV" but not "Abbey Road".',
                'explanation_c': 'Correct! "Abbey Road" was The Beatles\' final studio album.',
                'explanation_d': 'Pink Floyd released "The Dark Side of the Moon" and others, but not "Abbey Road".',
                'reference_link': 'https://en.wikipedia.org/wiki/Abbey_Road',
                'difficulty_level': 'medium'
            },
        ]

        # Add all questions to database
        all_questions = [
            ('Science & Technology', science_questions),
            ('History & Culture', history_questions),
            ('Geography & Nature', geography_questions),
            ('Literature & Arts', literature_questions),
            ('Sports & Entertainment', sports_questions),
        ]

        for category_name, questions in all_questions:
            category = Category.objects.get(name=category_name)
            for q_data in questions:
                question, created = Question.objects.get_or_create(
                    category=category,
                    question_text=q_data['question_text'],
                    defaults=q_data
                )
                if created:
                    self.stdout.write(f'✓ Created question: {question.question_text[:50]}...')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated quiz data!')
        )
        self.stdout.write(f'Total categories: {Category.objects.count()}')
        self.stdout.write(f'Total questions: {Question.objects.count()}')