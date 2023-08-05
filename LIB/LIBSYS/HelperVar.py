"""
Holds variables used in the models.
"""

# variables
online = 'ebook'
physical = 'print'
both = 'print/ebook'

active = 'active'
overDue = 'Over Due'
pending = 'Pending'
acquired = 'Acquired'

STATE = [
    (online, online),
    (physical, physical),
    (both, both)
]
# BY: BEN MUNYASIA BCSC01/0018/2018
STATUS = [
    (active, 'Active'),
    (overDue, 'Over Due')
]

REQUEST_STATUS = [
    (pending, 'Pending'),
    (acquired, 'Acquired')
]

GENRE = [
    ('Engineering', (
        ('Civil Engineering', 'Civil Engineering'),
        ('Software Engineering', 'Software Engineering'),
        ('Computer Science', 'Computer Science')
    )
     ),
    ('Economics', (
        (' Classical economics', ' Classical economics'),
        ('Neo-classical economics', 'Neo-classical economics')
    )

     ),
    ('Novel', 'Novel'),
    ('Science', 'Science'),
    ('Business', 'Business'),
    ('Mathematics', 'Mathematics'),

]
FINESTATUS = [
    ('Unpaid', 'Unpaid'),
    ('Paid', 'Paid')
]

main_exam = "Main exam"
cat = "CAT"

TYPE_OF_EXAM = [
    (main_exam, main_exam),
    (cat, cat)
]

library_of_congress = {
    'A': 'General Works (encyclopedias, dictionaries, etc.)',
    'B': 'Philosophy',
    'BF': 'Psychology',
    'BL-BX': 'Religion',
    'C': 'Genealogy, Biography',
    'D': 'History-General & Eastern Hemispheres',
    'E-F': 'History--Americas',
    'G': 'Geography, Anthropology, Recreation',
    'HB-HJ': 'Business & Economics',
    'HM-HQ': "Sociology, Family, Women's Studies",
    'J': 'Political Sciences',
    'K': 'Law',
    'L': 'Education',
    'M': 'Music and books on Music',
    'N': 'Fine Arts',
    'P': 'Language & Literature',
    'Q-QD': 'Math, Physics, Chemistry',
    'QE': 'Geology',
    'QH-QK': 'Biology, Botany',
    'QL-QR': 'Zoology, Physiology, Microbiology',
    'TA-TK': 'Engineering, Computing',
    'U': 'Military Science',
    'V': 'Naval Science',
    'Z': 'History of Books & Printing, Library Science, Bibliography'
}
