import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

fake = Faker("en_US")
Faker.seed(SEED)

NUM_ROWS = 8950
OUTPUT_CSV = "HumanResources.csv"

# States and cities (HQ is New York City)
STATE_TO_CITIES = {
    "New York": ["New York City", "Buffalo", "Rochester"],
    "Virginia": ["Virginia Beach", "Norfolk", "Richmond"],
    "Florida": ["Miami", "Orlando", "Tampa"],
    "Illinois": ["Chicago", "Aurora", "Naperville"],
    "Pennsylvania": ["Philadelphia", "Pittsburgh", "Allentown"],
    "Ohio": ["Columbus", "Cleveland", "Cincinnati"],
    "North Carolina": ["Charlotte", "Raleigh", "Greensboro"],
    "Michigan": ["Detroit", "Grand Rapids", "Warren"],
}
STATES = list(STATE_TO_CITIES.keys())
STATE_WEIGHTS = [0.7, 0.02, 0.01, 0.03, 0.05, 0.03, 0.05, 0.11]

DEPARTMENTS = [
    "HR",
    "IT",
    "Sales",
    "Marketing",
    "Finance",
    "Operations",
    "Customer Service",
]
DEPT_WEIGHTS = [0.02, 0.15, 0.21, 0.08, 0.05, 0.30, 0.19]

DEPT_TO_TITLES = {
    "HR": ["HR Manager", "HR Coordinator", "Recruiter", "HR Assistant"],
    "IT": ["IT Manager", "Software Developer", "System Administrator", "IT Support Specialist"],
    "Sales": ["Sales Manager", "Sales Consultant", "Sales Specialist", "Sales Representative"],
    "Marketing": ["Marketing Manager", "SEO Specialist", "Content Creator", "Marketing Coordinator"],
    "Finance": ["Finance Manager", "Accountant", "Financial Analyst", "Accounts Payable Specialist"],
    "Operations": ["Operations Manager", "Operations Analyst", "Logistics Coordinator", "Inventory Specialist"],
    "Customer Service": ["Customer Service Manager", "Customer Service Representative", "Support Specialist", "Help Desk Technician"],
}
TITLE_MIX = {
    "HR": [0.03, 0.30, 0.47, 0.20],
    "IT": [0.02, 0.47, 0.20, 0.31],
    "Sales": [0.03, 0.25, 0.32, 0.40],
    "Marketing": [0.04, 0.25, 0.41, 0.30],
    "Finance": [0.03, 0.37, 0.40, 0.20],
    "Operations": [0.02, 0.20, 0.40, 0.38],
    "Customer Service": [0.04, 0.30, 0.38, 0.28],
}

EDUCATION_LEVELS = ["High School", "Bachelor", "Master", "PhD"]

# Title -> possible education levels
TITLE_TO_EDU = {
    "HR Manager": ["Master", "PhD"],
    "HR Coordinator": ["Bachelor", "Master"],
    "Recruiter": ["High School", "Bachelor"],
    "HR Assistant": ["High School", "Bachelor"],
    "IT Manager": ["PhD", "Master"],
    "Software Developer": ["Bachelor", "Master"],
    "System Administrator": ["Bachelor", "Master"],
    "IT Support Specialist": ["High School", "Bachelor"],
    "Sales Manager": ["Master", "PhD"],
    "Sales Consultant": ["Bachelor", "Master", "PhD"],
    "Sales Specialist": ["Bachelor", "Master", "PhD"],
    "Sales Representative": ["Bachelor"],
    "Marketing Manager": ["Bachelor", "Master", "PhD"],
    "SEO Specialist": ["High School", "Bachelor"],
    "Content Creator": ["High School", "Bachelor"],
    "Marketing Coordinator": ["Bachelor"],
    "Finance Manager": ["Master", "PhD"],
    "Accountant": ["Bachelor"],
    "Financial Analyst": ["Bachelor", "Master", "PhD"],
    "Accounts Payable Specialist": ["Bachelor"],
    "Operations Manager": ["Bachelor", "Master"],
    "Operations Analyst": ["Bachelor", "Master"],
    "Logistics Coordinator": ["Bachelor"],
    "Inventory Specialist": ["High School", "Bachelor"],
    "Customer Service Manager": ["Bachelor", "Master", "PhD"],
    "Customer Service Representative": ["High School", "Bachelor"],
    "Support Specialist": ["High School", "Bachelor"],
    "Customer Success Manager": ["Bachelor", "Master", "PhD"],  # not used by title mix, kept for completeness
    "Help Desk Technician": ["High School", "Bachelor"],
}

