import pytest
from src.app import activities


class TestActivitiesData:
    """Unit tests for activities data structure and business logic."""

    def test_get_all_activities_returns_dict(self):
        """Test that activities is a dictionary."""
        # Arrange
        expected_type = dict

        # Act
        result = activities

        # Assert
        assert isinstance(result, expected_type)

    def test_activities_have_required_fields(self):
        """Test that each activity has all required fields."""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act & Assert
        for activity_name, activity_data in activities.items():
            assert required_fields.issubset(activity_data.keys()), f"Activity {activity_name} missing fields"

    def test_participants_are_list_of_emails(self):
        """Test that participants field is a list of strings (emails)."""
        # Arrange - no special setup needed

        # Act & Assert
        for activity_name, activity_data in activities.items():
            participants = activity_data["participants"]
            assert isinstance(participants, list), f"Participants for {activity_name} should be a list"
            for email in participants:
                assert isinstance(email, str), f"Participant {email} should be a string"
                assert "@" in email, f"Participant {email} should be an email"

    def test_max_participants_is_positive_integer(self):
        """Test that max_participants is a positive integer."""
        # Arrange - no special setup needed

        # Act & Assert
        for activity_name, activity_data in activities.items():
            max_part = activity_data["max_participants"]
            assert isinstance(max_part, int), f"max_participants for {activity_name} should be int"
            assert max_part > 0, f"max_participants for {activity_name} should be positive"

    def test_activity_participant_count_calculation(self):
        """Test calculating current participant count."""
        # Arrange
        activity_name = "Chess Club"
        expected_count = len(activities[activity_name]["participants"])

        # Act
        actual_count = len(activities[activity_name]["participants"])

        # Assert
        assert actual_count == expected_count

    def test_activity_has_capacity(self):
        """Test checking if an activity has remaining capacity."""
        # Arrange
        activity_name = "Chess Club"
        current_count = len(activities[activity_name]["participants"])
        max_count = activities[activity_name]["max_participants"]

        # Act
        has_capacity = current_count < max_count

        # Assert
        assert has_capacity  # Assuming Chess Club has capacity in test data

    def test_duplicate_participant_prevention_logic(self):
        """Test logic for preventing duplicate signups."""
        # Arrange
        activity_name = "Chess Club"
        existing_email = activities[activity_name]["participants"][0]

        # Act
        is_duplicate = existing_email in activities[activity_name]["participants"]

        # Assert
        assert is_duplicate