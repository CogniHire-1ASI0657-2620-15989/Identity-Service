Feature: Profile and Expectations Management
    As a user
    I want to update my personal information and expected job role
    So that the platform knows what to recommend me and keeps my CV updated

    Scenario: Successfully update professional profile and expectations
        Given an authenticated user with a valid bearer token
        When a PUT request is sent to "/api/v1/profile/me" with valid profile details and expected role
        Then the response status is 200 OK
        And the response body contains the updated user profile data

    Scenario: Attempt to update profile without authentication
        Given an unauthenticated user
        When a PUT request is sent to "/api/v1/profile/me" with profile updates
        Then the response status is 401 Unauthorized
        And the response body indicates missing or invalid token

    Scenario: Successfully add work experience to the profile
        Given an authenticated user with a valid bearer token
        When a POST request is sent to "/api/v1/profile/me/experience" with position "Backend Developer" at company "PathBridge" from "2024-01" to "2025-06"
        Then the response status is 201 Created
        And the response body contains the experience "Backend Developer" at "PathBridge"

    Scenario: Attempt to add work experience with an invalid date range
        Given an authenticated user with a valid bearer token
        When a POST request is sent to "/api/v1/profile/me/experience" with position "Backend Developer" at company "PathBridge" from "2025-06" to "2024-01"
        Then the response status is 422 Unprocessable Entity
