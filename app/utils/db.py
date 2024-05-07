from datetime import datetime

#### TABLES
user = [
    {
    'id':1,
    'name':'user 1',
    'email':'user1@lambdatest.com',
    'active':True,
    'hashed_password': "1hfskdf3i9@ksdfb@@&ahsd#a2"
    }
]

licenses = [
    {
        'id':1,
        'user_id':1,
        'parallel_jobs_license':2,
        'puchase_date':'2023-10-01',
        'expiry':'2023-10-01',
        'active':True
    }
]

jobs = [
    {'id':1,
    'name':'test app',
    'status':None,
    # standard columns -
    'created':datetime.now(),
    'updated':datetime.now(),
    'active':True,
    'created_by': 'user1@lamdatest.com',
    'updated_by': 'user1@lamdatest.com',
    }
]

#job_id is the foreign key
tasks = [
    {'id':1,
    'job_id':1,
    'name':'job 1',
    'metadata':{'execute_on_platform':'MacOS','tests':{1: ['Run the App','Press execute button','Close the app'], 2: ['Run the App','Open Camera on the app','Take a picture','Open Gallery','Close the']}},
    'status':None,
    # standard columns -
    'created':datetime.now(),
    'updated':datetime.now(),
    'active':True,
    'created_by': 'user1@lamdatest.com',
    'updated_by': 'user1@lamdatest.com',
    },
    {'id':2,
    'job_id':1,
    'name':'job 1',
    'metadata':{'execute_on_platform':'MacOS','tests':{1: ['Run the App','Press execute button','Close the app'], 2: ['Run the App','Open Camera on the app','Take a picture','Open Gallery','Close the']}},
    'status':None,
    # standard columns -
    'created':datetime.now(),
    'updated':datetime.now(),
    'active':True,
    'created_by': 'user1@lamdatest.com',
    'updated_by': 'user1@lamdatest.com',
    },
    {'id':3,
    'job_id':1,
    'name':'job 1',
    'metadata':{'execute_on_platform':'MacOS','tests':{1: ['Run the App','Press execute button','Close the app'], 2: ['Run the App','Open Camera on the app','Take a picture','Open Gallery','Close the']}},
    'status':None,
    # standard columns -
    'created':datetime.now(),
    'updated':datetime.now(),
    'active':True,
    'created_by': 'user1@lamdatest.com',
    'updated_by': 'user1@lamdatest.com',
    },
    {'id':4,
    'job_id':1,
    'name':'job 1',
    'metadata':{'execute_on_platform':'MacOS','tests':{1: ['Run the App','Press execute button','Close the app'], 2: ['Run the App','Open Camera on the app','Take a picture','Open Gallery','Close the']}},
    'name':'job 1',
    # standard columns -
    'created':datetime.now(),
    'updated':datetime.now(),
    'active':True,
    'created_by': 'user1@lamdatest.com',
    'updated_by': 'user1@lamdatest.com',
    }
]
