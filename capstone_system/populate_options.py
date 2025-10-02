import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capstone_system.settings')
django.setup()

from jobs.models import EducationCategory, EducationLevel, EligibilityCategory, EligibilityType

def populate_education():
    print("Populating Education data...")
    
    # Information Technology & Computing
    it_category = EducationCategory.objects.create(
        name="Information Technology & Computing",
        icon="💻",
        order=1
    )
    it_programs = [
        ("BS in Information Technology", "BSIT"),
        ("BS in Computer Science", "BSCS"),
        ("BS in Information Systems", "BSIS"),
        ("BS in Computer Engineering", "BSCpE"),
        ("BS in Entertainment and Multimedia Computing", ""),
        ("BS in Data Science / AI", ""),
    ]
    for idx, (name, abbr) in enumerate(it_programs):
        EducationLevel.objects.create(
            category=it_category,
            name=name,
            abbreviation=abbr,
            order=idx
        )
    
    # Health & Allied Health
    health_category = EducationCategory.objects.create(
        name="Health & Allied Health",
        icon="🏥",
        order=2
    )
    health_programs = [
        ("BS in Nursing", "BSN"),
        ("BS in Medical Technology", "BSMT"),
        ("BS in Pharmacy", "BSP"),
        ("BS in Physical Therapy", "BSPT"),
        ("BS in Occupational Therapy", "BSOT"),
        ("BS in Radiologic Technology", "BSRT"),
        ("BS in Nutrition and Dietetics", ""),
        ("BS in Public Health", ""),
        ("BS in Psychology", ""),
    ]
    for idx, (name, abbr) in enumerate(health_programs):
        EducationLevel.objects.create(
            category=health_category,
            name=name,
            abbreviation=abbr,
            order=idx
        )
    
    # Business, Finance & Management
    business_category = EducationCategory.objects.create(
        name="Business, Finance & Management",
        icon="💰",
        order=3
    )
    business_programs = [
        ("BS in Business Administration", "BSBA"),
        ("BS in Accountancy", "BSA"),
        ("BS in Management Accounting", "BSMA"),
        ("BS in Accounting Information System", "BSAIS"),
        ("BS in Entrepreneurship", ""),
        ("BS in Real Estate Management", ""),
        ("BS in Customs Administration", ""),
        ("BS in Office Administration", ""),
    ]
    for idx, (name, abbr) in enumerate(business_programs):
        EducationLevel.objects.create(
            category=business_category,
            name=name,
            abbreviation=abbr,
            order=idx
        )
    
    # Engineering & Technology
    eng_category = EducationCategory.objects.create(
        name="Engineering & Technology",
        icon="🏗️",
        order=4
    )
    eng_programs = [
        ("BS in Civil Engineering", "BSCE"),
        ("BS in Mechanical Engineering", "BSME"),
        ("BS in Electrical Engineering", "BSEE"),
        ("BS in Electronics Engineering", "BSECE"),
        ("BS in Industrial Engineering", "BSIE"),
        ("BS in Chemical Engineering", "BSChE"),
        ("BS in Sanitary Engineering", ""),
        ("BS in Geodetic Engineering", ""),
        ("BS in Mining Engineering", ""),
    ]
    for idx, (name, abbr) in enumerate(eng_programs):
        EducationLevel.objects.create(
            category=eng_category,
            name=name,
            abbreviation=abbr,
            order=idx
        )
    
    # Social Sciences & Humanities
    social_category = EducationCategory.objects.create(
        name="Social Sciences & Humanities",
        icon="📊",
        order=5
    )
    social_programs = [
        ("AB/BA in Political Science", "AB/BA PolSci"),
        ("AB/BA in Communication", ""),
        ("AB/BA in Sociology", ""),
        ("AB/BA in Psychology", ""),
        ("AB/BA in History", ""),
        ("AB/BA in Philosophy", ""),
        ("AB/BA in Literature / English Studies", ""),
    ]
    for idx, (name, abbr) in enumerate(social_programs):
        EducationLevel.objects.create(
            category=social_category,
            name=name,
            abbreviation=abbr,
            order=idx
        )
    
    # Natural & Applied Sciences
    science_category = EducationCategory.objects.create(
        name="Natural & Applied Sciences",
        icon="🧪",
        order=6
    )
    science_programs = [
        ("BS in Biology", ""),
        ("BS in Chemistry", ""),
        ("BS in Physics", ""),
        ("BS in Environmental Science", ""),
        ("BS in Mathematics / Applied Mathematics", ""),
        ("BS in Statistics", ""),
    ]
    for idx, (name, abbr) in enumerate(science_programs):
        EducationLevel.objects.create(
            category=science_category,
            name=name,
            abbreviation=abbr,
            order=idx
        )
    
    # Arts, Design & Media
    arts_category = EducationCategory.objects.create(
        name="Arts, Design & Media",
        icon="🎨",
        order=7
    )
    arts_programs = [
        ("Bachelor of Fine Arts", "BFA"),
        ("Bachelor of Multimedia Arts", "BMA"),
        ("Bachelor of Arts in Communication / Journalism", ""),
        ("Bachelor of Performing Arts", ""),
        ("Bachelor of Film / Digital Media", ""),
    ]
    for idx, (name, abbr) in enumerate(arts_programs):
        EducationLevel.objects.create(
            category=arts_category,
            name=name,
            abbreviation=abbr,
            order=idx
        )
    
    # Tourism, Hospitality & Service
    tourism_category = EducationCategory.objects.create(
        name="Tourism, Hospitality & Service",
        icon="✈️",
        order=8
    )
    tourism_programs = [
        ("BS in Hospitality Management", "BSHM"),
        ("BS in Tourism Management", "BSTM"),
        ("BS in Hotel and Restaurant Management", "BSHRM"),
        ("BS in Cruise Line Operations", ""),
    ]
    for idx, (name, abbr) in enumerate(tourism_programs):
        EducationLevel.objects.create(
            category=tourism_category,
            name=name,
            abbreviation=abbr,
            order=idx
        )
    
    # Education & Teacher Training
    education_category = EducationCategory.objects.create(
        name="Education & Teacher Training",
        icon="🎓",
        order=9
    )
    education_programs = [
        ("Bachelor of Elementary Education", "BEEd"),
        ("Bachelor of Secondary Education", "BSEd"),
        ("Bachelor of Early Childhood Education", ""),
        ("Bachelor of Physical Education", "BPEd"),
        ("Bachelor of Technical-Vocational Teacher Education", ""),
    ]
    for idx, (name, abbr) in enumerate(education_programs):
        EducationLevel.objects.create(
            category=education_category,
            name=name,
            abbreviation=abbr,
            order=idx
        )
    
    # General/Other
    general_category = EducationCategory.objects.create(
        name="General Education Levels",
        icon="📚",
        order=10
    )
    general_programs = [
        ("High School Diploma", ""),
        ("Senior High School Graduate", ""),
        ("Vocational Course", ""),
        ("Any Bachelor's Degree", ""),
        ("Master's Degree", ""),
        ("Doctorate Degree", "PhD"),
    ]
    for idx, (name, abbr) in enumerate(general_programs):
        EducationLevel.objects.create(
            category=general_category,
            name=name,
            abbreviation=abbr,
            order=idx
        )
    
    print("✅ Education data populated!")