# Hire year weights (relative, not percentages)
HIRE_YEAR_WEIGHTS = {
    2015: 5,
    2016: 8,
    2017: 17,
    2018: 9,
    2019: 10,
    2020: 11,
    2021: 5,
    2022: 12,
    2023: 14,
    2024: 9,
}

# Termination distribution (relative, not percentages)
TERM_YEAR_WEIGHTS = {
    2015: 5,
    2016: 7,
    2017: 10,
    2018: 12,
    2019: 9,
    2020: 10,
    2021: 20,
    2022: 10,
    2023: 7,
    2024: 10,
}
TERMINATION_RATE = 0.112  # 11.2%

# Salary bands by department/title (inclusive ranges)
SALARY_BANDS = {
    "HR": {
        "HR Manager": (60000, 90000),
        "HR Coordinator": (50000, 60000),
        "Recruiter": (50000, 70000),
        "HR Assistant": (50000, 60000),
    },
    "IT": {
        "IT Manager": (80000, 120000),
        "Software Developer": (70000, 95000),
        "System Administrator": (60000, 90000),
        "IT Support Specialist": (50000, 60000),
    },
    "Sales": {
        "Sales Manager": (70000, 110000),
        "Sales Consultant": (60000, 90000),
        "Sales Specialist": (50000, 80000),
        "Sales Representative": (50000, 70000),
    },
    "Marketing": {
        "Marketing Manager": (70000, 100000),
        "SEO Specialist": (50000, 80000),
        "Content Creator": (50000, 60000),
        "Marketing Coordinator": (50000, 70000),
    },
    "Finance": {
        "Finance Manager": (80000, 120000),
        "Accountant": (50000, 80000),
        "Financial Analyst": (60000, 90000),
        "Accounts Payable Specialist": (50000, 60000),
    },
    "Operations": {
        "Operations Manager": (70000, 100000),
        "Operations Analyst": (50000, 80000),
        "Logistics Coordinator": (50000, 60000),
        "Inventory Specialist": (50000, 60000),
    },
    "Customer Service": {
        "Customer Service Manager": (60000, 90000),
        "Customer Service Representative": (50000, 60000),
        "Support Specialist": (50000, 60000),
        "Help Desk Technician": (50000, 80000),
    },
}

# Education x Gender salary multipliers
EDU_GENDER_MULT = {
    "High School": {"Male": 1.03, "Female": 1.00},
    "Bachelor": {"Male": 1.115, "Female": 1.00},
    "Master": {"Male": 1.00, "Female": 1.07},
    "PhD": {"Male": 1.00, "Female": 1.17},
}

def draw_weighted_year(weight_map: dict) -> int:
    """Return a year sampled by relative weights."""
    years = list(weight_map.keys())
    weights = list(weight_map.values())
    return random.choices(years, weights=weights, k=1)[0]

def random_date_in_year(year: int) -> datetime:
    """Uniformly pick a datetime within the given year (bounded to 28-day months for simplicity)."""
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return fake.date_time_between(
        start_date=datetime(year, 1, 1),
        end_date=datetime(year, 12, 31)
    ).replace(hour=0, minute=0, second=0, microsecond=0)

def pick_title(dept: str) -> str:
    return np.random.choice(DEPT_TO_TITLES[dept], p=TITLE_MIX[dept])

def base_salary_for(dept: str, title: str) -> int:
    low, high = SALARY_BANDS[dept][title]
    # randint is end-inclusive; match original behavior via numpy
    return int(np.random.randint(low, high))

def pick_state_city() -> tuple[str, str]:
    state = np.random.choice(STATES, p=STATE_WEIGHTS)
    city = np.random.choice(STATE_TO_CITIES[state])
    return state, city

def pick_education(title: str) -> str:
    return np.random.choice(TITLE_TO_EDU[title])

