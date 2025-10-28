"""
Specification Pattern - Reusable business rules.

Specifications encapsulate business rules that can be combined and reused.
They follow the Specification pattern from Domain-Driven Design.

Example usage:
    min_grade_spec = MinimumGradeSpecification("Mathematics", 4)
    special_comp_spec = SpecialCompetenceSpecification()

    combined = min_grade_spec.and_(special_comp_spec)
    if combined.is_satisfied_by(student):
        # Student meets both criteria
        pass
"""
