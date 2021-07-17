from django.contrib.auth.decorators import user_passes_test


def user_in_group(function=None, group=None, redirect_field_name="", login_url="/404"):
    def user_in_the_group(user):
        if user:
            return user.groups.filter(name=group).count() > 0
        return False
    actual_decorator = user_passes_test(
        user_in_the_group,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
