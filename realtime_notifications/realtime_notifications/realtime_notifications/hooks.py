# realtime_notifications/hooks.py
from . import __version__ as app_version

app_name = "realtime_notifications"
app_title = "Realtime Notifications"
app_publisher = "Nilesh Awari"
app_description = "Real-time notification system for CRM and other modules"
app_icon = "octicon octicon-bell"
app_color = "blue"
app_email = "nileshawari2000@gmail.com"
app_license = "MIT"

# Includes in <head>
app_include_js = "/assets/realtime_notifications/js/realtime_notifications.js"
app_include_css = "/assets/realtime_notifications/css/realtime_notifications.css"

# Document Events - Hook into Lead creation
doc_events = {
    "Lead": {
        "after_insert": "realtime_notifications.api.notifications.notify_new_lead"
    },
    "Opportunity": {
        "after_insert": "realtime_notifications.api.notifications.notify_new_opportunity"
    }
}

# Custom permissions for notification methods
override_whitelisted_methods = {
    "realtime_notifications.api.notifications.send_notification": "realtime_notifications.api.notifications.send_notification"
}