def age_from_birthdate(born: datetime.date) -> int:
    today = pd.Timestamp("today").date()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def synthesize_birthdate(job_title: str, edu: str) -> datetime.date:
    """
    Draw a birthdate given job seniority hints and broad age buckets:
      under_25: 11%, 25-34: 25%, 35-44: 31%, 45-54: 24%, 55+: 9%
    Managers skew older; PhD can skew older as well.
    """
    age_mix = {
        "under_25": 0.11,
        "25_34": 0.25,
        "35_44": 0.31,
        "45_54": 0.24,
        "55_plus": 0.09,
    }
    bucket = np.random.choice(list(age_mix.keys()), p=list(age_mix.values()))

    if "Manager" in job_title:
        age = random.randint(30, 65)
    elif edu == "PhD":
        age = random.randint(27, 65)
    elif bucket == "under_25":
        age = random.randint(20, 24)
    elif bucket == "25_34":
        age = random.randint(25, 34)
    elif bucket == "35_44":
        age = random.randint(35, 44)
    elif bucket == "45_54":
        age = random.randint(45, 54)
    else:
        age = random.randint(56, 65)

    # Faker can generate a date for a given exact age by constraining min/max the same.
    return fake.date_of_birth(minimum_age=age, maximum_age=age)

def adjust_salary(base: int, gender: str, edu: str, birthdate: datetime.date) -> int:
    """
    Apply education+gender multiplier and age-based increment (0.1%–0.3% per year of age).
    Keep adjusted salary >= base, round to int.
    """
    multiplier = EDU_GENDER_MULT.get(edu, {}).get(gender, 1.0)
    adjusted = base * multiplier

    age = age_from_birthdate(birthdate)
    annual_increase = np.random.uniform(0.001, 0.003)  # 0.1%–0.3%
    adjusted *= (1 + annual_increase * age)

    return int(round(max(adjusted, base)))

def make_employee_row() -> list:
    emp_id = f"00-{random.randint(10000000, 99999999)}"
    first = fake.first_name()
    last = fake.last_name()
    gender = np.random.choice(["Female", "Male"], p=[0.46, 0.54])

    state, city = pick_state_city()

    hired_year = draw_weighted_year(HIRE_YEAR_WEIGHTS)
    hire_dt = random_date_in_year(hired_year)

    dept = np.random.choice(DEPARTMENTS, p=DEPT_WEIGHTS)
    title = pick_title(dept)

    edu = pick_education(title)

    perf = np.random.choice(["Excellent", "Good", "Satisfactory", "Needs Improvement"],
                            p=[0.12, 0.50, 0.30, 0.08])

    overtime = np.random.choice(["Yes", "No"], p=[0.30, 0.70])

    base_pay = base_salary_for(dept, title)

    birth_dt = synthesize_birthdate(title, edu)

    # compute adjusted salary and set as final "salary" (schema compatibility)
    final_salary = adjust_salary(base_pay, gender, edu, birth_dt)

    return [
        emp_id,
        first,
        last,
        gender,
        state,
        city,
        hire_dt,
        dept,
        title,
        edu,
        final_salary,
        perf,
        overtime,
        birth_dt,
        None,  # placeholder for termdate; filled later
    ]

rows = [make_employee_row() for _ in range(NUM_ROWS)]

columns = [
    "employee_id",
    "first_name",
    "last_name",
    "gender",
    "state",
    "city",
    "hiredate",
    "department",
    "job_title",
    "education_level",
    "salary",
    "performance_rating",
    "overtime",
    "birthdate",
    "termdate",
]

df = pd.DataFrame(rows, columns=columns)

# Ensure date types are proper
df["hiredate"] = pd.to_datetime(df["hiredate"]).dt.date
df["birthdate"] = pd.to_datetime(df["birthdate"]).dt.date

num_terminated = int(NUM_ROWS * TERMINATION_RATE)
terminated_idxs = np.random.choice(df.index, size=num_terminated, replace=False)

# Build a pool of termination years proportionally
term_years = []
total_weight = sum(TERM_YEAR_WEIGHTS.values())
for year, w in TERM_YEAR_WEIGHTS.items():
    k = int(round(num_terminated * (w / total_weight)))
    term_years.extend([year] * k)

# Align list length to num_terminated (in case of rounding issues)
while len(term_years) < num_terminated:
    term_years.append(random.choice(list(TERM_YEAR_WEIGHTS.keys())))
if len(term_years) > num_terminated:
    term_years = term_years[:num_terminated]

random.shuffle(term_years)

# Assign termination dates & enforce ≥ 180 days after hire
for idx, year in zip(terminated_idxs, term_years):
    proposed = random_date_in_year(year).date()
    min_allowed = df.at[idx, "hiredate"] + timedelta(days=180)
    if proposed < min_allowed:
        proposed = min_allowed
    df.at[idx, "termdate"] = proposed

df["termdate"] = pd.to_datetime(df["termdate"]).dt.date

print(df.head(3))
df.to_csv(OUTPUT_CSV, index=False)
