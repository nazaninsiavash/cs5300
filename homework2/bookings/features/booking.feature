# features/booking.feature
# BDD tests for the Movie Theater Booking application

Feature: Movie Theater Booking

  Background:
    Given the database is clean
    And a user "alice" with password "pass123" exists
    And a movie "Inception" with 5 available seats exists

  Scenario: Viewing the movie list
    When I visit the movie list page
    Then I should see "Inception" in the response

  Scenario: Booking a seat successfully
    Given I am logged in as "alice" with password "pass123"
    When I book seat "A1" for movie "Inception"
    Then the booking should be created successfully
    And seat "A1" should be marked as booked

  Scenario: Cannot book an already booked seat
    Given I am logged in as "alice" with password "pass123"
    And seat "A1" for movie "Inception" is already booked
    When I try to book seat "A1" for movie "Inception"
    Then I should see an error about the seat being already booked

  Scenario: Viewing booking history
    Given I am logged in as "alice" with password "pass123"
    And I have a booking for seat "A1" in movie "Inception"
    When I visit the booking history page
    Then I should see "Inception" in the response

  Scenario: Cancelling a booking
    Given I am logged in as "alice" with password "pass123"
    And I have a booking for seat "A1" in movie "Inception"
    When I cancel my booking
    Then the booking should be removed
    And seat "A1" should be available again
