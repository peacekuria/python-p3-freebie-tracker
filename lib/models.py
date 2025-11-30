from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    # Relationships: Freebie belongs to Dev and Company
    dev = relationship('Dev', backref=backref('freebies', lazy=True))
    company = relationship('Company', backref=backref('freebies', lazy=True))

    def __repr__(self):
        return f'<Freebie {self.item_name}>'

    def print_details(self):
        # Returns formatted string: "{dev name} owns a {freebie item_name} from {company name}"
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    def __repr__(self):
        return f'<Company {self.name}>'

    @property
    def devs(self):
        return list(set([freebie.dev for freebie in self.freebies]))

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        return freebie

    @classmethod
    def oldest_company(cls):
        return cls.query.order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    def __repr__(self):
        return f'<Dev {self.name}>'

    # freebies property is handled by backref

    @property
    def companies(self):
        # Returns collection of all companies that the dev has collected freebies from
        return list(set([freebie.company for freebie in self.freebies]))

    def received_one(self, item_name):
        # Returns True if any of the freebies associated with the dev has that item_name
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        # Changes the freebie's dev to the given dev; only if the freebie belongs to this dev
        if freebie.dev == self:
            freebie.dev = dev
        return freebie
