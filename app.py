import base64
import enum
import io
import os
from enum import Enum as EnumBase
from os.path import join

import requests
from flask import (Flask, jsonify, request, send_file, send_from_directory,
                   url_for)
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt
from sqlalchemy import (ARRAY, Enum, ForeignKey, Integer, LargeBinary, String,
                        Table)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from werkzeug.utils import secure_filename

# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{join(app.root_path, 'projectdetails.db')}"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

app.config['SECRET_KEY'] = '1GPkJM2AJOtRck5lJFDDlC1C2L-0VSbGmxKWx4sSSYY'
# Define your UPLOAD_FOLDER
app.config['getimage'] = './getimage'

basedir = os.path.abspath(os.path.dirname(__file__))
uploads_path = os.path.join(basedir, 'uploads') 

# Sign up
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = bcrypt.hash(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    # Establish a one-to-one relationship with other models
    # userdetails = db.relationship('User', back_populates='person')
    biography = db.relationship('Biography', back_populates='person')
    topic_descriptions = db.relationship('TopicDescription', back_populates='person')
    testimonials = db.relationship('Testimonial', back_populates='person')
    images = db.relationship('Images', back_populates='person')
    video = db.relationship('Video', back_populates='person')
    podcasts = db.relationship('Podcast', back_populates='person')
    books = db.relationship('Book', back_populates='person')
    media_mentions = db.relationship('MediaMention', back_populates='person')
    white_papers_case_studies = db.relationship('WhitePaperCaseStudy', back_populates='person')
    degree_files = db.relationship('DegreesCertificatesAwards', back_populates='person')
    # certificate_files = db.relationship('Certificates', back_populates='person')
    # awards_files = db.relationship('Awards', back_populates='person')
    speaker_contact_information = db.relationship('SpeakerContactInformation', back_populates='person', uselist=False)
    manager_or_teammate = db.relationship('ManagerOrTeammate', back_populates='person', uselist=False)
    social_media_personal = db.relationship('SocialMediaPersonal', back_populates='person', uselist=False)
    business_info = db.relationship('BusinessInfo', back_populates='person', uselist=False)
    social_media_business = db.relationship('SocialMediaBusiness', back_populates='person', uselist=False)
    brand_campaignstheme1 = db.relationship('BrandCampaignOrganizationtheme1', back_populates='person')
    brand_campaignstheme2 = db.relationship('BrandCampaignOrganizationtheme2', back_populates='person')
    at_events = db.relationship('AtEvents',back_populates='person',uselist=False)
    help_us_book_you = db.relationship('HelpUsBookYou', uselist=False, back_populates='person')
    help_us_work_with_you = db.relationship('HelpUsWorkWithYou', uselist=False, back_populates='person')
    fees = db.relationship('Fees', uselist=False, back_populates='person')
    speaker_pitches = db.relationship('SpeakerPitch', back_populates='person')
    previous_clients = db.relationship('PreviousClient', back_populates='person', cascade='all, delete-orphan')
    
# Define the User model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     username = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255))

#     def __init__(self, email, username, password, person_id):
#         self.email = email
#         self.username = username
#         self.password = bcrypt.hash(password)
#         self.person_id = person_id

#     def verify_password(self, password):
#         return bcrypt.verify(password, self.password)

#     # Define a foreign key relationship with Person
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
#     person = db.relationship('Person', back_populates='userdetails')   


# #  Define the Biography model
# class Biography(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     highlight = db.Column(db.Text)
#     long_bio = db.Column(db.Text)
#     sort_bio = db.Column(db.Text)
#     speaker_topics = db.Column(db.String(255))
#     speaker_topics_additional_keywords = db.Column(db.String(255))
#     speaker_tags = db.Column(db.String(255))
#     descriptive_title_type = db.Column(db.String(255))
#     descriptive_title_1 = db.Column(db.String(255))
#     descriptive_title_2 = db.Column(db.String(255))
#     descriptive_title_3 = db.Column(db.String(255))
#     city = db.Column(db.String(255))
#     province_state = db.Column(db.String(255))
#     microphonetext = db.Column(db.Text)
#     microphone = db.Column(LargeBinary)
    
#     # Define a foreign key relationship with Person
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
#     person = db.relationship('Person', back_populates='biography')

# class SpeakerTopicEnum(EnumBase):
#     pass
#     ReactJs = 'react'
#     Html = 'html'
#     NextJs = 'nextjs'
#     JavaScript = 'javascript'

# class SpeakerTopicEnum:
#     # Define a class-level attribute to store the dictionary
#     topic_dict = {}
#     pass

class SpeakerTopicEnum(EnumBase):
    Accessibility = 'accessibility'
    Adaptability__amp_Agility = 'adaptability_amp_agility'
    Addictions__amp_Substance_Abuse = 'addictions_amp_substance_abuse'
    Alliances__amp_Partnerships = 'alliances_amp_partnerships'
    Artificial_Intelligence_AI = 'artificial_intelligenceAI'
    Big_Data = 'bigdata'
    Blockchain__amp_Metaverse = 'blockchain_amp_metaverse'
    Bullying_At_Work = 'bullyingatwork'    
    Burnout_Prevention = 'burnoutprevention'
    Business__amp_Corporate = 'business_amp_corporate'
    Business_Ethics__amp_Values = 'business_ethics_amp_values'
    Business_Growth = 'businessgrowth'
    Business_Leadership = 'business_leadership'
    Business_Management = 'business_management'
    Business_Technology = 'business_technology'
    Business_Transitions = 'business_transitions'
    Change_Management = 'change_management'
    Collaboration = 'collaboration'
    Communications = 'communications'
    Conflict_Resolution = 'conflict_resolution'
    Consumer_Behaviour__amp_Retail = 'consumer_behaviour_amp_retail'
    Corporate_Responsibility_CSR = 'corporate_responsibility_CSR'
    Cultural_Diversity = 'cultural_diversity'
    Customer_service = 'customer_service'
    Cyber_Security = 'cyber_security'
    Digital_marketing = 'digital_marketing' 
    Disability = 'disability'
    Disruption_Management = 'disruption_management'
    Disruptive_Innovation = 'disruptive_innovation'
    Diversity__amp_Inclusion = 'Diversity_amp_inclusion'
    Economics = 'economics'
    Emotional_Intelligence = 'emotional_intelligence'
    Employee_Engagement = 'employee_engagement'
    Employee_Management = 'employee_management'
    Employee_Retention = 'employee_retention'
    Entrepreneurship = 'entrepreneurship'
    Excellence__amp_Success = 'Excellence_amp_success'
    Future_of_Work = 'future_of_work'
    Future_Trends = 'future_trends'
    Futurists = 'futurists'
    Gender_Equality = 'gender_equality'
    Generations_At_Work = 'generations_at_work'
    Genrational_Differences = 'genrational_differences'
    Global_Business_Solutions = 'global_business_solutions'
    Happiness__amp_Positivity = 'happiness_amp_positivity'
    Health__amp_Human_Performance = 'health_amp_human_performance'
    Health__amp_Wellness = 'health_amp_wellness'
    HR__amp_Corporate_Culture = 'hr_amp_corporate_culture'
    Humour_At_Workplace = 'humour_at_workplace'
    Inclusive_Leadership = 'inclusive_leadership'
    Indigenous = 'indigenous'
    Influence__amp_Negotiation = 'influence_amp_negotiation'
    Innovation__amp_Creativity = 'innovation_amp_creativity' 
    Inter_Generational_Workplace = 'inter_generational_workplace'
    Leadership = 'leadership'
    Leadership__amp_Change = 'leadership_amp_change'
    Leadership_Development = 'leadership_development'
    LGBTQ2S = 'LGBTQ2S+'
    Marketing__amp_Branding = 'marketing_amp_branding'
    Memory_networking = 'memory_networking'
    Mental_Health = 'mental_health'
    Mentoring_At_Work = 'mentoring_at_work'
    Mergers__amp_Acquisitions = 'mergers_amp_acquisitions'
    Mindfulness = 'mindfulness'
    Mindset__amp_Attitude = 'mindset_amp_attitude'
    Mindset__amp_Goal_Accomplishment = 'mindset_amp_goal_accomplishment'
    Neurodiversity = 'neurodiversity'
    Nutrition__amp_Fitness = 'nutrition_amp_fitness'
    Organizational_Change = 'organizational_change'
    Organizational_Leadership = 'organizational_leadership'
    Peak_Performance = 'peak_performance'
    Personal_Growth = 'personal_growth'
    Personal_Leadership = 'personal_leadership'
    Positive_Psychology = 'positive_psychology'
    Presentation_Skills = 'presentation_skills'
    Privacy = 'privacy'   
    Process__amp_Systems = 'process_amp_systems'
    Project_Management = 'project_management'
    Psychological_Safety = 'psychological_safety'
    PTSD__amp_Trauma = 'ptsd_amp_trauma'
    Public_Relations = 'public_relations'
    Purposeful_Work = 'purposeful_work'
    Racial_Justice = 'racial_justice'
    Resilience__amp_Adversity = 'resilience_amp_adversity'
    Resilience__amp_Change = 'resilience_amp_change'
    Sales = 'sales'
    Self_Improvement__amp_Self_Care = 'self_improvement_amp_self_care' 
    Small_Business_Development = 'small_business_development'
    Social_media = 'social_media'
    Soft_Skills_Development = 'soft_skills_development'
    STEM = 'stem'
    Strategic_thinking = 'strategic_thinking'
    Stress_Management = 'stress_management'
    Suicide_Prevention = 'suicide_prevention'
    Talent_Management = 'talent_management'
    Teamwork = 'teamwork'
    Tech_trends = 'tech_trends'
    Time_Management = 'time_management'
    Transformation = 'transformation'
    Trust_Relationships = 'trust_relationships'
    Unconscious_Bias = 'unconscious_bias'
    Women_In_Business = 'women_in_business'
    Women_Of_Influence = 'women_of_influence'
    Womens_Leadership = 'womens_leadership'
    Womens_Rights__amp_MeToo = 'womens_rights_amp_metoo'
    Work_Life_Balance ='work_life_balance'
    Workplace_Culture = 'workplace_culture'
     
# Model for storing speaker topics
class SpeakerTopic(db.Model):
    id = db.Column(Integer, primary_key=True)
    topic = db.Column(Enum(SpeakerTopicEnum))
    
    def add_speaker_topic(topic):
        if SpeakerTopic.query.filter_by(topic=topic).first() is None:
            new_topic = SpeakerTopic(topic=topic)
            db.session.add(new_topic)
            db.session.commit()
        else:
            print(f"Topic '{topic}' already exists.")
      
speaker_topic_association = Table(
    'speaker_topic_association',
    db.metadata,
    db.Column('biography_id', Integer, db.ForeignKey('biography.id')),
    db.Column('speaker_topic_id', Integer, db.ForeignKey(SpeakerTopic.id))
)

class SpeakerTagEnum(EnumBase):
    ReactJs = 'reactjs'
    Html = 'html'
    Java = 'java'
    Python = 'python'
    
class SpeakerTag(db.Model):
    id = db.Column(Integer, primary_key=True)
    tag = db.Column(Enum(SpeakerTagEnum))
    
    def add_speaker_tag(tag):
        if SpeakerTag.query.filter_by(tag=tag).first() is None:
            new_tag = SpeakerTag(tag=tag)
            db.session.add(new_tag)
            db.session.commit()
        else:
            print(f"Topic '{tag}' already exists.")
      
speaker_tag_association = Table(
    'speaker_tag_association',
    db.metadata,
    db.Column('biography_id', Integer, db.ForeignKey('biography.id')),
    db.Column('speaker_tag_id', Integer, db.ForeignKey(SpeakerTag.id))
)    


class DescriptiveTitlesEnum(EnumBase):
    Academia = 'academia'
    Adventurers = 'adventurers'
    Agriculture__amp_Farming = 'agriculture__amp_farming'
    All_Staff_Meeting = 'all_staff_meeting'
    Annual_General_Meetings = 'annual_general_meetings'
    Associations__amp_Unions = 'associations__amp_unions'
    Athletes__amp_Sports = 'athletes__amp_sports'
    Award_Galas__amp_After_Dinner = 'award_galas__amp_after_dinner'
    Awareness_Days = 'awareness_days'
    Bilingual__amp_French = 'bilingual__amp_french'
    Board_Meetings__amp_Strategic_Advisory = 'board_meetings__amp_strategic_advisory'
    Campus__amp_University_Speakers = 'campus__amp_university_speakers'
    Cancer_Awareness = 'cancer_awareness'
    Career_Development = 'career_development'
    Celebrity = 'celebrity'
    Certified_Speakers = 'certified_speakers'
    Certified_Speaking_Professionals_CSP = 'certified_speaking_professionals_csp'
    Charities__amp_Foundations = 'charities__amp_foundations'
    Community_Engagement_Events = 'community_engagement_events'
    Conference = 'conference'
    Conferences__amp_Summits = 'conferences__amp_summits'
    Consultant__amp_Coach = 'consultant__amp_coach'
    Corporate_Audience = 'corporate_audience'
    Corporate_Entertainers = 'corporate_entertainers'
    Corporations__amp_Businesses = 'corporations__amp_businesses'
    Department_Meeting = 'department_meeting'
    Economic_Development = 'economic_development'
    Education__amp_Teachers = 'education__amp_teachers'
    Endorsement__amp_Product_Launch = 'endorsement__amp_product_launch'
    Environment__amp_Climate_Change = 'environment__amp_climate_change'
    Event_Hosts__amp_Moderators = 'event_hosts__amp_moderators'
    Executive_Leadership__amp_C_Suite = 'executive_leadership__amp_c_suite'
    Family__amp_Parenting = 'family__amp_parenting'
    Finance__amp_Insurance = 'finance__amp_insurance'
    First_Nation_Motivational_Speakers = 'first_nation_motivational_speakers'
    First_Responders = 'first_responders'
    Fundraisers__amp_Banquets = 'fundraisers__amp_banquets'
    Funny__amp_Comedy = 'funny__amp_comedy'
    Government_Departments__amp_Agencies = 'government_departments__amp_agencies'
    Guest_Panelist__amp_Guided_Q_ampA = 'guest_panelist__amp_guided_q_ampa'
    Hall_of_Fame = 'hall_of_fame'
    Health_and_Safety = 'health_and_safety'
    Healthcare = 'healthcare'
    Home__amp_Garden = 'home__amp_garden'
    Hybrid_Workplace = 'hybrid_workplace'
    Industry_types = 'industry_types'
    Infrastructure__amp_Urban_Planning = 'infrastructure__amp_urban_planning'
    Inspirational = 'inspirational'
    Interactive__amp_Experience = 'interactive__amp_experience'
    Key_Note = 'key_note'
    Lifestyle__amp_Health = 'lifestyle__amp_health'
    Managing_remote_employees = 'managing_remote_employees'
    Medical__amp_Healthcare = 'medical__amp_healthcare'
    Men = 'men'
    Mentalists__amp_Hypnotists = 'mentalists__amp_hypnotists'
    Military = 'military'
    Most_Requested = 'most_requested'
    Motivation = 'motivation' 
    Mountain_Climbers = 'mountain_climbers'
    Non_Binary = 'non_binary'
    Olympians__amp_Olympics = 'olympians__amp_olympics'
    Opening__amp_Closing_Keynote = 'opening__amp_closing_keynote'
    Orateur__amp_Conférencier = 'orateur__amp_conférencier'
    Patient_Safety__amp_Patient_Care = 'patient_safety__amp_patient_care'
    Philanthropy__amp_Giving_Back = 'philanthropy__amp_giving_back'
    Pofessional_development_days_PD_DAYS = 'pofessional_development_days_pd_days'
    Politicians = 'politicians'
    Presentation_formats = 'presentation_formats'
    Real_Estate  = 'real_estate'
    Research__amp_Science = 'research__amp_science'
    Safety = 'safety'
    Sales_Motivation__amp_Sales_Kick_Off = 'sales_motivation__amp_sales_kick_off'
    School_boards = 'school_boards'
    Scientific__amp_Technical = 'scientific__amp_technical'
    Social__amp_Cultural = 'social__amp_cultural'
    Social_Justice__amp_Human_Rights = 'social_justice__amp_human_rights'
    Sort_by = 'sort_by'
    Speaker_Types = 'speaker_types'
    Staff_Appreciation__amp_Employee_Recognition = 'staff_appreciation__amp_employee_recognition'
    Storytelling = 'storytelling'
    Sustainable_Development = 'sustainable_development'
    TED__amp_TEDx = 'ted__amp_tedx'
    Town_Halls__amp_Retreats = 'town_halls__amp_retreats'
    Trade_Shows__amp_Conventions = 'trade_shows__amp_conventions'
    Under_5000 = 'Under $5,000'
    Virtual__amp_Online_Meetings = 'virtual__amp_online_meetings'
    Virtual_engagement = 'virtual_engagement'
    Virtual_Speakers = 'virtual_speakers'
    Virtual_teams__amp_Remote_workers = 'virtual_teams__amp_remote_workers'
    Women = 'women'
    Workshop__amp_Training = 'workshop__amp_training'
    Youth_Leadership__amp_Students = 'youth_leadership__amp_students'
    Youth_Leadership_and_Student_Empowerment = 'youth_leadership_and_student_empowerment'
    
    
class DescriptiveTitles(db.Model):
    id = db.Column(Integer, primary_key=True)
    title = db.Column(Enum(DescriptiveTitlesEnum))
    
    def add_descriptive_title(title):
        if DescriptiveTitles.query.filter_by(title=title).first() is None:
            new_tag = DescriptiveTitles(title=title)
            db.session.add(new_tag)
            db.session.commit()
        else:
            print(f"Topic '{title}' already exists.")
      
descriptive_title_association = Table(
    'descriptive_title_association',
    db.metadata,
    db.Column('biography_id', Integer, db.ForeignKey('biography.id')),
    db.Column('descriptive_title_id', Integer, db.ForeignKey(DescriptiveTitles.id))
)    

      
#  Define the Biography model
class Biography(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    highlight = db.Column(db.Text)
    long_bio = db.Column(db.Text)
    sort_bio = db.Column(db.Text)
    speaker_topics_additional_keywords = db.Column(db.Text)
    descriptive_title_type = db.Column(db.String(255))
    city = db.Column(db.String(255))
    province_state = db.Column(db.String(255))
    microphonetext = db.Column(db.Text)
    microphone = db.Column(LargeBinary)
    speaker_topics = relationship("SpeakerTopic", secondary=speaker_topic_association)
    speaker_tags = relationship("SpeakerTag", secondary=speaker_tag_association)
    descriptive_titles = relationship("DescriptiveTitles", secondary=descriptive_title_association)
   


    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='biography')   
      

    
class TopicDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body_text = db.Column(db.Text)
    delivered_as = db.Column(db.String(255))
    audio_clip = db.Column(LargeBinary)
    audiotext = db.Column(db.Text)
    video_clip = db.Column(db.String(255))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='topic_descriptions')   


# Define the Testimonial model
class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organizer_name = db.Column(db.String(255))
    organization_name = db.Column(db.String(255))
    link_to_video = db.Column(db.String(255))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='testimonials')
    
    
class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_data = db.Column(LargeBinary)
    image_name = db.Column(db.String(255))
    croped_image_data = db.Column(LargeBinary)
    crop_image_name = db.Column(db.String(255))
    own_right = db.Column(db.Boolean, nullable=False)
    sbc_permission = db.Column(db.Boolean, nullable=False)
    
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='images') 

# class Images(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     own_right = db.Column(db.Boolean, nullable=False)
#     sbc_permission = db.Column(db.Boolean, nullable=False)
    
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
#     person = db.relationship('Person', back_populates='images') 

#     # Define a one-to-many relationship with ImageData
#     image_data = db.relationship('ImageData', back_populates='image', cascade='all, delete-orphan')

#     # Define a one-to-many relationship with CroppedImageData
#     cropped_image_data = db.relationship('CroppedImageData', back_populates='image', cascade='all, delete-orphan')


# class ImageData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     image_data = db.Column(db.LargeBinary)

#     # Define a foreign key relationship with Images
#     image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
#     image = db.relationship('Images', back_populates='image_data')


# class CroppedImageData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     cropped_image_data = db.Column(db.LargeBinary)

#     # Define a foreign key relationship with Images
#     image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
#     image = db.relationship('Images', back_populates='cropped_image_data')

    
    
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    hd_quality = db.Column(db.Boolean, nullable=False)
    own_rights = db.Column(db.Boolean, nullable=False)
    grant_permission = db.Column(db.Boolean, nullable=False)
    reason = db.Column(db.String(200))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='video')
    

class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link = db.Column(db.String(255))
    source = db.Column(db.String(255))

    # Define foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='podcasts')


# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upload_book_image = db.Column(LargeBinary)
    book_name = db.Column(db.String(255))
    title = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    authors = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    link = db.Column(db.String(255))
    cost_per_book_cad = db.Column(db.String(255))
    bulk_order_purchase_offered = db.Column(db.Boolean)
    price_per_book_cad = db.Column(db.String(255))
    number_of_books = db.Column(db.Integer)

    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='books')    

# # Define the Book model
# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255))
#     description = db.Column(db.String(1000))
#     authors = db.Column(db.String(255))
#     publisher = db.Column(db.String(255))
#     link = db.Column(db.String(255))
#     cost_per_book_cad = db.Column(db.String(255))
#     bulk_order_purchase_offered = db.Column(db.Boolean)
#     price_per_book_cad = db.Column(db.String(255))
#     number_of_books = db.Column(db.Integer)

#     # Define a one-to-many relationship with BookImageData
#     upload_book_images = db.relationship('BookImageData', back_populates='book', cascade='all, delete-orphan')

#     # Define a foreign key relationship with Person
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
#     person = db.relationship('Person', back_populates='books')


# # Define the BookImageData model
# class BookImageData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     image_data = db.Column(db.LargeBinary)

#     # Define a foreign key relationship with Book
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
#     book = db.relationship('Book', back_populates='upload_book_images')


# class BulkOrderDetail(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     price_per_book_cad = db.Column(db.String(255))
#     number_of_books = db.Column(db.Integer)

#     # Define a foreign key relationship with Book
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
#     book = db.relationship('Book', back_populates='bulk_order_details')
    
class MediaMention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(255))
    interview_article_title = db.Column(db.String(255))
    link = db.Column(db.String(255))
    date = db.Column(db.String(255))
    interview_source_name = db.Column(db.String(255))

    # Define foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='media_mentions')    
    
# class MediaMention(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     organization_name = db.Column(db.String(255))
#     written_interview = db.Column(db.Boolean)
#     audio_interview = db.Column(db.Boolean)
#     video_interview = db.Column(db.Boolean)
#     film = db.Column(db.Boolean)
#     link = db.Column(db.String(255))
#     date = db.Column(db.String(255))
#     interview_source_name = db.Column(db.String(255))

#     # Define foreign key relationship with Person
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
#     person = db.relationship('Person', back_populates='media_mentions')

# Define the WhitePaperCaseStudy model
class WhitePaperCaseStudy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(255))
    title = db.Column(db.String(255))
    topics = db.Column(db.String(255))
    description = db.Column(db.Text)
    link = db.Column(db.String(255))
    date = db.Column(db.String(10))
    
    # Define foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='white_papers_case_studies')

class DegreesCertificatesAwards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree_data = db.Column(LargeBinary)
    degreescertificatesawards_name = db.Column(db.String(255))
    
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='degree_files') 
    
    
# class Certificates(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     certifications_data = db.Column(LargeBinary)
    
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
#     person = db.relationship('Person', back_populates='certificate_files')  
    
    
# class Awards(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     awards_data = db.Column(LargeBinary)
    
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
#     person = db.relationship('Person', back_populates='awards_files')        
    
# Define the SpeakerContactInformation model
class SpeakerContactInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    middle_initials = db.Column(db.String(10))
    secondary_names_nick_name = db.Column(db.String(50))
    pronouns = db.Column(db.String(50))
    cell_phone = db.Column(db.String(20))
    main_email = db.Column(db.String(100))
    website_link = db.Column(db.String(200))
    rss_blog_link = db.Column(db.String(200))
    rss_blog_link_2 = db.Column(db.String(200))
    closest_major_airport = db.Column(db.String(50))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='speaker_contact_information')

# Define the ManagerOrTeammate model
class ManagerOrTeammate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assist_coordinating = db.Column(db.Boolean)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    pronouns = db.Column(db.String(50))
    cell_phone = db.Column(db.String(20))
    main_email = db.Column(db.String(100))
    website = db.Column(db.String(200))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='manager_or_teammate')

# Define the SocialMediaPersonal model
class SocialMediaPersonal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facebook_link = db.Column(db.String(200))
    facebook_handle = db.Column(db.String(50))
    facebook_followers = db.Column(db.String(50))
    instagram_link = db.Column(db.String(200))
    instagram_handle = db.Column(db.String(50))
    instagram_followers = db.Column(db.String(50))
    twitter_link = db.Column(db.String(200))
    twitter_handle = db.Column(db.String(50))
    twitter_followers = db.Column(db.String(50))
    linkedin_link = db.Column(db.String(200))
    linkedin_handle = db.Column(db.String(50))
    linkedin_followers = db.Column(db.String(50))
    tiktok_link = db.Column(db.String(200))
    tiktok_handle = db.Column(db.String(50))
    tiktok_followers = db.Column(db.String(50))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='social_media_personal')
    


# Define the BusinessInfo model
class BusinessInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_payment = db.Column(db.Boolean)
    official_business_name = db.Column(db.String(100))
    business_email = db.Column(db.String(100))
    business_phone = db.Column(db.String(15))
    business_number = db.Column(db.String(20))
    website = db.Column(db.String(200))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='business_info')

# Define the SocialMediaBusiness model
class SocialMediaBusiness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facebook_link = db.Column(db.String(200))
    facebook_handle = db.Column(db.String(50))
    facebook_followers = db.Column(db.String(50))
    instagram_link = db.Column(db.String(200))
    instagram_handle = db.Column(db.String(50))
    instagram_followers = db.Column(db.String(50))
    twitter_link = db.Column(db.String(200))
    twitter_handle = db.Column(db.String(50))
    twitter_followers = db.Column(db.String(50))
    linkedin_link = db.Column(db.String(200))
    linkedin_handle = db.Column(db.String(50))
    linkedin_followers = db.Column(db.String(50))
    tiktok_link = db.Column(db.String(200))
    tiktok_handle = db.Column(db.String(50))
    tiktok_followers = db.Column(db.String(50))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='social_media_business')

class BrandCampaignOrganizationtheme1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_of_social_media = db.Column(db.Boolean)
    
    organization_name = db.Column(db.String(255))
    platforms = db.Column(db.String(255))
    link_to_campaign = db.Column(db.String(255))
    start_year = db.Column(db.String(4))
    end_year = db.Column(db.String(4))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='brand_campaignstheme1')
    
    
class BrandCampaignOrganizationtheme2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_of_social_media = db.Column(db.Boolean)
    
    organization_name = db.Column(db.String(255))
    platforms = db.Column(db.String(255))
    link_to_campaign = db.Column(db.String(255))
    start_year = db.Column(db.String(4))
    end_year = db.Column(db.String(4))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='brand_campaignstheme2')    


# Define the AtEvents model
class AtEvents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    using_presentation_software = db.Column(db.Boolean)
    presentation_software_name = db.Column(db.String(255))
    
    using_audience_interaction_software = db.Column(db.Boolean)
    audience_interaction_software_name = db.Column(db.String(255))
    
    attending_sessions_before_after_presentation = db.Column(db.Boolean)
    
    attending_meals_networking_sessions = db.Column(db.Boolean)
    dietary_requirements_restrictions = db.Column(db.String(255))
    A_V_requirements = db.Column(db.String(255))
    prefer_to_book_travel = db.Column(db.String(255))
    
    # Define speaker_introduction as a separate table
    speaker_introduction = db.relationship('SpeakerIntroduction', back_populates='at_events', uselist=True, cascade='all, delete-orphan')
    
    prefer_to_book_travel= db.Column(db.Boolean)
    
    use_travel_agent = db.Column(db.Boolean)
    Preferred_Seating = db.Column(db.String(255))
    Preferred_Airline = db.Column(db.String(255))
    West_Jet_number = db.Column(db.String(255))
    Air_Canada_number = db.Column(db.String(255))
    
    special_conditions_for_travel_arrangements = db.Column(db.Boolean)
    table_for_book_sales = db.Column(db.Boolean)
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='at_events')

# Define the SpeakerIntroduction model
class SpeakerIntroduction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    introduction_text = db.Column(db.String(255))
    
    # Define a foreign key relationship with AtEvents
    at_events_id = db.Column(db.Integer, db.ForeignKey('at_events.id'))
    at_events = db.relationship('AtEvents', back_populates='speaker_introduction')   

 

class HelpUsBookYou(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speaker_reason_to_work_with = db.Column(db.String(255))
    
    value_adds_and_offerings = db.Column(db.Boolean)
    books_how_many_items = db.Column(db.String(255))
    books_value_per_item = db.Column(db.String(255))
    online_training_how_many_items = db.Column(db.String(255))
    online_training_value_per_item = db.Column(db.String(255))
    merch_how_many_items = db.Column(db.String(255))
    merch_value_per_item = db.Column(db.String(255))
    merch_2_how_many_items = db.Column(db.String(255))
    merch_2_value_per_item = db.Column(db.String(255))
    
    complementary_virtual_follow_sessions_consultation = db.Column(db.Boolean)
    inclusive_of_travel_expenses = db.Column(db.String(255))
    
    industries_do_you_not_work_with = db.Column(db.String(255))
    favorite_audiences_event_types = db.Column(db.String(255))
    target_audiences_industries = db.Column(db.String(255))
    
    English_French = db.Column(db.Boolean)
    Q_A_in_French = db.Column(db.Boolean)
    offer_recordings = db.Column(db.Boolean)
    primary_source_of_income = db.Column(db.Boolean)
    
    hoping_for_speaking_to_become_your_primary_source_income = db.Column(db.Boolean)
    current_speak_per_month = db.Column(db.String(255))
    virtual_events_over_pandemic = db.Column(db.String(255))
    speak_per_month = db.Column(db.String(255))
    market_yourself_as_a_speaker = db.Column(db.String(255))
    affiliated_with_any_other_speakers_agencies = db.Column(db.String(255))
    percentage_of_bookings = db.Column(db.String(255))
    Approximately_what_percentage = db.Column(db.String(255))
    speakers_are_you_affiliated_with = db.Column(db.String(255))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='help_us_book_you')
 

# Define the HelpUsWorkWithYou model
class HelpUsWorkWithYou(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    newsletter_onboarding = db.Column(db.String(255))
    tracking_system = db.Column(db.Boolean)
    whatsapp = db.Column(db.Boolean)
    business_ownership = db.Column(db.Boolean)
    crm_usage = db.Column(db.String(255))
    appointment_booking_software = db.Column(db.String(255))
    expectations_with_sbc = db.Column(db.String(255))
    something_about_you = db.Column(db.String(255))
    stories = db.Column(db.String(255))

    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='help_us_work_with_you')


# Define the Fees model
class Fees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Pro_Bono_Events = db.Column(db.String(255))
    
    Corporate_Keynote_20_60_Minutes = db.Column(db.String(255))
    Corporate_Workshop_60_120_Minutes = db.Column(db.String(255))
    Corporate_Half_Day_Training_or_Keynote_Breakout = db.Column(db.String(255))
    Corporate_Full_Day_Training = db.Column(db.String(255))
    
    Concurrent_Sessions_Fee = db.Column(db.String(255))
    One_Session_in_the_Morning_Fee = db.Column(db.String(255))
    One_Session_in_the_Afternoon_Fee = db.Column(db.String(255))
    
    Multiple_Sessions_on_Concurrent_Days = db.Column(db.String(255))
    Multiple_Sessions_Over_a_Period_of_Time = db.Column(db.String(255))
    
    Lowest_Acceptance_for_Informal_Talk = db.Column(db.String(255))
    
    One_Day_Event = db.Column(db.String(255))
    One_Day_Plus_Evening_Ceremony_Keynote = db.Column(db.String(255))
    Two_Day_Event = db.Column(db.String(255))
    Two_Day_Plus_Evening_Ceremony_Keynote = db.Column(db.String(255))
    Three_Day_Event = db.Column(db.String(255))
    Three_Day_Plus_Evening_Ceremony_Keynote = db.Column(db.String(255))
    Four_Day_Event = db.Column(db.String(255))
    Four_Day_Plus_Evening_Ceremony_Keynote = db.Column(db.String(255))
    What_is_your_corporate_speaker_fee = db.Column(db.String(255))
    lowest_you_will_accept = db.Column(db.String(255))
    limitations_or_condition = db.Column(db.String(255))
    Driving_Distance_Fee = db.Column(db.String(255))
    Province_Fee = db.Column(db.String(255))
    Western_Canada_Fee = db.Column(db.String(255))
    Eastern_Canada_Fee = db.Column(db.String(255))
    Northern_Canada_Fee = db.Column(db.String(255))
    Remote_Location_Fee = db.Column(db.String(255))
    
    Local_Discount = db.Column(db.Boolean)
    Local_Fee = db.Column(db.String(255))
    Client_Direct_Approach_for_Local_Event = db.Column(db.String(255))
    
    Virtual_Discount = db.Column(db.Boolean)
    Virtual_Fee = db.Column(db.String(255))
    Client_Direct_Approach_for_Virtual_Event = db.Column(db.String(255))
    
    Small_Audience_Discount = db.Column(db.Boolean)
    Small_Audience_Fee = db.Column(db.String(255))
    Client_Direct_Approach_for_Small_Audience_Event = db.Column(db.String(255))
    Qualification_for_Small_Audience = db.Column(db.String(255))
    
    Nonprofit_Discount = db.Column(db.Boolean)
    Nonprofit_Fee = db.Column(db.String(255))
    Client_Direct_Approach_for_Nonprofit = db.Column(db.String(255))
    
    Charitable_Organization_Discount = db.Column(db.Boolean)
    Charitable_Fee = db.Column(db.String(255))
    Client_Direct_Approach_for_Charitable_Organization = db.Column(db.String(255))
    outside_of_speaker_fee_ranges = db.Column(db.String(255))
    
    Rate_Increase = db.Column(db.Boolean)
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='fees')
    
   
class SpeakerPitch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    general_pitch = db.Column(db.String(255))
    keyword_topic_focus_pitch = db.Column(db.String(255))
    Short_pitch_up = db.Column(db.String(255))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='speaker_pitches') 
    
class PreviousClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(255))
    
    # Define a foreign key relationship with Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='previous_clients') 
    
with app.app_context():
    db.create_all()

# # POST API of Person 
# @app.route('/person', methods=['POST'])
# def create_person():
#     try:
#         data = request.get_json()

#         # Extract the 'person' data from the JSON
#         person_data = data.get('person')

#         # Create a Person object
#         person = Person(name=person_data['name'])

#         db.session.add(person)
#         db.session.commit()

#         return jsonify(message='Person created successfully'), 201
#     except Exception as e:
#         return jsonify(error=str(e)), 400

@app.route('/person', methods=['POST'])
def create_person():
    try:
        data = request.get_json()

        # Extract the 'person' data from the JSON
        person_data = data.get('person')
        print('person_data------>',person_data)

        # Create a Person object
        person = Person(
            email=person_data.get('email'),  # Updated to include 'email'
            username=person_data.get('username'),
            password=person_data.get('password')
        )

        db.session.add(person)
        db.session.commit()

        return jsonify(message='Person created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Extract the 'login' data from the JSON
        login_data = data.get('login')

        # Extract the 'username' and 'password' from the 'login' data
        username = login_data.get('username')
        provided_password = login_data.get('password')

        # Query the Person table to retrieve the stored hashed password
        person = Person.query.filter_by(username=username).first()

        if person and bcrypt.verify(provided_password, person.password):
            # Include the ID of the logged-in user in the response
            response_data = {
                'message': 'Login successful',
                'user_id': person.id  # Add the ID here
            }
            return jsonify(response_data), 200
        else:
            return jsonify(message='Invalid username or password'), 401

    except Exception as e:
        return jsonify(error=str(e)), 500
    
# @app.route('/user/<int:person_id>', methods=['POST'])
# def create_user(person_id):
#     try:
#         data = request.get_json()

#         # Extract the 'user' data from the JSON
#         user_data = data.get('user')

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404

#         # Create a new User
#         new_user = User(
#             email=user_data['email'],
#             username=user_data['username'],
#             password=user_data['password'],
#             person_id=person_id  # Associate the user with the specified person_id
#         )
#         person.userdetails.append(new_user)

#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify(message='User created successfully'), 201

#     except Exception as e:
#         return jsonify(error=str(e)), 400


# @app.route('/user', methods=['POST'])
# def create_user():
#     try:
#         data = request.get_json()

#         # Extract the 'user' data from the JSON
#         user_data = data.get('user')

#         # person_id = user_data['person_id']
#         # # Get the associated person
#         # if person_id:
#         #     person = Person.query.get(person_id)
#         #     if person is None:
#         #         return jsonify(error='Person not found with the specified person_id'), 404

#         # Create a new User
#         new_user = User(
#             email=user_data['email'],
#             username=user_data['username'],
#             password=user_data['password']
#             # person_id=person_id  # Associate the user with the specified person_id
#         )
#         Person.userdetails.append(new_user)

#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify(message='User created successfully'), 201

#     except Exception as e:
#         return jsonify(error=str(e)), 400
    
    
        
    
# stage1    
@app.route('/stage1/<int:person_id>', methods=['POST'])
def create_speaker_contact_info(person_id):
    try:
        data = request.get_json()

        # Extract the 'speaker_contact_information' data from the JSON
        speaker_contact_info_data = data.get('speaker_contact_information')
        # Extract the 'manager_or_teammate' data from the JSON
        manager_teammate_data = data.get('manager_or_teammate')
        # Extract the 'social_media_personal' data from the JSON
        social_media_personal_data = data.get('social_media_personal')

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

                
        speaker_contact_info = SpeakerContactInformation(
            first_name=speaker_contact_info_data['first_name'],
            last_name=speaker_contact_info_data['last_name'],
            middle_initials=speaker_contact_info_data['middle_initials'],
            secondary_names_nick_name=speaker_contact_info_data['secondary_names_nick_name'],
            pronouns=speaker_contact_info_data['pronouns'],
            cell_phone=speaker_contact_info_data['cell_phone'],
            main_email=speaker_contact_info_data['main_email'],
            website_link=speaker_contact_info_data['website_link'],
            rss_blog_link=speaker_contact_info_data['rss_blog_link'],
            rss_blog_link_2=speaker_contact_info_data['rss_blog_link_2'],
            closest_major_airport=speaker_contact_info_data['closest_major_airport']
        )
        person.speaker_contact_information = speaker_contact_info
        
        
        manager_teammate = ManagerOrTeammate(
            assist_coordinating=manager_teammate_data['assist_coordinating'],
            first_name=manager_teammate_data['contact_info']['first_name'],
            last_name=manager_teammate_data['contact_info']['last_name'],
            pronouns=manager_teammate_data['contact_info']['pronouns'],
            cell_phone=manager_teammate_data['contact_info']['cell_phone'],
            main_email=manager_teammate_data['contact_info']['main_email'],
            website=manager_teammate_data['contact_info']['website']
        )
        person.manager_or_teammate = manager_teammate
        
        social_media_personal = SocialMediaPersonal(
            facebook_link=social_media_personal_data['facebook']['link'],
            facebook_handle=social_media_personal_data['facebook']['handle'],
            facebook_followers=social_media_personal_data['facebook']['followers'],
            instagram_link=social_media_personal_data['instagram']['link'],
            instagram_handle=social_media_personal_data['instagram']['handle'],
            instagram_followers=social_media_personal_data['instagram']['followers'],
            twitter_link=social_media_personal_data['twitter']['link'],
            twitter_handle=social_media_personal_data['twitter']['handle'],
            twitter_followers=social_media_personal_data['twitter']['followers'],
            linkedin_link=social_media_personal_data['linkedin']['link'],
            linkedin_handle=social_media_personal_data['linkedin']['handle'],
            linkedin_followers=social_media_personal_data['linkedin']['followers'],
            tiktok_link=social_media_personal_data['tiktok']['link'],
            tiktok_handle=social_media_personal_data['tiktok']['handle'],
            tiktok_followers=social_media_personal_data['tiktok']['followers']
        )
        person.social_media_personal = social_media_personal

        db.session.commit()

        return jsonify(message='Speaker contact information created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400    


@app.route('/stage1', methods=['PUT'])
def update_speaker_contact_information():
    try:
        data = request.get_json()
        person_id = data.get('person_id')  # Get the person_id from the JSON payload

        # Retrieve the person object from the database based on person_id
        person = Person.query.get(person_id)

        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404


        # Extract the 'speaker_contact_information' data
        speaker_contact_info_data = data.get('speaker_contact_information')
        if speaker_contact_info_data:
            speaker_contact_info = person.speaker_contact_information
            if not speaker_contact_info:
                speaker_contact_info = SpeakerContactInformation()
                person.speaker_contact_information = speaker_contact_info

            speaker_contact_info.first_name = speaker_contact_info_data.get('first_name', speaker_contact_info.first_name)
            speaker_contact_info.last_name = speaker_contact_info_data.get('last_name', speaker_contact_info.last_name)
            speaker_contact_info.middle_initials = speaker_contact_info_data.get('middle_initials', speaker_contact_info.middle_initials)
            speaker_contact_info.secondary_names_nick_name = speaker_contact_info_data.get('secondary_names_nick_name', speaker_contact_info.secondary_names_nick_name)
            speaker_contact_info.pronouns = speaker_contact_info_data.get('pronouns', speaker_contact_info.pronouns)
            speaker_contact_info.cell_phone = speaker_contact_info_data.get('cell_phone', speaker_contact_info.cell_phone)
            speaker_contact_info.main_email = speaker_contact_info_data.get('main_email', speaker_contact_info.main_email)
            speaker_contact_info.website_link = speaker_contact_info_data.get('website_link', speaker_contact_info.website_link)
            speaker_contact_info.rss_blog_link = speaker_contact_info_data.get('rss_blog_link', speaker_contact_info.rss_blog_link)
            speaker_contact_info.rss_blog_link_2 = speaker_contact_info_data.get('rss_blog_link_2', speaker_contact_info.rss_blog_link_2)
            speaker_contact_info.closest_major_airport = speaker_contact_info_data.get('closest_major_airport', speaker_contact_info.closest_major_airport)

        # Extract the 'manager_or_teammate' data
        manager_teammate_data = data.get('manager_or_teammate')
        if manager_teammate_data:
            manager_or_teammate = person.manager_or_teammate
            if not manager_or_teammate:
                manager_or_teammate = ManagerOrTeammate()
                person.manager_or_teammate = manager_or_teammate

            manager_or_teammate.assist_coordinating = manager_teammate_data.get('assist_coordinating', manager_or_teammate.assist_coordinating)
            contact_info = manager_teammate_data.get('contact_info')
            if contact_info:
                manager_or_teammate.first_name = contact_info.get('first_name', manager_or_teammate.first_name)
                manager_or_teammate.last_name = contact_info.get('last_name', manager_or_teammate.last_name)
                manager_or_teammate.pronouns = contact_info.get('pronouns', manager_or_teammate.pronouns)
                manager_or_teammate.cell_phone = contact_info.get('cell_phone', manager_or_teammate.cell_phone)
                manager_or_teammate.main_email = contact_info.get('main_email', manager_or_teammate.main_email)
                manager_or_teammate.website = contact_info.get('website', manager_or_teammate.website)

        # Extract the 'social_media_personal' data
        social_media_personal_data = data.get('social_media_personal')
        if social_media_personal_data:
            social_media_personal = person.social_media_personal
            if not social_media_personal:
                social_media_personal = SocialMediaPersonal()
                person.social_media_personal = social_media_personal

            social_media_personal.facebook_link = social_media_personal_data['facebook']['link']
            social_media_personal.facebook_handle = social_media_personal_data['facebook']['handle']
            social_media_personal.facebook_followers = social_media_personal_data['facebook']['followers']
            social_media_personal.instagram_link = social_media_personal_data['instagram']['link']
            social_media_personal.instagram_handle = social_media_personal_data['instagram']['handle']
            social_media_personal.instagram_followers = social_media_personal_data['instagram']['followers']
            social_media_personal.twitter_link = social_media_personal_data['twitter']['link']
            social_media_personal.twitter_handle = social_media_personal_data['twitter']['handle']
            social_media_personal.twitter_followers = social_media_personal_data['twitter']['followers']
            social_media_personal.linkedin_link = social_media_personal_data['linkedin']['link']
            social_media_personal.linkedin_handle = social_media_personal_data['linkedin']['handle']
            social_media_personal.linkedin_followers = social_media_personal_data['linkedin']['followers']
            social_media_personal.tiktok_link = social_media_personal_data['tiktok']['link']
            social_media_personal.tiktok_handle = social_media_personal_data['tiktok']['handle']
            social_media_personal.tiktok_followers = social_media_personal_data['tiktok']['followers']

        db.session.commit()

        return jsonify(message='Speaker contact information updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400

    
    
# @app.route('/stage2/<int:person_id>', methods=['POST'])
# def create_biographgy(person_id):
#     try:
        
        
#         microphone = request.files.getlist('Microphone')
        
#         microphonetext = request.form.get('Microphonetext')
#         highlight = request.form.get('Highlight')
#         sort_bio = request.form.get('Sort_Bio')
#         long_bio = request.form.get('Long_Bio')
#         speaker_topics = request.form.get('Speaker_Topics')
#         keywords = request.form.get('Speaker_Topics_additional_keywords_separated_by_commas')
#         speaker_tags = request.form.get('Speaker_Tags')
#         descriptive_title_type = request.form.get('Descriptive_Title_Type')
#         descriptive_title_1 = request.form.get('Descriptive_Title_1')
#         descriptive_title_2 = request.form.get('Descriptive_Title_2')
#         descriptive_title_3 = request.form.get('Descriptive_Title_3')
#         city = request.form.get('City')
#         province_state = request.form.get('Province_State')
        

#         person = Person.query.get(person_id)
        

#         # Books
#         for file in microphone:
#             if file:
#                 file_data = file.read()
#                 new_bio = Biography(microphone=file_data)
#                 new_bio.microphonetext = microphonetext
#                 new_bio.highlight = highlight
#                 new_bio.long_bio = sort_bio
#                 new_bio.sort_bio = long_bio
#                 new_bio.speaker_topics = speaker_topics
#                 new_bio.speaker_topics_additional_keywords = keywords
#                 new_bio.speaker_tags = speaker_tags
#                 new_bio.descriptive_title_type = descriptive_title_type
#                 new_bio.descriptive_title_1 = descriptive_title_1
#                 new_bio.descriptive_title_2 = descriptive_title_2
#                 new_bio.descriptive_title_3 = descriptive_title_3
#                 new_bio.city = city
#                 new_bio.province_state = province_state
#                 person.biography.append(new_bio)       
                
#         db.session.commit()

#         return jsonify({'message': 'biographgy created successfully'}), 201
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500 





@app.route('/stage2/<int:person_id>', methods=['POST'])
def create_biographgy(person_id):
    try:
        microphone = request.files.getlist('Microphone')
        microphonetext = request.form.get('Microphonetext')
        highlight = request.form.get('Highlight')
        sort_bio = request.form.get('Sort_Bio')
        long_bio = request.form.get('Long_Bio')
        speaker_topics_additional_keywords = request.form.get('Additional_keywords')
        descriptive_title_type = request.form.get('Descriptive_title_type') 
        print("descriptive_title_type",descriptive_title_type)
        
        speaker_topics = request.form.getlist('speaker_topicss')
        print("speaker_topicsss",speaker_topics)
        # topics = str(speaker_topics).split(',')
        # print("topics",speaker_topics)
        
        speaker_tags = request.form.getlist('speaker_tagss')
        print("speaker_tagsss",speaker_tags)
        # tags = str(speaker_tags).split(',')
        # print("tags",tags)
        
        descriptive_titles = request.form.getlist('descriptive_titlee')
        print("descriptive_titlessss",descriptive_titles)
        # titles = str(descriptive_titles).split(',')
        # print("titles",titles)
        
        
        city = request.form.get('City')
        province_state = request.form.get('Province_State')
        person = Person.query.get(person_id)
        new_bio = Biography(highlight=highlight,microphonetext=microphonetext,sort_bio=sort_bio,long_bio=long_bio,speaker_topics_additional_keywords=speaker_topics_additional_keywords,descriptive_title_type=descriptive_title_type,city=city,province_state=province_state)
        
        
        for i in range(len(speaker_topics)):
            # print("length----->",len(speaker_topics))
            print("topic",speaker_topics[i])
            top = str(speaker_topics[i]).strip().replace(" ", "_").replace("&", "_").replace("-", "_").replace(";", "").replace("'", "").replace("#", "").replace("+", "").replace("(", "").replace(")", "").replace("$", "").replace(",", "")
            # print("ttt",top)
            if top in SpeakerTopicEnum.__members__:
                
                new_bio.speaker_topics.append(SpeakerTopic(topic=top))
            else:
                return "Invalid speaker topics provided", 400
        person.biography.append(new_bio)
        
        print("<><><><><><><><><><><><><>")
        
        for i in range(len(speaker_tags)):
            # print("length----->",len(tags))
            print("tags",speaker_tags[i])
            top = str(speaker_tags[i])#.strip().replace(" ", "_").replace("&", "_").replace("-", "_").replace(";", "").replace("'", "").replace("#", "").replace("+", "").replace("(", "").replace(")", "").replace("$", "").replace(",", "")
            # print("ttt",top)
            if top in SpeakerTagEnum.__members__:
                
                new_bio.speaker_tags.append(SpeakerTag(tag=top))
            else:
                return "Invalid speaker tags provided", 400
        person.biography.append(new_bio)
        
        print("<><><><><><><><><><><><><>")
        
        for i in range(len(descriptive_titles)):
            print("length----->",len(descriptive_titles))
            print("titles",descriptive_titles[i])
            top = str(descriptive_titles[i]).strip().replace(" ", "_").replace("&", "_").replace("-", "_").replace(";", "").replace("'", "").replace("#", "").replace("+", "").replace("(", "").replace(")", "").replace("$", "").replace(",", "")
            if top in DescriptiveTitlesEnum.__members__:
                
                new_bio.descriptive_titles.append(DescriptiveTitles(title=top))
            else:
                return "Invalid speaker titles provided", 400
        person.biography.append(new_bio)
        
        #        # Books
        # for file in microphone:
        #     if file:  
        #         file.save(os.path.join(uploads_path , file.filename))   
        #         bio_data = file.read()   
        #         new_bio = Book(microphone=bio_data,book_name=file.filename)
                
        for file in microphone:
            if file:
                file_data = file.read()
                new_bio.microphone = file_data
                new_bio.microphone_name = file.filename

        db.session.commit()
        
        return jsonify({'message': 'Biography created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
       
    
# @app.route('/stage3/<int:person_id>', methods=['POST'])
# def create_topicdescription(person_id):
#     try:
#         person = Person.query.get(person_id)
        
        
#         Audio_file = request.files.getlist('Audio_Clip_for_Topic_Description_1')
        
#         audiotext = request.form.get('Audio_text')
#         title = request.form.get('Topic_Description_Title')
#         body_text = request.form.get('Topic_Description_Body_Text')
#         topic_delivered = request.form.get('Topic_delivered_as')
#         video_link = request.form.get('Video_Clip_for_Topic_Description_1')
        
        

#         new_bio = TopicDescription(audiotext=audiotext, title=title, body_text=body_text, delivered_as=topic_delivered, video_clip=video_link)
        
    
#         for file in Audio_file:
#             if file:
#                 file_data = file.read()
#                 new_bio.microphone = file_data             
                
#         db.session.commit()

#         return jsonify({'message': 'topicdescription created successfully'}), 201
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500  


@app.route('/stage3/<int:person_id>', methods=['POST'])
def create_topicdescription(person_id):
    try:
        person = Person.query.get(person_id)
        if person is None:
            return jsonify({'error': 'Person not found'}), 404

        # Extract data from the request
        audiotext = request.form.get('Audio_text')
        title = request.form.get('Topic_Description_Title')
        body_text = request.form.get('Topic_Description_Body_Text')
        delivered_as = request.form.get('Topic_delivered_as')
        video_link = request.form.get('Video_Clip_for_Topic_Description_1')

        # Create a new TopicDescription object
        new_topic_description = TopicDescription(
            audiotext=audiotext,
            title=title,
            body_text=body_text,
            delivered_as=delivered_as,
            video_clip=video_link,
        )

        # Handle audio file(s)
        audio_files = request.files.getlist('Audio_Clip_for_Topic_Description_1')
        for audio_file in audio_files:
            if audio_file:
                file_data = audio_file.read()
                new_topic_description.audio_clip = file_data

        # Associate the TopicDescription with the Person
        new_topic_description.person = person

        # Add the new TopicDescription object to the session and commit
        db.session.add(new_topic_description)
        db.session.commit()

        return jsonify({'message': 'Topic description created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/stage4/<int:person_id>', methods=['POST'])
def create_image(person_id):
    try:
        
        images = request.files.getlist('image')
        print('images------>',images)
        croped_images = request.files.getlist('crop_image')
        print('croped_images------>',croped_images)
        own_rights = request.form.get('own_rights')
        print('own_rights------>',own_rights)
        sbc_permissions = request.form.get('sbc_permissions')
        print('sbc_permissions------>',sbc_permissions)

        person = Person.query.get(person_id)
        

        # Images
        for image_file, croped_image_file in zip(images, croped_images):
            if image_file and croped_image_file:
                image_file.save(os.path.join(uploads_path , image_file.filename))
                croped_image_file.save(os.path.join(uploads_path , croped_image_file.filename))
                image_data = image_file.read()
                croped_image_data = croped_image_file.read()

                new_images = Images(image_data=image_data,image_name=image_file.filename,crop_image_name=croped_image_file.filename,croped_image_data=croped_image_data)
                new_images.own_right = own_rights == 'true'
                new_images.sbc_permission = sbc_permissions == 'true'
                person.images.append(new_images)


        db.session.commit()

        return jsonify({'message': 'Image created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @app.route('/stage4/<int:person_id>', methods=['POST'])
# def create_image(person_id):
#     try:
#         images = request.files.getlist('image')
#         cropped_images = request.files.getlist('crop_image')
#         own_rights = request.form.get('own_rights')
#         sbc_permissions = request.form.get('sbc_permissions')

#         person = Person.query.get(person_id)

#         # Images
#         new_images = Images(own_right=own_rights == 'true', sbc_permission=sbc_permissions == 'true')

#         for image_file in images:
#             if image_file:
#                 image_data = image_file.read()
#                 new_image_data = ImageData(image_data=image_data)
#                 new_images.image_data.append(new_image_data)

#         for cropped_image_file in cropped_images:
#             if cropped_image_file:
#                 cropped_image_data = cropped_image_file.read()
#                 new_cropped_image_data = CroppedImageData(cropped_image_data=cropped_image_data)
#                 new_images.cropped_image_data.append(new_cropped_image_data)

#         person.images.append(new_images)

#         db.session.commit()

#         return jsonify({'message': 'Images created successfully'}), 201

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500



@app.route('/stage5/<int:person_id>', methods=['POST'])
def create_videos(person_id):
    try:
        data = request.get_json()

        # Extract the 'Video' data from the JSON
        videos_data = data.get('Video')

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        for video_data in videos_data:
            title = video_data.get('Title')
            link = video_data.get('Link')
            source_info = video_data.get('source_if_not', {})
            hd_quality = source_info.get('HD_Quality')
            own_rights = source_info.get('Do_you_own_the_rights_to_this_video')
            grant_permission = source_info.get('Do_you_grant_SBC_permission_and_all_clients_permission_to_use_this_video_for_promoting_you_as_a_speaker')
            reason = video_data.get('why_not')

            # Create a Video instance
            video = Video(
                title=title,
                link=link,
                hd_quality=hd_quality,
                own_rights=own_rights,
                grant_permission=grant_permission,
                reason=reason
            )
            person.video.append(video)

        db.session.commit()

        return jsonify(message='Videos created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400 
    
    

    
 
@app.route('/stage6/<int:person_id>', methods=['POST'])
def create_podcasts(person_id):
    try:
        data = request.get_json()

        # Extract the 'podcasts' data from the JSON
        podcasts_data = data.get('podcasts')

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        for podcast_info in podcasts_data:
            podcast = Podcast(
                title=podcast_info['title'],
                link=podcast_info['link'],
                source=podcast_info['source']
            )
            person.podcasts.append(podcast)

        db.session.commit()

        return jsonify(message='Podcasts created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400
    
    
@app.route('/stage7/<int:person_id>', methods=['POST'])
def create_books(person_id):
    try:
        books = request.files.getlist('book_file')
        
        
        book_title = request.form.get('book_title')
        book_description = request.form.get('book_description')
        book_authors = request.form.get('book_authors')
        book_publisher = request.form.get('book_publisher')
        book_link = request.form.get('book_link')
        book_cost = request.form.get('book_cost')
        book_bulk_order = request.form.get('book_bulkorder')
        book_price = request.form.get('book_price')
        book_number = request.form.get('book_number')
        

        person = Person.query.get(person_id)
        
        # Books
        for file in books:
            if file:  
                file.save(os.path.join(uploads_path , file.filename))   
                book_data = file.read()   
                new_book = Book(upload_book_image=book_data,book_name=file.filename)
                new_book.title = book_title
                new_book.description = book_description
                new_book.authors = book_authors
                new_book.publisher = book_publisher
                new_book.link = book_link
                new_book.cost_per_book_cad = book_cost
                new_book.bulk_order_purchase_offered = book_bulk_order == 'true'
                new_book.price_per_book_cad = book_price
                new_book.number_of_books = book_number
                person.books.append(new_book)          
        db.session.commit()

        return jsonify({'message': 'books created successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500   

    
# @app.route('/stage7/<int:person_id>', methods=['POST'])
# def create_books(person_id):
#     try:
#         books = request.files.getlist('book_file')
        
#         book_title = request.form.get('book_title')
#         book_description = request.form.get('book_description')
#         book_authors = request.form.get('book_authors')
#         book_publisher = request.form.get('book_publisher')
#         book_link = request.form.get('book_link')
#         book_cost = request.form.get('book_cost')
#         book_bulk_order = request.form.get('book_bulkorder')
#         book_price = request.form.get('book_price')
#         book_number = request.form.get('book_number')

#         person = Person.query.get(person_id)

#         # Create Book instance
#         new_book = Book(
#             title=book_title,
#             description=book_description,
#             authors=book_authors,
#             publisher=book_publisher,
#             link=book_link,
#             cost_per_book_cad=book_cost,
#             bulk_order_purchase_offered=book_bulk_order == 'true',
#             price_per_book_cad=book_price,
#             number_of_books=book_number
#         )

#         # Create BookImageData instances and link them to Book
#         for file in books:
#             if file:
#                 file_data = file.read()
#                 book_image_data = BookImageData(image_data=file_data)
#                 new_book.upload_book_images.append(book_image_data)

#         person.books.append(new_book)

#         db.session.commit()

#         return jsonify({'message': 'Book created successfully'}), 201

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    
    
@app.route('/stage8/<int:person_id>', methods=['POST'])
def create_media_mentions(person_id):
    try:
        data = request.get_json()

        # Extract the 'media_mentions' data from the JSON
        media_mentions_data = data.get('media_mentions')

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        for media_data in media_mentions_data:
            organization_name = media_data.get('organization_name')
            interview_article_titles = media_data.get('interview_article_title')
            link = media_data.get('link')
            date = media_data.get('date')
            interview_source_name = media_data.get('interview_source_name')

            # Join the interview article titles into a single string
            interview_article_title = ', '.join(interview_article_titles)

            # Create a MediaMention instance with the concatenated interview article titles
            media_mention = MediaMention(
                organization_name=organization_name,
                interview_article_title=interview_article_title,
                link=link,
                date=date,
                interview_source_name=interview_source_name
            )
            person.media_mentions.append(media_mention)

        db.session.commit()

        return jsonify(message='Media mentions created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400
   
    
    
    
@app.route('/stage9/<int:person_id>', methods=['POST'])
def create_white_papers_case_studies(person_id):
    try:
        data = request.get_json()

        # Extract the 'white_papers_case_studies' data from the JSON
        white_papers_data = data.get('white_papers_case_studies')

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        for white_paper_data in white_papers_data:
            organization_name = white_paper_data.get('organization_name')
            title = white_paper_data.get('title')
            topics = white_paper_data.get('topics')
            description = white_paper_data.get('description')
            link = white_paper_data.get('link')
            date = white_paper_data.get('date')

            # Create a WhitePaperCaseStudy instance
            white_paper = WhitePaperCaseStudy(
                organization_name=organization_name,
                title=title,
                topics=topics,
                description=description,
                link=link,
                date=date
            )
            person.white_papers_case_studies.append(white_paper)

        db.session.commit()

        return jsonify(message='White papers/case studies created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400    
    
    
@app.route('/stage10/<int:person_id>', methods=['POST'])
def create_degrees_certifications_awards(person_id):
    try:
        
        degreescertificatesawards = request.files.getlist('degreescertificatesawards')
        # certifications = request.files.getlist('certifications')
        # awards = request.files.getlist('awards')
        
        person = Person.query.get(person_id)
        
        # Degrees
        for file in degreescertificatesawards:
            if file:
                file_data = file.read()
                new_degrees = DegreesCertificatesAwards(degree_data=file_data, degreescertificatesawards_name=file.filename)
                person.degree_files.append(new_degrees)
                
        # # Certificates        
        # for file in certifications:
        #     if file:
        #         file_data = file.read()
        #         new_certifications = Certificates(certifications_data=file_data)
        #         person.certificate_files.append(new_certifications)   
                
        # # Awards        
        # for file in awards:
        #     if file:
        #         file_data = file.read()
        #         new_awards = Awards(awards_data=file_data)
        #         person.awards_files.append(new_awards)
                
        db.session.commit()

        return jsonify({'message': 'degrees_certifications_awards files created successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500     
       
        

@app.route('/stage11/<int:person_id>', methods=['POST'])
def create_testimonial(person_id):
    try:
        data = request.get_json()

        # Extract the 'Testimonials' data from the JSON
        testimonials_data = data.get('Testimonials')

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        for testimonial_data in testimonials_data:
            organizer_name = testimonial_data.get('Organizer_Name')
            organization_name = testimonial_data.get('Testimonial_Organization_Name')
            link_to_video = testimonial_data.get('Link_to_Video')

            # Create a Testimonial instance
            testimonial = Testimonial(
                organizer_name=organizer_name,
                organization_name=organization_name,
                link_to_video=link_to_video
            )
            person.testimonials.append(testimonial)

        db.session.commit()

        return jsonify(message='Testimonials created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400   


    
    

@app.route('/stage12/<int:person_id>', methods=['POST'])
def create_business_info(person_id):
    try:
        data = request.get_json()

        # Extract the 'business_info' data from the JSON
        business_info_data = data.get('business_info')
        # Extract the 'social_media_business' data from the JSON
        social_media_business_data = data.get('social_media_business')

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        
        business_info = BusinessInfo(
            issue_payment=business_info_data['business_issue_payment'],
            official_business_name=business_info_data['business_information']['official_business_name'],
            business_email=business_info_data['business_information']['business_email'],
            business_phone=business_info_data['business_information']['business_phone'],
            business_number=business_info_data['business_information']['business_number'],
            website=business_info_data['business_information']['website']
        )
        person.business_info = business_info

        social_media_business = SocialMediaBusiness(
            facebook_link=social_media_business_data['facebook']['link'],
            facebook_handle=social_media_business_data['facebook']['handle'],
            facebook_followers=social_media_business_data['facebook']['followers'],
            instagram_link=social_media_business_data['instagram']['link'],
            instagram_handle=social_media_business_data['instagram']['handle'],
            instagram_followers=social_media_business_data['instagram']['followers'],
            twitter_link=social_media_business_data['twitter']['link'],
            twitter_handle=social_media_business_data['twitter']['handle'],
            twitter_followers=social_media_business_data['twitter']['followers'],
            linkedin_link=social_media_business_data['linkedin']['link'],
            linkedin_handle=social_media_business_data['linkedin']['handle'],
            linkedin_followers=social_media_business_data['linkedin']['followers'],
            tiktok_link=social_media_business_data['tiktok']['link'],
            tiktok_handle=social_media_business_data['tiktok']['handle'],
            tiktok_followers=social_media_business_data['tiktok']['followers']
        )
        person.social_media_business = social_media_business
        db.session.commit()

        return jsonify(message='Business information created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400  
    
    
@app.route('/stage13/<int:person_id>', methods=['POST'])
def create_brand_campaigns(person_id):
    try:
        data = request.get_json()

        # Extract the 'Brand_Product_Campaigns&Endorsementstheme1' and 'Brand_Product_Campaigns&Endorsementstheme2' data from the JSON
        brand_campaigns_data1 = data.get('Brand_Product_CampaignsEndorsementstheme1')
        brand_campaigns_data2 = data.get('Brand_Product_CampaignsEndorsementstheme2')

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        # Process 'Brand_Product_Campaigns&Endorsementstheme1' data
        for organization_data in brand_campaigns_data1:
            part_of_social_media = organization_data.get('part_of_social_media', False)
            organization_name = organization_data.get('organization_name')
            platforms = organization_data.get('platforms')
            link_to_campaign = organization_data.get('link_to_campaign')
            start_year = organization_data.get('start_year')
            end_year = organization_data.get('end_year')

            brand_campaign = BrandCampaignOrganizationtheme1(
                part_of_social_media=part_of_social_media,
                organization_name=organization_name,
                platforms=platforms,
                link_to_campaign=link_to_campaign,
                start_year=start_year,
                end_year=end_year
            )
            person.brand_campaignstheme1.append(brand_campaign)

        # Process 'Brand_Product_Campaigns&Endorsementstheme2' data
        for organization_data in brand_campaigns_data2:
            part_of_social_media = organization_data.get('part_of_social_media', False)
            organization_name = organization_data.get('organization_name')
            platforms = organization_data.get('platforms')
            link_to_campaign = organization_data.get('link_to_campaign')
            start_year = organization_data.get('start_year')
            end_year = organization_data.get('end_year')

            brand_campaign = BrandCampaignOrganizationtheme2(
                part_of_social_media=part_of_social_media,
                organization_name=organization_name,
                platforms=platforms,
                link_to_campaign=link_to_campaign,
                start_year=start_year,
                end_year=end_year
            )
            person.brand_campaignstheme2.append(brand_campaign)

        db.session.commit()

        return jsonify(message='Brand/Product Campaigns & Endorsements created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400
    
    
@app.route('/stage14/<int:person_id>', methods=['POST'])
def create_at_events(person_id):
    try:
        data = request.get_json()

        # Extract the 'at_events' data from the JSON
        at_events_data = data.get('at_events')[0]  # Assuming 'at_events' is a list with one dictionary

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        # Process 'at_events' data
        at_events = AtEvents(
            using_presentation_software=at_events_data['presentation_software']['using_presentation_software'],
            presentation_software_name=at_events_data['presentation_software']['presentation_software_name'],
            using_audience_interaction_software=at_events_data['audience_interaction_software']['using_audience_interaction_software'],
            audience_interaction_software_name=at_events_data['audience_interaction_software']['audience_interaction_software_name'],
            attending_sessions_before_after_presentation=at_events_data['attending_sessions_before_after_presentation'],
            attending_meals_networking_sessions=at_events_data['meal_networking_session']['attending_meals_networking_sessions'],
            dietary_requirements_restrictions=at_events_data['meal_networking_session']['dietary_requirements_restrictions'],
            A_V_requirements=at_events_data['meal_networking_session']['A_V_requirements'],
            prefer_to_book_travel=at_events_data['prefer_to_book_travel'],
            special_conditions_for_travel_arrangements=at_events_data['special_conditions_for_travel_arrangements'],
            table_for_book_sales=at_events_data['table_for_book_sales']
        )

        # Process 'speaker_introduction' data
        speaker_introductions_data = at_events_data['meal_networking_session']['speaker_introduction']
        for introduction_data in speaker_introductions_data:
            for key, introduction_text in introduction_data.items():
                speaker_introduction = SpeakerIntroduction(
                    introduction_text=introduction_text
                )
                at_events.speaker_introduction.append(speaker_introduction)
        
        # Process 'travel_agent' data
        travel_agent_data = at_events_data.get('travel_agent', {})
        use_travel_agent = travel_agent_data.get('use_travel_agent', False)
        Preferred_Seating = travel_agent_data.get('Preferred_Seating', '')
        Preferred_Airline = travel_agent_data.get('Preferred_Airline', '')
        West_Jet_number = travel_agent_data.get('West_Jet#', '')
        Air_Canada_number = travel_agent_data.get('Air_Canada#', '')
        at_events.use_travel_agent = use_travel_agent
        at_events.Preferred_Seating = Preferred_Seating
        at_events.Preferred_Airline = Preferred_Airline
        at_events.West_Jet_number = West_Jet_number
        at_events.Air_Canada_number = Air_Canada_number

        person.at_events = at_events

        db.session.commit()

        return jsonify(message='At Events and Speaker Introduction created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/stage15/<int:person_id>', methods=['POST'])
def create_help_us_book_you(person_id):
    try:
        data = request.get_json()

        # Extract the 'Help_us_book_you' data from the JSON
        help_us_book_you_data = data.get('Help_us_book_you')

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        
        help_us_book_you = HelpUsBookYou(
            speaker_reason_to_work_with=help_us_book_you_data['speaker_reason_to_work_with'],
            value_adds_and_offerings=help_us_book_you_data['value_adds_and_offerings']['offer_any_value_adds'],
            books_how_many_items=help_us_book_you_data['value_adds_and_offerings']['books']['how_many_items'],
            books_value_per_item=help_us_book_you_data['value_adds_and_offerings']['books']['value_per_item'],
            online_training_how_many_items=help_us_book_you_data['value_adds_and_offerings']['online_training']['how_many_items'],
            online_training_value_per_item=help_us_book_you_data['value_adds_and_offerings']['online_training']['value_per_item'],
            merch_how_many_items=help_us_book_you_data['value_adds_and_offerings']['merch']['how_many_items'],
            merch_value_per_item=help_us_book_you_data['value_adds_and_offerings']['merch']['value_per_item'],
            merch_2_how_many_items=help_us_book_you_data['value_adds_and_offerings']['merch_2']['how_many_items'],
            merch_2_value_per_item=help_us_book_you_data['value_adds_and_offerings']['merch_2']['value_per_item'],
            complementary_virtual_follow_sessions_consultation=help_us_book_you_data['complementary_virtual_follow_sessions_consultation'],
            inclusive_of_travel_expenses=help_us_book_you_data['inclusive_of_travel_expenses'],
            industries_do_you_not_work_with=help_us_book_you_data['industry_you_specialize_with']['industries_do_you_not_work_with'],
            favorite_audiences_event_types=help_us_book_you_data['industry_you_specialize_with']['favorite_audiences_event_types'],
            target_audiences_industries=help_us_book_you_data['industry_you_specialize_with']['target_audiences_industries'],
            English_French=help_us_book_you_data['English_&_French'],
            Q_A_in_French=help_us_book_you_data['Q&A_in_French'],
            offer_recordings=help_us_book_you_data['offer_recordings'],
            primary_source_of_income=help_us_book_you_data['primary_source_of_income'],
            hoping_for_speaking_to_become_your_primary_source_income=help_us_book_you_data['speaking_frequency']['hoping_for_speaking_to_become_your_primary_source_income'],
            current_speak_per_month=help_us_book_you_data['speaking_frequency']['current_speak_per_month'],
            virtual_events_over_pandemic=help_us_book_you_data['speaking_frequency']['virtual_events_over_pandemic'],
            speak_per_month=help_us_book_you_data['speaking_frequency']['speak_per_month'],
            market_yourself_as_a_speaker=help_us_book_you_data['speaking_frequency']['market_yourself_as_a_speaker'],
            affiliated_with_any_other_speakers_agencies=help_us_book_you_data['speaking_frequency']['affiliated_with_any_other_speakers_agencies'],
            percentage_of_bookings=help_us_book_you_data['speaking_frequency']['percentage_of_bookings'],
            Approximately_what_percentage=help_us_book_you_data['speaking_frequency']['Approximately_what_percentage'],
            speakers_are_you_affiliated_with=help_us_book_you_data['speaking_frequency']['speakers_are_you_affiliated_with']
        )
        person.help_us_book_you = help_us_book_you


        db.session.commit()

        return jsonify(message='Help Us Book You created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400    
    
    
@app.route('/stage16/<int:person_id>', methods=['POST'])
def create_help_us_work_with_you(person_id):
    try:
        data = request.get_json()

        # Extract the 'Help_us_work_with_you' data from the JSON
        help_us_work_with_you_data = data.get('Help_us_work_with_you')

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        
        help_us_work_with_you = HelpUsWorkWithYou(
            newsletter_onboarding=help_us_work_with_you_data['newsletter_onboarding'],
            tracking_system=help_us_work_with_you_data['tracking_system'],
            whatsapp=help_us_work_with_you_data['whatsapp'],
            business_ownership=help_us_work_with_you_data['business_ownership'],
            crm_usage=help_us_work_with_you_data['crm_usage'],
            appointment_booking_software=help_us_work_with_you_data['appointment_booking_software'],
            expectations_with_sbc=help_us_work_with_you_data['expectations_with_sbc'],
            something_about_you=help_us_work_with_you_data['something_about_you'],
            stories=help_us_work_with_you_data['stories']
        )
        person.help_us_work_with_you = help_us_work_with_you
        
        
        db.session.commit()

        return jsonify(message='Help Us Work With You created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400    
    
    
@app.route('/stage17/<int:person_id>', methods=['POST'])
def create_fees(person_id):
    try:
        data = request.get_json()

        # Extract the 'Fees' data from the JSON
        fees_data = data.get('Fees')
        
        
        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404


        # Extract the 'Fees' data from the JSON
        fees_data = data.get('Fees')
        fees = Fees(
            Pro_Bono_Events=fees_data['Pro_Bono_Events'],
            Corporate_Keynote_20_60_Minutes=fees_data['Discounted_Rate_Events']['Corporate_Keynote_20-60_Minutes'],
            Corporate_Workshop_60_120_Minutes=fees_data['Discounted_Rate_Events']['Corporate_Workshop_60-120_Minutes'],
            Corporate_Half_Day_Training_or_Keynote_Breakout=fees_data['Discounted_Rate_Events']['Corporate_Half_Day_Training_or_Keynote_Breakout'],
            Corporate_Full_Day_Training=fees_data['Discounted_Rate_Events']['Corporate_Full_Day_Training'],
            Concurrent_Sessions_Fee=fees_data['Multiple_Sessions_on_the_Same_Day']['Concurrent_Sessions_Fee'],
            One_Session_in_the_Morning_Fee=fees_data['Multiple_Sessions_on_the_Same_Day']['One_Session_in_the_Morning_Fee'],
            One_Session_in_the_Afternoon_Fee=fees_data['Multiple_Sessions_on_the_Same_Day']['One_Session_in_the_Afternoon_Fee'],
            Multiple_Sessions_on_Concurrent_Days=fees_data['Multiple_Sessions_on_Concurrent_Days'],
            Multiple_Sessions_Over_a_Period_of_Time=fees_data['Multiple_Sessions_Over_a_Period_of_Time'],
            Lowest_Acceptance_for_Informal_Talk=fees_data['Lowest_Acceptance_for_Informal_Talk'],
            One_Day_Event=fees_data['Host_or_Emcee_Fees']['One_Day_Event'],
            One_Day_Plus_Evening_Ceremony_Keynote=fees_data['Host_or_Emcee_Fees']['One_Day_Plus_Evening_Ceremony_Keynote'],
            Two_Day_Event=fees_data['Host_or_Emcee_Fees']['Two_Day_Event'],
            Two_Day_Plus_Evening_Ceremony_Keynote=fees_data['Host_or_Emcee_Fees']['Two_Day_Plus_Evening_Ceremony_Keynote'],
            Three_Day_Event=fees_data['Host_or_Emcee_Fees']['Three_Day_Event'],
            Three_Day_Plus_Evening_Ceremony_Keynote=fees_data['Host_or_Emcee_Fees']['Three_Day_Plus_Evening_Ceremony_Keynote'],
            Four_Day_Event=fees_data['Host_or_Emcee_Fees']['Four_Day_Event'],
            Four_Day_Plus_Evening_Ceremony_Keynote=fees_data['Host_or_Emcee_Fees']['Four_Day_Plus_Evening_Ceremony_Keynote'],
            What_is_your_corporate_speaker_fee=fees_data['Host_or_Emcee_Fees']['What_is_your_corporate_speaker_fee'],
            lowest_you_will_accept=fees_data['Host_or_Emcee_Fees']['lowest_you_will_accept'],
            limitations_or_condition=fees_data['Host_or_Emcee_Fees']['limitations_or_condition'],
            Driving_Distance_Fee=fees_data['Host_or_Emcee_Fees']['Driving_Distance_Fee'],
            Province_Fee=fees_data['Host_or_Emcee_Fees']['Province_Fee'],
            Western_Canada_Fee=fees_data['Host_or_Emcee_Fees']['Western_Canada_Fee'],
            Eastern_Canada_Fee=fees_data['Host_or_Emcee_Fees']['Eastern_Canada_Fee'],
            Northern_Canada_Fee=fees_data['Host_or_Emcee_Fees']['Northern_Canada_Fee'],
            Remote_Location_Fee=fees_data['Host_or_Emcee_Fees']['Remote_Location_Fee'],
            Local_Discount=fees_data['Local_Discount']['Local_Discount'],
            Local_Fee=fees_data['Local_Discount']['Local_Fee'],
            Client_Direct_Approach_for_Local_Event=fees_data['Local_Discount']['Client_Direct_Approach_for_Local_Event'],
            Virtual_Discount=fees_data['Virtual_Discount']['Virtual_Discountt'],
            Virtual_Fee=fees_data['Virtual_Discount']['Virtual_Fee'],
            Client_Direct_Approach_for_Virtual_Event=fees_data['Virtual_Discount']['Client_Direct_Approach_for_Virtual_Event'],
            Small_Audience_Discount=fees_data['Small_Audience_Discount']['Small_Audience_Discountt'],
            Small_Audience_Fee=fees_data['Small_Audience_Discount']['Small_Audience_Fee'],
            Client_Direct_Approach_for_Small_Audience_Event=fees_data['Small_Audience_Discount']['Client_Direct_Approach_for_Small_Audience_Event'],
            Qualification_for_Small_Audience=fees_data['Small_Audience_Discount']['Qualification_for_Small_Audience'],
            Nonprofit_Discount=fees_data['Nonprofit_Discount']['Nonprofit_Discountt'],
            Nonprofit_Fee=fees_data['Nonprofit_Discount']['Nonprofit_Fee'],
            Client_Direct_Approach_for_Nonprofit=fees_data['Nonprofit_Discount']['Client_Direct_Approach_for_Nonprofit'],
            Charitable_Organization_Discount=fees_data['Charitable_Organization_Discount']['Charitable_Organization_Discountt'],
            Charitable_Fee=fees_data['Charitable_Organization_Discount']['Charitable_Fee'],
            Client_Direct_Approach_for_Charitable_Organization=fees_data['Charitable_Organization_Discount']['Client_Direct_Approach_for_Charitable_Organization'],
            outside_of_speaker_fee_ranges=fees_data['Charitable_Organization_Discount']['outside_of_speaker_fee_ranges'],
            Rate_Increase=fees_data['Rate_Increase']
        )
        person.fees = fees

        db.session.commit()

        return jsonify(message='Fees created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400    
    
    
# Define the Person model here (assuming you have it)

@app.route('/stage18/<int:person_id>', methods=['POST'])
def create_speaker_pitches(person_id):
    try:
        data = request.get_json()

        # Extract the 'speaker_pitches' data from the JSON
        speaker_pitches_data = data.get('speaker_pitches')
        print('speaker_pitches_data---------->',speaker_pitches_data)

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        # Clear existing speaker pitches for the person (optional, depends on your use case)
        person.speaker_pitches = []

        # Create instances of SpeakerPitch and append them to the person's speaker_pitches
        for pitch_data in speaker_pitches_data:
            speaker_pitch = SpeakerPitch(
                general_pitch=pitch_data['general_pitch'],
                keyword_topic_focus_pitch=pitch_data['keyword_topic_focus_pitch'],
                Short_pitch_up=pitch_data['Short_pitch_up']
            )
            person.speaker_pitches.append(speaker_pitch)

        db.session.commit()

        return jsonify(message='Speaker pitches created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400
    
    
@app.route('/stage19/<int:person_id>', methods=['POST'])
def create_previous_clients(person_id):
    try:
        data = request.get_json()

        # Extract the 'previous_clients' data from the JSON
        previous_clients_data = data.get('previous_clients', [])

        # Get the associated person
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        previous_clients = []

        for client_data in previous_clients_data:
            if isinstance(client_data, dict):
                organization_name = client_data.get('organization_name')
                client = PreviousClient(organization_name=organization_name)
                previous_clients.append(client)
            else:
                # Handle cases where the value is just a string (organization name)
                organization_name = client_data
                client = PreviousClient(organization_name=organization_name)
                previous_clients.append(client)

        person.previous_clients = previous_clients

        db.session.commit()

        return jsonify(message='Previous clients created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route('/get_data_speakertopics', methods=['GET'])
def get_data_speakertopics():

    api_url = "https://speakerscanada.com/json-api/?auth-key=sbcprivatekey&action=topics"

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            # print('data----------->',data)  
            return jsonify(data)
        
        else:
            return jsonify({"error": "Failed to retrieve data from the external API"})
    except Exception as e:
        return jsonify({"error": str(e)})   
    
@app.route('/get_data_descriptivetitles', methods=['GET'])
def get_data_descriptivetitles():

    api_url = "https://speakerscanada.com/json-api/?auth-key=sbcprivatekey&action=types"

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            # print('data----------->',data)  
            return jsonify(data)
        
        else:
            return jsonify({"error": "Failed to retrieve data from the external API"})
    except Exception as e:
        return jsonify({"error": str(e)})      
    
    
# Define the GET API to retrieve biography data by ID
@app.route('/biography/<int:biography_id>', methods=['GET'])
def get_biography_by_id(biography_id):
    try:
        biography = Biography.query.get(biography_id)
        print('biography<><><><><>',biography.speaker_topics)
        print('biography<><><><><>',biography.descriptive_titles)
        print('biography<><><><><>',biography.speaker_tags)
        
        bio=[]
        
        
        speaker_topic=[]
        for topic in biography.speaker_topics:
            # print("topics of speaker",str(topic.topic))
            name = str(topic.topic).split('.')[-1].split(': ')[0]
            speaker_topic.append(name)  
            
        speaker_tag=[]
        for tag in biography.speaker_tags:
            print("tags of speaker",str(tag.tag))
            name = str(tag.tag).split('.')[-1].split(': ')[0]
            speaker_tag.append(name)    
          
        descriptive_title = [] 
        for title in biography.descriptive_titles:
            # print("topics of speaker",str(title.title))
            name = str(title.title).split('.')[-1].split(': ')[0]
            descriptive_title.append(name)  
          

        if biography is None:
            return jsonify({'message': 'Biography not found'}), 404

        # Create a dictionary to store biography data
        biography_data = {
            'biography_id': biography.id,
            'highlight': biography.highlight,
            'long_bio': biography.long_bio,
            'sort_bio': biography.sort_bio,
            'speaker_topics_additional_keywords': biography.speaker_topics_additional_keywords,
            'descriptive_title_type': biography.descriptive_title_type,
            'city': biography.city,
            'province_state': biography.province_state,
            'microphonetext': biography.microphonetext,
            #'topics': topics
        }
        
        # Append both dictionaries to the list
        bio.append({'speaker_topic': speaker_topic, 'biography_data': biography_data,'speaker_tag':speaker_tag, 'descriptive_title':descriptive_title})

        return jsonify(bio), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    

@app.route('/get_files/<filename>')
def get_files(filename):
    return send_from_directory(uploads_path, filename)


@app.route('/get_all_dataa/<int:person_id>', methods=['GET'])
def get_all_dataa(person_id):
    try:
        person = Person.query.get(person_id)
        if person is None:
            return jsonify(error='Person not found with the specified person_id'), 404

        # Extract data for speaker_contact_information, manager_or_teammate, and social_media_personal (as you've already done)

        # Fetch biography data for the person
        biography_data = []
        for biography in person.biography:
            bio = {
                'biography_id': biography.id,
                'highlight': biography.highlight,
                'long_bio': biography.long_bio,
                'sort_bio': biography.sort_bio,
                'speaker_topics_additional_keywords': biography.speaker_topics_additional_keywords,
                'descriptive_title_type': biography.descriptive_title_type,
                'city': biography.city,
                'province_state': biography.province_state,
                'microphonetext': biography.microphonetext,
                'speaker_topics': [str(topic.topic).split('.')[-1].split(': ')[0] for topic in biography.speaker_topics],
                'descriptive_titles': [str(title.title).split('.')[-1].split(': ')[0] for title in biography.descriptive_titles],
                'speaker_tags': [str(tag.tag).split('.')[-1].split(': ')[0] for tag in biography.speaker_tags]
            }
            biography_data.append(bio)

        response_data = {
            'person_id': person.id,
            'email': person.email,
            'username': person.username,
            'biographies': biography_data,
            'fees': {},
            'images': [],
            'books': [],
            'degrees_certifications_awards': []
            
        }
        
        
        # Extract data for speaker_contact_information
        if person.speaker_contact_information:
            speaker_contact_info = person.speaker_contact_information
            response_data['speaker_contact_information'] = {
                'id': speaker_contact_info.id,
                'first_name': speaker_contact_info.first_name,
                'last_name': speaker_contact_info.last_name,
                'middle_initials': speaker_contact_info.middle_initials,
                'secondary_names_nick_name': speaker_contact_info.secondary_names_nick_name,
                'pronouns': speaker_contact_info.pronouns,
                'cell_phone': speaker_contact_info.cell_phone,
                'main_email': speaker_contact_info.main_email,
                'website_link': speaker_contact_info.website_link,
                'rss_blog_link': speaker_contact_info.rss_blog_link,
                'rss_blog_link_2': speaker_contact_info.rss_blog_link_2,
                'closest_major_airport': speaker_contact_info.closest_major_airport,
            }

        # Extract data for manager_or_teammate
        if person.manager_or_teammate:
            manager_teammate = person.manager_or_teammate
            response_data['manager_or_teammate'] = {
                'id': manager_teammate.id,
                'assist_coordinating': manager_teammate.assist_coordinating,
                'contact_info': {
                    'first_name': manager_teammate.first_name,
                    'last_name': manager_teammate.last_name,
                    'pronouns': manager_teammate.pronouns,
                    'cell_phone': manager_teammate.cell_phone,
                    'main_email': manager_teammate.main_email,
                    'website': manager_teammate.website,
                }
            }

        # Extract data for social_media_personal
        if person.social_media_personal:
            social_media_personal = person.social_media_personal
            response_data['social_media_personal'] = {
                'id': social_media_personal.id,
                'facebook': {
                    'link': social_media_personal.facebook_link,
                    'handle': social_media_personal.facebook_handle,
                    'followers': social_media_personal.facebook_followers,
                },
                'instagram': {
                    'link': social_media_personal.instagram_link,
                    'handle': social_media_personal.instagram_handle,
                    'followers': social_media_personal.instagram_followers,
                },
                'twitter': {
                    'link': social_media_personal.twitter_link,
                    'handle': social_media_personal.twitter_handle,
                    'followers': social_media_personal.twitter_followers,
                },
                'linkedin': {
                    'link': social_media_personal.linkedin_link,
                    'handle': social_media_personal.linkedin_handle,
                    'followers': social_media_personal.linkedin_followers,
                },
                'tiktok': {
                    'link': social_media_personal.tiktok_link,
                    'handle': social_media_personal.tiktok_handle,
                    'followers': social_media_personal.tiktok_followers,
                },
            }
            
        topic_description_data = []
        for topic in person.topic_descriptions:
            topic_data = {
                'topic_description_id': topic.id,
                'title': topic.title,
                'body_text': topic.body_text,
                'delivered_as': topic.delivered_as,
                'video_link': topic.video_clip,
                'audio': base64.b64encode(topic.audio_clip).decode('utf-8') if topic.audio_clip else None,
            }
            topic_description_data.append(topic_data)
        response_data['topic_descriptions'] = topic_description_data  
        
        # # Extract data for images
        # image_data = []
        # for img in person.images:
        #     img_data = {
        #         'image_id': img.id,
        #         'own_rights': img.own_right,
        #         'sbc_permissions': img.sbc_permission,
        #         'image_data': base64.b64encode(img.image_data).decode('utf-8'),  # Encode to Base64
        #         'cropped_image_data': base64.b64encode(img.croped_image_data).decode('utf-8'),  # Encode cropped image
        #     }
        #     image_data.append(img_data)

        # response_data['images'] = image_data  
        
        for img in person.images:
            if img.image_name == None or img.image_name == '':
                print("image_name is nonw ")
                image_url = None
            else:
                print("elseee",img.image_name)
                image_url= url_for('get_files',filename= img.image_name) 
            print("image_url",image_url) 
            
        for img in person.images:
            if img.crop_image_name == None or img.crop_image_name == '':
                print("crop_image_name is nonw ")
                cropped_image_url = None
            else:
                print("elseee",img.crop_image_name)
                cropped_image_url= url_for('get_files',filename= img.crop_image_name) 
            print("image_url",cropped_image_url)    

            # Append image URLs to response_data
            response_data['images'].append({
                'image_id': img.id,
                'own_rights': img.own_right,
                'sbc_permissions': img.sbc_permission,
                'image_url': image_url,
                'cropped_image_url': cropped_image_url
            })

        # # Extract data for books
        # book_data = []
        # for book in person.books:
        #     book_data.append({
        #         'id': book.id,
        #         'title': book.title,
        #         'description': book.description,
        #         'authors': book.authors,
        #         'publisher': book.publisher,
        #         'link': book.link,
        #         'cost_per_book_cad': book.cost_per_book_cad,
        #         'bulk_order_purchase_offered': book.bulk_order_purchase_offered,
        #         'price_per_book_cad': book.price_per_book_cad,
        #         'number_of_books': book.number_of_books,
        #         'upload_book_image': base64.b64encode(book.upload_book_image).decode('utf-8') if book.upload_book_image else None
        #     })

        # response_data['books'] = book_data    
                

        # Extract data for videos
        video_data = []
        for video in person.video:
            video_data.append({
                'id': video.id,
                'title': video.title,
                'link': video.link,
                'HD_QualityY/N': video.hd_quality,
                'Do_you_own_the_rights_to_this_video': video.own_rights,
                'Do_you_grant_SBC_permission_and_all_clients_permission_to_use_this_video_for_promoting_you_as_a_speaker': video.grant_permission,
                'why not': video.reason
            })

        response_data['videos'] = video_data
        
        # Extract data for podcasts
        podcast_data = []
        for podcast in person.podcasts:
            podcast_data.append({
                'id': podcast.id,
                'title': podcast.title,
                'link': podcast.link,
                'source': podcast.source
            })

        response_data['podcasts'] = podcast_data
        
        
        # # Extract data for books
        # book_data = []
        # for book in person.books:
        #     book_data.append({
        #         'id': book.id,
        #         'title': book.title,
        #         'description': book.description,
        #         'authors': book.authors,
        #         'publisher': book.publisher,
        #         'link': book.link,
        #         'cost_per_book_cad': book.cost_per_book_cad,
        #         'bulk_order_purchase_offered': book.bulk_order_purchase_offered,
        #         'price_per_book_cad': book.price_per_book_cad,
        #         'number_of_books': book.number_of_books,
        #         'upload_book_image': base64.b64encode(book.upload_book_image).decode('utf-8') if book.upload_book_image else None
        #     })

        # response_data['books'] = book_data
        
        
                
        
        
        # Iterate through the books to get book URLs
        for book in person.books:
            if book.book_name is None or book.book_name == '':
                print("book_name is None")
                book_url = None
            else:
                print("Else: ", book.book_name)
                book_url = url_for('get_files', filename=book.book_name)

            # Append book information to response_data
            response_data['books'].append({
                'title': book.title,
                'description': book.description,
                'authors': book.authors,
                'publisher': book.publisher,
                'link': book.link,
                'cost_per_book_cad': book.cost_per_book_cad,
                'bulk_order_purchase_offered': book.bulk_order_purchase_offered,
                'price_per_book_cad': book.price_per_book_cad,
                'number_of_books': book.number_of_books,
                'upload_book_image_url': book_url,
            })
        
        # Extract data for media mentions
        media_mentions_data = []
        for media_mention in person.media_mentions:
            interview_article_titles = media_mention.interview_article_title.split(', ')
            media_mentions_data.append({
                'id': media_mention.id,
                'organization_name': media_mention.organization_name,
                'interview_article_title': interview_article_titles,
                'link': media_mention.link,
                'date': media_mention.date,
                'interview_source_name': media_mention.interview_source_name
            })

        response_data['media_mentions'] = media_mentions_data
        
        
        
        # Extract data for white papers and case studies
        white_papers_case_studies_data = []
        for white_paper in person.white_papers_case_studies:
            white_papers_case_studies_data.append({
                'id': white_paper.id,
                'organization_name': white_paper.organization_name,
                'title': white_paper.title,
                'topics': white_paper.topics,
                'description': white_paper.description,
                'link': white_paper.link,
                'date': white_paper.date
            })

        response_data['white_papers_case_studies'] = white_papers_case_studies_data
        
        # # Extract data for degrees, certifications, and awards
        # degrees_certifications_awards_data = []
        # for degree in person.degree_files:
        #     degrees_certifications_awards_data.append({
        #         'id': degree.id,
        #         'degree_data': base64.b64encode(degree.degree_data).decode('utf-8')  # Encode to Base64
        #     })

        # response_data['degrees_certifications_awards'] = degrees_certifications_awards_data

            
        # Iterate through the degrees_certifications_awards to get URLs
        for degree in person.degree_files:
            if degree.degreescertificatesawards_name is None or degree.degreescertificatesawards_name == '':
                print("degreescertificatesawards_name is None")
                degree_url = None
            else:
                print("Else: ", degree.degreescertificatesawards_name)
                degree_url = url_for('get_files', filename=degree.degreescertificatesawards_name)

            # Append degree information to response_data
            response_data['degrees_certifications_awards'].append({
                'degree_id': degree.id,
                'degree_data_url': degree_url,
            })    
             
        
        # Extract data for testimonials
        testimonials_data = []
        for testimonial in person.testimonials:
            testimonials_data.append({
                'id': testimonial.id,
                'Organizer_Name': testimonial.organizer_name,
                'Testimonial_Organization_Name': testimonial.organization_name,
                'Link_to_Video': testimonial.link_to_video
            })

        response_data['testimonials'] = testimonials_data
        
        
        # Extract data for business information
        business_info_data = {}
        if person.business_info:
            business_info_data = {
                'id': person.business_info.id,
                'business_issue_payment': person.business_info.issue_payment,
                'business_information': {
                    'official_business_name': person.business_info.official_business_name,
                    'business_email': person.business_info.business_email,
                    'business_phone': person.business_info.business_phone,
                    'business_number': person.business_info.business_number,
                    'website': person.business_info.website,
                }
            }
        response_data['business_info'] = business_info_data

        # Extract data for social media (business)
        social_media_business_data = {}
        if person.social_media_business:
            social_media_business_data = {
                'id': person.social_media_business.id,
                'facebook': {
                    'link': person.social_media_business.facebook_link,
                    'handle': person.social_media_business.facebook_handle,
                    'followers': person.social_media_business.facebook_followers
                },
                'instagram': {
                    'link': person.social_media_business.instagram_link,
                    'handle': person.social_media_business.instagram_handle,
                    'followers': person.social_media_business.instagram_followers
                },
                'twitter': {
                    'link': person.social_media_business.twitter_link,
                    'handle': person.social_media_business.twitter_handle,
                    'followers': person.social_media_business.twitter_followers
                },
                'linkedin': {
                    'link': person.social_media_business.linkedin_link,
                    'handle': person.social_media_business.linkedin_handle,
                    'followers': person.social_media_business.linkedin_followers
                },
                'tiktok': {
                    'link': person.social_media_business.tiktok_link,
                    'handle': person.social_media_business.tiktok_handle,
                    'followers': person.social_media_business.tiktok_followers
                }
            }
        response_data['social_media_business'] = social_media_business_data


   
        # Extract data for Brand/Product Campaigns & Endorsements (theme 1)
        brand_campaigns_data1 = []
        for brand_campaign in person.brand_campaignstheme1:
            brand_campaigns_data1.append({
                'id': brand_campaign.id,
                'part_of_social_media': brand_campaign.part_of_social_media,
                'organization_name': brand_campaign.organization_name,
                'platforms': brand_campaign.platforms,
                'link_to_campaign': brand_campaign.link_to_campaign,
                'start_year': brand_campaign.start_year,
                'end_year': brand_campaign.end_year
            })

        response_data['Brand_Product_CampaignsEndorsementstheme1'] = brand_campaigns_data1

        # Extract data for Brand/Product Campaigns & Endorsements (theme 2)
        brand_campaigns_data2 = []
        for brand_campaign in person.brand_campaignstheme2:
            brand_campaigns_data2.append({
                'id': brand_campaign.id,
                'part_of_social_media': brand_campaign.part_of_social_media,
                'organization_name': brand_campaign.organization_name,
                'platforms': brand_campaign.platforms,
                'link_to_campaign': brand_campaign.link_to_campaign,
                'start_year': brand_campaign.start_year,
                'end_year': brand_campaign.end_year
            })

        response_data['Brand_Product_CampaignsEndorsementstheme2'] = brand_campaigns_data2
        
        
        
        # Extract data for At Events and Speaker Introduction
        at_events_data = {}
        if person.at_events:
            at_events_data = {
                'id': person.at_events.id,
                'presentation_software': {
                    'using_presentation_software': person.at_events.using_presentation_software,
                    'presentation_software_name': person.at_events.presentation_software_name
                },
                'audience_interaction_software': {
                    'using_audience_interaction_software': person.at_events.using_audience_interaction_software,
                    'audience_interaction_software_name': person.at_events.audience_interaction_software_name
                },
                'attending_sessions_before_after_presentation': person.at_events.attending_sessions_before_after_presentation,
                'meal_networking_session': {
                    'attending_meals_networking_sessions': person.at_events.attending_meals_networking_sessions,
                    'dietary_requirements_restrictions': person.at_events.dietary_requirements_restrictions,
                    'A_V_requirements': person.at_events.A_V_requirements,
                    'speaker_introduction': []
                },
                'prefer_to_book_travel': person.at_events.prefer_to_book_travel,
                'special_conditions_for_travel_arrangements': person.at_events.special_conditions_for_travel_arrangements,
                'table_for_book_sales': person.at_events.table_for_book_sales,
                'travel_agent': {
                    'use_travel_agent': person.at_events.use_travel_agent,
                    'Preferred_Seating': person.at_events.Preferred_Seating,
                    'Preferred_Airline': person.at_events.Preferred_Airline,
                    'West_Jet#': person.at_events.West_Jet_number,
                    'Air_Canada#': person.at_events.Air_Canada_number
                }
            }

            for introduction in person.at_events.speaker_introduction:
                at_events_data['meal_networking_session']['speaker_introduction'].append({
                    'id': introduction.id,
                    'introduction_text': introduction.introduction_text
                })

        response_data['at_events'] = [at_events_data]
        
        
                
        # Extract data for Help Us Book You
        help_us_book_you_data = {}
        if person.help_us_book_you:
            help_us_book_you_data = {
                'id': person.help_us_book_you.id,
                'speaker_reason_to_work_with': person.help_us_book_you.speaker_reason_to_work_with,
                'value_adds_and_offerings': {
                    'offer_any_value_adds': person.help_us_book_you.value_adds_and_offerings,
                    'books': {
                        'how_many_items': person.help_us_book_you.books_how_many_items,
                        'value_per_item': person.help_us_book_you.books_value_per_item
                    },
                    'online_training': {
                        'how_many_items': person.help_us_book_you.online_training_how_many_items,
                        'value_per_item': person.help_us_book_you.online_training_value_per_item
                    },
                    'merch': {
                        'how_many_items': person.help_us_book_you.merch_how_many_items,
                        'value_per_item': person.help_us_book_you.merch_value_per_item
                    },
                    'merch_2': {
                        'how_many_items': person.help_us_book_you.merch_2_how_many_items,
                        'value_per_item': person.help_us_book_you.merch_2_value_per_item
                    },
                },
                'complementary_virtual_follow_sessions_consultation': person.help_us_book_you.complementary_virtual_follow_sessions_consultation,
                'inclusive_of_travel_expenses': person.help_us_book_you.inclusive_of_travel_expenses,
                'industry_you_specialize_with': {
                    'industries_do_you_not_work_with': person.help_us_book_you.industries_do_you_not_work_with,
                    'favorite_audiences_event_types': person.help_us_book_you.favorite_audiences_event_types,
                    'target_audiences_industries': person.help_us_book_you.target_audiences_industries,
                },
                'English_&_French': person.help_us_book_you.English_French,
                'Q&A_in_French': person.help_us_book_you.Q_A_in_French,
                'offer_recordings': person.help_us_book_you.offer_recordings,
                'primary_source_of_income': person.help_us_book_you.primary_source_of_income,
                'speaking_frequency': {
                    'hoping_for_speaking_to_become_your_primary_source_income': person.help_us_book_you.hoping_for_speaking_to_become_your_primary_source_income,
                    'current_speak_per_month': person.help_us_book_you.current_speak_per_month,
                    'virtual_events_over_pandemic': person.help_us_book_you.virtual_events_over_pandemic,
                    'speak_per_month': person.help_us_book_you.speak_per_month,
                    'market_yourself_as_a_speaker': person.help_us_book_you.market_yourself_as_a_speaker,
                    'affiliated_with_any_other_speakers_agencies': person.help_us_book_you.affiliated_with_any_other_speakers_agencies,
                    'percentage_of_bookings': person.help_us_book_you.percentage_of_bookings,
                    'Approximately_what_percentage': person.help_us_book_you.Approximately_what_percentage,
                    'speakers_are_you_affiliated_with': person.help_us_book_you.speakers_are_you_affiliated_with
                }
            }

        response_data['Help_us_book_you'] = help_us_book_you_data

        
        
        # Extract data for Help Us Work With You
        help_us_work_with_you_data = {}
        if person.help_us_work_with_you:
            help_us_work_with_you_data = {
                'id': person.help_us_work_with_you.id,
                'newsletter_onboarding': person.help_us_work_with_you.newsletter_onboarding,
                'tracking_system': person.help_us_work_with_you.tracking_system,
                'whatsapp': person.help_us_work_with_you.whatsapp,
                'business_ownership': person.help_us_work_with_you.business_ownership,
                'crm_usage': person.help_us_work_with_you.crm_usage,
                'appointment_booking_software': person.help_us_work_with_you.appointment_booking_software,
                'expectations_with_sbc': person.help_us_work_with_you.expectations_with_sbc,
                'something_about_you': person.help_us_work_with_you.something_about_you,
                'stories': person.help_us_work_with_you.stories,
            }

        response_data['Help_us_work_with_you'] = help_us_work_with_you_data

        if person.fees:
            response_data['fees'] = {
                'id': person.fees.id,  # Include the ID
                'Pro_Bono_Events': person.fees.Pro_Bono_Events,
                'Corporate_Keynote_20_60_Minutes': person.fees.Corporate_Keynote_20_60_Minutes,
                'Corporate_Workshop_60_120_Minutes': person.fees.Corporate_Workshop_60_120_Minutes,
                'Corporate_Half_Day_Training_or_Keynote_Breakout': person.fees.Corporate_Half_Day_Training_or_Keynote_Breakout,
                'Corporate_Full_Day_Training': person.fees.Corporate_Full_Day_Training,
                'Concurrent_Sessions_Fee': person.fees.Concurrent_Sessions_Fee,
                'One_Session_in_the_Morning_Fee': person.fees.One_Session_in_the_Morning_Fee,
                'One_Session_in_the_Afternoon_Fee': person.fees.One_Session_in_the_Afternoon_Fee,
                'Multiple_Sessions_on_Concurrent_Days': person.fees.Multiple_Sessions_on_Concurrent_Days,
                'Multiple_Sessions_Over_a_Period_of_Time': person.fees.Multiple_Sessions_Over_a_Period_of_Time,
                'Lowest_Acceptance_for_Informal_Talk': person.fees.Lowest_Acceptance_for_Informal_Talk,
                'One_Day_Event': person.fees.One_Day_Event,
                'One_Day_Plus_Evening_Ceremony_Keynote': person.fees.One_Day_Plus_Evening_Ceremony_Keynote,
                'Two_Day_Event': person.fees.Two_Day_Event,
                'Two_Day_Plus_Evening_Ceremony_Keynote': person.fees.Two_Day_Plus_Evening_Ceremony_Keynote,
                'Three_Day_Event': person.fees.Three_Day_Event,
                'Three_Day_Plus_Evening_Ceremony_Keynote': person.fees.Three_Day_Plus_Evening_Ceremony_Keynote,
                'Four_Day_Event': person.fees.Four_Day_Event,
                'Four_Day_Plus_Evening_Ceremony_Keynote': person.fees.Four_Day_Plus_Evening_Ceremony_Keynote,
                'What_is_your_corporate_speaker_fee': person.fees.What_is_your_corporate_speaker_fee,
                'lowest_you_will_accept': person.fees.lowest_you_will_accept,
                'limitations_or_condition': person.fees.limitations_or_condition,
                'Driving_Distance_Fee': person.fees.Driving_Distance_Fee,
                'Province_Fee': person.fees.Province_Fee,
                'Western_Canada_Fee': person.fees.Western_Canada_Fee,
                'Eastern_Canada_Fee': person.fees.Eastern_Canada_Fee,
                'Northern_Canada_Fee': person.fees.Northern_Canada_Fee,
                'Remote_Location_Fee': person.fees.Remote_Location_Fee,
                'Local_Discount': person.fees.Local_Discount,
                'Local_Fee': person.fees.Local_Fee,
                'Client_Direct_Approach_for_Local_Event': person.fees.Client_Direct_Approach_for_Local_Event,
                'Virtual_Discount': person.fees.Virtual_Discount,
                'Virtual_Fee': person.fees.Virtual_Fee,
                'Client_Direct_Approach_for_Virtual_Event': person.fees.Client_Direct_Approach_for_Virtual_Event,
                'Small_Audience_Discount': person.fees.Small_Audience_Discount,
                'Small_Audience_Fee': person.fees.Small_Audience_Fee,
                'Client_Direct_Approach_for_Small_Audience_Event': person.fees.Client_Direct_Approach_for_Small_Audience_Event,
                'Qualification_for_Small_Audience': person.fees.Qualification_for_Small_Audience,
                'Nonprofit_Discount': person.fees.Nonprofit_Discount,
                'Nonprofit_Fee': person.fees.Nonprofit_Fee,
                'Client_Direct_Approach_for_Nonprofit': person.fees.Client_Direct_Approach_for_Nonprofit,
                'Charitable_Organization_Discount': person.fees.Charitable_Organization_Discount,
                'Charitable_Fee': person.fees.Charitable_Fee,
                'Client_Direct_Approach_for_Charitable_Organization': person.fees.Client_Direct_Approach_for_Charitable_Organization,
                'outside_of_speaker_fee_ranges': person.fees.outside_of_speaker_fee_ranges,
                'Rate_Increase': person.fees.Rate_Increase,
            }
        
        
        # Extract data for Speaker Pitches
        speaker_pitches_data = []
        for pitch in person.speaker_pitches:
            pitch_data = {
                'id': pitch.id,
                'general_pitch': pitch.general_pitch,
                'keyword_topic_focus_pitch': pitch.keyword_topic_focus_pitch,
                'Short_pitch_up': pitch.Short_pitch_up,

            }
            speaker_pitches_data.append(pitch_data)

        response_data['speaker_pitches'] = speaker_pitches_data
        
        
        # Extract data for Previous Clients
        previous_clients_data = []
        for client in person.previous_clients:
            client_data = {
                'id': client.id,  # Include the ID
                'organization_name': client.organization_name,
                
            }
            previous_clients_data.append(client_data)

        response_data['previous_clients'] = previous_clients_data
    
            

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify(error=str(e)), 400
    
    
# Add new routes for serving images dynamically
@app.route('/get_all_dataa_images/<int:person_id>/<int:image_id>', methods=['GET'])
def get_all_dataa_images(person_id, image_id):
    try:
        # Fetch the image from the database based on person_id and image_id
        img = Images.query.filter_by(person_id=person_id, id=image_id).first()
        if img is None:
            return jsonify(error='Image not found'), 404

        # Return the image data as a response
        return send_file(io.BytesIO(img.image_data), mimetype='image/png')

    except Exception as e:
        return jsonify(error=str(e)), 400

# Add new routes for serving cropped images dynamically
@app.route('/get_all_dataa_cropped_images/<int:person_id>/<int:image_id>', methods=['GET'])
def get_all_dataa_cropped_images(person_id, image_id):
    try:
        # Fetch the image from the database based on person_id and image_id
        img = Images.query.filter_by(person_id=person_id, id=image_id).first()
        if img is None:
            return jsonify(error='Image not found'), 404

        # Perform any cropping logic here if needed

        # Return the cropped image data as a response
        return send_file(io.BytesIO(img.image_data), mimetype='image/png')

    except Exception as e:
        return jsonify(error=str(e)), 400    
    
    
# @app.route('/get_all_data/<int:person_id>', methods=['GET'])
# def get_all_data(person_id):
#     try:
#         person = Person.query.get(person_id)
#         print('person----->',person)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404

#         response_data = {
#             'person_id': person.id,
#             'email': person.email,
#             'username': person.username,
            # Extract Fees data
            # 'fees': {
                
            #     'id': person.fees.id,  # Include the ID
            #     'Pro_Bono_Events': person.fees.Pro_Bono_Events,
            #     'Corporate_Keynote_20_60_Minutes': person.fees.Corporate_Keynote_20_60_Minutes,
            #     'Corporate_Workshop_60_120_Minutes': person.fees.Corporate_Workshop_60_120_Minutes,
            #     'Corporate_Half_Day_Training_or_Keynote_Breakout': person.fees.Corporate_Half_Day_Training_or_Keynote_Breakout,
            #     'Corporate_Full_Day_Training': person.fees.Corporate_Full_Day_Training,
            #     'Concurrent_Sessions_Fee': person.fees.Concurrent_Sessions_Fee,
            #     'One_Session_in_the_Morning_Fee': person.fees.One_Session_in_the_Morning_Fee,
            #     'One_Session_in_the_Afternoon_Fee': person.fees.One_Session_in_the_Afternoon_Fee,
            #     'Multiple_Sessions_on_Concurrent_Days': person.fees.Multiple_Sessions_on_Concurrent_Days,
            #     'Multiple_Sessions_Over_a_Period_of_Time': person.fees.Multiple_Sessions_Over_a_Period_of_Time,
            #     'Lowest_Acceptance_for_Informal_Talk': person.fees.Lowest_Acceptance_for_Informal_Talk,
            #     'One_Day_Event': person.fees.One_Day_Event,
            #     'One_Day_Plus_Evening_Ceremony_Keynote': person.fees.One_Day_Plus_Evening_Ceremony_Keynote,
            #     'Two_Day_Event': person.fees.Two_Day_Event,
            #     'Two_Day_Plus_Evening_Ceremony_Keynote': person.fees.Two_Day_Plus_Evening_Ceremony_Keynote,
            #     'Three_Day_Event': person.fees.Three_Day_Event,
            #     'Three_Day_Plus_Evening_Ceremony_Keynote': person.fees.Three_Day_Plus_Evening_Ceremony_Keynote,
            #     'Four_Day_Event': person.fees.Four_Day_Event,
            #     'Four_Day_Plus_Evening_Ceremony_Keynote': person.fees.Four_Day_Plus_Evening_Ceremony_Keynote,
            #     'What_is_your_corporate_speaker_fee': person.fees.What_is_your_corporate_speaker_fee,
            #     'lowest_you_will_accept': person.fees.lowest_you_will_accept,
            #     'limitations_or_condition': person.fees.limitations_or_condition,
            #     'Driving_Distance_Fee': person.fees.Driving_Distance_Fee,
            #     'Province_Fee': person.fees.Province_Fee,
            #     'Western_Canada_Fee': person.fees.Western_Canada_Fee,
            #     'Eastern_Canada_Fee': person.fees.Eastern_Canada_Fee,
            #     'Northern_Canada_Fee': person.fees.Northern_Canada_Fee,
            #     'Remote_Location_Fee': person.fees.Remote_Location_Fee,
            #     'Local_Discount': person.fees.Local_Discount,
            #     'Local_Fee': person.fees.Local_Fee,
            #     'Client_Direct_Approach_for_Local_Event': person.fees.Client_Direct_Approach_for_Local_Event,
            #     'Virtual_Discount': person.fees.Virtual_Discount,
            #     'Virtual_Fee': person.fees.Virtual_Fee,
            #     'Client_Direct_Approach_for_Virtual_Event': person.fees.Client_Direct_Approach_for_Virtual_Event,
            #     'Small_Audience_Discount': person.fees.Small_Audience_Discount,
            #     'Small_Audience_Fee': person.fees.Small_Audience_Fee,
            #     'Client_Direct_Approach_for_Small_Audience_Event': person.fees.Client_Direct_Approach_for_Small_Audience_Event,
            #     'Qualification_for_Small_Audience': person.fees.Qualification_for_Small_Audience,
            #     'Nonprofit_Discount': person.fees.Nonprofit_Discount,
            #     'Nonprofit_Fee': person.fees.Nonprofit_Fee,
            #     'Client_Direct_Approach_for_Nonprofit': person.fees.Client_Direct_Approach_for_Nonprofit,
            #     'Charitable_Organization_Discount': person.fees.Charitable_Organization_Discount,
            #     'Charitable_Fee': person.fees.Charitable_Fee,
            #     'Client_Direct_Approach_for_Charitable_Organization': person.fees.Client_Direct_Approach_for_Charitable_Organization,
            #     'outside_of_speaker_fee_ranges': person.fees.outside_of_speaker_fee_ranges,
            #     'Rate_Increase': person.fees.Rate_Increase,
                
            # },
           
        
    #     }

    #     # Extract data for speaker_contact_information
    #     if person.speaker_contact_information:
    #         speaker_contact_info = person.speaker_contact_information
    #         response_data['speaker_contact_information'] = {
    #             'id': speaker_contact_info.id,
    #             'first_name': speaker_contact_info.first_name,
    #             'last_name': speaker_contact_info.last_name,
    #             'middle_initials': speaker_contact_info.middle_initials,
    #             'secondary_names_nick_name': speaker_contact_info.secondary_names_nick_name,
    #             'pronouns': speaker_contact_info.pronouns,
    #             'cell_phone': speaker_contact_info.cell_phone,
    #             'main_email': speaker_contact_info.main_email,
    #             'website_link': speaker_contact_info.website_link,
    #             'rss_blog_link': speaker_contact_info.rss_blog_link,
    #             'rss_blog_link_2': speaker_contact_info.rss_blog_link_2,
    #             'closest_major_airport': speaker_contact_info.closest_major_airport,
    #         }

    #     # Extract data for manager_or_teammate
    #     if person.manager_or_teammate:
    #         manager_teammate = person.manager_or_teammate
    #         response_data['manager_or_teammate'] = {
    #             'id': manager_teammate.id,
    #             'assist_coordinating': manager_teammate.assist_coordinating,
    #             'contact_info': {
    #                 'first_name': manager_teammate.first_name,
    #                 'last_name': manager_teammate.last_name,
    #                 'pronouns': manager_teammate.pronouns,
    #                 'cell_phone': manager_teammate.cell_phone,
    #                 'main_email': manager_teammate.main_email,
    #                 'website': manager_teammate.website,
    #             }
    #         }

    #     # Extract data for social_media_personal
    #     if person.social_media_personal:
    #         social_media_personal = person.social_media_personal
    #         response_data['social_media_personal'] = {
    #             'id': social_media_personal.id,
    #             'facebook': {
    #                 'link': social_media_personal.facebook_link,
    #                 'handle': social_media_personal.facebook_handle,
    #                 'followers': social_media_personal.facebook_followers,
    #             },
    #             'instagram': {
    #                 'link': social_media_personal.instagram_link,
    #                 'handle': social_media_personal.instagram_handle,
    #                 'followers': social_media_personal.instagram_followers,
    #             },
    #             'twitter': {
    #                 'link': social_media_personal.twitter_link,
    #                 'handle': social_media_personal.twitter_handle,
    #                 'followers': social_media_personal.twitter_followers,
    #             },
    #             'linkedin': {
    #                 'link': social_media_personal.linkedin_link,
    #                 'handle': social_media_personal.linkedin_handle,
    #                 'followers': social_media_personal.linkedin_followers,
    #             },
    #             'tiktok': {
    #                 'link': social_media_personal.tiktok_link,
    #                 'handle': social_media_personal.tiktok_handle,
    #                 'followers': social_media_personal.tiktok_followers,
    #             },
    #         }
            
            
    #     # bio = []
        
    #     # speaker_topic = []
    #     # for topic in biography.speaker_topics:
    #     #     name = str(topic.topic).split('.')[-1].split(': ')[0]
    #     #     speaker_topic.append(name)

    #     # speaker_tag = []
    #     # for tag in biography.speaker_tags:
    #     #     name = str(tag.tag).split('.')[-1].split(': ')[0]
    #     #     speaker_tag.append(name)

    #     # descriptive_title = []
    #     # for title in biography.descriptive_titles:
    #     #     name = str(title.title).split('.')[-1].split(': ')[0]
    #     #     descriptive_title.append(name)

    #     # # Create a dictionary to store biography data
    #     # biography_data = {
    #     #     'biography_id': biography.id,
    #     #     'highlight': biography.highlight,
    #     #     'long_bio': biography.long_bio,
    #     #     'sort_bio': biography.sort_bio,
    #     #     'speaker_topics_additional_keywords': biography.speaker_topics_additional_keywords,
    #     #     'descriptive_title_type': biography.descriptive_title_type,
    #     #     'city': biography.city,
    #     #     'province_state': biography.province_state,
    #     #     'microphonetext': biography.microphonetext,
    #     # }

    #     # # Append both dictionaries to the list
    #     # bio.append({'speaker_topic': speaker_topic, 'biography_data': biography_data, 'speaker_tag': speaker_tag, 'descriptive_title': descriptive_title})
        
        
        
    #     topic_description_data = []
    #     for topic in person.topic_descriptions:
    #         topic_data = {
    #             'topic_description_id': topic.id,
    #             'title': topic.title,
    #             'body_text': topic.body_text,
    #             'delivered_as': topic.delivered_as,
    #             'video_link': topic.video_clip,
    #             'audio': base64.b64encode(topic.audio_clip).decode('utf-8'),
    #         }
    #         topic_description_data.append(topic_data)

    #     response_data['topic_descriptions'] = topic_description_data
        
    #     # Extract data for images
    #     image_data = []
    #     for img in person.images:
    #         img_data = {
    #             'image_id': img.id,
    #             'own_rights': img.own_right,
    #             'sbc_permissions': img.sbc_permission,
    #             'image_data': base64.b64encode(img.image_data).decode('utf-8'),  # Encode to Base64
    #             'cropped_image_data': base64.b64encode(img.croped_image_data).decode('utf-8'),  # Encode cropped image
    #         }
    #         image_data.append(img_data)

    #     response_data['images'] = image_data
        
    #     # Extract data for videos
    #     video_data = []
    #     for video in person.video:
    #         video_data.append({
    #             'id': video.id,
    #             'title': video.title,
    #             'link': video.link,
    #             'HD_QualityY/N': video.hd_quality,
    #             'Do_you_own_the_rights_to_this_video': video.own_rights,
    #             'Do_you_grant_SBC_permission_and_all_clients_permission_to_use_this_video_for_promoting_you_as_a_speaker': video.grant_permission,
    #             'why not': video.reason
    #         })

    #     response_data['videos'] = video_data
        
    #     # Extract data for podcasts
    #     podcast_data = []
    #     for podcast in person.podcasts:
    #         podcast_data.append({
    #             'id': podcast.id,
    #             'title': podcast.title,
    #             'link': podcast.link,
    #             'source': podcast.source
    #         })

    #     response_data['podcasts'] = podcast_data
        
        
    #     # Extract data for books
    #     book_data = []
    #     for book in person.books:
    #         book_data.append({
    #             'id': book.id,
    #             'title': book.title,
    #             'description': book.description,
    #             'authors': book.authors,
    #             'publisher': book.publisher,
    #             'link': book.link,
    #             'cost_per_book_cad': book.cost_per_book_cad,
    #             'bulk_order_purchase_offered': book.bulk_order_purchase_offered,
    #             'price_per_book_cad': book.price_per_book_cad,
    #             'number_of_books': book.number_of_books
    #         })

    #     response_data['books'] = book_data
        
        
    #     # Extract data for media mentions
    #     media_mentions_data = []
    #     for media_mention in person.media_mentions:
    #         interview_article_titles = media_mention.interview_article_title.split(', ')
    #         media_mentions_data.append({
    #             'id': media_mention.id,
    #             'organization_name': media_mention.organization_name,
    #             'interview_article_title': interview_article_titles,
    #             'link': media_mention.link,
    #             'date': media_mention.date,
    #             'interview_source_name': media_mention.interview_source_name
    #         })

    #     response_data['media_mentions'] = media_mentions_data
        
        
        
    #     # Extract data for white papers and case studies
    #     white_papers_case_studies_data = []
    #     for white_paper in person.white_papers_case_studies:
    #         white_papers_case_studies_data.append({
    #             'id': white_paper.id,
    #             'organization_name': white_paper.organization_name,
    #             'title': white_paper.title,
    #             'topics': white_paper.topics,
    #             'description': white_paper.description,
    #             'link': white_paper.link,
    #             'date': white_paper.date
    #         })

    #     response_data['white_papers_case_studies'] = white_papers_case_studies_data
        
    #     # Extract data for degrees, certifications, and awards
    #     degrees_certifications_awards_data = []
    #     for degree in person.degree_files:
    #         degrees_certifications_awards_data.append({
    #             'id': degree.id,
    #             'degree_data': base64.b64encode(degree.degree_data).decode('utf-8')  # Encode to Base64
    #         })

    #     response_data['degrees_certifications_awards'] = degrees_certifications_awards_data
        
    #     # Extract data for testimonials
    #     testimonials_data = []
    #     for testimonial in person.testimonials:
    #         testimonials_data.append({
    #             'id': testimonial.id,
    #             'Organizer_Name': testimonial.organizer_name,
    #             'Testimonial_Organization_Name': testimonial.organization_name,
    #             'Link_to_Video': testimonial.link_to_video
    #         })

    #     response_data['testimonials'] = testimonials_data
        
        
    #     # Extract data for business information
    #     business_info_data = {
    #         'id': person.business_info.id,
    #         'business_issue_payment': person.business_info.issue_payment,
    #         'business_information': {
    #             'official_business_name': person.business_info.official_business_name,
    #             'business_email': person.business_info.business_email,
    #             'business_phone': person.business_info.business_phone,
    #             'business_number': person.business_info.business_number,
    #             'website': person.business_info.website,
    #         }
    #     }
    #     response_data['business_info'] = business_info_data

    #     # Extract data for social media (business)
    #     social_media_business_data = {
    #         'id': person.social_media_business.id,
    #         'facebook': {
    #             'link': person.social_media_business.facebook_link,
    #             'handle': person.social_media_business.facebook_handle,
    #             'followers': person.social_media_business.facebook_followers
    #         },
    #         'instagram': {
    #             'link': person.social_media_business.instagram_link,
    #             'handle': person.social_media_business.instagram_handle,
    #             'followers': person.social_media_business.instagram_followers
    #         },
    #         'twitter': {
    #             'link': person.social_media_business.twitter_link,
    #             'handle': person.social_media_business.twitter_handle,
    #             'followers': person.social_media_business.twitter_followers
    #         },
    #         'linkedin': {
    #             'link': person.social_media_business.linkedin_link,
    #             'handle': person.social_media_business.linkedin_handle,
    #             'followers': person.social_media_business.linkedin_followers
    #         },
    #         'tiktok': {
    #             'link': person.social_media_business.tiktok_link,
    #             'handle': person.social_media_business.tiktok_handle,
    #             'followers': person.social_media_business.tiktok_followers
    #         }
    #     }
    #     response_data['social_media_business'] = social_media_business_data

   
    #     # Extract data for Brand/Product Campaigns & Endorsements (theme 1)
    #     brand_campaigns_data1 = []
    #     for brand_campaign in person.brand_campaignstheme1:
    #         brand_campaigns_data1.append({
    #             'id': brand_campaign.id,
    #             'part_of_social_media': brand_campaign.part_of_social_media,
    #             'organization_name': brand_campaign.organization_name,
    #             'platforms': brand_campaign.platforms,
    #             'link_to_campaign': brand_campaign.link_to_campaign,
    #             'start_year': brand_campaign.start_year,
    #             'end_year': brand_campaign.end_year
    #         })

    #     response_data['Brand_Product_CampaignsEndorsementstheme1'] = brand_campaigns_data1

    #     # Extract data for Brand/Product Campaigns & Endorsements (theme 2)
    #     brand_campaigns_data2 = []
    #     for brand_campaign in person.brand_campaignstheme2:
    #         brand_campaigns_data2.append({
    #             'id': brand_campaign.id,
    #             'part_of_social_media': brand_campaign.part_of_social_media,
    #             'organization_name': brand_campaign.organization_name,
    #             'platforms': brand_campaign.platforms,
    #             'link_to_campaign': brand_campaign.link_to_campaign,
    #             'start_year': brand_campaign.start_year,
    #             'end_year': brand_campaign.end_year
    #         })

    #     response_data['Brand_Product_CampaignsEndorsementstheme2'] = brand_campaigns_data2
        
        
        
    #     # Extract data for At Events and Speaker Introduction
    #     at_events_data = {
    #         'id': person.at_events.id,
    #         'presentation_software': {
    #             'using_presentation_software': person.at_events.using_presentation_software,
    #             'presentation_software_name': person.at_events.presentation_software_name
    #         },
    #         'audience_interaction_software': {
    #             'using_audience_interaction_software': person.at_events.using_audience_interaction_software,
    #             'audience_interaction_software_name': person.at_events.audience_interaction_software_name
    #         },
    #         'attending_sessions_before_after_presentation': person.at_events.attending_sessions_before_after_presentation,
    #         'meal_networking_session': {
    #             'attending_meals_networking_sessions': person.at_events.attending_meals_networking_sessions,
    #             'dietary_requirements_restrictions': person.at_events.dietary_requirements_restrictions,
    #             'A_V_requirements': person.at_events.A_V_requirements,
    #             'speaker_introduction': []
    #         },
    #         'prefer_to_book_travel': person.at_events.prefer_to_book_travel,
    #         'special_conditions_for_travel_arrangements': person.at_events.special_conditions_for_travel_arrangements,
    #         'table_for_book_sales': person.at_events.table_for_book_sales,
    #         'travel_agent': {
    #             'use_travel_agent': person.at_events.use_travel_agent,
    #             'Preferred_Seating': person.at_events.Preferred_Seating,
    #             'Preferred_Airline': person.at_events.Preferred_Airline,
    #             'West_Jet#': person.at_events.West_Jet_number,
    #             'Air_Canada#': person.at_events.Air_Canada_number
    #         }
    #     }

    #     for introduction in person.at_events.speaker_introduction:
    #         at_events_data['meal_networking_session']['speaker_introduction'].append({
    #             'id': introduction.id,
    #             'introduction_text': introduction.introduction_text
    #         })

    #     response_data['at_events'] = [at_events_data]
        
        
        
    #     # Extract data for Help Us Book You
    #     help_us_book_you_data = {
    #         'id': person.help_us_book_you.id,
    #         'speaker_reason_to_work_with': person.help_us_book_you.speaker_reason_to_work_with,
    #         'value_adds_and_offerings': {
    #             'offer_any_value_adds': person.help_us_book_you.value_adds_and_offerings,
    #             'books': {
    #                 'how_many_items': person.help_us_book_you.books_how_many_items,
    #                 'value_per_item': person.help_us_book_you.books_value_per_item
    #             },
    #             'online_training': {
    #                 'how_many_items': person.help_us_book_you.online_training_how_many_items,
    #                 'value_per_item': person.help_us_book_you.online_training_value_per_item
    #             },
    #             'merch': {
    #                 'how_many_items': person.help_us_book_you.merch_how_many_items,
    #                 'value_per_item': person.help_us_book_you.merch_value_per_item
    #             },
    #             'merch_2': {
    #                 'how_many_items': person.help_us_book_you.merch_2_how_many_items,
    #                 'value_per_item': person.help_us_book_you.merch_2_value_per_item
    #             },
    #         },
    #         'complementary_virtual_follow_sessions_consultation': person.help_us_book_you.complementary_virtual_follow_sessions_consultation,
    #         'inclusive_of_travel_expenses': person.help_us_book_you.inclusive_of_travel_expenses,
    #         'industry_you_specialize_with': {
    #             'industries_do_you_not_work_with': person.help_us_book_you.industries_do_you_not_work_with,
    #             'favorite_audiences_event_types': person.help_us_book_you.favorite_audiences_event_types,
    #             'target_audiences_industries': person.help_us_book_you.target_audiences_industries,
    #         },
    #         'English_&_French': person.help_us_book_you.English_French,
    #         'Q&A_in_French': person.help_us_book_you.Q_A_in_French,
    #         'offer_recordings': person.help_us_book_you.offer_recordings,
    #         'primary_source_of_income': person.help_us_book_you.primary_source_of_income,
    #         'speaking_frequency': {
    #             'hoping_for_speaking_to_become_your_primary_source_income': person.help_us_book_you.hoping_for_speaking_to_become_your_primary_source_income,
    #             'current_speak_per_month': person.help_us_book_you.current_speak_per_month,
    #             'virtual_events_over_pandemic': person.help_us_book_you.virtual_events_over_pandemic,
    #             'speak_per_month': person.help_us_book_you.speak_per_month,
    #             'market_yourself_as_a_speaker': person.help_us_book_you.market_yourself_as_a_speaker,
    #             'affiliated_with_any_other_speakers_agencies': person.help_us_book_you.affiliated_with_any_other_speakers_agencies,
    #             'percentage_of_bookings': person.help_us_book_you.percentage_of_bookings,
    #             'Approximately_what_percentage': person.help_us_book_you.Approximately_what_percentage,
    #             'speakers_are_you_affiliated_with': person.help_us_book_you.speakers_are_you_affiliated_with
    #         }
    #     }

    #     response_data['Help_us_book_you'] = help_us_book_you_data
        
        
    #     # Extract data for Help Us Work With You
    #     help_us_work_with_you_data = {
    #         'id': person.help_us_work_with_you.id,
    #         'newsletter_onboarding': person.help_us_work_with_you.newsletter_onboarding,
    #         'tracking_system': person.help_us_work_with_you.tracking_system,
    #         'whatsapp': person.help_us_work_with_you.whatsapp,
    #         'business_ownership': person.help_us_work_with_you.business_ownership,
    #         'crm_usage': person.help_us_work_with_you.crm_usage,
    #         'appointment_booking_software': person.help_us_work_with_you.appointment_booking_software,
    #         'expectations_with_sbc': person.help_us_work_with_you.expectations_with_sbc,
    #         'something_about_you': person.help_us_work_with_you.something_about_you,
    #         'stories': person.help_us_work_with_you.stories,
    #     }

    #     response_data['Help_us_work_with_you'] = help_us_work_with_you_data
        
        
    #     # Extract data for Speaker Pitches
    #     speaker_pitches_data = []
    #     for pitch in person.speaker_pitches:
    #         pitch_data = {
    #             'id': pitch.id,
    #             'general_pitch': pitch.general_pitch,
    #             'keyword_topic_focus_pitch': pitch.keyword_topic_focus_pitch,
    #             'Short_pitch_up': pitch.Short_pitch_up,

    #         }
    #         speaker_pitches_data.append(pitch_data)

    #     response_data['speaker_pitches'] = speaker_pitches_data
        
        
    #     # Extract data for Previous Clients
    #     previous_clients_data = []
    #     for client in person.previous_clients:
    #         client_data = {
    #             'id': client.id,  # Include the ID
    #             'organization_name': client.organization_name,
                
    #         }
    #         previous_clients_data.append(client_data)

    #     response_data['previous_clients'] = previous_clients_data


    #     return jsonify(response_data), 200

    # except Exception as e:
    #     return jsonify(error=str(e)), 400
    
 


# @app.route('/get_all_data/<int:person_id>', methods=['GET'])
# def get_all_data(person_id):
#     try:
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404

#         # Extract all the fields and IDs for the person
#         person_data = {
#             'person_id': person.id,
#             'name': person.name,
#             # Add other person fields here
#         }

#         users_data = []
#         for user in person.userdetails:
#             user_data = {
#                 'user_id': user.id,
#                 'email': user.email,
#                 'username': user.username,
#                 'password': user.password,
#             }
#             users_data.append(user_data)
        
        
#         speaker_contact_info = person.speaker_contact_information
#         if speaker_contact_info is None:
#             return jsonify(error='Speaker contact information not found for this person'), 404

#         manager_teammate = person.manager_or_teammate
#         if manager_teammate is None:
#             return jsonify(error='Manager or teammate information not found for this person'), 404

#         social_media_personal = person.social_media_personal
#         if social_media_personal is None:
#             return jsonify(error='Social media personal information not found for this person'), 404

#         response_data = {
#             'person': person_data,
#             'users': users_data,
#             "speaker_contact_information": {
#                 "id":speaker_contact_info.id,
#                 "first_name": speaker_contact_info.first_name,
#                 "last_name": speaker_contact_info.last_name,
#                 "middle_initials": speaker_contact_info.middle_initials,
#                 "secondary_names_nick_name": speaker_contact_info.secondary_names_nick_name,
#                 "pronouns": speaker_contact_info.pronouns,
#                 "cell_phone": speaker_contact_info.cell_phone,
#                 "main_email": speaker_contact_info.main_email,
#                 "website_link": speaker_contact_info.website_link,
#                 "rss_blog_link": speaker_contact_info.rss_blog_link,
#                 "rss_blog_link_2": speaker_contact_info.rss_blog_link_2,
#                 "closest_major_airport": speaker_contact_info.closest_major_airport
#             },
#             "manager_or_teammate": {
#                 "id":manager_teammate.id,
#                 "assist_coordinating": manager_teammate.assist_coordinating,
#                 "contact_info": {
#                     "first_name": manager_teammate.first_name,
#                     "last_name": manager_teammate.last_name,
#                     "pronouns": manager_teammate.pronouns,
#                     "cell_phone": manager_teammate.cell_phone,
#                     "main_email": manager_teammate.main_email,
#                     "website": manager_teammate.website
#                 }
#             },
#             "social_media_personal": {
#                 "id":social_media_personal.id,
#                 "facebook": {
#                     "link": social_media_personal.facebook_link,
#                     "handle": social_media_personal.facebook_handle,
#                     "followers": social_media_personal.facebook_followers
#                 },
#                 "instagram": {
#                     "link": social_media_personal.instagram_link,
#                     "handle": social_media_personal.instagram_handle,
#                     "followers": social_media_personal.instagram_followers
#                 },
#                 "twitter": {
#                     "link": social_media_personal.twitter_link,
#                     "handle": social_media_personal.twitter_handle,
#                     "followers": social_media_personal.twitter_followers
#                 },
#                 "linkedin": {
#                     "link": social_media_personal.linkedin_link,
#                     "handle": social_media_personal.linkedin_handle,
#                     "followers": social_media_personal.linkedin_followers
#                 },
#                 "tiktok": {
#                     "link": social_media_personal.tiktok_link,
#                     "handle": social_media_personal.tiktok_handle,
#                     "followers": social_media_personal.tiktok_followers
#                 }
#             }
#         }
        
#         # Stage 2 data
#         biography_data = []
#         for bio in person.biography:
#             bio_data = {
#                 'biography_id': bio.id,
#                 'highlight': bio.highlight,
#                 'sort_bio': bio.sort_bio,
#                 'long_bio': bio.long_bio,
#                 'speaker_topics': bio.speaker_topics,
#                 'speaker_topics_additional_keywords': bio.speaker_topics_additional_keywords,
#                 'speaker_tags': bio.speaker_tags,
#                 'descriptive_title_type': bio.descriptive_title_type,
#                 'descriptive_title_1': bio.descriptive_title_1,
#                 'descriptive_title_2': bio.descriptive_title_2,
#                 'descriptive_title_3': bio.descriptive_title_3,
#                 'city': bio.city,
#                 'province_state': bio.province_state,
#                 'microphone': base64.b64encode(bio.microphone).decode('utf-8')  # Encode to Base64
#             }
#             biography_data.append(bio_data)
        
#         # Include stage3 data
#         topic_description_data = []
#         for topic in person.topic_descriptions:
#             topic_data = {
#                 'topic_description_id': topic.id,
#                 'title': topic.title,
#                 'body_text': topic.body_text,
#                 'delivered_as': topic.delivered_as,
#                 'video_link': topic.video_clip,
#                 'audio':base64.b64encode(topic.audio_clip).decode('utf-8') 
#             }
#             topic_description_data.append(topic_data)

#         # Include stage4 data
#         image_data = []
#         for img in person.images:
#             img_data = {
#                 'image_id': img.id,
#                 'own_rights': img.own_right,
#                 'sbc_permissions': img.sbc_permission,
#                 'image_data': base64.b64encode(img.image_data).decode('utf-8')  # Encode to Base64
#             }
#             image_data.append(img_data)
            
                
#         video_data = []
#         for video in person.video:
#             video_data.append({
#                 'id':video.id,
#                 'title': video.title,
#                 'link': video.link,
#                 'HD_QualityY/N': video.hd_quality,
#                 'Do_you_own_the_rights_to_this_video': video.own_rights,
#                 'Do_you_grant_SBC_permission_and_all_clients_permission_to_use_this_video_for_promoting_you_as_a_speaker': video.grant_permission,
#                 'why not': video.reason
#             })

#         # Include stage 4 data (podcasts)
#         podcast_data = []
#         for podcast in person.podcasts:
#             podcast_data.append({
#                 'id':podcast.id,
#                 'title': podcast.title,
#                 'link': podcast.link,
#                 'source': podcast.source
#             })

#         # Combine all data
#         response_data['biography'] = biography_data
#         response_data['topic_descriptions'] = topic_description_data
#         response_data['images'] = image_data
#         response_data['videos'] = video_data
#         response_data['podcasts'] = podcast_data   


#         return jsonify(response_data), 200

#     except Exception as e:
#         return jsonify(error=str(e)), 400





    
    
    
    
    
# @app.route('/person/<int:person_id>', methods=['GET'])
# def get_person(person_id):
#     try:
#         person = Person.query.filter_by(id=person_id).first()
        
#         if person is None:
#             return jsonify(message='Person not found'), 404

#                 # Build a dictionary to represent the person and their related data
#         if person is not None:
            
#             person_data = {
#                 'id': person.id,
#                 'name': person.name,
#                 'age': person.age,
#                 'Biography': {
#                     'id': person.biography.id,
#                     'Long_Bio': person.biography.long_bio,
#                     'Speaker_Topics': person.biography.speaker_topics,
#                     'Speaker_Topics_additional_keywords_separated_by_commas': person.biography.speaker_topics_additional_keywords,
#                     'Speaker_Tags': person.biography.speaker_tags,
#                     'Sort_Bio': person.biography.sort_bio,
#                     'Introductory_Bio': person.biography.introductory_bio,
#                     'Descriptive_Title_Type': person.biography.descriptive_title_type,
#                     'Descriptive_Title_1': person.biography.descriptive_title_1,
#                     'Descriptive_Title_2': person.biography.descriptive_title_2,
#                     'Descriptive_Title_3': person.biography.descriptive_title_3,
#                     'Location': {
#                         'City': person.biography.city,
#                         'Province/State': person.biography.province_state
#                     },
#                     'Click_To_Start_Record_Audio_Introduction': {
#                         'Microphone': person.biography.microphone
#                     }
#                 },
#                 'topic_descriptions': [],
#                 'Testimonials': [],
#                 'Videos': [],
#                 'Podcasts': [],
#                 'MediaMentions': [],
#                 'WhitePapersCaseStudies': [],
#                 'SpeakerContactInformation': {
#                     'id':person.speaker_contact_information.id,
#                     'first_name': person.speaker_contact_information.first_name,
#                     'last_name': person.speaker_contact_information.last_name,
#                     'middle_initials': person.speaker_contact_information.middle_initials,
#                     'secondary_names_nick_name': person.speaker_contact_information.secondary_names_nick_name,
#                     'pronouns': person.speaker_contact_information.pronouns,
#                     'cell_phone': person.speaker_contact_information.cell_phone,
#                     'main_email': person.speaker_contact_information.main_email,
#                     'website_link': person.speaker_contact_information.website_link,
#                     'rss_blog_link': person.speaker_contact_information.rss_blog_link,
#                     'rss_blog_link_2': person.speaker_contact_information.rss_blog_link_2,
#                     'closest_major_airport': person.speaker_contact_information.closest_major_airport
#                 },
#                 'ManagerOrTeammate': {
#                     'id':person.manager_or_teammate.id,
#                     'assist_coordinating': person.manager_or_teammate.assist_coordinating,
#                     'contact_info': {
#                         'first_name': person.manager_or_teammate.first_name,
#                         'last_name': person.manager_or_teammate.last_name,
#                         'pronouns': person.manager_or_teammate.pronouns,
#                         'cell_phone': person.manager_or_teammate.cell_phone,
#                         'main_email': person.manager_or_teammate.main_email,
#                         'website': person.manager_or_teammate.website
#                     }
#                 },
#                 'SocialMediaPersonal': {
#                     'id': person.social_media_personal.id,
#                     'facebook': {
#                         'link': person.social_media_personal.facebook_link,
#                         'handle': person.social_media_personal.facebook_handle,
#                         'followers': person.social_media_personal.facebook_followers
#                     },
#                     'instagram': {
#                         'link': person.social_media_personal.instagram_link,
#                         'handle': person.social_media_personal.instagram_handle,
#                         'followers': person.social_media_personal.instagram_followers
#                     },
#                     'twitter': {
#                         'link': person.social_media_personal.twitter_link,
#                         'handle': person.social_media_personal.twitter_handle,
#                         'followers': person.social_media_personal.twitter_followers
#                     },
#                     'linkedin': {
#                         'link': person.social_media_personal.linkedin_link,
#                         'handle': person.social_media_personal.linkedin_handle,
#                         'followers': person.social_media_personal.linkedin_followers
#                     },
#                     'tiktok': {
#                         'link': person.social_media_personal.tiktok_link,
#                         'handle': person.social_media_personal.tiktok_handle,
#                         'followers': person.social_media_personal.tiktok_followers
#                     }
#                 },
#                 'BusinessInfo': {
#                     'id': person.business_info.id,  
#                     'business_issue_payment': person.business_info.issue_payment,
#                     'business_information': {
#                         'official_business_name': person.business_info.official_business_name,
#                         'business_email': person.business_info.business_email,
#                         'business_phone': person.business_info.business_phone,
#                         'business_number': person.business_info.business_number,
#                         'website': person.business_info.website
#                     }
#                 },
#                 'SocialMediaBusiness': {
#                     'id': person.social_media_business.id,  # Include ID here
#                     'facebook': {
#                         'id': person.social_media_business.id,
#                         'link': person.social_media_business.facebook_link,
#                         'handle': person.social_media_business.facebook_handle,
#                         'followers': person.social_media_business.facebook_followers
#                     },
#                     'instagram': {
#                         'id': person.social_media_business.id,
#                         'link': person.social_media_business.instagram_link,
#                         'handle': person.social_media_business.instagram_handle,
#                         'followers': person.social_media_business.instagram_followers
#                     },
#                     'twitter': {
#                         'id': person.social_media_business.id,
#                         'link': person.social_media_business.twitter_link,
#                         'handle': person.social_media_business.twitter_handle,
#                         'followers': person.social_media_business.twitter_followers
#                     },
#                     'linkedin': {
#                         'id': person.social_media_business.id,
#                         'link': person.social_media_business.linkedin_link,
#                         'handle': person.social_media_business.linkedin_handle,
#                         'followers': person.social_media_business.linkedin_followers
#                     },
#                     'tiktok': {
#                         'id': person.social_media_business.id,
#                         'link': person.social_media_business.tiktok_link,
#                         'handle': person.social_media_business.tiktok_handle,
#                         'followers': person.social_media_business.tiktok_followers
#                     }
#                 },
#                 'BrandCampaigns': [],
                
#                 'AtEvents': {},
#                 'HelpUsBookYou': {},
#                 'HelpUsWorkWithYou': {},
#                 'Fees': {},
#                 'speaker_pitches': [] ,
#                 'PreviousClients': []
#             }

#             for topic_description in person.topic_descriptions:
#                 topic_data = {
#                     'id': topic_description.id,
#                     'Topic_Description_Title': topic_description.title,
#                     'Topic_Description_Body_Text': topic_description.body_text,
#                     'Topic_delivered_as': topic_description.delivered_as,
#                     'Audio_Clip_for_Topic_Description_1': topic_description.audio_clip,
#                     'Video_Clip_for_Topic_Description_1': topic_description.video_clip
#                 }
#                 person_data['topic_descriptions'].append(topic_data)
                
#             # Add Testimonials
#             for testimonial in person.testimonials:
#                 testimonial_data = {
#                     'id': testimonial.id,
#                     'Organizer_Name': testimonial.organizer_name,
#                     'Testimonial_Organization_Name': testimonial.organization_name,
#                     'Link_to_Video': testimonial.link_to_video
#                 }
#                 person_data['Testimonials'].append(testimonial_data)

#             # Add Videos
#             for video in person.video:
#                 video_data = {
#                     'id': video.id, 
#                     'Title': video.title,
#                     'Link': video.link,
#                     'source_if_not': {
#                         'HD_QualityY/N': video.hd_quality,
#                         'Do_you_own_the_rights_to_this_video': video.own_rights,
#                         'Do_you_grant_SBC_permission_and_all_clients_permission_to_use_this_video_for_promoting_you_as_a_speaker': video.grant_permission,
#                         'why not': video.reason
#                     }
#                 }
#                 person_data['Videos'].append(video_data)

#             # Add Podcasts
#             for podcast in person.podcasts:
#                 podcast_data = {
#                     'id': podcast.id,
#                     'title': podcast.title,
#                     'link': podcast.link,
#                     'source': podcast.source
#                 }
#                 person_data['Podcasts'].append(podcast_data)    
                
#             # Add Media Mentions
#             for media_mention in person.media_mentions:
#                 media_mention_data = {
#                     'id': media_mention.id, 
#                     'organization_name': media_mention.organization_name,
#                     'interview_article_title': media_mention.interview_article_title,
#                     'Interview/Article Title': {
#                         'written_interview': media_mention.written_interview,
#                         'audio_interview': media_mention.audio_interview,
#                         'video_interview': media_mention.video_interview,
#                         'film': media_mention.film
#                     },
#                     'link': media_mention.link,
#                     'date': media_mention.date,
#                     'interview_source_name': media_mention.interview_source_name
#                 }
#                 person_data['MediaMentions'].append(media_mention_data)

#             # Add White Papers/Case Studies
#             for white_paper_case_study in person.white_papers_case_studies:
#                 white_paper_data = {
#                     'id': white_paper_case_study.id,
#                     'organization_name': white_paper_case_study.organization_name,
#                     'title': white_paper_case_study.title,
#                     'topics': white_paper_case_study.topics,
#                     'description': white_paper_case_study.description,
#                     'link': white_paper_case_study.link,
#                     'date': white_paper_case_study.date
#                 }
#                 person_data['WhitePapersCaseStudies'].append(white_paper_data)
            
            
#             for brand_campaign in person.brand_campaigns:
#                 brand_campaign_data = {
#                     'id': brand_campaign.id,
#                     'part_of_social_media': brand_campaign.part_of_social_media,
#                     'organization_name': brand_campaign.organization_name,
#                     'platforms': brand_campaign.platforms,
#                     'link_to_campaign': brand_campaign.link_to_campaign,
#                     'start_year': brand_campaign.start_year,
#                     'end_year': brand_campaign.end_year
#                 }
#                 person_data['BrandCampaigns'].append(brand_campaign_data)  
            
#             request_data = request.get_json()
             
            
            
#             # Add At Events
#             if person.at_events:
#                 at_events = {
#                     'id': person.at_events.id,
#                     'using_presentation_software': person.at_events.using_presentation_software,
#                     'presentation_software_name': person.at_events.presentation_software_name,
#                     'using_audience_interaction_software': person.at_events.using_audience_interaction_software,
#                     'audience_interaction_software_name': person.at_events.audience_interaction_software_name,
#                     'attending_sessions_before_after_presentation': person.at_events.attending_sessions_before_after_presentation,
#                     'attending_meals_networking_sessions': person.at_events.attending_meals_networking_sessions,
#                     'dietary_requirements_restrictions': person.at_events.dietary_requirements_restrictions,
#                     'A_V_requirements': person.at_events.A_V_requirements,
#                     'use_travel_agent': person.at_events.use_travel_agent,
#                     'Preferred_Seating': person.at_events.Preferred_Seating,
#                     'Preferred_Airline': person.at_events.Preferred_Airline,
#                     'West_Jet_number': person.at_events.West_Jet_number,
#                     'Air_Canada_number': person.at_events.Air_Canada_number,
#                     'special_conditions_for_travel_arrangements': person.at_events.special_conditions_for_travel_arrangements,
#                     'table_for_book_sales': person.at_events.table_for_book_sales,
#                     'SpeakerIntroduction': []
#                 }

#                 for introduction in person.at_events.speaker_introduction:
#                     introduction_data = {
#                         'id': introduction.id,
#                         'introduction_text': introduction.introduction_text
#                     }
#                     at_events['SpeakerIntroduction'].append(introduction_data)

#                 person_data['AtEvents'] = at_events
            
            

            

#             # Add Help Us Work With You
#             if person.help_us_book_you:
#                 help_us_book_you = {
#                     'id': person.help_us_book_you.id,
#                     'speaker_reason_to_work_with': person.help_us_book_you.speaker_reason_to_work_with,
#                     'value_adds_and_offerings': person.help_us_book_you.value_adds_and_offerings,
#                     'books_how_many_items': person.help_us_book_you.books_how_many_items,
#                     'books_value_per_item': person.help_us_book_you.books_value_per_item,
#                     'online_training_how_many_items': person.help_us_book_you.online_training_how_many_items,
#                     'online_training_value_per_item': person.help_us_book_you.online_training_value_per_item,
#                     'merch_how_many_items': person.help_us_book_you.merch_how_many_items,
#                     'merch_value_per_item': person.help_us_book_you.merch_value_per_item,
#                     'merch_2_how_many_items': person.help_us_book_you.merch_2_how_many_items,
#                     'merch_2_value_per_item': person.help_us_book_you.merch_2_value_per_item,
#                     'complementary_virtual_follow_sessions_consultation': person.help_us_book_you.complementary_virtual_follow_sessions_consultation,
#                     'inclusive_of_travel_expenses': person.help_us_book_you.inclusive_of_travel_expenses,
#                     'industries_do_you_not_work_with': person.help_us_book_you.industries_do_you_not_work_with,
#                     'favorite_audiences_event_types': person.help_us_book_you.favorite_audiences_event_types,
#                     'target_audiences_industries': person.help_us_book_you.target_audiences_industries,
#                     'English_French': person.help_us_book_you.English_French,
#                     'Q_A_in_French': person.help_us_book_you.Q_A_in_French,
#                     'offer_recordings': person.help_us_book_you.offer_recordings,
#                     'primary_source_of_income': person.help_us_book_you.primary_source_of_income,
#                     'hoping_for_speaking_to_become_your_primary_source_income': person.help_us_book_you.hoping_for_speaking_to_become_your_primary_source_income,
#                     'current_speak_per_month': person.help_us_book_you.current_speak_per_month,
#                     'virtual_events_over_pandemic': person.help_us_book_you.virtual_events_over_pandemic,
#                     'speak_per_month': person.help_us_book_you.speak_per_month,
#                     'market_yourself_as_a_speaker': person.help_us_book_you.market_yourself_as_a_speaker,
#                     'affiliated_with_any_other_speakers_agencies': person.help_us_book_you.affiliated_with_any_other_speakers_agencies,
#                     'percentage_of_bookings': person.help_us_book_you.percentage_of_bookings,
#                     'Approximately_what_percentage': person.help_us_book_you.Approximately_what_percentage,
#                     'speakers_are_you_affiliated_with': person.help_us_book_you.speakers_are_you_affiliated_with
#                 }
#                 person_data['HelpUsBookYou'] = help_us_book_you   
                
                
                
#             if person.help_us_work_with_you:
#                 help_us_work_with_you = {
#                     'id': person.help_us_work_with_you.id,
#                     'newsletter_onboarding': person.help_us_work_with_you.newsletter_onboarding,
#                     'tracking_system': person.help_us_work_with_you.tracking_system,
#                     'whatsapp': person.help_us_work_with_you.whatsapp,
#                     'business_ownership': person.help_us_work_with_you.business_ownership,
#                     'crm_usage': person.help_us_work_with_you.crm_usage,
#                     'appointment_booking_software': person.help_us_work_with_you.appointment_booking_software,
#                     'expectations_with_sbc': person.help_us_work_with_you.expectations_with_sbc,
#                     'something_about_you': person.help_us_work_with_you.something_about_you,
#                     'stories': person.help_us_work_with_you.stories,
#                 }
#                 person_data['HelpUsWorkWithYou'] = help_us_work_with_you    
   
            
            
            
#             if person.speaker_pitches:
#                 # Iterate through speaker pitches and add them to the response
#                 for speaker_pitch in person.speaker_pitches:
#                     speaker_pitch_data = {
#                         'id': speaker_pitch.id,
#                         'general_pitch': speaker_pitch.general_pitch,
#                         'keyword_topic_focus_pitch': speaker_pitch.keyword_topic_focus_pitch,
#                         'Short_pitch_up': speaker_pitch.Short_pitch_up
#                     }
#                     person_data['speaker_pitches'].append(speaker_pitch_data)
                    
                    
#             # Add Previous Clients if data is available
#             if person.previous_clients:
#                 previous_clients = []
#                 for client in person.previous_clients:
#                     previous_clients_data = {
#                         'id': client.id,
#                         'organization_name': client.organization_name
#                     }
#                     previous_clients.append(previous_clients_data)
#                 person_data['PreviousClients'] = previous_clients
        
                
                
#             # Degrees data
#             if person.degree_files:
#                 degrees_data = []
#                 for degree in person.degree_files:
#                     degree_info = {
#                         'id': degree.id,  # Include ID here
#                         'degree_data': base64.b64encode(degree.degree_data).decode('utf-8'),
#                     }
#                     degrees_data.append(degree_info)
#                 person_data['Degrees'] = degrees_data

#             # Certificates data
#             if person.certificate_files:
#                 certificates_data = []
#                 for certificate in person.certificate_files:
#                     certificate_info = {
#                         'id': certificate.id,  # Include ID here
#                         'certifications_data': base64.b64encode(certificate.certifications_data).decode('utf-8'),
#                     }
#                     certificates_data.append(certificate_info)
#                 person_data['Certificates'] = certificates_data

#             # Awards data
#             if person.awards_files:
#                 awards_data = []
#                 for award in person.awards_files:
#                     award_info = {
#                         'id': award.id,  # Include ID here
#                         'awards_data': base64.b64encode(award.awards_data).decode('utf-8'),
#                     }
#                     awards_data.append(award_info)
#                 person_data['Awards'] = awards_data

#             # Images data
#             if person.images:
#                 images_data = []
#                 for image in person.images:
#                     image_info = {
#                         'id': image.id,  # Include ID here
#                         'image_data': base64.b64encode(image.image_data).decode('utf-8'),
#                         'own_right': image.own_right,
#                         'sbc_permission': image.sbc_permission,
#                     }
#                     images_data.append(image_info)
#                 person_data['Images'] = images_data

#             # Books data
#             if person.books:
#                 books_data = []
#                 for book in person.books:
#                     book_info = {
#                         'id': book.id,  # Include ID here
#                         'upload_book_image': base64.b64encode(book.upload_book_image).decode('utf-8'),
#                         'title': book.title,
#                         'description': book.description,
#                         'authors': book.authors,
#                         'publisher': book.publisher,
#                         'link': book.link,
#                         'cost_per_book_cad': book.cost_per_book_cad,
#                         'bulk_order_purchase_offered': book.bulk_order_purchase_offered,
#                         'price_per_book_cad': book.price_per_book_cad,
#                         'number_of_books': book.number_of_books,
#                     }
#                     books_data.append(book_info)
#                 person_data['Books'] = books_data
            
        

#         return jsonify(person_data), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400    


# @app.route('/person/<int:person_id>', methods=['PUT'])
# def update_person(person_id):
#     try:
#         data = request.get_json()

#         # Get the existing person record by ID
#         person = Person.query.get(person_id)

#         if person is None:
#             return jsonify(message='Person not found'), 404

#         # Update the 'person' data
#         person_data = data.get('person')
#         person.name = person_data['name']

#         db.session.commit()

#         return jsonify(message='Person updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400    
    

@app.route('/person/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    try:
        data = request.get_json()

        # Get the existing person record by ID
        person = Person.query.get(person_id)

        if person is None:
            return jsonify(message='Person not found'), 404

        # Update the 'person' data
        person_data = data.get('person')

        # Add the properties you want to update (in this case, 'email' and 'username')
        person.email = person_data.get('email')
        person.username = person_data.get('username')
        person.password = person_data.get('password')

        db.session.commit()

        return jsonify(message='Person updated successfully'), 200
    except Exception as e:
        return jsonify(error=str(e)), 400    
    
    
# @app.route('/user/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     try:
#         data = request.get_json()
#         user_data = data.get('user')

#         # Find the existing user by ID
#         existing_user = User.query.get(user_id)
#         if existing_user is None:
#             return jsonify(error=f'User not found with the specified user_id'), 404

#         # Update the user fields
#         if 'email' in user_data:
#             existing_user.email = user_data['email']
#         if 'username' in user_data:
#             existing_user.username = user_data['username']
#         if 'password' in user_data:
#             existing_user.password = bcrypt.hash(user_data['password'])

#         db.session.commit()

#         return jsonify(message='User updated successfully'), 200

#     except Exception as e:
#         return jsonify(error=str(e)), 400
    

# @app.route('/stage1/<int:person_id>', methods=['PUT'])
# def update_speaker_contact_info(person_id):
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404

#         # Update the 'speaker_contact_information' data
#         speaker_contact_info_data = data.get('speaker_contact_information')
#         if speaker_contact_info_data:
#             speaker_contact_info = person.speaker_contact_information
#             if not speaker_contact_info:
#                 speaker_contact_info = SpeakerContactInformation()
#                 person.speaker_contact_information = speaker_contact_info

#             speaker_contact_info.first_name = speaker_contact_info_data.get('first_name', speaker_contact_info.first_name)
#             speaker_contact_info.last_name = speaker_contact_info_data.get('last_name', speaker_contact_info.last_name)
#             speaker_contact_info.middle_initials = speaker_contact_info_data.get('middle_initials', speaker_contact_info.middle_initials)
#             speaker_contact_info.secondary_names_nick_name = speaker_contact_info_data.get('secondary_names_nick_name', speaker_contact_info.secondary_names_nick_name)
#             speaker_contact_info.pronouns = speaker_contact_info_data.get('pronouns', speaker_contact_info.pronouns)
#             speaker_contact_info.cell_phone = speaker_contact_info_data.get('cell_phone', speaker_contact_info.cell_phone)
#             speaker_contact_info.main_email = speaker_contact_info_data.get('main_email', speaker_contact_info.main_email)
#             speaker_contact_info.website_link = speaker_contact_info_data.get('website_link', speaker_contact_info.website_link)
#             speaker_contact_info.rss_blog_link = speaker_contact_info_data.get('rss_blog_link', speaker_contact_info.rss_blog_link)
#             speaker_contact_info.rss_blog_link_2 = speaker_contact_info_data.get('rss_blog_link_2', speaker_contact_info.rss_blog_link_2)
#             speaker_contact_info.closest_major_airport = speaker_contact_info_data.get('closest_major_airport', speaker_contact_info.closest_major_airport)

#         # Update the 'manager_or_teammate' data
#         manager_teammate_data = data.get('manager_or_teammate')
#         if manager_teammate_data:
#             manager_or_teammate = person.manager_or_teammate
#             if not manager_or_teammate:
#                 manager_or_teammate = ManagerOrTeammate()
#                 person.manager_or_teammate = manager_or_teammate

#             manager_or_teammate.assist_coordinating = manager_teammate_data.get('assist_coordinating', manager_or_teammate.assist_coordinating)
#             contact_info = manager_teammate_data.get('contact_info')
#             if contact_info:
#                 manager_or_teammate.first_name = contact_info.get('first_name', manager_or_teammate.first_name)
#                 manager_or_teammate.last_name = contact_info.get('last_name', manager_or_teammate.last_name)
#                 manager_or_teammate.pronouns = contact_info.get('pronouns', manager_or_teammate.pronouns)
#                 manager_or_teammate.cell_phone = contact_info.get('cell_phone', manager_or_teammate.cell_phone)
#                 manager_or_teammate.main_email = contact_info.get('main_email', manager_or_teammate.main_email)
#                 manager_or_teammate.website = contact_info.get('website', manager_or_teammate.website)

#         # Update the 'social_media_personal' data
#         social_media_personal_data = data.get('social_media_personal')
#         if social_media_personal_data:
#             social_media_personal = person.social_media_personal
#             if not social_media_personal:
#                 social_media_personal = SocialMediaPersonal()
#                 person.social_media_personal = social_media_personal

#             social_media_personal.facebook_link = social_media_personal_data['facebook']['link']
#             social_media_personal.facebook_handle = social_media_personal_data['facebook']['handle']
#             social_media_personal.facebook_followers = social_media_personal_data['facebook']['followers']
#             social_media_personal.instagram_link = social_media_personal_data['instagram']['link']
#             social_media_personal.instagram_handle = social_media_personal_data['instagram']['handle']
#             social_media_personal.instagram_followers = social_media_personal_data['instagram']['followers']
#             social_media_personal.twitter_link = social_media_personal_data['twitter']['link']
#             social_media_personal.twitter_handle = social_media_personal_data['twitter']['handle']
#             social_media_personal.twitter_followers = social_media_personal_data['twitter']['followers']
#             social_media_personal.linkedin_link = social_media_personal_data['linkedin']['link']
#             social_media_personal.linkedin_handle = social_media_personal_data['linkedin']['handle']
#             social_media_personal.linkedin_followers = social_media_personal_data['linkedin']['followers']
#             social_media_personal.tiktok_link = social_media_personal_data['tiktok']['link']
#             social_media_personal.tiktok_handle = social_media_personal_data['tiktok']['handle']
#             social_media_personal.tiktok_followers = social_media_personal_data['tiktok']['followers']

#         db.session.commit()

#         return jsonify(message='Speaker contact information updated successfully'), 200

#     except Exception as e:
#         return jsonify(error=str(e)), 400


@app.route('/update_speaker_information', methods=['PUT'])
def update_speaker_information():
    try:
        data = request.get_json()

        speaker_contact_info_data = data.get('speaker_contact_information')
        manager_or_teammate_data = data.get('manager_or_teammate')
        social_media_data = data.get('social_media_personal')

        if speaker_contact_info_data:
            speaker_contact_info_id = speaker_contact_info_data.get('id')
            speaker_contact_info = SpeakerContactInformation.query.get(speaker_contact_info_id)

            if speaker_contact_info:
                speaker_contact_info.cell_phone = speaker_contact_info_data.get('cell_phone', speaker_contact_info.cell_phone)
                speaker_contact_info.closest_major_airport = speaker_contact_info_data.get('closest_major_airport', speaker_contact_info.closest_major_airport)
                speaker_contact_info.first_name = speaker_contact_info_data.get('first_name', speaker_contact_info.first_name)
                speaker_contact_info.last_name = speaker_contact_info_data.get('last_name', speaker_contact_info.last_name)
                speaker_contact_info.main_email = speaker_contact_info_data.get('main_email', speaker_contact_info.main_email)
                speaker_contact_info.middle_initials = speaker_contact_info_data.get('middle_initials', speaker_contact_info.middle_initials)
                speaker_contact_info.pronouns = speaker_contact_info_data.get('pronouns', speaker_contact_info.pronouns)
                speaker_contact_info.rss_blog_link = speaker_contact_info_data.get('rss_blog_link', speaker_contact_info.rss_blog_link)
                speaker_contact_info.rss_blog_link_2 = speaker_contact_info_data.get('rss_blog_link_2', speaker_contact_info.rss_blog_link_2)
                speaker_contact_info.secondary_names_nick_name = speaker_contact_info_data.get('secondary_names_nick_name', speaker_contact_info.secondary_names_nick_name)
                speaker_contact_info.website_link = speaker_contact_info_data.get('website_link', speaker_contact_info.website_link)

        if manager_or_teammate_data:
            manager_teammate_id = manager_or_teammate_data.get('id')
            manager_teammate = ManagerOrTeammate.query.get(manager_teammate_id)

            if manager_teammate:
                manager_teammate.assist_coordinating = manager_or_teammate_data.get('assist_coordinating', manager_teammate.assist_coordinating)
                contact_info = manager_or_teammate_data.get('contact_info', {})
                manager_teammate.first_name = contact_info.get('first_name', manager_teammate.first_name)
                manager_teammate.last_name = contact_info.get('last_name', manager_teammate.last_name)
                manager_teammate.pronouns = contact_info.get('pronouns', manager_teammate.pronouns)
                manager_teammate.cell_phone = contact_info.get('cell_phone', manager_teammate.cell_phone)
                manager_teammate.main_email = contact_info.get('main_email', manager_teammate.main_email)
                manager_teammate.website = contact_info.get('website', manager_teammate.website)

        if social_media_data:
            social_media_id = social_media_data.get('id')
            social_media_personal = SocialMediaPersonal.query.get(social_media_id)

            if social_media_personal:
                facebook_data = social_media_data.get('facebook', {})
                social_media_personal.facebook_link = facebook_data.get('link', social_media_personal.facebook_link)
                social_media_personal.facebook_handle = facebook_data.get('handle', social_media_personal.facebook_handle)
                social_media_personal.facebook_followers = facebook_data.get('followers', social_media_personal.facebook_followers)
                
                # Add similar updates for Instagram
                instagram_data = social_media_data.get('instagram', {})
                social_media_personal.instagram_link = instagram_data.get('link', social_media_personal.instagram_link)
                social_media_personal.instagram_handle = instagram_data.get('handle', social_media_personal.instagram_handle)
                social_media_personal.instagram_followers = instagram_data.get('followers', social_media_personal.instagram_followers)
                
                # Add similar updates for Twitter
                twitter_data = social_media_data.get('twitter', {})
                social_media_personal.twitter_link = twitter_data.get('link', social_media_personal.twitter_link)
                social_media_personal.twitter_handle = twitter_data.get('handle', social_media_personal.twitter_handle)
                social_media_personal.twitter_followers = twitter_data.get('followers', social_media_personal.twitter_followers)
                
                # Add similar updates for LinkedIn
                linkedin_data = social_media_data.get('linkedin', {})
                social_media_personal.linkedin_link = linkedin_data.get('link', social_media_personal.linkedin_link)
                social_media_personal.linkedin_handle = linkedin_data.get('handle', social_media_personal.linkedin_handle)
                social_media_personal.linkedin_followers = linkedin_data.get('followers', social_media_personal.linkedin_followers)
                
                # Add similar updates for TikTok
                tiktok_data = social_media_data.get('tiktok', {})
                social_media_personal.tiktok_link = tiktok_data.get('link', social_media_personal.tiktok_link)
                social_media_personal.tiktok_handle = tiktok_data.get('handle', social_media_personal.tiktok_handle)
                social_media_personal.tiktok_followers = tiktok_data.get('followers', social_media_personal.tiktok_followers)

        db.session.commit()

        return jsonify(message='Speaker information updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400
    
            
    
# @app.route('/stage2/biography/<int:biography_id>', methods=['PUT'])
# def update_biography(biography_id):
#     try:
#         # Get the form data from the request
#         microphonetext = request.form.get('Microphonetext')
#         highlight = request.form.get('Highlight')
#         sort_bio = request.form.get('Sort_Bio')
#         long_bio = request.form.get('Long_Bio')
#         speaker_topics = request.form.get('Speaker_Topics')
#         keywords = request.form.get('Speaker_Topics_additional_keywords_separated_by_commas')
#         speaker_tags = request.form.get('Speaker_Tags')
#         descriptive_title_type = request.form.get('Descriptive_Title_Type')
#         descriptive_title_1 = request.form.get('Descriptive_Title_1')
#         descriptive_title_2 = request.form.get('Descriptive_Title_2')
#         descriptive_title_3 = request.form.get('Descriptive_Title_3')
#         city = request.form.get('City')
#         province_state = request.form.get('Province/State')

#         # Get the associated biography
#         biography = Biography.query.get(biography_id)
#         if biography is None:
#             return jsonify(error='Biography not found with the specified biography_id'), 404

#         # Update biography fields
#         biography.microphonetext = microphonetext
#         biography.highlight = highlight
#         biography.sort_bio = sort_bio
#         biography.long_bio = long_bio
#         biography.speaker_topics = speaker_topics
#         biography.speaker_topics_additional_keywords = keywords
#         biography.speaker_tags = speaker_tags
#         biography.descriptive_title_type = descriptive_title_type
#         biography.descriptive_title_1 = descriptive_title_1
#         biography.descriptive_title_2 = descriptive_title_2
#         biography.descriptive_title_3 = descriptive_title_3
#         biography.city = city
#         biography.province_state = province_state

#         # Handle the microphone file if provided in the update
#         microphone_file = request.files.get('Microphone')
#         if microphone_file:
#             microphone_data = microphone_file.read()
#             biography.microphone = microphone_data

#         db.session.commit()

#         return jsonify(message='Biography updated successfully'), 200

#     except Exception as e:
#         return jsonify(error=str(e)), 400


@app.route('/update_biography', methods=['PUT'])
def update_biography():
    try:
                # Get the form data from the request
        biography_id = request.form.get('id')
        if biography_id is None:
            return jsonify({'error': 'Biography ID is missing in the request'}), 400

        biography_id = int(biography_id)   # Include the biography_id in the form data
        microphonetext = request.form.get('Microphonetext')
        highlight = request.form.get('Highlight')
        sort_bio = request.form.get('Sort_Bio')
        long_bio = request.form.get('Long_Bio')
        speaker_topics_additional_keywords = request.form.get('Additional_keywords')
        descriptive_title_type = request.form.get('Descriptive_title_type')
        city = request.form.get('City')
        province_state = request.form.get('Province_State')

        # Get the associated biography
        biography = Biography.query.get(biography_id)
        if biography is None:
            return jsonify(error='Biography not found with the specified biography_id'), 404

        # Update biography fields
        biography.microphonetext = microphonetext
        biography.highlight = highlight
        biography.sort_bio = sort_bio
        biography.long_bio = long_bio
        biography.speaker_topics_additional_keywords = speaker_topics_additional_keywords
        biography.descriptive_title_type = descriptive_title_type
        biography.city = city
        biography.province_state = province_state

        # Handle the microphone file if provided in the update
        microphone_files = request.files.getlist('Microphone')
        for microphone_file in microphone_files:
            if microphone_file:
                microphone_data = microphone_file.read()
                biography.microphone = microphone_data

        # Update speaker topics
        student_topic_ids = request.form.getlist('studenttopic_id')
        print('student_topic_ids---------->',student_topic_ids)
        speaker_topics = request.form.getlist('speaker_topicss')
        print('speaker_topics----------->',speaker_topics)
        for topic_id, topic in zip(student_topic_ids, speaker_topics):
            topic = topic.strip().replace(" ", "_").replace("&", "_").replace("-", "_").replace(";", "").replace("'", "").replace("#", "").replace("+", "").replace("(", "").replace(")", "").replace("$", "").replace(",", "")
            topic_id = int(topic_id)
            if topic in SpeakerTopicEnum.__members__:
                existing_topic = SpeakerTopic.query.get(topic_id)
                if existing_topic:
                    existing_topic.topic = topic
                else:
                    return f"Invalid speaker topic id provided: {topic_id}", 400
            else:
                return f"Invalid speaker topics provided: {topic}", 400
        
        # Update speaker tags
        student_tag_ids = request.form.getlist('studenttag_id')
        print('student_tag_ids---------->',student_tag_ids)
        speaker_tags = request.form.getlist('speaker_tagss')
        print('speaker_tags---------->',speaker_tags)
        for tag_id, tag in zip(student_tag_ids, speaker_tags):
            tag = tag.strip()
            tag_id = int(tag_id)
            if tag in SpeakerTagEnum.__members__:
                existing_tag = SpeakerTag.query.get(tag_id)
                if existing_tag:
                    existing_tag.tag = tag
                else:
                    return f"Invalid speaker tag id provided: {tag_id}", 400
            else:
                return f"Invalid speaker tags provided: {tag}", 400

        # Update speaker tags
        student_tag_ids = request.form.getlist('descriptivetitlee_id')
        speaker_tags = request.form.getlist('descriptive_titlee')
        for tag_id, tag in zip(student_tag_ids, speaker_tags):
            tag = tag.strip().replace(" ", "_").replace("&", "_").replace("-", "_").replace(";", "").replace("'", "").replace("#", "").replace("+", "").replace("(", "").replace(")", "").replace("$", "").replace(",", "")
            tag_id = int(tag_id)
            if tag in DescriptiveTitlesEnum.__members__:
                existing_tag = DescriptiveTitles.query.get(tag_id)
                if existing_tag:
                    existing_tag.title = tag
                else:
                    return f"Invalid descriptive title id provided: {tag_id}", 400
            else:
                return f"Invalid descriptive titles provided: {tag}", 400

        db.session.commit()

        return jsonify(message='Biography updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400
    


    
# @app.route('/stage3/topicdescription/<int:topicdescription_id>', methods=['PUT'])
# def update_topicdescription(topicdescription_id):
#     try:
#         # Get the form data from the request
#         audiotext = request.form.get('Audio_text')
#         title = request.form.get('Topic_Description_Title')
#         body_text = request.form.get('Topic_Description_Body_Text')
#         topic_delivered = request.form.get('Topic_delivered_as')
#         video_link = request.form.get('Video_Clip_for_Topic_Description_1')

#         # Get the associated topicdescription
#         topicdescription = TopicDescription.query.get(topicdescription_id)
#         if topicdescription is None:
#             return jsonify(error='TopicDescription not found with the specified topicdescription_id'), 404

#         # Update topicdescription fields
#         topicdescription.audiotext = audiotext
#         topicdescription.title = title
#         topicdescription.body_text = body_text
#         topicdescription.delivered_as = topic_delivered
#         topicdescription.video_clip = video_link

#         # Handle the audio file if provided in the update
#         audio_clip_file = request.files.get('Audio_Clip_for_Topic_Description_1')
#         if audio_clip_file:
#             audio_clip_data = audio_clip_file.read()
#             topicdescription.audio_clip = audio_clip_data

#         db.session.commit()

#         return jsonify(message='TopicDescription updated successfully'), 200

#     except Exception as e:
#         return jsonify(error=str(e)), 400    


@app.route('/update_topicdescription', methods=['PUT'])
def update_topicdescription():
    try:
        # Extract data from the request
        topic_description_id = request.form.get('id')
        print('topic_description_id--------->',topic_description_id)
        if topic_description_id is None:
            return jsonify({'error': 'TopicDescription ID is missing in the request'}), 400

        topic_description_id = int(topic_description_id)  # Convert to int
        audiotext = request.form.get('Audio_text')
        title = request.form.get('Topic_Description_Title')
        body_text = request.form.get('Topic_Description_Body_Text')
        delivered_as = request.form.get('Topic_delivered_as')
        video_link = request.form.get('Video_Clip_for_Topic_Description_1')
        print('video_link--------->',video_link)

        # Retrieve the existing TopicDescription object by ID
        topic_description = TopicDescription.query.get(topic_description_id)
        print('topic_description---------->',topic_description)
        if topic_description is None:
            return jsonify({'error': 'TopicDescription not found'}), 404

        # Update the TopicDescription attributes
        topic_description.audiotext = audiotext
        topic_description.title = title
        topic_description.body_text = body_text
        topic_description.delivered_as = delivered_as
        topic_description.video_clip = video_link
        

        # Handle audio file(s) if provided
        audio_file = request.files.get('Audio_Clip_for_Topic_Description_1')
        if audio_file:
            file_data = audio_file.read()
            topic_description.audio_clip = file_data

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Topic description updated successfully'}), 200
    except Exception as e:
        return jsonify(error=str(e)), 400  

    
# @app.route('/stage4/images/<int:image_id>', methods=['PUT'])
# def update_image(image_id):
#     try:
#         # Get the form data from the request
#         own_rights = request.form.get('images_data1')
#         sbc_permissions = request.form.get('images_data2')
        
#         # Get the associated image
#         image = Images.query.get(image_id)
#         if image is None:
#             return jsonify(error='Image not found with the specified image_id'), 404

#         # Update image fields
#         image.own_right = own_rights == 'true'
#         image.sbc_permission = sbc_permissions == 'true'

#         # Handle the image file if provided in the update
#         image_file = request.files.get('images_file')
#         if image_file:
#             image_data = image_file.read()
#             image.image_data = image_data
            
#         croped_images = request.files.get('crop_image')    

#         db.session.commit()

#         return jsonify(message='Image updated successfully'), 200

#     except Exception as e:
#         return jsonify(error=str(e)), 400    


@app.route('/update_images', methods=['PUT'])
def update_images():
    try:
        # Extract data from the request
        image_id = request.form.get('id')
        if image_id is None:
            return jsonify({'error': 'Images ID is missing in the request'}), 400

        image_id = int(image_id)  # Convert to int
        own_rights = request.form.get('own_rights')
        sbc_permissions = request.form.get('sbc_permissions')

        # Retrieve the existing Images object by ID
        images = Images.query.get(image_id)
        if images is None:
            return jsonify({'error': 'Images not found'}), 404

        # Update the Images attributes
        images.own_right = own_rights == 'true'
        images.sbc_permission = sbc_permissions == 'true'

        # Handle binary image data if provided
        image_files = request.files.getlist('image_data')
        cropped_image_files = request.files.getlist('cropped_image_data')

        # Clear existing images
        images.image_data = []
        images.cropped_image_data = []

        for image_file, cropped_image_file in zip(image_files, cropped_image_files):
            if image_file:
                images.image_data.append(image_file.read())
            if cropped_image_file:
                images.cropped_image_data.append(cropped_image_file.read())


        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Images updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
# @app.route('/stage5/<int:person_id>', methods=['PUT'])
# def update_videos(person_id):
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404      
#         # Update the 'Video' data
#         video_data = data.get('Video')

#         for video_item in video_data:
#             for video_key, video_info in video_item.items():
#                 # Find the existing video by ID
#                 video_id = video_info.get('id')
#                 if video_id:
#                     existing_video = Video.query.get(video_id)
#                     if existing_video:
#                         existing_video.title = video_info['Title']
#                         existing_video.link = video_info['Link']
#                         source_if_not = video_info.get('source_if_not', {})
#                         existing_video.hd_quality = source_if_not.get('HD_QualityY/N', False)
#                         existing_video.own_rights = source_if_not.get('Do_you_own_the_rights_to_this_video', True)
#                         existing_video.sbc_permission = source_if_not.get('Do_you_grant_SBC_permission_and_all_clients_permission_to_use_this_video_for_promoting_you_as_a_speaker', True)
#                         existing_video.why_not = video_info.get('why not')       

#         db.session.commit()

#         return jsonify(message='videos updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400    
    
@app.route('/update_videos', methods=['PUT'])
def update_videos():
    try:
        data = request.get_json()

        videos_data = data.get('videos')

        for video_data in videos_data:
            video_id = video_data.get('id')
            video = Video.query.get(video_id)

            if video:
                video.title = video_data.get('title', video.title)
                video.link = video_data.get('link', video.link)

                source_info = video_data.get('source_if_not', {})
                video.hd_quality = source_info.get('HD_Quality', video.hd_quality)
                video.own_rights = source_info.get('Do_you_own_the_rights_to_this_video', video.own_rights)
                video.grant_permission = source_info.get('Do_you_grant_SBC_permission_and_all_clients_permission_to_use_this_video_for_promoting_you_as_a_speaker', video.grant_permission)
                video.reason = video_data.get('why not', video.reason)

        db.session.commit()

        return jsonify(message='Videos updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400
    
    
# @app.route('/stage6/<int:person_id>', methods=['PUT'])
# def update_podcasts(person_id):
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404          
#         # Update the 'podcasts' data
#         podcasts_data = data.get('podcasts')

#         for podcast_item in podcasts_data:
#             for podcast_key, podcast_info in podcast_item.items():
#                 # Find the existing podcast by ID
#                 podcast_id = podcast_info.get('id')
#                 if podcast_id:
#                     existing_podcast = Podcast.query.get(podcast_id)
#                     if existing_podcast:
#                         existing_podcast.title = podcast_info['title']
#                         existing_podcast.link = podcast_info['link']
#                         existing_podcast.source = podcast_info['source']

#         db.session.commit()

#         return jsonify(message='podcasts updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400       


@app.route('/update_podcasts', methods=['PUT'])
def update_podcasts():
    try:
        data = request.get_json()

        podcasts_data = data.get('podcasts')

        for podcast_data in podcasts_data:
            podcast_id = podcast_data.get('id')
            podcast = Podcast.query.get(podcast_id)

            if podcast:
                podcast.title = podcast_data.get('title', podcast.title)
                podcast.link = podcast_data.get('link', podcast.link)
                podcast.source = podcast_data.get('source', podcast.source)

        db.session.commit()

        return jsonify(message='Podcasts updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400

    
    
# @app.route('/stage7/books/<int:book_id>', methods=['PUT'])
# def update_book(book_id):
#     try:
#         # Get the form data from the request
#         book_title = request.form.get('book_title')
#         book_description = request.form.get('book_description')
#         book_authors = request.form.get('book_authors')
#         book_publisher = request.form.get('book_publisher')
#         book_link = request.form.get('book_link')
#         book_cost = request.form.get('book_cost')
#         book_bulk_order = request.form.get('book_bulkorder')
#         book_price = request.form.get('book_price')
#         book_number = request.form.get('book_number')
        
#         # Get the associated book
#         book = Book.query.get(book_id)
#         if book is None:
#             return jsonify(error='Book not found with the specified book_id'), 404

#         # Update book fields
#         book.title = book_title
#         book.description = book_description
#         book.authors = book_authors
#         book.publisher = book_publisher
#         book.link = book_link
#         book.cost_per_book_cad = book_cost
#         book.bulk_order_purchase_offered = book_bulk_order == 'true'
#         book.price_per_book_cad = book_price
#         book.number_of_books = book_number

#         # Handle the book file if provided in the update
#         book_file = request.files.get('book_file')
#         if book_file:
#             book_image_data = book_file.read()
#             book.upload_book_image = book_image_data

#         db.session.commit()

#         return jsonify(message='Book updated successfully'), 200

#     except Exception as e:
#         return jsonify(error=str(e)), 400    


@app.route('/update_book', methods=['PUT'])
def update_book():
    try:
        # Get the form data from the request
        book_id = int(request.form.get('id'))  # Include the book_id in the form data
        book_title = request.form.get('book_title')
        book_description = request.form.get('book_description')
        book_authors = request.form.get('book_authors')
        book_publisher = request.form.get('book_publisher')
        book_link = request.form.get('book_link')
        book_cost = request.form.get('book_cost')
        book_bulk_order = request.form.get('book_bulkorder')
        book_price = request.form.get('book_price')
        book_number = request.form.get('book_number')

        # Get the associated book
        book = Book.query.get(book_id)
        if book is None:
            return jsonify(error='Book not found with the specified book_id'), 404

        # Update book fields
        book.title = book_title
        book.description = book_description
        book.authors = book_authors
        book.publisher = book_publisher
        book.link = book_link
        book.cost_per_book_cad = book_cost
        book.bulk_order_purchase_offered = book_bulk_order == 'true'
        book.price_per_book_cad = book_price
        book.number_of_books = book_number

        # Handle the book file if provided in the update
        book_file = request.files.get('book_file')
        if book_file:
            book_image_data = book_file.read()
            book.upload_book_image = book_image_data

        db.session.commit()

        return jsonify(message='Book updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400

    
    
# @app.route('/stage8/<int:person_id>', methods=['PUT'])
# def update_media_mentions(person_id):
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404   
#         # Update the 'media_mentions' data
#         media_mentions_data = data.get('media_mentions')

#         for media_mention_item in media_mentions_data:
#             for media_mention_key, media_mention_info in media_mention_item.items():
#                 # Find the existing media mention by ID
#                 media_mention_id = media_mention_info.get('id')
#                 if media_mention_id:
#                     existing_media_mention = MediaMention.query.get(media_mention_id)
#                     if existing_media_mention:
#                         existing_media_mention.organization_name = media_mention_info['organization_name']
#                         existing_media_mention.interview_article_title = media_mention_info['interview_article_title']
#                         interview_title_info = media_mention_info.get('Interview/Article Title', {})
#                         existing_media_mention.written_interview = interview_title_info.get('written_interview', False)
#                         existing_media_mention.audio_interview = interview_title_info.get('audio_interview', False)
#                         existing_media_mention.video_interview = interview_title_info.get('video_interview', False)
#                         existing_media_mention.film = interview_title_info.get('film', False)
#                         existing_media_mention.link = media_mention_info['link']
#                         existing_media_mention.date = media_mention_info['date']
#                         existing_media_mention.interview_source_name = media_mention_info['interview_source_name']       
#         db.session.commit()

#         return jsonify(message='media_mentions updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400    


@app.route('/update_media_mentions', methods=['PUT'])
def update_media_mentions():
    try:
        data = request.get_json()

        media_mentions_data = data.get('media_mentions')

        for media_mention_data in media_mentions_data:
            media_mention_id = media_mention_data.get('id')
            media_mention = MediaMention.query.get(media_mention_id)

            if media_mention:
                # Convert the list to a string using a separator (e.g., ', ')
                interview_article_title = ', '.join(media_mention_data.get('interview_article_title', []))
                media_mention.date = media_mention_data.get('date', media_mention.date)
                media_mention.interview_article_title = interview_article_title
                media_mention.interview_source_name = media_mention_data.get('interview_source_name', media_mention.interview_source_name)
                media_mention.link = media_mention_data.get('link', media_mention.link)
                media_mention.organization_name = media_mention_data.get('organization_name', media_mention.organization_name)

        db.session.commit()

        return jsonify(message='Media mentions updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400
    
    
    
# @app.route('/stage9/<int:person_id>', methods=['PUT'])
# def update_white_papers_case_studies(person_id):
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404       
        
#         # Update the 'white_papers_case_studies' data
#         white_papers_case_studies_data = data.get('white_papers_case_studies')

#         for case_study_item in white_papers_case_studies_data:
#             for case_study_key, case_study_info in case_study_item.items():
#                 # Find the existing white paper / case study by ID
#                 case_study_id = case_study_info.get('id')
#                 if case_study_id:
#                     existing_case_study = WhitePaperCaseStudy.query.get(case_study_id)
#                     if existing_case_study:
#                         existing_case_study.organization_name = case_study_info['organization_name']
#                         existing_case_study.title = case_study_info['title']
#                         existing_case_study.topics = case_study_info['topics']
#                         existing_case_study.description = case_study_info['description']
#                         existing_case_study.link = case_study_info['link']
#                         existing_case_study.date = case_study_info['date'] 
#         db.session.commit()

#         return jsonify(message='white_papers_case_studies updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400 


@app.route('/update_white_papers_case_studies', methods=['PUT'])
def update_white_papers_case_studies():
    try:
        data = request.get_json()

        white_papers_case_studies_data = data.get('white_papers_case_studies')

        for item_data in white_papers_case_studies_data:
            white_paper_case_study_id = item_data.get('id')
            white_paper_case_study = WhitePaperCaseStudy.query.get(white_paper_case_study_id)

            if white_paper_case_study:
                white_paper_case_study.date = item_data.get('date', white_paper_case_study.date)
                white_paper_case_study.description = item_data.get('description', white_paper_case_study.description)
                white_paper_case_study.link = item_data.get('link', white_paper_case_study.link)
                white_paper_case_study.organization_name = item_data.get('organization_name', white_paper_case_study.organization_name)
                white_paper_case_study.title = item_data.get('title', white_paper_case_study.title)
                white_paper_case_study.topics = item_data.get('topics', white_paper_case_study.topics)

        db.session.commit()

        return jsonify(message='White papers and case studies updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400

# @app.route('/stage10/degrees/<int:degree_id>', methods=['PUT'])
# def update_degree(degree_id):
#     try:
#         # Get the form data from the request
#         degrees_file = request.files.get('degrees')
        
#         # Get the associated degree
#         degree = Degrees.query.get(degree_id)
#         if degree is None:
#             return jsonify(error='Degree not found with the specified degree_id'), 404

#         # Handle the degree file if provided in the update
#         if degrees_file:
#             degree_data = degrees_file.read()
#             degree.degree_data = degree_data

#         db.session.commit()

#         return jsonify(message='Degree updated successfully'), 200

#     except Exception as e:
#         return jsonify(error=str(e)), 400

# @app.route('/stage10/certifications/<int:certification_id>', methods=['PUT'])
# def update_certification(certification_id):
#     try:
#         # Get the form data from the request
#         certifications_file = request.files.get('certifications')
        
#         # Get the associated certification
#         certification = Certificates.query.get(certification_id)
#         if certification is None:
#             return jsonify(error='Certification not found with the specified certification_id'), 404

#         # Handle the certification file if provided in the update
#         if certifications_file:
#             certification_data = certifications_file.read()
#             certification.certifications_data = certification_data

#         db.session.commit()

#         return jsonify(message='Certification updated successfully'), 200

#     except Exception as e:
#         return jsonify(error=str(e)), 400

# @app.route('/stage10/awards/<int:award_id>', methods=['PUT'])
# def update_award(award_id):
#     try:
#         # Get the form data from the request
#         awards_file = request.files.get('awards')
        
#         # Get the associated award
#         award = Awards.query.get(award_id)
#         if award is None:
#             return jsonify(error='Award not found with the specified award_id'), 404

#         # Handle the award file if provided in the update
#         if awards_file:
#             award_data = awards_file.read()
#             award.awards_data = award_data

#         db.session.commit()

#         return jsonify(message='Award updated successfully'), 200

#     except Exception as e:
#         return jsonify(error=str(e)), 400   



@app.route('/update_testimonials', methods=['PUT'])
def update_testimonialss():
    try:
        data = request.get_json()

        testimonials_data = data.get('testimonials')

        for item_data in testimonials_data:
            testimonial_id = item_data.get('id')
            testimonial = Testimonial.query.get(testimonial_id)

            if testimonial:
                testimonial.link_to_video = item_data.get('Link_to_Video', testimonial.link_to_video)
                testimonial.organizer_name = item_data.get('Organizer_Name', testimonial.organizer_name)
                testimonial.organization_name = item_data.get('Testimonial_Organization_Name', testimonial.organization_name)

        db.session.commit()

        return jsonify(message='Testimonials updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400 
    
# @app.route('/stage11/<int:person_id>', methods=['PUT'])
# def update_testimonials(person_id):
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404    
#         # Update the 'Testimonials' data
#         testimonials_data = data.get('Testimonials')

#         for testimonial_data in testimonials_data:
#             for testimonial_name, testimonial_info in testimonial_data.items():
#                 # Find the existing testimonial by ID
#                 testimonial_id = testimonial_info.get('id')
#                 if testimonial_id:
#                     existing_testimonial = Testimonial.query.get(testimonial_id)
#                     if existing_testimonial:
#                         existing_testimonial.organizer_name = testimonial_info['Organizer_Name']
#                         existing_testimonial.testimonial_organization_name = testimonial_info['Testimonial_Organization_Name']
#                         existing_testimonial.link_to_video = testimonial_info['Link_to_Video']


#         db.session.commit()

#         return jsonify(message='testimonials updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400    
    
    
    
# @app.route('/stage12/<int:person_id>', methods=['PUT'])
# def update_business_info(person_id):
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404       
#         # Update the 'business_info' data
#         business_info_data = data.get('business_info')
#         business_info_id = business_info_data.get('id')

#         if business_info_id:
#             existing_business_info = BusinessInfo.query.get(business_info_id)
#             if existing_business_info:
#                 existing_business_info.issue_payment = business_info_data['business_issue_payment']
                
#                 business_information = business_info_data.get('business_information')
#                 if business_information:
#                     existing_business_info.official_business_name = business_information['official_business_name']
#                     existing_business_info.business_email = business_information['business_email']
#                     existing_business_info.business_phone = business_information['business_phone']
#                     existing_business_info.business_number = business_information['business_number']
#                     existing_business_info.website = business_information['website']
                    
#         # Assuming that 'data' is your JSON data
#         social_media_business_data = data.get('social_media_business')

#         if social_media_business_data:
#             social_media_business = SocialMediaBusiness.query.filter_by(id=1).first()
#             if not social_media_business:
#                 # If the record doesn't exist, create a new one
#                 social_media_business = SocialMediaBusiness(id=1)
            
#             # Extract Facebook details
#             facebook_data = social_media_business_data.get('facebook')
#             if facebook_data:
#                 social_media_business.facebook_link = facebook_data.get('link')
#                 social_media_business.facebook_handle = facebook_data.get('handle')
#                 social_media_business.facebook_followers = facebook_data.get('followers')
            
#             # Extract Instagram details
#             instagram_data = social_media_business_data.get('instagram')
#             if instagram_data:
#                 social_media_business.instagram_link = instagram_data.get('link')
#                 social_media_business.instagram_handle = instagram_data.get('handle')
#                 social_media_business.instagram_followers = instagram_data.get('followers')
            
#             # Extract Twitter details
#             twitter_data = social_media_business_data.get('twitter')
#             if twitter_data:
#                 social_media_business.twitter_link = twitter_data.get('link')
#                 social_media_business.twitter_handle = twitter_data.get('handle')
#                 social_media_business.twitter_followers = twitter_data.get('followers')
            
#             # Extract LinkedIn details
#             linkedin_data = social_media_business_data.get('linkedin')
#             if linkedin_data:
#                 social_media_business.linkedin_link = linkedin_data.get('link')
#                 social_media_business.linkedin_handle = linkedin_data.get('handle')
#                 social_media_business.linkedin_followers = linkedin_data.get('followers')
            
#             # Extract TikTok details
#             tiktok_data = social_media_business_data.get('tiktok')
#             if tiktok_data:
#                 social_media_business.tiktok_link = tiktok_data.get('link')
#                 social_media_business.tiktok_handle = tiktok_data.get('handle')
#                 social_media_business.tiktok_followers = tiktok_data.get('followers')    
                
#         db.session.commit()

#         return jsonify(message='business_info updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400         


@app.route('/update_business_info_and_social_media', methods=['PUT'])
def update_business_info_and_social_media():
    try:
        data = request.get_json()

        business_info_data = data.get('business_info')
        social_media_data = data.get('social_media_business')

        # Update Business Info
        if business_info_data:
            business_info_id = business_info_data.get('id')
            business_info = BusinessInfo.query.get(business_info_id)

            if business_info:
                business_info.issue_payment = business_info_data.get('business_issue_payment', business_info.issue_payment)
                business_information = business_info_data.get('business_information', {})
                business_info.official_business_name = business_information.get('official_business_name', business_info.official_business_name)
                business_info.business_email = business_information.get('business_email', business_info.business_email)
                business_info.business_phone = business_information.get('business_phone', business_info.business_phone)
                business_info.business_number = business_information.get('business_number', business_info.business_number)
                business_info.website = business_information.get('website', business_info.website)

        # Update Social Media Business
        if social_media_data:
            social_media_id = social_media_data.get('id')
            social_media = SocialMediaBusiness.query.get(social_media_id)

            if social_media:
                facebook_data = social_media_data.get('facebook', {})
                social_media.facebook_link = facebook_data.get('link', social_media.facebook_link)
                social_media.facebook_handle = facebook_data.get('handle', social_media.facebook_handle)
                social_media.facebook_followers = facebook_data.get('followers', social_media.facebook_followers)

                # Add similar updates for Instagram
                instagram_data = social_media_data.get('instagram', {})
                social_media.instagram_link = instagram_data.get('link', social_media.instagram_link)
                social_media.instagram_handle = instagram_data.get('handle', social_media.instagram_handle)
                social_media.instagram_followers = instagram_data.get('followers', social_media.instagram_followers)

                # Add similar updates for LinkedIn
                linkedin_data = social_media_data.get('linkedin', {})
                social_media.linkedin_link = linkedin_data.get('link', social_media.linkedin_link)
                social_media.linkedin_handle = linkedin_data.get('handle', social_media.linkedin_handle)
                social_media.linkedin_followers = linkedin_data.get('followers', social_media.linkedin_followers)

                # Add similar updates for TikTok
                tiktok_data = social_media_data.get('tiktok', {})
                social_media.tiktok_link = tiktok_data.get('link', social_media.tiktok_link)
                social_media.tiktok_handle = tiktok_data.get('handle', social_media.tiktok_handle)
                social_media.tiktok_followers = tiktok_data.get('followers', social_media.tiktok_followers)

                # Add similar updates for Twitter
                twitter_data = social_media_data.get('twitter', {})
                social_media.twitter_link = twitter_data.get('link', social_media.twitter_link)
                social_media.twitter_handle = twitter_data.get('handle', social_media.twitter_handle)
                social_media.twitter_followers = twitter_data.get('followers', social_media.twitter_followers)

        db.session.commit()

        return jsonify(message='Business info and social media updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400

      
                 
# @app.route('/stage13/<int:person_id>', methods=['PUT'])
# def update_brand_product(person_id):
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404                       
#         # Update the 'Brand_Product_Campaigns&Endorsements' data
#         brand_campaigns_data1 = data.get('Brand_Product_Campaigns&Endorsementstheme1')
#         brand_campaigns_data2 = data.get('Brand_Product_Campaigns&Endorsementstheme2')

#         for organization_entry in brand_campaigns_data1:
#             for organization_key, organization_data in organization_entry.items():
#                 brand_campaign_id = organization_data.get('id')
#                 if brand_campaign_id:
#                     existing_brand_campaign = BrandCampaignOrganizationtheme1.query.get(brand_campaign_id)
#                     if existing_brand_campaign:
#                         existing_brand_campaign.part_of_social_media = organization_data['part_of_social_media']
                        
#                         organization_details = organization_data.get(f'{organization_key}_details')
#                         if organization_details:
#                             existing_brand_campaign.organization_name = organization_details['organization_name']
#                             existing_brand_campaign.platforms = organization_details['platforms']
#                             existing_brand_campaign.link_to_campaign = organization_details['link_to_campaign']
#                             existing_brand_campaign.start_year = organization_details['start_year']
#                             existing_brand_campaign.end_year = organization_details['end_year']     
                            
                            
#         for organization_entry in brand_campaigns_data2:
#             for organization_key, organization_data in organization_entry.items():
#                 brand_campaign_id = organization_data.get('id')
#                 if brand_campaign_id:
#                     existing_brand_campaign = BrandCampaignOrganizationtheme2.query.get(brand_campaign_id)
#                     if existing_brand_campaign:
#                         existing_brand_campaign.part_of_social_media = organization_data['part_of_social_media']
                        
#                         organization_details = organization_data.get(f'{organization_key}_details')
#                         if organization_details:
#                             existing_brand_campaign.organization_name = organization_details['organization_name']
#                             existing_brand_campaign.platforms = organization_details['platforms']
#                             existing_brand_campaign.link_to_campaign = organization_details['link_to_campaign']
#                             existing_brand_campaign.start_year = organization_details['start_year']
#                             existing_brand_campaign.end_year = organization_details['end_year']                                      
                
#         db.session.commit()

#         return jsonify(message='Brand_Product updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400   


@app.route('/update_brand_campaigns_endorsements', methods=['PUT'])
def update_brand_campaigns_endorsements():
    try:
        data = request.get_json()

        themes1_data = data.get('Brand_Product_CampaignsEndorsementstheme1')
        themes2_data = data.get('Brand_Product_CampaignsEndorsementstheme2')

        # Update Brand Campaigns and Endorsements for Theme 1
        if themes1_data:
            for item in themes1_data:
                item_id = item.get('id')
                brand_campaign = BrandCampaignOrganizationtheme1.query.get(item_id)

                if brand_campaign:
                    brand_campaign.part_of_social_media = item.get('part_of_social_media', brand_campaign.part_of_social_media)
                    brand_campaign.organization_name = item.get('organization_name', brand_campaign.organization_name)
                    brand_campaign.platforms = item.get('platforms', brand_campaign.platforms)
                    brand_campaign.link_to_campaign = item.get('link_to_campaign', brand_campaign.link_to_campaign)
                    brand_campaign.start_year = item.get('start_year', brand_campaign.start_year)
                    brand_campaign.end_year = item.get('end_year', brand_campaign.end_year)

        # Update Brand Campaigns and Endorsements for Theme 2
        if themes2_data:
            for item in themes2_data:
                item_id = item.get('id')
                brand_campaign = BrandCampaignOrganizationtheme2.query.get(item_id)

                if brand_campaign:
                    brand_campaign.part_of_social_media = item.get('part_of_social_media', brand_campaign.part_of_social_media)
                    brand_campaign.organization_name = item.get('organization_name', brand_campaign.organization_name)
                    brand_campaign.platforms = item.get('platforms', brand_campaign.platforms)
                    brand_campaign.link_to_campaign = item.get('link_to_campaign', brand_campaign.link_to_campaign)
                    brand_campaign.start_year = item.get('start_year', brand_campaign.start_year)
                    brand_campaign.end_year = item.get('end_year', brand_campaign.end_year)

        db.session.commit()

        return jsonify(message='Brand campaigns and endorsements updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400      
    
    
# @app.route('/stage14/<int:person_id>', methods=['PUT'])
# def update_at_event(person_id):
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404

#         # Update the 'at_events' data
#         at_events_data = data.get('at_events')

#         for at_event_data in at_events_data:
#             at_event_id = at_event_data.get('id')
#             if at_event_id:
#                 existing_at_event = AtEvents.query.get(at_event_id)
#                 if existing_at_event:
#                     presentation_software_data = at_event_data.get('presentation_software')
#                     if presentation_software_data:
#                         existing_at_event.using_presentation_software = presentation_software_data['using_presentation_software']
#                         existing_at_event.presentation_software_name = presentation_software_data['presentation_software_name']

#                     audience_interaction_software_data = at_event_data.get('audience_interaction_software')
#                     if audience_interaction_software_data:
#                         existing_at_event.using_audience_interaction_software = audience_interaction_software_data['using_audience_interaction_software']
#                         existing_at_event.audience_interaction_software_name = audience_interaction_software_data['audience_interaction_software_name']

#                     existing_at_event.attending_sessions_before_after_presentation = at_event_data['attending_sessions_before_after_presentation']

#                     meal_networking_session_data = at_event_data.get('meal_networking_session')
#                     if meal_networking_session_data:
#                         existing_at_event.attending_meals_networking_sessions = meal_networking_session_data['attending_meals_networking_sessions']
#                         existing_at_event.dietary_requirements_restrictions = meal_networking_session_data['dietary_requirements_restrictions']
#                         existing_at_event.A_V_requirements = meal_networking_session_data['A_V_requirements']

#                         # Update SpeakerIntroduction records
#                         speaker_introduction_data = meal_networking_session_data.get('speaker_introduction')
#                         if speaker_introduction_data:
#                             for introduction in speaker_introduction_data:
#                                 introduction_id = introduction.get('id')
#                                 introduction_text = introduction.get(f'introduction_{introduction_id}')
#                                 if introduction_text:
#                                     # Find the existing SpeakerIntroduction record by ID
#                                     existing_speaker_intro = next((si for si in existing_at_event.speaker_introduction if si.id == introduction_id), None)
#                                     if existing_speaker_intro:
#                                         existing_speaker_intro.introduction_text = introduction_text

#                     existing_at_event.prefer_to_book_travel = at_event_data['prefer_to_book_travel']

#                     travel_agent_data = at_event_data.get('travel_agent')
#                     if travel_agent_data:
#                         existing_at_event.use_travel_agent = travel_agent_data['use_travel_agent']
#                         existing_at_event.Preferred_Seating = travel_agent_data['Preferred_Seating']
#                         existing_at_event.Preferred_Airline = travel_agent_data['Preferred_Airline']
#                         existing_at_event.West_Jet_number = travel_agent_data['West_Jet#']
#                         existing_at_event.Air_Canada_number = travel_agent_data['Air_Canada#']

#                     existing_at_event.special_conditions_for_travel_arrangements = at_event_data['special_conditions_for_travel_arrangements']
#                     existing_at_event.table_for_book_sales = at_event_data['table_for_book_sales']

#         db.session.commit()

#         return jsonify(message='at_event updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400


@app.route('/update_at_events', methods=['PUT'])
def update_at_events():
    try:
        data = request.get_json()

        at_events_data = data.get('at_events')

        if at_events_data:
            for item in at_events_data:
                item_id = item.get('id')
                at_event = AtEvents.query.get(item_id)

                if at_event:
                    at_event.attending_sessions_before_after_presentation = item.get('attending_sessions_before_after_presentation', at_event.attending_sessions_before_after_presentation)

                    audience_interaction_data = item.get('audience_interaction_software', {})
                    at_event.audience_interaction_software_name = audience_interaction_data.get('audience_interaction_software_name', at_event.audience_interaction_software_name)
                    at_event.using_audience_interaction_software = audience_interaction_data.get('using_audience_interaction_software', at_event.using_audience_interaction_software)

                    meal_networking_data = item.get('meal_networking_session', {})
                    at_event.A_V_requirements = meal_networking_data.get('A_V_requirements', at_event.A_V_requirements)
                    at_event.attending_meals_networking_sessions = meal_networking_data.get('attending_meals_networking_sessions', at_event.attending_meals_networking_sessions)
                    at_event.dietary_requirements_restrictions = meal_networking_data.get('dietary_requirements_restrictions', at_event.dietary_requirements_restrictions)

                    speaker_introductions = meal_networking_data.get('speaker_introduction', [])
                    for intro in speaker_introductions:
                        intro_id = intro.get('id')
                        speaker_intro = SpeakerIntroduction.query.get(intro_id)
                        if speaker_intro:
                            speaker_intro.introduction_text = intro.get('introduction_text', speaker_intro.introduction_text)

                    at_event.prefer_to_book_travel = item.get('prefer_to_book_travel', at_event.prefer_to_book_travel)

                    presentation_software_data = item.get('presentation_software', {})
                    at_event.presentation_software_name = presentation_software_data.get('presentation_software_name', at_event.presentation_software_name)
                    at_event.using_presentation_software = presentation_software_data.get('using_presentation_software', at_event.using_presentation_software)

                    at_event.special_conditions_for_travel_arrangements = item.get('special_conditions_for_travel_arrangements', at_event.special_conditions_for_travel_arrangements)
                    at_event.table_for_book_sales = item.get('table_for_book_sales', at_event.table_for_book_sales)

                    travel_agent_data = item.get('travel_agent', {})
                    at_event.Air_Canada_number = travel_agent_data.get('Air_Canada#', at_event.Air_Canada_number)
                    at_event.Preferred_Airline = travel_agent_data.get('Preferred_Airline', at_event.Preferred_Airline)
                    at_event.Preferred_Seating = travel_agent_data.get('Preferred_Seating', at_event.Preferred_Seating)
                    at_event.West_Jet_number = travel_agent_data.get('West_Jet#', at_event.West_Jet_number)
                    at_event.use_travel_agent = travel_agent_data.get('use_travel_agent', at_event.use_travel_agent)

        db.session.commit()

        return jsonify(message='At events information updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400
    
    
# @app.route('/stage15/<int:person_id>', methods=['PUT'])
# def update_help_us_book_you(person_id):
#     try:
#         data = request.get_json()

#         # Extract the 'Help_us_book_you' data from the JSON
#         help_us_book_you_data = data.get('Help_us_book_you')

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404

#         # Check if 'Help_us_book_you' exists for this person
#         if not person.help_us_book_you:
#             return jsonify(error='Help_us_book_you not found for the specified person_id'), 404

#         # Update the 'HelpUsBookYou' data
#         help_us_book_you = person.help_us_book_you
#         help_us_book_you.speaker_reason_to_work_with = help_us_book_you_data['speaker_reason_to_work_with']
#         help_us_book_you.value_adds_and_offerings = help_us_book_you_data['value_adds_and_offerings']['offer_any_value_adds']
#         help_us_book_you.books_how_many_items = help_us_book_you_data['value_adds_and_offerings']['books']['how_many_items']
#         help_us_book_you.books_value_per_item = help_us_book_you_data['value_adds_and_offerings']['books']['value_per_item']
#         help_us_book_you.online_training_how_many_items = help_us_book_you_data['value_adds_and_offerings']['online_training']['how_many_items']
#         help_us_book_you.online_training_value_per_item = help_us_book_you_data['value_adds_and_offerings']['online_training']['value_per_item']
#         help_us_book_you.merch_how_many_items = help_us_book_you_data['value_adds_and_offerings']['merch']['how_many_items']
#         help_us_book_you.merch_value_per_item = help_us_book_you_data['value_adds_and_offerings']['merch']['value_per_item']
#         help_us_book_you.merch_2_how_many_items = help_us_book_you_data['value_adds_and_offerings']['merch_2']['how_many_items']
#         help_us_book_you.merch_2_value_per_item = help_us_book_you_data['value_adds_and_offerings']['merch_2']['value_per_item']
#         help_us_book_you.complementary_virtual_follow_sessions_consultation = help_us_book_you_data['complementary_virtual_follow_sessions_consultation']
#         help_us_book_you.inclusive_of_travel_expenses = help_us_book_you_data['inclusive_of_travel_expenses']
#         help_us_book_you.industries_do_you_not_work_with = help_us_book_you_data['industry_you_specialize_with']['industries_do_you_not_work_with']
#         help_us_book_you.favorite_audiences_event_types = help_us_book_you_data['industry_you_specialize_with']['favorite_audiences_event_types']
#         help_us_book_you.target_audiences_industries = help_us_book_you_data['industry_you_specialize_with']['target_audiences_industries']
#         help_us_book_you.English_French = help_us_book_you_data['English_&_French']
#         help_us_book_you.Q_A_in_French = help_us_book_you_data['Q&A_in_French']
#         help_us_book_you.offer_recordings = help_us_book_you_data['offer_recordings']
#         help_us_book_you.primary_source_of_income = help_us_book_you_data['primary_source_of_income']
#         help_us_book_you.hoping_for_speaking_to_become_your_primary_source_income = help_us_book_you_data['speaking_frequency']['hoping_for_speaking_to_become_your_primary_source_income']
#         help_us_book_you.current_speak_per_month = help_us_book_you_data['speaking_frequency']['current_speak_per_month']
#         help_us_book_you.virtual_events_over_pandemic = help_us_book_you_data['speaking_frequency']['virtual_events_over_pandemic']
#         help_us_book_you.speak_per_month = help_us_book_you_data['speaking_frequency']['speak_per_month']
#         help_us_book_you.market_yourself_as_a_speaker = help_us_book_you_data['speaking_frequency']['market_yourself_as_a_speaker']
#         help_us_book_you.affiliated_with_any_other_speakers_agencies = help_us_book_you_data['speaking_frequency']['affiliated_with_any_other_speakers_agencies']
#         help_us_book_you.percentage_of_bookings = help_us_book_you_data['speaking_frequency']['percentage_of_bookings']
#         help_us_book_you.Approximately_what_percentage = help_us_book_you_data['speaking_frequency']['Approximately_what_percentage']
#         help_us_book_you.speakers_are_you_affiliated_with = help_us_book_you_data['speaking_frequency']['speakers_are_you_affiliated_with']

#         db.session.commit()

#         return jsonify(message='Help Us Book You updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400    


@app.route('/update_help_us_book_you', methods=['PUT'])
def update_help_us_book_you():
    try:
        data = request.get_json()

        help_us_book_you_data = data.get('Help_us_book_you')

        if help_us_book_you_data:
            item_id = help_us_book_you_data.get('id')
            help_us_book_you = HelpUsBookYou.query.get(item_id)

            if help_us_book_you:
                help_us_book_you.English_French = help_us_book_you_data.get('English_&_French', help_us_book_you.English_French)
                help_us_book_you.Q_A_in_French = help_us_book_you_data.get('Q&A_in_French', help_us_book_you.Q_A_in_French)
                help_us_book_you.complementary_virtual_follow_sessions_consultation = help_us_book_you_data.get('complementary_virtual_follow_sessions_consultation', help_us_book_you.complementary_virtual_follow_sessions_consultation)
                help_us_book_you.inclusive_of_travel_expenses = help_us_book_you_data.get('inclusive_of_travel_expenses', help_us_book_you.inclusive_of_travel_expenses)
                help_us_book_you.primary_source_of_income = help_us_book_you_data.get('primary_source_of_income', help_us_book_you.primary_source_of_income)
                help_us_book_you.speaker_reason_to_work_with = help_us_book_you_data.get('speaker_reason_to_work_with', help_us_book_you.speaker_reason_to_work_with)

                industry_specialization_data = help_us_book_you_data.get('industry_you_specialize_with', {})
                help_us_book_you.favorite_audiences_event_types = industry_specialization_data.get('favorite_audiences_event_types', help_us_book_you.favorite_audiences_event_types)
                help_us_book_you.industries_do_you_not_work_with = industry_specialization_data.get('industries_do_you_not_work_with', help_us_book_you.industries_do_you_not_work_with)
                help_us_book_you.target_audiences_industries = industry_specialization_data.get('target_audiences_industries', help_us_book_you.target_audiences_industries)

                help_us_book_you.offer_recordings = help_us_book_you_data.get('offer_recordings', help_us_book_you.offer_recordings)

                speaking_frequency_data = help_us_book_you_data.get('speaking_frequency', {})
                help_us_book_you.Approximately_what_percentage = speaking_frequency_data.get('Approximately_what_percentage', help_us_book_you.Approximately_what_percentage)
                help_us_book_you.affiliated_with_any_other_speakers_agencies = speaking_frequency_data.get('affiliated_with_any_other_speakers_agencies', help_us_book_you.affiliated_with_any_other_speakers_agencies)
                help_us_book_you.current_speak_per_month = speaking_frequency_data.get('current_speak_per_month', help_us_book_you.current_speak_per_month)
                help_us_book_you.hoping_for_speaking_to_become_your_primary_source_income = speaking_frequency_data.get('hoping_for_speaking_to_become_your_primary_source_income', help_us_book_you.hoping_for_speaking_to_become_your_primary_source_income)
                help_us_book_you.market_yourself_as_a_speaker = speaking_frequency_data.get('market_yourself_as_a_speaker', help_us_book_you.market_yourself_as_a_speaker)
                help_us_book_you.percentage_of_bookings = speaking_frequency_data.get('percentage_of_bookings', help_us_book_you.percentage_of_bookings)
                help_us_book_you.speak_per_month = speaking_frequency_data.get('speak_per_month', help_us_book_you.speak_per_month)
                help_us_book_you.speakers_are_you_affiliated_with = speaking_frequency_data.get('speakers_are_you_affiliated_with', help_us_book_you.speakers_are_you_affiliated_with)
                help_us_book_you.virtual_events_over_pandemic = speaking_frequency_data.get('virtual_events_over_pandemic', help_us_book_you.virtual_events_over_pandemic)

                value_adds_and_offerings_data = help_us_book_you_data.get('value_adds_and_offerings', {})
                help_us_book_you.value_adds_and_offerings = value_adds_and_offerings_data.get('offer_any_value_adds', help_us_book_you.value_adds_and_offerings)

                books_data = value_adds_and_offerings_data.get('books', {})
                help_us_book_you.books_how_many_items = books_data.get('how_many_items', help_us_book_you.books_how_many_items)
                help_us_book_you.books_value_per_item = books_data.get('value_per_item', help_us_book_you.books_value_per_item)

                merch_data = value_adds_and_offerings_data.get('merch', {})
                help_us_book_you.merch_how_many_items = merch_data.get('how_many_items', help_us_book_you.merch_how_many_items)
                help_us_book_you.merch_value_per_item = merch_data.get('value_per_item', help_us_book_you.merch_value_per_item)

                merch_2_data = value_adds_and_offerings_data.get('merch_2', {})
                help_us_book_you.merch_2_how_many_items = merch_2_data.get('how_many_items', help_us_book_you.merch_2_how_many_items)
                help_us_book_you.merch_2_value_per_item = merch_2_data.get('value_per_item', help_us_book_you.merch_2_value_per_item)

                online_training_data = value_adds_and_offerings_data.get('online_training', {})
                help_us_book_you.online_training_how_many_items = online_training_data.get('how_many_items', help_us_book_you.online_training_how_many_items)
                help_us_book_you.online_training_value_per_item = online_training_data.get('value_per_item', help_us_book_you.online_training_value_per_item)

        db.session.commit()

        return jsonify(message='HelpUsBookYou information updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400

    
    
@app.route('/update_help_us_work_with_you', methods=['PUT'])
def update_help_us_work_with_you():
    try:
        data = request.get_json()

        help_us_work_with_you_data = data.get('Help_us_work_with_you')

        if help_us_work_with_you_data:
            item_id = help_us_work_with_you_data.get('id')
            help_us_work_with_you = HelpUsWorkWithYou.query.get(item_id)

            if help_us_work_with_you:
                help_us_work_with_you.appointment_booking_software = help_us_work_with_you_data.get('appointment_booking_software', help_us_work_with_you.appointment_booking_software)
                help_us_work_with_you.business_ownership = help_us_work_with_you_data.get('business_ownership', help_us_work_with_you.business_ownership)
                help_us_work_with_you.crm_usage = help_us_work_with_you_data.get('crm_usage', help_us_work_with_you.crm_usage)
                help_us_work_with_you.expectations_with_sbc = help_us_work_with_you_data.get('expectations_with_sbc', help_us_work_with_you.expectations_with_sbc)
                help_us_work_with_you.newsletter_onboarding = help_us_work_with_you_data.get('newsletter_onboarding', help_us_work_with_you.newsletter_onboarding)
                help_us_work_with_you.something_about_you = help_us_work_with_you_data.get('something_about_you', help_us_work_with_you.something_about_you)
                help_us_work_with_you.stories = help_us_work_with_you_data.get('stories', help_us_work_with_you.stories)
                help_us_work_with_you.tracking_system = help_us_work_with_you_data.get('tracking_system', help_us_work_with_you.tracking_system)
                help_us_work_with_you.whatsapp = help_us_work_with_you_data.get('whatsapp', help_us_work_with_you.whatsapp)

        db.session.commit()

        return jsonify(message='HelpUsWorkWithYou information updated successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 400
    
    
# @app.route('/stage17/<int:person_id>', methods=['PUT'])
# def update_fees(person_id):
#     try:
#         data = request.get_json()

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404

#         # Check if 'Fees' exists for this person
#         if not person.fees:
#             return jsonify(error='Fees not found for the specified person_id'), 404

#         # Update the 'Fees' data
#         fees_data = data.get('Fees')
#         fees = person.fees
#         fees.Pro_Bono_Events = fees_data['Pro_Bono_Events']
#         fees.Corporate_Keynote_20_60_Minutes = fees_data['Discounted_Rate_Events']['Corporate_Keynote_20-60_Minutes']
#         fees.Corporate_Workshop_60_120_Minutes = fees_data['Discounted_Rate_Events']['Corporate_Workshop_60-120_Minutes']
#         fees.Corporate_Half_Day_Training_or_Keynote_Breakout = fees_data['Discounted_Rate_Events']['Corporate_Half_Day_Training_or_Keynote_Breakout']
#         fees.Corporate_Full_Day_Training = fees_data['Discounted_Rate_Events']['Corporate_Full_Day_Training']
#         fees.Concurrent_Sessions_Fee = fees_data['Multiple_Sessions_on_the_Same_Day']['Concurrent_Sessions_Fee']
#         fees.One_Session_in_the_Morning_Fee = fees_data['Multiple_Sessions_on_the_Same_Day']['One_Session_in_the_Morning_Fee']
#         fees.One_Session_in_the_Afternoon_Fee = fees_data['Multiple_Sessions_on_the_Same_Day']['One_Session_in_the_Afternoon_Fee']
#         fees.Multiple_Sessions_on_Concurrent_Days = fees_data['Multiple_Sessions_on_Concurrent_Days']
#         fees.Multiple_Sessions_Over_a_Period_of_Time = fees_data['Multiple_Sessions_Over_a_Period_of_Time']
#         fees.Lowest_Acceptance_for_Informal_Talk = fees_data['Lowest_Acceptance_for_Informal_Talk']
#         fees.One_Day_Event = fees_data['Host_or_Emcee_Fees']['One_Day_Event']
#         fees.One_Day_Plus_Evening_Ceremony_Keynote = fees_data['Host_or_Emcee_Fees']['One_Day_Plus_Evening_Ceremony_Keynote']
#         fees.Two_Day_Event = fees_data['Host_or_Emcee_Fees']['Two_Day_Event']
#         fees.Two_Day_Plus_Evening_Ceremony_Keynote = fees_data['Host_or_Emcee_Fees']['Two_Day_Plus_Evening_Ceremony_Keynote']
#         fees.Three_Day_Event = fees_data['Host_or_Emcee_Fees']['Three_Day_Event']
#         fees.Three_Day_Plus_Evening_Ceremony_Keynote = fees_data['Host_or_Emcee_Fees']['Three_Day_Plus_Evening_Ceremony_Keynote']
#         fees.Four_Day_Event = fees_data['Host_or_Emcee_Fees']['Four_Day_Event']
#         fees.Four_Day_Plus_Evening_Ceremony_Keynote = fees_data['Host_or_Emcee_Fees']['Four_Day_Plus_Evening_Ceremony_Keynote']
#         fees.What_is_your_corporate_speaker_fee = fees_data['Host_or_Emcee_Fees']['What is your corporate speaker fee']
#         fees.lowest_you_will_accept = fees_data['Host_or_Emcee_Fees']['lowest you will accept']
#         fees.limitations_or_condition = fees_data['Host_or_Emcee_Fees']['limitations or condition']
#         fees.Driving_Distance_Fee = fees_data['Host_or_Emcee_Fees']['Driving Distance Fee']
#         fees.Province_Fee = fees_data['Host_or_Emcee_Fees']['Province Fee']
#         fees.Western_Canada_Fee = fees_data['Host_or_Emcee_Fees']['Western Canada Fee']
#         fees.Eastern_Canada_Fee = fees_data['Host_or_Emcee_Fees']['Eastern Canada Fee']
#         fees.Northern_Canada_Fee = fees_data['Host_or_Emcee_Fees']['Northern Canada Fee']
#         fees.Remote_Location_Fee = fees_data['Host_or_Emcee_Fees']['Remote Location Fee']
#         fees.Local_Discount = fees_data['Local_Discount']['Local_Discount']
#         fees.Local_Fee = fees_data['Local_Discount']['Local_Fee']
#         fees.Client_Direct_Approach_for_Local_Event = fees_data['Local_Discount']['Client_Direct_Approach_for_Local_Event']
#         fees.Virtual_Discount = fees_data['Virtual_Discount']['Virtual_Discountt']
#         fees.Virtual_Fee = fees_data['Virtual_Discount']['Virtual_Fee']
#         fees.Client_Direct_Approach_for_Virtual_Event = fees_data['Virtual_Discount']['Client_Direct_Approach_for_Virtual_Event']
#         fees.Small_Audience_Discount = fees_data['Small_Audience_Discount']['Small_Audience_Discountt']
#         fees.Small_Audience_Fee = fees_data['Small_Audience_Discount']['Small_Audience_Fee']
#         fees.Client_Direct_Approach_for_Small_Audience_Event = fees_data['Small_Audience_Discount']['Client_Direct_Approach_for_Small_Audience_Event']
#         fees.Qualification_for_Small_Audience = fees_data['Small_Audience_Discount']['Qualification_for_Small_Audience']
#         fees.Nonprofit_Discount = fees_data['Nonprofit_Discount']['Nonprofit_Discountt']
#         fees.Nonprofit_Fee = fees_data['Nonprofit_Discount']['Nonprofit_Fee']
#         fees.Client_Direct_Approach_for_Nonprofit = fees_data['Nonprofit_Discount']['Client_Direct_Approach_for_Nonprofit']
#         fees.Charitable_Organization_Discount = fees_data['Charitable_Organization_Discount']['Charitable_Organization_Discountt']
#         fees.Charitable_Fee = fees_data['Charitable_Organization_Discount']['Charitable_Fee']
#         fees.Client_Direct_Approach_for_Charitable_Organization = fees_data['Charitable_Organization_Discount']['Client_Direct_Approach_for_Charitable_Organization']
#         fees.outside_of_speaker_fee_ranges = fees_data['Charitable_Organization_Discount']['outside_of_speaker_fee_ranges']
#         fees.Rate_Increase = fees_data['Rate_Increase']

#         db.session.commit()

#         return jsonify(message='Fees updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400       


@app.route('/update_fees', methods=['PUT'])
def update_fees():
    try:
        data = request.get_json()

        fees_data = data.get('fees')

        if fees_data:
            item_id = fees_data.get('id')
            fees = Fees.query.get(item_id)

            if fees:
                fees.Pro_Bono_Events = fees_data.get('Pro_Bono_Events', fees.Pro_Bono_Events)
                fees.Corporate_Keynote_20_60_Minutes = fees_data.get('Corporate_Keynote_20_60_Minutes', fees.Corporate_Keynote_20_60_Minutes)
                fees.Corporate_Workshop_60_120_Minutes = fees_data.get('Corporate_Workshop_60_120_Minutes', fees.Corporate_Workshop_60_120_Minutes)
                fees.Corporate_Half_Day_Training_or_Keynote_Breakout = fees_data.get('Corporate_Half_Day_Training_or_Keynote_Breakout', fees.Corporate_Half_Day_Training_or_Keynote_Breakout)
                fees.Corporate_Full_Day_Training = fees_data.get('Corporate_Full_Day_Training', fees.Corporate_Full_Day_Training)
                fees.Concurrent_Sessions_Fee = fees_data.get('Concurrent_Sessions_Fee', fees.Concurrent_Sessions_Fee)
                fees.One_Session_in_the_Morning_Fee = fees_data.get('One_Session_in_the_Morning_Fee', fees.One_Session_in_the_Morning_Fee)
                fees.One_Session_in_the_Afternoon_Fee = fees_data.get('One_Session_in_the_Afternoon_Fee', fees.One_Session_in_the_Afternoon_Fee)
                fees.Multiple_Sessions_on_Concurrent_Days = fees_data.get('Multiple_Sessions_on_Concurrent_Days', fees.Multiple_Sessions_on_Concurrent_Days)
                fees.Multiple_Sessions_Over_a_Period_of_Time = fees_data.get('Multiple_Sessions_Over_a_Period_of_Time', fees.Multiple_Sessions_Over_a_Period_of_Time)
                fees.Lowest_Acceptance_for_Informal_Talk = fees_data.get('Lowest_Acceptance_for_Informal_Talk', fees.Lowest_Acceptance_for_Informal_Talk)
                fees.One_Day_Event = fees_data.get('One_Day_Event', fees.One_Day_Event)
                fees.One_Day_Plus_Evening_Ceremony_Keynote = fees_data.get('One_Day_Plus_Evening_Ceremony_Keynote', fees.One_Day_Plus_Evening_Ceremony_Keynote)
                fees.Two_Day_Event = fees_data.get('Two_Day_Event', fees.Two_Day_Event)
                fees.Two_Day_Plus_Evening_Ceremony_Keynote = fees_data.get('Two_Day_Plus_Evening_Ceremony_Keynote', fees.Two_Day_Plus_Evening_Ceremony_Keynote)
                fees.Three_Day_Event = fees_data.get('Three_Day_Event', fees.Three_Day_Event)
                fees.Three_Day_Plus_Evening_Ceremony_Keynote = fees_data.get('Three_Day_Plus_Evening_Ceremony_Keynote', fees.Three_Day_Plus_Evening_Ceremony_Keynote)
                fees.Four_Day_Event = fees_data.get('Four_Day_Event', fees.Four_Day_Event)
                fees.Four_Day_Plus_Evening_Ceremony_Keynote = fees_data.get('Four_Day_Plus_Evening_Ceremony_Keynote', fees.Four_Day_Plus_Evening_Ceremony_Keynote)
                fees.What_is_your_corporate_speaker_fee = fees_data.get('What_is_your_corporate_speaker_fee', fees.What_is_your_corporate_speaker_fee)
                fees.lowest_you_will_accept = fees_data.get('lowest_you_will_accept', fees.lowest_you_will_accept)
                fees.limitations_or_condition = fees_data.get('limitations_or_condition', fees.limitations_or_condition)
                fees.Driving_Distance_Fee = fees_data.get('Driving_Distance_Fee', fees.Driving_Distance_Fee)
                fees.Province_Fee = fees_data.get('Province_Fee', fees.Province_Fee)
                fees.Western_Canada_Fee = fees_data.get('Western_Canada_Fee', fees.Western_Canada_Fee)
                fees.Eastern_Canada_Fee = fees_data.get('Eastern_Canada_Fee', fees.Eastern_Canada_Fee)
                fees.Northern_Canada_Fee = fees_data.get('Northern_Canada_Fee', fees.Northern_Canada_Fee)
                fees.Remote_Location_Fee = fees_data.get('Remote_Location_Fee', fees.Remote_Location_Fee)
                fees.Local_Discount = fees_data.get('Local_Discount', fees.Local_Discount)
                fees.Local_Fee = fees_data.get('Local_Fee', fees.Local_Fee)
                fees.Client_Direct_Approach_for_Local_Event = fees_data.get('Client_Direct_Approach_for_Local_Event', fees.Client_Direct_Approach_for_Local_Event)
                fees.Virtual_Discount = fees_data.get('Virtual_Discount', fees.Virtual_Discount)
                fees.Virtual_Fee = fees_data.get('Virtual_Fee', fees.Virtual_Fee)
                fees.Client_Direct_Approach_for_Virtual_Event = fees_data.get('Client_Direct_Approach_for_Virtual_Event', fees.Client_Direct_Approach_for_Virtual_Event)
                fees.Small_Audience_Discount = fees_data.get('Small_Audience_Discount', fees.Small_Audience_Discount)
                fees.Small_Audience_Fee = fees_data.get('Small_Audience_Fee', fees.Small_Audience_Fee)
                fees.Client_Direct_Approach_for_Small_Audience_Event = fees_data.get('Client_Direct_Approach_for_Small_Audience_Event', fees.Client_Direct_Approach_for_Small_Audience_Event)
                fees.Qualification_for_Small_Audience = fees_data.get('Qualification_for_Small_Audience', fees.Qualification_for_Small_Audience)
                fees.Nonprofit_Discount = fees_data.get('Nonprofit_Discount', fees.Nonprofit_Discount)
                fees.Nonprofit_Fee = fees_data.get('Nonprofit_Fee', fees.Nonprofit_Fee)
                fees.Client_Direct_Approach_for_Nonprofit = fees_data.get('Client_Direct_Approach_for_Nonprofit', fees.Client_Direct_Approach_for_Nonprofit)
                fees.Charitable_Organization_Discount = fees_data.get('Charitable_Organization_Discount', fees.Charitable_Organization_Discount)
                fees.Charitable_Fee = fees_data.get('Charitable_Fee', fees.Charitable_Fee)
                fees.Client_Direct_Approach_for_Charitable_Organization = fees_data.get('Client_Direct_Approach_for_Charitable_Organization', fees.Client_Direct_Approach_for_Charitable_Organization)
                fees.outside_of_speaker_fee_ranges = fees_data.get('outside_of_speaker_fee_ranges', fees.outside_of_speaker_fee_ranges)
                fees.Rate_Increase = fees_data.get('Rate_Increase', fees.Rate_Increase)

                db.session.commit()

                return jsonify(message='Fees information updated successfully'), 200
            else:
                return jsonify(error='Fees with the specified ID not found'), 404
        else:
            return jsonify(error='No data provided in the request'), 400

    except Exception as e:
        return jsonify(error=str(e)), 400

    
# @app.route('/stage18/<int:person_id>', methods=['PUT'])
# def update_speaker_pitches(person_id):
#     try:
#         data = request.get_json()

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404    
#         # Assuming that 'data' is your JSON data
#         speaker_pitches_data = data.get('speaker_pitches')

#         if speaker_pitches_data:
#             # Iterate through each pitch in the JSON data
#             for pitch_entry in speaker_pitches_data:
#                 # Extract the pitch details
#                 pitch_details = list(pitch_entry.values())[0]  # Get the dictionary with pitch details
#                 pitch_id = pitch_details.get('id')  # Assuming you have a unique ID for each pitch

#                 # Check if the pitch exists in the database
#                 existing_pitch = SpeakerPitch.query.get(pitch_id)

#                 if existing_pitch:
#                     # Update the pitch data
#                     existing_pitch.general_pitch = pitch_details['general_pitch']
#                     existing_pitch.keyword_topic_focus_pitch = pitch_details['keyword_topic_focus_pitch']
#                     existing_pitch.Short_pitch_up = pitch_details['Short_pitch_up']
                    
#         db.session.commit()

#         return jsonify(message='speaker_pitches updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400         



@app.route('/update_speaker_pitches', methods=['PUT'])
def update_speaker_pitches():
    try:
        data = request.get_json()

        speaker_pitches_data = data.get('speaker_pitches')

        if speaker_pitches_data:
            for pitch_data in speaker_pitches_data:
                item_id = pitch_data.get('id')
                speaker_pitch = SpeakerPitch.query.get(item_id)

                if speaker_pitch:
                    speaker_pitch.general_pitch = pitch_data.get('general_pitch', speaker_pitch.general_pitch)
                    speaker_pitch.keyword_topic_focus_pitch = pitch_data.get('keyword_topic_focus_pitch', speaker_pitch.keyword_topic_focus_pitch)
                    speaker_pitch.Short_pitch_up = pitch_data.get('Short_pitch_up', speaker_pitch.Short_pitch_up)
                    db.session.commit()

            return jsonify(message='Speaker pitches updated successfully'), 200
        else:
            return jsonify(error='No data provided in the request'), 400

    except Exception as e:
        return jsonify(error=str(e)), 400             
                    
                    
# @app.route('/stage19/<int:person_id>', methods=['PUT'])
# def update_previous_clients(person_id):
#     try:
#         data = request.get_json()

#         # Get the associated person
#         person = Person.query.get(person_id)
#         if person is None:
#             return jsonify(error='Person not found with the specified person_id'), 404                    
#         # Assuming that 'data' is your JSON data
#         previous_clients_data = data.get('previous_clients')

#         if previous_clients_data:
#             # Iterate through each previous client in the JSON data
#             for client_entry in previous_clients_data:
#                 # Extract the client details
#                 for key, value in client_entry.items():
#                     if key != 'id':
#                         # Assuming you have a unique ID for each previous client
#                         client_id = client_entry.get('id')
                        
#                         # Check if the client exists in the database
#                         existing_client = PreviousClient.query.get(client_id)

#                         if existing_client:
#                             # Update the client data
#                             existing_client.organization_name = value      
#         db.session.commit()

#         return jsonify(message='previous_clients updated successfully'), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 400      


@app.route('/update_previous_clients', methods=['PUT'])
def update_previous_clients():
    try:
        data = request.get_json()

        previous_clients_data = data.get('previous_clients')

        if previous_clients_data:
            for client_data in previous_clients_data:
                item_id = client_data.get('id')
                previous_client = PreviousClient.query.get(item_id)

                if previous_client:
                    previous_client.organization_name = client_data.get('organization_name', previous_client.organization_name)
                    db.session.commit()

            return jsonify(message='Previous clients updated successfully'), 200
        else:
            return jsonify(error='No data provided in the request'), 400

    except Exception as e:
        return jsonify(error=str(e)), 400
    
    




'''
JSON OF DELETE
'''

# {
#     "topic_description_ids": [2],  
#     "testimonial_ids": [1],           
#     "image_ids": [4, 5],              
#     "video_ids": [2],                
#     "podcast_ids": [3],               
#     "book_ids": [1, 2],             
#     "bulk_order_detail_ids": [1],    
#     "media_mention_ids": [2],         
#     "white_paper_case_study_ids": [1], 
#     "degree_ids": [1],                   
#     "certificate_ids": [1],                 
#     "award_ids": [1],
#     "social_media_campaign_ids": [1],
#     "brand_endorsement_ids": [1],
#     "speaker_pitch_ids": [1],
#     "keyword_topic_focus_pitch_ids": [2],
#     "previous_client_ids": [14, 15]

# }  

   


# @app.route('/person/<int:person_id>', methods=['DELETE'])
# def delete_associated_records(person_id):
#     try:
#         # Query the Person with the given ID
#         person = Person.query.get(person_id)
#         print('person------------>',person)

#         if person is None:
#             return jsonify({'error': 'Person not found'}), 404

#         data = request.get_json()
#         print('data----------->',data)
#         if 'topic_description_ids' in data:
#             topic_description_ids = data['topic_description_ids']
#             for topic_description_id in topic_description_ids:
#                 topic_description = TopicDescription.query.get(topic_description_id)
#                 if topic_description:
#                     person.topic_descriptions.remove(topic_description)
#                     db.session.delete(topic_description)

#         if 'testimonial_ids' in data:
#             testimonial_ids = data['testimonial_ids']
#             for testimonial_id in testimonial_ids:
#                 testimonial = Testimonial.query.get(testimonial_id)
#                 if testimonial:
#                     person.testimonials.remove(testimonial)
#                     db.session.delete(testimonial)

#         if 'image_ids' in data:
#             image_ids = data['image_ids']
#             for image_id in image_ids:
#                 image = Image.query.get(image_id)
#                 if image:
#                     person.images.remove(image)
#                     db.session.delete(image)

#         if 'video_ids' in data:
#             video_ids = data['video_ids']
#             for video_id in video_ids:
#                 video = Video.query.get(video_id)
#                 if video:
#                     person.videos.remove(video)
#                     db.session.delete(video)

#         if 'podcast_ids' in data:
#             podcast_ids = data['podcast_ids']
#             for podcast_id in podcast_ids:
#                 podcast = Podcast.query.get(podcast_id)
#                 if podcast:
#                     person.podcasts.remove(podcast)
#                     db.session.delete(podcast)

#         if 'book_ids' in data:
#             book_ids = data['book_ids']
#             for book_id in book_ids:
#                 book = Book.query.get(book_id)
#                 if book:
#                     person.books.remove(book)
#                     db.session.delete(book)

#         if 'bulk_order_detail_ids' in data:
#             bulk_order_detail_ids = data['bulk_order_detail_ids']
#             for bulk_order_detail_id in bulk_order_detail_ids:
#                 bulk_order_detail = BulkOrderDetail.query.get(bulk_order_detail_id)
#                 if bulk_order_detail:
#                     db.session.delete(bulk_order_detail)

#         if 'media_mention_ids' in data:
#             media_mention_ids = data['media_mention_ids']
#             for media_mention_id in media_mention_ids:
#                 media_mention = MediaMention.query.get(media_mention_id)
#                 if media_mention:
#                     person.media_mentions.remove(media_mention)
#                     db.session.delete(media_mention)

#         if 'white_paper_case_study_ids' in data:
#             white_paper_case_study_ids = data['white_paper_case_study_ids']
#             for white_paper_case_study_id in white_paper_case_study_ids:
#                 white_paper_case_study = WhitePaperCaseStudy.query.get(white_paper_case_study_id)
#                 if white_paper_case_study:
#                     person.white_papers_case_studies.remove(white_paper_case_study)
#                     db.session.delete(white_paper_case_study)
                    
#         if 'degree_ids' in data:
#             degree_ids = data['degree_ids']
#             for degree_id in degree_ids:
#                 degree = Degrees.query.get(degree_id)
#                 if degree:
#                     person.degree_files.remove(degree)
#                     db.session.delete(degree)

        
#         if 'certificate_ids' in data:
#             certificate_ids = data['certificate_ids']
#             for certificate_id in certificate_ids:
#                 certificate = Certificates.query.get(certificate_id)
#                 if certificate:
#                     person.certificate_files.remove(certificate)
#                     db.session.delete(certificate)

        
#         if 'award_ids' in data:
#             award_ids = data['award_ids']
#             for award_id in award_ids:
#                 award = Awards.query.get(award_id)
#                 if award:
#                     person.awards_files.remove(award)
#                     db.session.delete(award)      
                    
                    
#         if 'social_media_campaign_ids' in data:
#             social_media_campaign_ids = data['social_media_campaign_ids']
#             for campaign_id in social_media_campaign_ids:
#                 campaign = SocialMediaMarketingCampaign.query.get(campaign_id)
#                 if campaign:
#                     person.social_media_marketing_campaigns.remove(campaign)
#                     db.session.delete(campaign)

#         if 'brand_endorsement_ids' in data:
#             brand_endorsement_ids = data['brand_endorsement_ids']
#             for endorsement_id in brand_endorsement_ids:
#                 endorsement = BrandEndorsement.query.get(endorsement_id)
#                 if endorsement:
#                     person.brand_endorsements.remove(endorsement)
#                     db.session.delete(endorsement)

#         if 'speaker_pitch_ids' in data:
#             speaker_pitch_ids = data['speaker_pitch_ids']
#             for pitch_id in speaker_pitch_ids:
#                 pitch = SpeakerPitch.query.get(pitch_id)
#                 if pitch:
#                     person.speaker_pitches.remove(pitch)
#                     db.session.delete(pitch)

#         if 'keyword_topic_focus_pitch_ids' in data:
#             keyword_topic_focus_pitch_ids = data['keyword_topic_focus_pitch_ids']
#             for pitch_id in keyword_topic_focus_pitch_ids:
#                 pitch = KeywordTopicFocusPitch.query.get(pitch_id)
#                 if pitch:
#                     person.speaker_pitches.remove(pitch)
#                     db.session.delete(pitch)
                                        
                    
#         if 'previous_client_ids' in data:
#             previous_client_ids = data['previous_client_ids']
#             for client_id in previous_client_ids:
#                 client = PreviousClient.query.get(client_id)
#                 if client:
#                     person.previous_clients.remove(client)
#                     db.session.delete(client)                  

#         db.session.commit()

#         return jsonify({'message': 'Selected associated records of the person have been deleted'}), 200

#     except Exception as e:
#         return jsonify({'errorrrrrrrrr': str(e)}), 400
    
    
    

# @app.route('/person/<int:person_id>', methods=['PUT'])
# def update_person(person_id):
#     try:
#         # Get the existing person record by ID
#         person = Person.query.get(person_id)

#         if not person:
#             return jsonify({'error': 'Person not found'}), 404

#         data = request.get_json()

#         # Update the 'person' data
#         person_data = data.get('person')
#         person.name = person_data.get('name')
#         person.age = person_data.get('age')

#         # Update the 'Biography' data
#         biography_data = data.get('Biography')
#         biography = person.biography
#         biography.long_bio = biography_data.get('Long_Bio')
#         biography.speaker_topics_selection = biography_data.get('Speaker_Topics_selection')
#         biography.speaker_topics_additional_keywords = biography_data.get('Speaker_Topics_additional_keywords_separated_by_commas')
#         biography.speaker_types_pop_up = biography_data.get('Speaker_Types_will_showcase_as_a_pop_up_as_they_submit_the_long_bio')
#         biography.additional_types_keywords = biography_data.get('Additional_Types_Keywords_Separated_by_Commas_to_profile_that_may_not_be_in_our_Speaker_Types_section')
#         biography.speaker_tags_keywords = biography_data.get('Speaker_Tags')
#         biography.short_bio = biography_data.get('Short_Bio')
#         introductory_bio = biography_data.get('Introductory_Bio')
#         biography.introductory_bio_title_type = introductory_bio.get('Descriptive_Title_Type')
#         biography.introductory_bio_title1 = introductory_bio.get('Descriptive_Title1')
#         biography.introductory_bio_title2 = introductory_bio.get('Descriptive_Title2')
#         biography.introductory_bio_title3 = introductory_bio.get('Descriptive_Title3')
#         biography.location_city_province_state = biography_data.get('Location_City_Province/State')
#         biography.audio_introduction_to_profile = biography_data.get('Audio_Introduction_to_Profile')
        
        
        
#         # Update the 'topic_descriptions' data
#         topic_descriptions_data = data.get('topic_descriptions')
#         if topic_descriptions_data:
#             # Clear existing topic descriptions
#             person.topic_descriptions.clear()
#             for topic_number, topic_data in topic_descriptions_data.items():
#                 # Join the list of topic delivered as strings with a comma separator
#                 topic_delivered_as = ', '.join(topic_data.get('Topic_delivered_as'))

#                 # Create or update an existing TopicDescription object
#                 topic_description = TopicDescription.query.filter_by(person_id=person_id, topic_description_title=topic_data.get('Topic_Description_Title')).first()
#                 if not topic_description:
#                     topic_description = TopicDescription(
#                         topic_description_title=topic_data.get('Topic_Description_Title')
#                     )
#                 topic_description.topic_description_body_text = topic_data.get('Topic_Description_Body_Text')
#                 topic_description.topic_delivered_as = topic_delivered_as
#                 # ... (update other attributes)

#                 # Append the updated topic description to the person's list
#                 person.topic_descriptions.append(topic_description)

#         # Update the 'Testimonials' data
#         testimonials_data = data.get('Testimonials')
#         # Clear existing testimonials
#         person.testimonials.clear()
#         for testimonial_data in testimonials_data:
#             for testimonial_key, testimonial_value in testimonial_data.items():
#                 # Create a new or update an existing Testimonial object
#                 testimonial = Testimonial.query.filter_by(person_id=person_id, organizer_name=testimonial_value.get('Organizer_Name')).first()
#                 if not testimonial:
#                     testimonial = Testimonial(
#                         organizer_name=testimonial_value.get('Organizer_Name')
#                     )
#                 testimonial.body_text = testimonial_value.get('Body_Text')
#                 testimonial.testimonial_organization_name = testimonial_value.get('Testimonial_Organization_Name')
#                 testimonial.link_to_video = testimonial_value.get('Link_to_Video')
#                 # Append the updated testimonial to the person's list
#                 person.testimonials.append(testimonial)

#         # Update the 'Images' data
#         images_data = data.get('Images')
#         # Clear existing images
#         person.images.clear()
#         for image_key, image_value in images_data.items():
#             # Create a new Image object
#             new_image = Image(
#                 owns_rights=image_value.get('Owns_Rights'),
#                 permission_granted=image_value.get('Permission_Granted')
#             )
#             # Append the new image to the person's list
#             person.images.append(new_image)

#         # # Update the 'topic_descriptions' data
#         # topic_descriptions_data = data.get('topic_descriptions')
#         # person.topic_descriptions = []
#         # if topic_descriptions_data:
#         #     for topic_number, topic_data in topic_descriptions_data.items():
#         #         # Join the list of topic delivered as strings with a comma separator
#         #         topic_delivered_as = ', '.join(topic_data.get('Topic_delivered_as'))

#         #         # Create a new TopicDescription object
#         #         topic_description = TopicDescription(
#         #             topic_description_title=topic_data.get('Topic_Description_Title'),
#         #             topic_description_body_text=topic_data.get('Topic_Description_Body_Text'),
#         #             topic_delivered_as=topic_delivered_as,  # Use the converted string
#         #             topic_description_keywords_category=topic_data.get('Topic_Description_1_Topics_Keyword_Category'),
#         #             topic_description_additional_keywords=topic_data.get('Topic_Description_1_additional_topic_keywords_separated_by_comma'),
#         #             topic_description_types_keyword_categories=topic_data.get('Topic_Description_1_Types_Keyword_Categories'),
#         #             topic_description_additional_types_keywords=topic_data.get('Topic_Description_1_additional_types_keywords_separated_by_commas'),
#         #             topic_description_awareness_days_selection=topic_data.get('Topic_Description_Awareness_Days_Selection'),
#         #             audio_clip_for_topic_description=topic_data.get('Audio_Clip_for_Topic_Description_1'),
#         #             video_clip_for_topic_description=topic_data.get('Video_Clip_for_Topic_Description_1')
#         #         )
#         #         person.topic_descriptions.append(topic_description)
        
#         # # Update the 'Testimonials' data
#         # testimonials_data = data.get('Testimonials')
#         # person.testimonials = []
#         # for testimonial_data in testimonials_data:
#         #     for testimonial_key, testimonial_value in testimonial_data.items():
#         #         testimonial = Testimonial(
#         #             body_text=testimonial_value.get('Body_Text'),
#         #             organizer_name=testimonial_value.get('Organizer_Name'),
#         #             testimonial_organization_name=testimonial_value.get('Testimonial_Organization_Name'),
#         #             link_to_video=testimonial_value.get('Link_to_Video')
#         #         )
#         #         person.testimonials.append(testimonial)

#         # Commit the changes to the database
#         db.session.commit()

#         return jsonify({'message': 'Person data updated successfully'}), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 400



# @app.route('/person/<int:person_id>', methods=['PUT'])
# def update_person(person_id):
#     try:
#         # Get the existing person record by ID
#         person = Person.query.get(person_id)

#         if not person:
#             return jsonify({'error': 'Person not found'}), 404

#         data = request.get_json()

#         # Update the 'person' data
#         person_data = data.get('person')
#         person.name = person_data.get('name')
#         person.age = person_data.get('age')

#         # Update the 'Biography' data
#         biography_data = data.get('Biography')
#         biography = person.biography
#         biography.long_bio = biography_data.get('Long_Bio')
#         biography.speaker_topics_selection = biography_data.get('Speaker_Topics_selection')
#         biography.speaker_topics_additional_keywords = biography_data.get('Speaker_Topics_additional_keywords_separated_by_commas')
#         biography.speaker_types_pop_up = biography_data.get('Speaker_Types_will_showcase_as_a_pop_up_as_they_submit_the_long_bio')
#         biography.additional_types_keywords = biography_data.get('Additional_Types_Keywords_Separated_by_Commas_to_profile_that_may_not_be_in_our_Speaker_Types_section')
#         biography.speaker_tags_keywords = biography_data.get('Speaker_Tags')
#         biography.short_bio = biography_data.get('Short_Bio')
#         introductory_bio = biography_data.get('Introductory_Bio')
#         biography.introductory_bio_title_type = introductory_bio.get('Descriptive_Title_Type')
#         biography.introductory_bio_title1 = introductory_bio.get('Descriptive_Title1')
#         biography.introductory_bio_title2 = introductory_bio.get('Descriptive_Title2')
#         biography.introductory_bio_title3 = introductory_bio.get('Descriptive_Title3')
#         biography.location_city_province_state = biography_data.get('Location_City_Province/State')
#         biography.audio_introduction_to_profile = biography_data.get('Audio_Introduction_to_Profile')

#         # Update the 'topic_descriptions' data
#         topic_descriptions_data = data.get('topic_descriptions')
#         if topic_descriptions_data:
#             # Clear existing topic descriptions
#             # person.topic_descriptions.clear()
#             for topic_number, topic_data in topic_descriptions_data.items():
#                 # Join the list of topic delivered as strings with a comma separator
#                 topic_delivered_as = ', '.join(topic_data.get('Topic_delivered_as'))

#                 # Create or update an existing TopicDescription object
#                 topic_description = TopicDescription.query.filter_by(person_id=person_id, topic_description_title=topic_data.get('Topic_Description_Title')).first()
#                 if not topic_description:
#                     topic_description = TopicDescription(
#                         topic_description_title=topic_data.get('Topic_Description_Title')
#                     )
#                 topic_description.topic_description_body_text = topic_data.get('Topic_Description_Body_Text')
#                 topic_description.topic_delivered_as = topic_delivered_as
#                 # Update all other attributes here
#                 topic_description.topic_description_keywords_category = topic_data.get('Topic_Description_1_Topics_Keyword_Category')
#                 topic_description.topic_description_additional_keywords = topic_data.get('Topic_Description_1_additional_topic_keywords_separated_by_comma')
#                 topic_description.topic_description_types_keyword_categories = topic_data.get('Topic_Description_1_Types_Keyword_Categories')
#                 topic_description.topic_description_additional_types_keywords = topic_data.get('Topic_Description_1_additional_types_keywords_separated_by_commas')
#                 topic_description.topic_description_awareness_days_selection = topic_data.get('Topic_Description_Awareness_Days_Selection')
#                 topic_description.audio_clip_for_topic_description = topic_data.get('Audio_Clip_for_Topic_Description_1')
#                 topic_description.video_clip_for_topic_description = topic_data.get('Video_Clip_for_Topic_Description_1')
                
#                 # Append the updated topic description to the person's list
#                 # person.topic_descriptions.append(topic_description)

#         # Update the 'Testimonials' data
#         testimonials_data = data.get('Testimonials')
#         # Clear existing testimonials
#         # person.testimonials.clear()
#         for testimonial_data in testimonials_data:
#             for testimonial_key, testimonial_value in testimonial_data.items():
#                 # Create a new or update an existing Testimonial object
#                 testimonial = Testimonial.query.filter_by(person_id=person_id, organizer_name=testimonial_value.get('Organizer_Name')).first()
#                 if not testimonial:
#                     testimonial = Testimonial(
#                         organizer_name=testimonial_value.get('Organizer_Name')
#                     )
#                 testimonial.body_text = testimonial_value.get('Body_Text')
#                 testimonial.testimonial_organization_name = testimonial_value.get('Testimonial_Organization_Name')
#                 testimonial.link_to_video = testimonial_value.get('Link_to_Video')
#                 # Update all other attributes here
                
#                 # Append the updated testimonial to the person's list
#                 # person.testimonials.append(testimonial)

#         # Update the 'Images' data
#         images_data = data.get('Images')
#         # Clear existing images
#         # person.images.clear()
#         for image_key, image_value in images_data.items():
#             # Create a new Image object
#             new_image = Image(
#                 owns_rights=image_value.get('Owns_Rights'),
#                 permission_granted=image_value.get('Permission_Granted')
#             )
#             # Update all other attributes here
            
#             # Append the new image to the person's list
#             # person.images.append(new_image)

#         # Commit the changes to the database
#         db.session.commit()

#         return jsonify({'message': 'Person data updated successfully'}), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 400


# @app.route('/person/<int:person_id>', methods=['PUT'])
# def update_person(person_id):
#     try:
#         data = request.get_json()
#         person_data = data.get('person')
#         biography_data = data.get('Biography')
#         topic_descriptions_data = data.get('topic_descriptions')
#         # testimonials_data = data.get('Testimonials')
#         # images_data = data.get('Images')
#         # print('image_data------------>',images_data)
#         videos_data = data.get('Videos')
#         podcasts_data = data.get('podcasts')
#         books_data = data.get('Books')
#         media_mentions_data = data.get('media_mentions')
#         white_papers_case_studies_data = data.get('white_papers_case_studies')

#         existing_person = Person.query.get(person_id)

#         if existing_person:
#             existing_person.name = person_data['name']
#             existing_person.age = person_data['age']

#             existing_person.biography.long_bio = biography_data.get('Long_Bio')
#             existing_person.biography.speaker_topics_selection = biography_data.get('Speaker_Topics_selection')
#             existing_person.biography.speaker_topics_additional_keywords = biography_data.get('Speaker_Topics_additional_keywords_separated_by_commas')
#             existing_person.biography.speaker_types_pop_up = biography_data.get('Speaker_Types_will_showcase_as_a_pop_up_as_they_submit_the_long_bio')
#             existing_person.biography.additional_types_keywords = biography_data.get('Additional_Types_Keywords_Separated_by_Commas_to_profile_that_may_not_be_in_our_Speaker_Types_section')
#             existing_person.biography.speaker_tags_keywords = biography_data.get('Speaker_Tags')
#             existing_person.biography.short_bio = biography_data.get('Short_Bio')
#             existing_person.biography.introductory_bio_title_type = biography_data.get('Introductory_Bio').get('Descriptive_Title_Type')
#             existing_person.biography.introductory_bio_title1 = biography_data.get('Introductory_Bio').get('Descriptive_Title1')
#             existing_person.biography.introductory_bio_title2 = biography_data.get('Introductory_Bio').get('Descriptive_Title2')
#             existing_person.biography.introductory_bio_title3 = biography_data.get('Introductory_Bio').get('Descriptive_Title3')
#             existing_person.biography.location_city_province_state = biography_data.get('Location_City_Province/State')
#             existing_person.biography.audio_introduction_to_profile = biography_data.get('Audio_Introduction_to_Profile')

#             if topic_descriptions_data:
#                 for topic_key, topic_data in topic_descriptions_data.items():
#                     # Assuming topic_key is "Topic 1", "Topic 2", etc.
#                     topic_number = int(topic_key.split()[1])  # Extract the topic number from the key
#                     if 1 <= topic_number <= len(existing_person.topic_descriptions):
#                         existing_topic_description = existing_person.topic_descriptions[topic_number - 1]

#                     if existing_topic_description:
#                         existing_topic_description.topic_description_title = topic_data.get('Topic_Description_Title')
#                         existing_topic_description.topic_description_body_text = topic_data.get('Topic_Description_Body_Text')
#                         existing_topic_description.topic_delivered_as = ', '.join(topic_data.get('Topic_delivered_as'))
#                         existing_topic_description.topic_description_keywords_category = topic_data.get('Topic_Description_1_Topics_Keyword_Category')
#                         existing_topic_description.topic_description_additional_keywords = topic_data.get('Topic_Description_1_additional_topic_keywords_separated_by_comma')
#                         existing_topic_description.topic_description_types_keyword_categories = topic_data.get('Topic_Description_1_Types_Keyword_Categories')
#                         existing_topic_description.topic_description_additional_types_keywords = topic_data.get('Topic_Description_1_additional_types_keywords_separated_by_commas')
#                         existing_topic_description.topic_description_awareness_days_selection = topic_data.get('Topic_Description_Awareness_Days_Selection')
#                         existing_topic_description.audio_clip_for_topic_description = topic_data.get('Audio_Clip_for_Topic_Description_1')
#                         existing_topic_description.video_clip_for_topic_description = topic_data.get('Video_Clip_for_Topic_Description_1')
                        
#             # Update the 'Testimonials' data
#             testimonials_data = data.get('Testimonials')
#             for testimonial_data in testimonials_data:
#                 for testimonial_key, testimonial_value in testimonial_data.items():
#                     testimonial = Testimonial.query.filter_by(person_id=person_id, organizer_name=testimonial_value.get('Organizer_Name')).first()
#                     print('testimonial---------->',testimonial)
#                     if not testimonial:
#                         testimonial = Testimonial(
#                             organizer_name=testimonial_value.get('Organizer_Name')
#                         )
#                     testimonial.body_text = testimonial_value.get('Body_Text')
#                     testimonial.testimonial_organization_name = testimonial_value.get('Testimonial_Organization_Name')
#                     testimonial.link_to_video = testimonial_value.get('Link_to_Video')
                    
                    
#             # Update the 'Images' data
#             images_data = data.get('Images')
#             print('image_data------------>',images_data)
#             for image_data in images_data:
#                 print('image_data.items----------->',image_data.items)
#                 for image_key, image_value in image_data.items():
#                     print('image_key---------->',image_key)
#                     print('image_value----->',image_value)
#                     image = Image.query.filter_by(person_id=person_id, owns_rights=image_value.get('Owns_Rights')).first()
#                     # print('image-------------->',image)
#                     if not image:
#                         image = Image(
#                             owns_rights=image_value.get('Owns_Rights')
#                         )
#                     image.permission_granted = image_value.get('Permission_Granted') 
                    
                    
                    

#             db.session.commit()
#             return jsonify({'message': 'Person, Biography, TopicDescriptions updated successfully'}), 200
#         else:
#             return jsonify({'error': 'Person not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# if __name__ == '__main__':
#     app.run(debug=True)


    
    
# @app.route('/person/<int:person_id>', methods=['PUT'])
# def update_person(person_id):
#     person = Person.query.get_or_404(person_id)
#     data = request.get_json()
    
#     person.name = data['name']
#     person.age = data['age']
#     db.session.commit()
#     return jsonify({'message': 'Person updated successfully'}), 200

# @app.route('/person/<int:person_id>', methods=['DELETE'])
# def delete_person(person_id):
#     person = Person.query.get_or_404(person_id)
#     db.session.delete(person)
#     db.session.commit()
#     return jsonify({'message': 'Person deleted successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)









