Feature: User Authentication Login
    As a registered user
    I want to log in with my credentials
    So that I can access my dashboard and profile

    Scenario: Successfully log in with correct credentials
        Given a registered user with email "ana.perez@example.com" and password "ClaveSegura123"
        When a POST request is sent to "/api/v1/auth/login" with the correct credentials
        Then the response status is 200 OK
        And the response body contains a valid bearer access token

    Scenario: Attempt to log in with incorrect password
        Given a registered user with email "ana.perez@example.com"
        When a POST request is sent to "/api/v1/auth/login" with an invalid password
        Then the response status is 401 Unauthorized
        And the response body contains the message "Credenciales inválidas."