Feature: Manage Education Offerings
  As an admission administrator
  I want to create, update, and delete education offerings
  So that students can apply to programs for upcoming intake periods

  Background:
    Given I am an admission administrator
    And a ruleset exists with id "nursing-rules-2025"
    And an admission process exists with id "ugh-2025"

  Scenario: Create a new education offering
    When I create an education with:
      | program_name         | Bachelor in Nursing |
      | institution          | NTNU                |
      | campus               | Trondheim           |
      | intake_term          | Autumn 2025         |
      | study_mode           | full-time           |
      | language             | Norwegian           |
      | ruleset_id           | nursing-rules-2025  |
      | admission_process_id | ugh-2025            |
    Then the education is created successfully
    And the education has state "Planned"
    And the education has a unique id
    And I can retrieve the education by its id

  Scenario: Create education with missing required field
    When I create an education without a program_name
    Then the creation fails with error "program_name is required"

  Scenario: Create education with invalid ruleset reference
    Given no ruleset exists with id "invalid-ruleset"
    When I create an education with ruleset_id "invalid-ruleset"
    Then the creation fails with error "Ruleset not found"

  Scenario: Create multiple educations for same program at different campuses
    Given an education exists for "Bachelor in Nursing, NTNU Trondheim, Autumn 2025"
    When I create an education for "Bachelor in Nursing, NTNU Gjøvik, Autumn 2025"
    Then both educations exist with different ids

  Scenario: Update education attributes
    Given an education exists with:
      | program_name | Bachelor in Nursing |
      | campus       | Trondheim           |
      | state        | Planned             |
    When I update the education campus to "Gjøvik"
    Then the education campus is "Gjøvik"
    And the education id remains unchanged

  Scenario: Update education ruleset reference
    Given an education exists with ruleset_id "nursing-rules-2025"
    And a ruleset exists with id "nursing-rules-2026"
    When I update the education ruleset_id to "nursing-rules-2026"
    Then the education references ruleset "nursing-rules-2026"

  Scenario: Update education state from Planned to Active
    Given an education exists with state "Planned"
    When I update the education state to "Active"
    Then the education state is "Active"

  Scenario: Update education state from Active to Finished
    Given an education exists with state "Active"
    When I update the education state to "Finished"
    Then the education state is "Finished"

  Scenario: Cannot update education with invalid state transition
    Given an education exists with state "Active"
    When I attempt to update the education state to "Planned"
    Then the update fails with error "Invalid state transition: Active → Planned"
    And the education state remains "Active"

  Scenario: Cannot update non-existent education
    Given no education exists with id "non-existent-id"
    When I attempt to update education "non-existent-id"
    Then the update fails with error "Education not found"

  Scenario: Delete education in Planned state
    Given an education exists with state "Planned"
    When I delete the education
    Then the education is removed from the system
    And I cannot retrieve the education by its id

  Scenario: Cannot delete education in Active state
    Given an education exists with state "Active"
    When I attempt to delete the education
    Then the deletion fails with error "Cannot delete education in Active state"
    And the education still exists

  Scenario: Cannot delete education in Finished state
    Given an education exists with state "Finished"
    When I attempt to delete the education
    Then the deletion fails with error "Cannot delete education in Finished state"
    And the education still exists

  Scenario: Cannot delete non-existent education
    Given no education exists with id "non-existent-id"
    When I attempt to delete education "non-existent-id"
    Then the deletion fails with error "Education not found"