def populate_eligibility():
    print("Populating Eligibility data...")
    
    # Career Service Eligibility
    cs_category = EligibilityCategory.objects.create(
        name="Career Service Eligibility",
        description="Civil Service Commission eligibility examinations",
        order=1
    )
    cs_types = [
        ("Career Service Professional (Second Level Eligibility)", "CS Professional", 
         "For professional or second level positions in government"),
        ("Career Service Sub-Professional (First Level Eligibility)", "CS Sub-Professional",
         "For sub-professional or first level positions in government"),
        ("First Level Eligibility", "First Level",
         "Basic eligibility for clerical and support positions"),
        ("Second Level Eligibility", "Second Level",
         "Higher eligibility for professional positions"),
    ]
    for idx, (name, code, desc) in enumerate(cs_types):
        EligibilityType.objects.create(
            category=cs_category,
            name=name,
            code=code,
            description=desc,
            order=idx
        )
    
    # Professional Board Examinations
    board_category = EligibilityCategory.objects.create(
        name="Professional Board Examinations",
        description="RA 1080 - Bar and Board examinations",
        order=2
    )
    board_types = [
        ("RA 1080 (Bar/Board Eligibility)", "RA 1080",
         "Passing professional licensure exams (Bar, Board of Accountancy, Engineering, etc.)"),
        ("Registered Professional (e.g., CPA, Engineer, Nurse)", "Licensed Professional",
         "Licensed professionals with board certification"),
    ]
    for idx, (name, code, desc) in enumerate(board_types):
        EligibilityType.objects.create(
            category=board_category,
            name=name,
            code=code,
            description=desc,
            order=idx
        )
    
    # Educational Eligibility
    edu_category = EligibilityCategory.objects.create(
        name="Educational Eligibility",
        description="Graduate studies as eligibility basis",
        order=3
    )
    edu_types = [
        ("Master's Degree", "Master's",
         "Holder of Master's degree from recognized institution"),
        ("Doctorate Degree (PhD)", "Doctorate",
         "Holder of Doctorate degree"),
        ("Magna Cum Laude / Summa Cum Laude", "Latin Honors",
         "Graduated with honors from college"),
    ]
    for idx, (name, code, desc) in enumerate(edu_types):
        EligibilityType.objects.create(
            category=edu_category,
            name=name,
            code=code,
            description=desc,
            order=idx
        )
    
    # Special Eligibility
    special_category = EligibilityCategory.objects.create(
        name="Special Eligibility",
        description="Specific eligibilities for certain positions",
        order=4
    )
    special_types = [
        ("MC 11, s. 1996 (Driver's License)", "Driver's License",
         "For driver positions requiring valid driver's license"),
        ("PBET (Professional Board Exam for Teachers)", "PBET",
         "For teaching positions"),
        ("BAR Examination (Lawyer)", "BAR",
         "For legal officer positions"),
        ("PRC License (Specific Profession)", "PRC License",
         "Professional Regulation Commission license"),
    ]
    for idx, (name, code, desc) in enumerate(special_types):
        EligibilityType.objects.create(
            category=special_category,
            name=name,
            code=code,
            description=desc,
            order=idx
        )
    
    # No Eligibility Required
    none_category = EligibilityCategory.objects.create(
        name="No Eligibility Required",
        description="Positions that don't require civil service eligibility",
        order=5
    )
    EligibilityType.objects.create(
        category=none_category,
        name="None Required",
        code="N/A",
        description="Position does not require eligibility",
        order=0
    )
    
    print("✅ Eligibility data populated!")


if __name__ == '__main__':
    print("Starting database population...")
    print("="*50)
    
    # Clear existing data
    print("Clearing existing data...")
    EducationLevel.objects.all().delete()
    EducationCategory.objects.all().delete()
    EligibilityType.objects.all().delete()
    EligibilityCategory.objects.all().delete()
    
    # Populate new data
    populate_education()
    populate_eligibility()
    
    print("="*50)
    print("✅ Database population completed!")
    print(f"Total Education Categories: {EducationCategory.objects.count()}")
    print(f"Total Education Programs: {EducationLevel.objects.count()}")
    print(f"Total Eligibility Categories: {EligibilityCategory.objects.count()}")
    print(f"Total Eligibility Types: {EligibilityType.objects.count()}")