Feature: User Registration
    As a new user
    I want to register in the platform with email and password
    So that I can create my professional profile

    Scenario: Successfully register a new user account
        Given the email "ana.perez@example.com" is not registered in the system
        When a POST request is sent to "/api/v1/auth/register" with valid registration details
        Then the response status is 201 Created
        And the response body contains an access token and user profile information

    Scenario: Attempt to register with an already existing email
        Given the email "ana.perez@example.com" is already registered in the system
        When a POST request is sent to "/api/v1/auth/register" with the duplicate email
        Then the response status is 409 Conflict
        And the response body contains the message "El email ya está registrado."

    Scenario: Attempt to register with identity data that does not match RENIEC
        Given the email "ana.perez@example.com" is not registered in the system
        When a POST request is sent to "/api/v1/auth/register" with a DNI whose names do not match RENIEC
        Then the response status is 422 Unprocessable Entity
        And the response body contains the message "Los datos de identidad no pudieron ser validados."
        And no user account is created for "ana.perez@example.com"
