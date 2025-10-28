"""
Factory Pattern - Complex object creation.

Factories encapsulate the logic for creating complex domain objects,
especially when creation involves validation, defaults, or multiple steps.

Example usage:
    rule_factory = AdmissionRuleFactory()
    rule = rule_factory.create_from_config({
        'type': 'minimum_grade',
        'subject': 'Mathematics',
        'grade': 4
    })

    student_factory = StudentFactory()
    student = student_factory.reconstitute(db_data)
"""
