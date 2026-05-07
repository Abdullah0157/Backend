import os
import re
from database import SessionLocal, engine
import models

# Recreate tables to wipe the previous ones and insert the full batch cleanly
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

def parse_and_seed():
    raw_data = """Posted TodayNew
High demand
Energy Regulatory Attorney
micro1
100 Openings
Required skills
Pjm interconnection compliance
Ferc regulations
Energy permitting
+2
Pay:$100 - $135/hour

https://jobs.micro1.ai/post/a3769b75-c39f-4227-a03d-1e4e6f1ab035?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted TodayNew
High demand
Paralegal
micro1
100 Openings
Required skills
Right-of-way acquisition
Site control documentation
Easement agreements
+2
Pay:$42 - $55/hour


https://jobs.micro1.ai/post/b0233e00-ed98-491d-b15c-c2b5bce27388?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted TodayNew
Law Clerk (Commercial Real Estate / Energy)
micro1
50 Openings
Required skills
Commercial real estate document review
Title & ownership understanding
Data extraction & attention to detail
+3
Pay:$50 - $120/hour
https://jobs.micro1.ai/post/03032271-800c-4013-8c48-821f281f705e?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Corporate M&A Paralegal
micro1
1 Opening
Required skills
Personally identifiable information
Compliance
Mergers & acquisitions
+1
Pay:$40 - $70/hour
Refer and earn$1000
Posted YesterdayNew
High demand
https://jobs.micro1.ai/post/a945e259-58b0-48c3-9eeb-77e935cd6d97?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Corporate/M&A Attorney
micro1
1 Opening
Required skills
Personally identifiable information
Compliance
Mergers & acquisitions
+1
Pay:$40 - $70/hour
Refer and earn$1000
Posted YesterdayNew
High demand
https://jobs.micro1.ai/post/b22ee3a5-69b5-455f-a8a2-27951ee9d575?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Visual Evaluation Specialist
micro1
499 Openings
Required skills
Visual content evaluation
Written communication
Analytical skills
+2
Pay:$20 - $70/hour
https://jobs.micro1.ai/post/937562ec-bc66-4321-afa7-19ea26fa838b?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral                          

AI Model Assessment Specialist
micro1
1000 Openings
Required skills
Ai model evaluation
Analytical thinking
Reading comprehension
+7
Pay:$22 - $70/hour
https://jobs.micro1.ai/post/681fb250-a874-423a-9c19-baf55a539fa3?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Data-Video Generalist
micro1
100 Openings
Required skills
Attention to detail
Video recording
Reliable output management
Pay:$6 - $6/hour
https://jobs.micro1.ai/post/4387c6bb-4b3d-402d-be90-dcbb98c17f3c?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Data-Video Generalist
micro1
9 Openings
Required skills
Video recording
Attention to detail
Physical ability for repetitive tasks
Pay:$13 - $13/hour

https://jobs.micro1.ai/post/3e8dd78b-aab6-49e9-a5a6-cb5709af78c0?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted YesterdayNew
High demand
UI/UX Designer
micro1
100 Openings
Required skills
Ui
Ux
Designing
Pay:$22 - $70/hour

https://jobs.micro1.ai/post/0a82fd1e-73a3-481e-8e13-751a2cbed072?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted YesterdayNew
High demand
AI Evaluation Specialist
micro1
1400 Openings
Required skills
Critical thinking
Editorial judgment
Content evaluation
+2
Pay:$22 - $70/hour

https://jobs.micro1.ai/post/86536b3b-1d21-4a7f-8f7d-ad99972c43e5?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted YesterdayNew
High demand
Management consultant
micro1
10 Openings
Required skills
Management consulting methodologies
Strategic analysis
Business process improvement
+15
Pay:$100 - $250/hour

https://jobs.micro1.ai/post/3a32cd4b-8817-417f-82f0-92c3c956282b?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted YesterdayNew
High demand
Data Scientist
micro1
10 Openings
Required skills
Statistics & mathematics
Data handling
Data collecting
+4
Pay:$30 - $130/hour

https://jobs.micro1.ai/post/4e8a5807-9cc3-4847-afa3-16cefb5dec7a?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted YesterdayNew
High demand
Legal Specialist
micro1
10 Openings
Required skills
Legal
Contract review & negotiation
Case analysis
+8
Pay:$35 - $50/hour

https://jobs.micro1.ai/post/5cb1fbff-aa4d-433e-b57a-1310d999ae85?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted YesterdayNew
High demand
Software Developer
micro1
100 Openings
Required skills
Python
Rust
Golang
+5
Pay:$60 - $120/hour
https://jobs.micro1.ai/post/981f9791-70f7-4e78-bd08-09bbe8c0ff25?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Backend Engineer
micro1
50 Openings
Required skills
Backend developement
Pay:$60 - $120/hour
https://jobs.micro1.ai/post/b7cfaaf8-f6d0-4623-a223-6670c5b92ca0?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 3 days agoNew
High demand
Frontend Engineer
micro1
52 Openings
Required skills
Javascript
Typescript
React
Pay:$60 - $120/hour

https://jobs.micro1.ai/post/04efd226-3dc5-4514-8013-4fdf3a96d56c?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral
Posted 3 days agoNew
High demand
Full Stack Developer
micro1
50 Openings
Required skills
Node.js
Typescript
React
+9
Pay:$60 - $120/hour

https://jobs.micro1.ai/post/2ae1527c-d640-4db6-bb43-5ae8556e03af?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted TodayNew
Medical Specialist
micro1
300 Openings
Required skills
Clinical diagnosis
Treatment planning
Medical knowledge & expertise
+8
Pay:$15 - $28/hour
https://jobs.micro1.ai/post/0b95255b-a273-4f09-b7d8-0f4205c7f18e?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted YesterdayNew
Legal Specialist
micro1
300 Openings
Required skills
Legal
Contract review & negotiation
Case analysis
+8
Pay:$15 - $28/hour

https://jobs.micro1.ai/post/0f6b7386-98e6-4bac-b959-cda758344350?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral
Posted YesterdayNew
Finance Specialist
micro1
299 Openings
Required skills
Financial modeling
Financial analysis
Forecasting
+9
Pay:$15 - $28/hour

https://jobs.micro1.ai/post/af84d7d4-7222-4a0d-9267-bbc6a4511bd9?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 3 days agoNew
Cross-Platform Game Programmer
micro1
10 Openings
Required skills
C++
Cocos2d-x
Cross-platform development
+19
Pay:$20 - $120/hour
https://jobs.micro1.ai/post/3a187070-b5a0-4e39-ad42-f2c4245396c8?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 3 days agoNew
High demand
Software Developer
micro1
100 Openings
Required skills
Python
Rust
Golang
+5
Pay:$60 - $120/hour

https://jobs.micro1.ai/post/579e38ac-33bf-4d85-955c-7c1a8d7ee17d?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 3 days agoNew
High demand
Hardware Operations Manager
micro1
1 Opening
Required skills
Device lifecycle/it ops
Mdm/device management
Inventory & hardware management
Pay:$85,000 - $130,000/year

https://jobs.micro1.ai/post/e53fe004-7165-417e-b5c6-cbe1e6d15b9c?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 4 days agoNew
Data Protection Officer (PII Compliance)
micro1
20 Openings
Required skills
Pii
Data management
Data privacy
+2
Pay:$40 - $70/hour


https://jobs.micro1.ai/post/f6a7bee2-63a7-49c0-91df-fb87dc0132cf?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 4 days agoNew
Growth Lead
micro1
1 Opening
Required skills
Marketing budget
Video content
Copywriting
+1
Pay:$75,000 - $150,000/year
https://jobs.micro1.ai/post/c2252c36-f215-4332-98d0-947e55370cbd?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 4 days agoNew
Paralegal / Legal Assistant (PII Compliance)
micro1
20 Openings
Required skills
Pii
M&a
Compliance
+2
Pay:$40 - $70/hour

https://jobs.micro1.ai/post/89204ad6-bd0f-445c-b253-7497740dfb64?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 4 days ago
S’gaw Karen Bilingual Expert
micro1
1 Opening
Required skills
S’gaw karen
English
Translation
+4
Pay:$20 - $65/hour

https://jobs.micro1.ai/post/782a3e48-be08-4d9c-a502-880ce0fed60e?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 4 days ago
High demand
Tax Professional (EA / CPA)
micro1
1 Opening
Required skills
Regulatory interpretation
Logical reasoning
Us tax law
Pay:$55 - $75/hour
https://jobs.micro1.ai/post/cc66baff-c6cd-4024-90e9-5a26263fe05a?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 4 days ago
Solutions Architect
micro1
1 Opening
Required skills
Microservices
Aws
Docker
+1
Pay:$30 - $150/hour
https://jobs.micro1.ai/post/11bcf004-157a-4578-a7a2-5d303a6262c5?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 4 days ago
Support Engineer
micro1
1 Opening
Required skills
Scripting
Cloud
Jira
+1
Pay:$30 - $90/hour
Refer and earn


https://jobs.micro1.ai/post/da2b476e-f083-4dc0-a240-fbced9680695?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 4 days ago
Sr Software Engineer
micro1
1 Opening
Required skills
Javascript
Java
Python
Pay:$30 - $130/hour
Refer and ea


https://jobs.micro1.ai/post/3c305526-0965-4a9b-b6b1-65fd0f916b0e?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 4 days ago
Mobile App Developer
micro1
1 Opening
Required skills
Ios development
Android development
Pay:$30 - $130/hour
Refer and earn$300

https://jobs.micro1.ai/post/e6983249-a9ba-4209-bc4a-4df51b92fbcc?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 4 days ago
AI/ML Engineer
micro1
1 Opening
Required skills
Machine learning
Python
Etl
Pay:$30 - $160/hour

https://jobs.micro1.ai/post/68a5150b-8310-4faf-b119-0647d364ca4a?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 5 days ago
Voice Actors Prompt Writter
micro1
150 Openings
Required skills
English
Writting skills
Pay:$15 - $35/hour
https://jobs.micro1.ai/post/81a4a612-e20a-4130-84a7-3dd30ab90f34?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 5 days ago
High demand
Salesforce User / Specialist
micro1
1 Opening
Required skills
Salesforce
Crm management
Salesforce navigation
+5
Pay:$30 - $60/hou
https://jobs.micro1.ai/post/7953bca4-eff4-4dd9-9b9d-6e500a7a7a07?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 5 days ago
High demand
SAP User / Specialist
micro1
15 Openings
Required skills
Sap erp
Sap modules (fi/co/mm/sd)
Sap navigation
+3
Pay:$30 - $60/hour

https://jobs.micro1.ai/post/964c89d1-d72f-4385-8b9b-e03b92e45815?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 5 days ago
High demand
Jira User / Specialist
micro1
1 Opening
Required skills
Jira
Issue tracking
Agile workflows
+5
Pay:$30 - $60/hour
https://jobs.micro1.ai/post/d3b664ed-0ea6-45a0-a1d8-00466c0f7e92?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral





Posted 5 days ago
High demand
Canva User/Specialist
micro1
15 Openings
Required skills
Canva
Digital asset management
Remote collaboration
+2
Pay:$20 - $70/hour
https://jobs.micro1.ai/post/2869b985-459c-42d8-aac4-09a46bf2d54c?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 5 days ago
High demand
Notion User/Specialist
micro1
12 Openings
Required skills
Notion
Digital documentation
Data annotation
+3
Pay:$20 - $70/hour

https://jobs.micro1.ai/post/62c44af7-07d8-4de7-9335-35601377bd12?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 5 days ago
Cantonese Bilingual Expert
micro1
1 Opening
Required skills
Cantonese
Language
Translation
+6
Pay:$25 - $50/hour


https://jobs.micro1.ai/post/165bc7f5-b188-449c-bee3-ed538fa98c28?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 5 days ago
High demand
Linear User/Specialist
micro1
15 Openings
Required skills
Linear (platform) expertise
Ai training support
Workflow analysis
+4
Pay:$20 - $70/hour


https://jobs.micro1.ai/post/e342eacf-e956-4eff-a959-ff5a301d2941?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral





Posted 5 days ago
High demand
Voice Actress (US or Canada Accent)
micro1
5 Openings
Required skills
Emotional range performance
Directed vocal tone execution
Professional voice recording
Pay:$20 - $50/hour
https://jobs.micro1.ai/post/843d78e1-11ea-4e02-b1b7-5925637f58b6?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 5 days ago
High demand
Slack User/ Specialist
micro1
15 Openings
Required skills
Slack administration
Slack workflow automation
Slack integrations
+2
Pay:$20 - $70/hour

https://jobs.micro1.ai/post/f3bd8c51-8603-4b36-9f74-12a09d1e24c2?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 5 days ago
Staff Ruby Engineer
micro1
50 Openings
Required skills
Expert ruby and rails
System design and architecture
Database design
+6
Pay:$20 - $80/hour

https://jobs.micro1.ai/post/54c19a8e-8179-4b76-8a42-189019b4ff7f?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 5 days ago
Senior Fullstack Engineer
micro1
50 Openings
Required skills
Advanced frontend
React
Performance
+15
Pay:$20 - $55/hour

https://jobs.micro1.ai/post/084536fe-a9a3-430b-a6fc-46aa2e07469e?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral





Posted 5 days ago
AWS Engineer
micro1
50 Openings
Required skills
Aws ec2
Aws s3
Iam
+9
Pay:$20 - $70/hour

https://jobs.micro1.ai/post/428b455c-4076-493b-8c7b-d8f0c5a20385?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 5 days ago
DevOps Engineer
micro1
50 Openings
Required skills

Linux
Network basics
Digital ocean
+15
Pay:
$20 - $70/hour




https://jobs.micro1.ai/post/feec8884-5d21-44c1-a677-c1d6b6669582?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 5 days ago
High demand
Pixel Artist (2D Game Art / Animation)
micro1
20 Openings
Required skills
Libresprite
Pixel art
Graphic design
+1
Pay:$20 - $70/hour


https://jobs.micro1.ai/post/c4218e45-188b-4bb9-81d1-f79b22da6de3?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 5 days ago
High demand
Insurance Specialist
micro1
50 Openings
Required skills
Risk assessment & underwriting insight
Regulatory knowledge & compliance
Client communication & advisory skills
+1
Pay:$20 - $40/hour

https://jobs.micro1.ai/post/1fd84407-47eb-4b02-92f2-7042f57987d0?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 5 days ago
High demand
Manufacturing Specialist
micro1
50 Openings
Required skills
Process optimization & lean manufacturing
Quality control & compliance
Technical & equipment expertise
+1
Pay:$20 - $40/hour
https://jobs.micro1.ai/post/e9822d5b-4ca7-46e2-9405-f23f35a87200?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 5 days ago
High demand
Construction Specialist
micro1
50 Openings
Required skills
Technical knowledge of construction methods
Project management & organization
Problem-solving & decision-making
+1
Pay:$20 - $45/hour

https://jobs.micro1.ai/post/954a6663-8856-42f3-9a5f-8723a5de8063?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 6 days ago
High demand
Nursing Specialist
micro1
1 Opening
Required skills
Nursing
Health
Patient care
Pay:$25 - $40/hour
https://jobs.micro1.ai/post/a3eef87f-0541-459d-998b-5ba7aedfa2ab?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 6 days ago
High demand
Education Specialist
micro1
1 Opening
Required skills
Instructional design
Learning sciences
Assessment design
+7
Pay:$20 - $40/hour


https://jobs.micro1.ai/post/fa52a9dd-d270-4dcf-9bca-2d9554d883aa?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 6 days ago
High demand
STEM Expert
micro1
100 Openings
Required skills

Stem subject-matter expertise
Curriculum development
Data analysis
+12
Pay:
$30 - $40/hour
https://jobs.micro1.ai/post/fa24cad5-ba08-4bfd-ab56-7529d1d20732?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 6 days ago
High demand
Legal Expert
micro1
100 Openings
Required skills
Legal
Pay:$30 - $40/hour
https://jobs.micro1.ai/post/7c7c8492-043b-43a7-aee9-c73dc71b2b39?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral





Posted 6 days ago
High demand
Finance Expert
micro1
100 Openings
Required skills
Financial modeling
Financial analysis
Forecasting
+17
Pay:$30 - $40/hour
https://jobs.micro1.ai/post/8de1a1c6-0b02-41ee-9e13-79d3773d9ae8?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 6 days ago
High demand
Healthcare Professional
micro1
100 Openings
Required skills
Clinical specialties & practice
Anatomy & physiology
Nutrition & dietetics
+7
Pay:$30 - $40/hour

https://jobs.micro1.ai/post/78ac8545-c3e1-4d1c-943d-38f297ab856e?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 6 days ago
High demand
Enterprise Client Partner (Frontier AI)
micro1
1 Opening
Required skills
Client acquisition
Outbound prospecting
Enterprise parnerships
+1
Pay:$220,000 - $400,000/year


https://jobs.micro1.ai/post/f9f4d1ad-4886-4a63-8edd-c409552dd08b?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 7 days ago
High demand
UX/UI Expert
micro1
Required skills
Wireframing
Prototyping
High-fidelity mockups
+5
Pay:$15 - $85/hour


https://jobs.micro1.ai/post/57fa8a01-f031-4657-8cbc-b6e73f3a834f?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 7 days ago
Video Editing Expert
micro1
Required skills
Adobe premiere pro
Final cut
Storytelling and narrative structure
+6
Pay:$15 - $40/hour

https://jobs.micro1.ai/post/2ca5dc9a-66a7-4e35-99ef-836c4a2b63bd?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 7 days ago
Design Expert (Multidisciplinary)
micro1
Required skills
Typography
Ux/ui fundamentals
Layout
+9
Pay:$15 - $40/hour

https://jobs.micro1.ai/post/5896caff-9101-4fca-9343-638d1530f8a5?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 7 days ago
Coding Expert (Multi-Language)
micro1
Required skills
Python
Javascript
Typescript
+8
Pay:$15 - $40/hour

https://jobs.micro1.ai/post/9637f811-ddba-4e2d-82d1-67dc147d5067?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 7 days ago
Legal Expert
micro1
Required skills
Legal research and analysis
Contract review and drafting
Knowledge of legal frameworks and regulations
+7
Pay:$15 - $40/hour
https://jobs.micro1.ai/post/853dcdc6-cc6f-4e48-b329-4a32bcb2780b?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 7 days ago
Finance Specialist
micro1
Required skills
Financial analysis and modeling
Accounting fundamentals (gaap/ifrs)
Budgeting and forecasting
+7
Pay:$15 - $40/hour
https://jobs.micro1.ai/post/87fde079-4613-44af-86bb-3181348ade17?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 7 days ago
High demand
Game Developer (Cocos2d-x)
micro1
10 Openings
Required skills
Cocos2d-x
Game development
Pay:$50 - $120/hour


https://jobs.micro1.ai/post/e39dfd2a-fd50-44cd-b592-0cf0c363485c?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 7 days ago
Chartered Accountant / Enrolled Agent
micro1
20 Openings
Required skills
Us tax law interpretation
Irs regulation analysis
Legal document review
+7
Pay:$15 - $30/hour

https://jobs.micro1.ai/post/848db0f3-9129-45a5-945f-39cdacb4efeb?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



osted 7 days ago
High demand
Junior Game Developer (Java / libGDX)
micro1
Required skills
Java
Libdxg
Pay:$20 - $120/hour

https://jobs.micro1.ai/post/03cd460b-81ae-46c1-9453-c92e57ee2c41?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 7 days ago
Accountant (CPA/CA)
micro1
Required skills
Us tax law interpretation
Irs regulation analysis
Legal document review
+7
Pay:$55 - $75/hour
https://jobs.micro1.ai/post/b8e24044-77f7-4bf6-acf1-a559e2f55030?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 7 days ago
High demand
Computational CAD Engineer (OpenSCAD)
micro1
Required skills
Openscad
Autocad
Syntax
+12
Pay:$40 - $120/hour

https://jobs.micro1.ai/post/2ad0f2e7-612e-4beb-b8c1-4980bef850c4?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 7 days ago
Infrastructure Engineer
micro1
Required skills
Aws
Azure
Google cloud platform
+19
Pay:$20 - $70/hour

https://jobs.micro1.ai/post/ef51aa26-2d87-4c53-984b-acd022841975?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 7 days ago
Backend Engineer
micro1
Required skills
Backend developement
Pay:$20 - $70/hour


https://jobs.micro1.ai/post/758ad28d-883e-44dc-8644-edb94c3f7aba?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 7 days ago
Frontend Engineer
micro1
Required skills
Javascript
Typescript
Pay:$20 - $70/hour

https://jobs.micro1.ai/post/ad6f918b-5d84-4ab0-8e35-d129411a46f9?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



osted 9 days ago
High demand
Software Engineer, New Grad (Zara)
micro1
1 Opening
Required skills
React
Node.js
Aws
+2
Pay:$180,000 - $250,000/year


https://jobs.micro1.ai/post/0b9d8e73-a9ab-4cfc-a270-ed9ee9dac1c5?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 4 days ago
C# Developer
micro1
10 Openings
Required skills
C#
Dotnet
.net
+5
Pay:$30 - $80/hour

https://jobs.micro1.ai/post/ab8b9ef4-7346-4a96-a2b9-2c88e0cc8ff9?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 4 days ago
SQL Developer
micro1
5 Openings
Required skills
Sql
Pay:$25 - $60/hour


https://jobs.micro1.ai/post/e8d2ca36-1b99-4ec0-b719-36cc5a4cfacf?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 4 days ago
RunOps Support – Platform and Infra
micro1
1 Opening
Required skills
Linux
Docker
Kubernetes
+4
Pay:$25 - $50/hour


https://jobs.micro1.ai/post/f90a03d4-c81d-4e84-9621-62c2f6523530?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 4 days ago
System Administrator
micro1
1 Opening
Required skills
Linux
Windows
Systems configuration
Pay:$25 - $50/hour

https://jobs.micro1.ai/post/82473406-fa09-4d42-a1b3-59d29f268639?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 4 days ago
Fullstack Developer
micro1
1 Opening
Required skills
React
Node.js
Javascript
+1


https://jobs.micro1.ai/post/5b7f7477-9ae0-414d-8594-e41ebd207414?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 10 days ago
High demand
Microsoft 365 Specialist
micro1
Required skills
Microsoft 365
Word
Excel
+23
Pay:$20 - $30/hour

https://jobs.micro1.ai/post/f205f5af-1be0-48b7-b83b-5b061cfddd6b?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 10 days ago
High demand
Library & Information Science Expert
micro1
Required skills
Information management
Metadata standards
Cataloging rules
+16
Pay:$20 - $50/hour

https://jobs.micro1.ai/post/d38d4be1-9e0b-4014-8427-851ab51311a9?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 10 days ago
High demand
History & Humanities Experts
micro1
Required skills
Historical research
Academic writing
Content development
+2

https://jobs.micro1.ai/post/6e1c340f-9015-4099-ad25-f9e7de1d2fbd?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 10 days ago
High demand
STEM Expert
micro1
Required skills
Stem subject-matter expertise
Curriculum development
Data analysis
+12


https://jobs.micro1.ai/post/3dc5e93b-eeba-4eb8-8152-313929761979?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 10 days ago
High demand
Journalist
micro1
Required skills
Research
Interviewing
Fact-checking
+13

https://jobs.micro1.ai/post/eb81315c-4729-4f9f-b40d-eef935decd49?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral





Posted 8 days ago
High demand
Site Reliability Engineer
micro1
Required skills
Terminal-native problem solving
Dynamic infrastructure recovery
Containerized environment mastery
+1
Pay:$40 - $70/hour

https://jobs.micro1.ai/post/4e25d4d3-e70c-45fe-8a2e-073e74a42f50?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 10 days ago
High demand
Systems & Infrastructure Specialist
micro1
Required skills
Terminal-native problem solving
Dynamic infrastructure recovery
Containerized environment mastery
+1
Pay:$40 - $70/hour

https://jobs.micro1.ai/post/0ccfa819-8bc0-489d-b52c-c2c9130c0a0d?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral





Posted 11 days ago
Personal Financial Advisor (Private Wealth)
micro1
Required skills
Financial planning
Investment management
Retirement planning
+7
Pay:$80 - $110/hour


https://jobs.micro1.ai/post/fbea9a18-b24e-4242-ae76-acb17b7b3247?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 11 days ago
High demand
Video Editor
micro1
Required skills
Cinelerra
Pay:$40 - $120/hour
https://jobs.micro1.ai/post/b931600a-958e-4ee7-9105-c259ef987729?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 11 days ago
Adobe Specialist (Illustrator)
micro1
Required skills
Adobe illustrator
Ai-powered design tools
Virtual training delivery
+7
Pay:$21 - $70/hour

https://jobs.micro1.ai/post/6a52ef74-2807-43ef-98f6-074f5c63b07c?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral





Posted 11 days ago
Adobe Specialist (After Effects)
micro1
Required skills
Adobe after effects
Motion graphics
Ai-powered animation workflows
+7
Pay:$21 - $70/hour
https://jobs.micro1.ai/post/0985805b-0228-4968-ad27-6c373d465d15?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 11 days ago
Adobe Specialist (Photoshop)
micro1
Required skills
Adobe photoshop
Photoshop ai features
Digital design
+12
Pay:$21 - $70/hour

https://jobs.micro1.ai/post/e88be4af-c23f-4a2e-b012-e2f438d7f310?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 11 days ago
Accounting Expert
micro1
Required skills
Akaunting
Cloud-based accounting platforms
Financial reporting
+24
Pay:$50 - $80/hour

https://jobs.micro1.ai/post/647bd931-39dc-4ea5-a20c-a559e7939909?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 11 days ago
Data Analytics Specialist
micro1
Required skills
Metabase
Sql
Data modeling
+17
Pay:$50 - $80/hour


https://jobs.micro1.ai/post/71adebb6-9700-4035-8e2c-3331043c3386?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 12 days ago
High demand
Motion Graphics Designer
micro1
Required skills
Adobe after effects
Adobe premiere pro
Adobe photoshop
+12
Pay:$15 - $65/hour


https://jobs.micro1.ai/post/e22e6e0d-be70-4b2f-91d1-4e55aa67ef6d?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 12 days ago
High demand
Film Editor
micro1
Required skills
Adobe premiere pro
Final cut pro
Davinci resolve
+7
Pay:$15 - $65/hour

https://jobs.micro1.ai/post/61719fab-180b-4cea-a518-e2ae4076993c?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




osted 12 days ago
Odia Audio transcription Expert
micro1
Required skills
Audio transcription
Multilingual communication
Ai transcription tools
+8
Pay:$10 - $20/hour

https://jobs.micro1.ai/post/daaa63fc-0aff-428f-887d-03e342ce132f?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 12 days ago
Malayalam Audio transcription Expert
micro1
Required skills
Audio transcription
Multilingual communication
Ai transcription tools
+8
Pay:$10 - $20/hour
https://jobs.micro1.ai/post/a742208a-eb52-4198-a9d7-ac3279f8017c?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Kannada Audio transcription Expert
micro1
Required skills
Audio transcription
Multilingual communication
Ai transcription tools
+8
Pay:$10 - $20/hour

https://jobs.micro1.ai/post/4a0ad37c-cb28-4cac-8721-52fe7450bc65?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Swiss German Audio transcription Expert
micro1
Required skills
Audio transcription
Multilingual communication
Ai transcription tools
+7
Pay:$10 - $20/hour
https://jobs.micro1.ai/post/3d6130a7-2c50-4e5b-9da8-31688f67d9e4?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 12 days ago
Thai Audio transcription Expert
micro1
Required skills
Audio transcription
Multilingual communication
Ai transcription tools
+8
Pay:$10 - $20/hour

https://jobs.micro1.ai/post/9232ac5f-14ad-4d3d-92bf-7f6792dcfd3d?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 12 days ago
Odia Audio Recording Expert
micro1
Required skills
Audio recording
Audio editing software
Voice-over
+12
Pay:$10 - $30/hour

https://jobs.micro1.ai/post/b0d96058-9b69-440c-a10e-e5578a2f2bf6?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 12 days ago
Malayalam Audio Recording Expert
micro1
Required skills
Audio recording
Audio editing software
Voice-over
+12
Pay:$10 - $30/hour

https://jobs.micro1.ai/post/ca488abe-20d5-487e-a8ff-93d12dc11ca1?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 12 days ago
Kannada Audio Recording Expert
micro1
Required skills
Audio recording
Audio editing software
Voice-over
+13
Pay:$10 - $30/hour

https://jobs.micro1.ai/post/5d9f885e-4874-4567-8864-e6955729ecea?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 12 days ago
Swiss German Audio Recording Expert
micro1
Required skills
Audio recording
Audio editing software
Voice-over
+13
Pay:$10 - $30/hour

https://jobs.micro1.ai/post/10006ece-8b91-41b4-9b4c-1aba81ce94d6?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



osted 12 days ago
Thai Audio Recording Expert
micro1
Required skills
Audio recording
Audio editing software
Voice-over
+13
Pay:$10 - $30/hour

https://jobs.micro1.ai/post/568a042a-bbb1-42fa-91f4-d10233475361?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 13 days ago
High demand
General Counsel
micro1
Required skills
Saas contract review
In-house legal experience
Contract negotiation
+4
Pay:$80 - $105/hour


https://jobs.micro1.ai/post/9fc71647-1e35-4e94-998e-2bbc932de7d4?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral





Posted 13 days ago
High demand
Contracting Attorney
micro1
Required skills
Adaptability
Saas contract review
Attention to detail
+5
Pay:$80 - $105/hour

https://jobs.micro1.ai/post/774e3d9a-3a60-459a-ba82-bca84da2ebf1?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 13 days ago
High demand
Philosophy Expert
micro1
Required skills
Philosophy expertise
Content annotation
Digital research
+7
Pay:$30 - $75/hour
https://jobs.micro1.ai/post/d98303bc-d830-4817-aac4-dd104df230a6?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 13 days ago
Customer Success Analyst
micro1
Required skills
Customer success management
Ai training task design
Zendesk
+15
Pay:$6 - $110/hour

https://jobs.micro1.ai/post/f070f113-5893-4fc7-ae21-e2fd02a181e1?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 7 days ago
Senior Frontend Engineer (Tailwind)
micro1
Required skills
React
Javascript
Tailwind css
Pay:$20 - $45/hour


https://jobs.micro1.ai/post/43ace019-9e3f-4b3a-b352-6adc79b220b3?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 7 days ago
Senior Full-Stack Software Engineer
micro1
Required skills
React
Javascript
Node/python
Pay:$20 - $55/hour

https://jobs.micro1.ai/post/9e874fc6-9948-43d4-893c-8cd4b0333ec7?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 7 days ago
iOS Developer
micro1
Required skills
Swift programming
Uikit
Swiftui
+2
Pay:$20 - $60/hour

https://jobs.micro1.ai/post/7edb8f28-4321-45ed-894a-c53219915b64?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 7 days ago
AI Engineer
micro1
Required skills
Machine learning
Ci/cd
Aws
+1
Pay:$20 - $90/hour


https://jobs.micro1.ai/post/3a23884d-a7f4-4e1b-b700-8aa7d4887dec?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 7 days ago
Frontend Developer (React)
micro1
Required skills
React
Javascript
Pay:$20 - $45/hour
https://jobs.micro1.ai/post/8a408adb-00de-4d39-b454-d3733bb574bf?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 13 days ago
Product Manager
micro1
Required skills
Jira
Linear
Agile
+13
Pay:$40 - $80/hour


https://jobs.micro1.ai/post/e9426d8a-a489-4286-8602-ca7e4b3ca6c4?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 13 days ago
Project and Operations Specialist
micro1
Required skills
Asana
Monday
Basecamp
Pay:$50 - $80/hour

https://jobs.micro1.ai/post/023dcc3e-276e-460d-810d-b4b9b8993d39?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 13 days ago
High demand
Data-Video Generalist
micro1
50 Openings
Required skills
Mobile app usage for data collection
Imu sensor data capture
Video recording
+8
Pay:$13 - $13/hour

https://jobs.micro1.ai/post/204600bf-1abe-4ab0-a474-cd2264999149?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 14 days ago
Cell/Molecular Biologist (Stem Cells)
micro1
Required skills
Stem cells
Celular biology
Biology
+1
Pay:$40 - $60/hour

https://jobs.micro1.ai/post/e3b68007-1e14-444e-bead-f2fadab0659f?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

osted 14 days ago
Chemical Biologist
micro1
Required skills
Chemistry
Biology
Synthetic compounds
+2
Pay:$40 - $60/hour



https://jobs.micro1.ai/post/8153f8fa-2e8a-48dc-8ea2-260c36807616?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 14 days ago
Plant Biologist
micro1
Required skills
Biology
Genetics
Plants
+3
Pay:$40 - $60/hour

https://jobs.micro1.ai/post/d5a65f29-dde6-445d-b7de-ceb151c8bd3b?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 14 days ago
Protein Biochemist
micro1
Required skills
Biology
Chemistry
Protein
+1
Pay:$40 - $60/hour



https://jobs.micro1.ai/post/28205810-079b-4413-84c4-1a08afcee1e4?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 14 days ago
Microbiologist
micro1
Required skills
Biology
Microbiology
Chemistry
+2
Pay:$40 - $60/hour


https://jobs.micro1.ai/post/7b01b7b6-db31-4eb6-a877-65cfdc6bcbca?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 15 days ago
High demand
Saas Contracting Attorney - AI Fellowship
micro1
Required skills
Saas contract review
Contract negotiation
Contract redlining
+12
Pay:$80 - $105/hour

https://jobs.micro1.ai/post/d9165951-e169-49b1-b90a-e07ff4adbfaf?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 5 days ago
High demand
Crowd Workers — Bilingual
micro1
Required skills
Native accent authenticity
Structured prompt recording
Self-directed audio capture
+1
Pay:$20 - $50/hour


https://jobs.micro1.ai/post/e759a707-d3f1-4993-bd07-62c80ef71a3d?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted YesterdayNew
Field Recorders
micro1
Required skills
Multi-environment audio capture
Ambient noise documentation
Mobile recording technique
+1
Pay:$30 - $50/hour
https://jobs.micro1.ai/post/01c47bb8-a687-4070-8f6e-2d316cc41540?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted YesterdayNew
Crowd Workers — Accents/Dialects
micro1
Required skills
Native accent authenticity
Structured prompt recording
Self-directed audio capture
+1
Pay:$20 - $50/hour



https://jobs.micro1.ai/post/e789836d-7adc-4a05-b844-c7d324447791?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 5 days ago
High demand
Voice Actors
micro1
5 Openings
Required skills
Emotional range performance
Directed vocal tone execution
Professional voice recording
Pay:$20 - $50/hour


https://jobs.micro1.ai/post/5ed5ec04-bc4d-444d-a003-e2e9a690f9f9?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted YesterdayNew
Studio Speakers
micro1
Required skills
Scripted read-aloud delivery
Consistent audio recording quality
Neutral/clear english articulation
+1
Pay:$30 - $50/hour

https://jobs.micro1.ai/post/64206597-45f9-49f5-973f-f8ed1ef1a567?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 17 days ago
Document Sourcing Specialist
micro1
Required skills
Attention to detail
Compliance review
Data collection
+4
Pay:$20 - $66/hour

https://jobs.micro1.ai/post/1ba4f212-c171-4f52-a616-5bc8ba7e2482?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 17 days ago
High demand
Python Game Developer (Panda3D)
micro1
Required skills
Github
Python
C++
+1
Pay:$50 - $120/hour



https://jobs.micro1.ai/post/922b0ffc-82ee-47ba-b3c0-a4ea377c443a?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 4 days ago
QA Automation Engineer
micro1
1 Opening
Required skills
Selenium
Postman
Cypress
+1
Pay:$30 - $80/hour

https://jobs.micro1.ai/post/5f53542e-5b28-49a5-8597-a386dd44b334?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 4 days ago
Data Engineer
micro1
1 Opening
Required skills
Mysql
Python
Etl
+1
Pay:$30 - $100/hour

https://jobs.micro1.ai/post/e756352a-0657-45db-82b7-17ef7fea4d73?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 4 days ago
Penetration Tester
micro1
7 Openings
Required skills
Ethical hacking
Vulnerability assessment
Penetration testing
Pay:$30 - $90/hour


https://jobs.micro1.ai/post/c2bce764-8a53-4f6c-bfec-7a595e70c2a5?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 4 days ago
Machine Vision Engineer
micro1
1 Opening
Required skills
Computer vision
Opencv
Image processing
Pay:$30 - $90/hour


https://jobs.micro1.ai/post/b0d06045-e8bb-41ce-b253-839bb0b3b4e2?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 4 days ago
C Developer
micro1
1 Opening
Required skills
C
Pay:$30 - $80/hour

https://jobs.micro1.ai/post/e69e976e-c872-437a-9dd0-40e6ec570c2e?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 4 days ago
Backend C#/.NET Developer
micro1
1 Opening
Required skills
C#
.net
Mysql
Pay:$30 - $80/hour

https://jobs.micro1.ai/post/f55c5e8b-d0e2-427c-b84f-7642e66e263f?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 7 days ago
Full-Stack Engineer (Frontend-focused)
micro1
10 Openings
Required skills
React
Node.js
Html
+1
Pay:$30 - $90/hour


https://jobs.micro1.ai/post/98f7c8d2-f8b9-4a38-8bee-2d92a47d4524?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 7 days ago
Web Scraper
micro1
Required skills
Python
Scrapy
Selenium
+11
Pay:$30 - $80/hour


https://jobs.micro1.ai/post/a06b3049-bb10-4acb-baca-da48b1baf875?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral

Posted 7 days ago
Frontend Engineer (Angular)
micro1
Required skills
React
Angular
Html
+1


https://jobs.micro1.ai/post/88d55352-9063-4dcd-a397-3b9ad15ddcb3?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 7 days ago
UI Engineer
micro1
Required skills
React
Typescript
Html
+1
Pay:$30 - $70/hour

https://jobs.micro1.ai/post/115f7512-cd4b-49b0-a5aa-0eeba0c7a735?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted 7 days ago
Cyber Security Analyst
micro1
6 Openings
Required skills
Threat detection
Network security
Penetration testing
Pay:$25 - $60/hour

https://jobs.micro1.ai/post/25d21ab1-f5e9-4a37-835b-c913684cad55?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral


Posted 9 days ago
Frontend Developer (Vue.js)
micro1
1 Opening
Required skills
Javascript
React
Vue.js
Pay:$30 - $70/hour




https://jobs.micro1.ai/post/ef7848b0-a465-4731-894c-678f754f05d8?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral




Posted YesterdayNew
AI Content Evaluation Specialist
micro1
Required skills
Content moderation or safety evaluation
Social media literacy
Image and text analysis
+1
Pay:$25 - $35/hour


https://jobs.micro1.ai/post/6d0d5814-b2f1-42db-b6fa-2ef3f7599f39?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 17 days ago
Video Evaluator (AI Content)
micro1
Required skills
Video evaluation
Quality assurance
Content review
+1
Pay:$25 - $34/hour


https://jobs.micro1.ai/post/eff4d05b-dada-4ebd-94b9-6038212acb59?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral



Posted 18 days ago
DevOps Engineer - US
micro1
Required skills

Devops
Aws
Kubernetes
+1
Pay:
$200,000 - $300,000/year


https://jobs.micro1.ai/post/247a16f0-430f-4c0c-a98e-a152b7c08447?referralCode=56cb07bd-d24b-4f8f-aea9-d037f43f01cf&utm_source=referral&utm_medium=share&utm_campaign=job_referral
"""
    
    # Simple parser
    blocks = raw_data.split('https://jobs.micro1.ai')
    
    db = SessionLocal()
    count = 0
    
    for i, block in enumerate(blocks):
        if i == 0:
            continue
        
        url = "https://jobs.micro1.ai" + block.split('\n')[0].strip()
        # Clean the previous block to extract job info
        prev_block = blocks[i-1].strip()
        lines = [line.strip() for line in prev_block.split('\n') if line.strip()]
        
        if not lines:
            continue
            
        # Parse fields from the bottom up since the top might have random stuff
        pay = "Competitive"
        title = "Unknown Job"
        skills = []
        openings = 10
        posted_at = "Recently"
        is_new = False
        is_high_demand = False
        bonus = 500
        
        for idx, line in enumerate(lines):
            line_lower = line.lower()
            if line_lower.startswith('pay:'):
                pay = line.replace('Pay:', '').strip()
            if 'openings' in line_lower or 'opening' in line_lower:
                try:
                    openings = int(line_lower.split(' ')[0])
                except:
                    pass
            if line.strip() == 'micro1':
                if idx >= 1:
                    title = lines[idx-1]
            if 'posted' in line_lower:
                posted_at = line.split('New')[0] if 'New' in line else line
                is_new = 'New' in line
            if 'high demand' in line_lower:
                is_high_demand = True
            if 'refer and earn' in line_lower:
                try:
                    bonus_str = line_lower.split('$')[1]
                    bonus = int(bonus_str.replace(',', ''))
                except:
                    pass
        
        # Extract skills (they are between "Required skills" and "+X" or "Pay:")
        try:
            skill_start = lines.index("Required skills") + 1
            skill_end = len(lines)
            for j in range(skill_start, len(lines)):
                if lines[j].startswith('+') or lines[j].lower().startswith('pay:'):
                    skill_end = j
                    break
            skills = lines[skill_start:skill_end]
        except ValueError:
            skills = ["Remote Work", "Communication"]
            
        if not skills:
            skills = ["Remote Work"]

        job = {
            "id": count + 1,
            "title": title,
            "company": "micro1",
            "location": "Remote",
            "type": "Contract",
            "salary": pay,
            "posted_at": posted_at,
            "logo": "https://media.licdn.com/dms/image/C4D0BAQG7X7X7X7X7X7/company-logo_200_200/0/1630123456789", 
            "tags": skills[:3],
            "description": f"Join the micro1 network as a {title}. Work with elite global teams on cutting-edge projects.",
            "benefits": ["Remote", "Global Impact", "Flexible"],
            "referral_bonus": bonus,
            "openings_count": openings,
            "is_new": is_new,
            "is_high_demand": is_high_demand,
            "apply_url": url.split()[0]  # Take only the URL, ignore anything after
        }
        db_job = models.Job(**job)
        db.add(db_job)
        count += 1
        
    db.commit()
    print(f"Restored {count} VIP jobs from the user's payload.")
    db.close()

if __name__ == "__main__":
    parse_and_seed()
