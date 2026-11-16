Feature: Password Recovery and Reset
    As a user
    I want to recover my password if I forget it
    So that I don't lose access to my account and progress

    Scenario: Successfully request a password recovery token
        Given a registered user with email "ana.perez@example.com"
        When a POST request is sent to "/api/v1/auth/password-recovery" with the email
        Then the response status is 200 OK
        And the response body indicates that a recovery token has been generated

    Scenario: Successfully reset password using a valid token
        Given a valid password recovery token for the user
        When a POST request is sent to "/api/v1/auth/password-reset" with the token and new password
        Then the response status is 204 No Content