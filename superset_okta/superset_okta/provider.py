"""

"""
import logging
from superset.security import SupersetSecurityManager

logger = logging.getLogger()


class SupersetCustomSecurityManager(SupersetSecurityManager):
    """Class for Superset customised security manager, based on SSO leveraging Okta"""

    def get_user_role(self, groups):
        """Assign role given the list of okta groups

        Args:
            groups (list): list of groups a user is assigned to in okta
        """
        if "Superset_Admin" in groups:
            return [self.find_role("Admin")]
        if "Superset_Explorer" in groups:
            return [self.find_role("Alpha"),
                    self.find_role("sql_lab")]
        return [self.find_role("Public")]

    # pylint: disable=method-hidden, unused-argument
    def oauth_user_info(self, provider, response=None):
        """Obtain user information from provider

        Args:
            provider (string): authentication provider
            response (string): server response

        Returns:
            user (Dict): dictionary with user information
        """
        if provider == "okta":
            # Obtain user information
            result = self.appbuilder.sm.oauth_remotes[provider].get("userinfo")
            user_info = result.json()

            # Return user information
            return {
                "username": user_info.get("preferred_username", ""),
                "name": user_info.get("name", ""),
                "email": user_info.get("email", ""),
                "first_name": user_info.get("given_name", ""),
                "last_name": user_info.get("family_name", ""),
                "role_keys": user_info.get("groups", []),
            }
        # Default return
        return {}

    def auth_user_oauth(self, userinfo):
        """OAuth user Authentication

        Args:
            userinfo (Dict): dict with user information the keys have the same name
            as User model columns

        Returns:
            user (User): User object for FAB
        """
        # Create User object
        user = self.find_user(username=userinfo.get("username"))
        okta_groups = userinfo.get("role_keys", [])
        # Apply readonly to those who are not in DE
        roles = self.get_user_role(okta_groups)
        # Fetch or add user if not registered, updating roles
        if user:
            # Get roles
            user.roles = roles
            # Update user stats
            self.update_user_auth_stat(user)
        else:
            # Add User object
            user = self.add_user(
                username=userinfo.get("username"),
                first_name=userinfo.get("first_name"),
                last_name=userinfo.get("last_name"),
                email=userinfo.get("email"),
                role=roles,
            )
        # Return User object
        return user
