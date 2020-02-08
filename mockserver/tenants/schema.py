from drf_yasg import openapi


OrganizationInviteSchema = openapi.Schema(
    title='Organization Invite',
    type='object',
    properties={
        'emails': openapi.Schema(
            title='Emails',
            type='array',
            items=openapi.Schema(
                title='email',
                type='string'
            )
        )
    }
)
