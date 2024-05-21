from common.responses import Unauthorized

PREMIUM_COURSE_LIMIT = 5

USER_LOGGED_OUT_RESPONSE = Unauthorized(content="User is logged out! Login required to perform this task!")