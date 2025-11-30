#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create some sample data for testing
    company1 = Company(name="TechCorp", founding_year=2000)
    company2 = Company(name="InnovateInc", founding_year=2010)

    dev1 = Dev(name="Alice")
    dev2 = Dev(name="Bob")

    session.add_all([company1, company2, dev1, dev2])
    session.commit()

    # Create freebies to test relationships
    freebie1 = Freebie(item_name="T-shirt", value=20, dev=dev1, company=company1)
    freebie2 = Freebie(item_name="Sticker", value=5, dev=dev1, company=company2)
    freebie3 = Freebie(item_name="Mug", value=15, dev=dev2, company=company1)

    session.add_all([freebie1, freebie2, freebie3])
    session.commit()

    print("Sample data created successfully!")
