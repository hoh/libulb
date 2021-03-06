import re


class Slug:

    def __init__(self, domain, faculty, number):
        self.domain = domain.strip().lower()
        if len(self.domain) > 4:
            raise ValueError("domain may not be longer than 4 chars")
        if not self.domain.isalpha():
            raise ValueError("domain may contain only alphabetic chars")

        self.faculty = faculty.strip().lower()
        if len(self.faculty) != 1:
            raise ValueError("faculty must be only one char long")
        if not self.faculty.isalpha():
            raise ValueError("faculty may contain only alphabetic chars")

        self.number = number.strip().lower()
        if len(self.number) > 4 or len(self.number) < 2:
            raise ValueError("number lenght must be 2, 3 or 4 chars only")
        if not self.number.isdigit():
            raise ValueError("number may contain only digits")

    @property
    def gehol(self):
        return "{}{}{}".format(self.domain, self.faculty, self.number).upper()

    @property
    def catalog(self):
        return "{}-{}{}".format(self.domain, self.faculty, self.number).upper()

    @property
    def dochub(self):
        return "{}-{}-{}".format(self.domain, self.faculty, self.number).lower()

    @classmethod
    def from_gehol(cls, string):
        match = re.match(r'([A-Za-z]+)([A-Za-z])(\d+)', string)
        if match is None:
            raise ValueError("Invalid slug format. Must be like 'INFOF103'")
        domain, faculty, number = match.groups()
        return cls(domain, faculty, number)

    @classmethod
    def from_catalog(cls, string):
        match = re.match(r'([A-Za-z]+)-([A-Za-z])(\d+)', string)
        if match is None:
            raise ValueError("Invalid slug format. Must be like 'INFO-F103'")
        domain, faculty, number = match.groups()
        return cls(domain, faculty, number)

    @classmethod
    def from_dochub(cls, string):
        match = re.match(r'([A-Za-z]+)-([A-Za-z])-(\d+)', string.upper())
        if match is None:
            raise ValueError("Invalid slug format. Must be like 'info-f-103'")
        domain, faculty, number = match.groups()
        return cls(domain, faculty, number)

    @classmethod
    def match_all(cls, string):
        for method in [cls.from_catalog, cls.from_dochub, cls.from_gehol]:
            try:
                return method(string)
            except ValueError:
                pass

        raise ValueError("Not valid slug found")

    def __repr__(self):
        return "<Slug: {}>".format(self)

    def __str__(self):
        return self.dochub

    def __eq__(self, other):
        return (self.domain, self.faculty, self.number) == (other.domain, other.faculty, other.number)

    def __hash__(self):
        return hash((self.domain, self.faculty, self.number))
