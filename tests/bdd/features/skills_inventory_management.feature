Feature: Skill Inventory Management
    As a user
    I want to add technical and soft skills that I already possess
    So that the system can calculate my compatibility with jobs

    Scenario: Successfully add a hard skill to the profile
        Given an authenticated user with a valid bearer token
        When a POST request is sent to "/api/v1/profile/me/skills/hard" with skill name "Python" and level "advanced"
        Then the response status is 200 OK
        And the response body contains the updated profile including the new skill

    Scenario: Successfully remove a skill from the profile
        Given an authenticated user who already has the skill "Python" registered
        When a DELETE request is sent to "/api/v1/profile/me/skills/hard/Python"
        Then the response status is 200 OK
        And the response body contains the profile without the specified skill

    Scenario: Attempt to add a skill that is already registered
        Given an authenticated user who already has the skill "Python" registered
        When a POST request is sent to "/api/v1/profile/me/skills/hard" with skill name "python" and level "advanced"
        Then the response status is 400 Bad Request
        And the response body contains the message "La habilidad ya existe."
