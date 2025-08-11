# realtime_notifications/api/notifications.py
import frappe
from frappe import _
import json

@frappe.whitelist()
def send_notification(message, title=None, user=None, notification_type="info", sound=True):
    """
    Send real-time notification to specific user or all users
    
    Args:
        message (str): Notification message
        title (str): Notification title
        user (str): Target user email (if None, sends to current user)
        notification_type (str): Type of notification (info, success, warning, error)
        sound (bool): Whether to play notification sound
    """
    try:
        if not user:
            user = frappe.session.user
            
        # Create notification data
        notification_data = {
            "message": message,
            "title": title or "Notification",
            "type": notification_type,
            "sound": sound,
            "timestamp": frappe.utils.now(),
            "from_user": frappe.session.user
        }
        
        # Use frappe.publish_realtime to send notification
        frappe.publish_realtime(
            event="notification",
            message=notification_data,
            user=user
        )
        
        # Log notification for debugging
        frappe.logger().info(f"Notification sent to {user}: {message}")
        
        return {"status": "success", "message": "Notification sent successfully"}
        
    except Exception as e:
        frappe.logger().error(f"Error sending notification: {str(e)}")
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def send_bulk_notification(message, title=None, users=None, notification_type="info"):
    """
    Send notification to multiple users
    
    Args:
        message (str): Notification message
        title (str): Notification title
        users (list): List of user emails
        notification_type (str): Type of notification
    """
    try:
        if not users:
            # Send to all active users with CRM access
            users = frappe.get_all("User", 
                                 filters={"enabled": 1, "user_type": "System User"}, 
                                 pluck="email")
        
        elif isinstance(users, str):
            users = json.loads(users)
        
        success_count = 0
        for user in users:
            result = send_notification(message, title, user, notification_type)
            if result.get("status") == "success":
                success_count += 1
        
        return {
            "status": "success", 
            "message": f"Notification sent to {success_count} users"
        }
        
    except Exception as e:
        frappe.logger().error(f"Error sending bulk notification: {str(e)}")
        return {"status": "error", "message": str(e)}

def notify_new_lead(doc, method):
    """
    Automatically notify relevant users when a new lead is created
    """
    try:
        # Get users who should be notified about new leads
        # You can customize this logic based on your requirements
        sales_users = frappe.get_all("User", 
                                   filters={
                                       "enabled": 1, 
                                       "user_type": "System User"
                                   }, 
                                   pluck="email")
        
        # Create notification message
        message = f"New Lead: {doc.lead_name} from {doc.company_name or 'Unknown Company'}"
        title = "New Lead Alert"
        
        # Send notification to sales team
        for user in sales_users:
            send_notification(
                message=message,
                title=title,
                user=user,
                notification_type="success",
                sound=True
            )
            
    except Exception as e:
        frappe.logger().error(f"Error in notify_new_lead: {str(e)}")

def notify_new_opportunity(doc, method):
    """
    Automatically notify relevant users when a new opportunity is created
    """
    try:
        # Get assigned user and sales manager
        users_to_notify = []
        
        if doc.opportunity_owner:
            users_to_notify.append(doc.opportunity_owner)
            
        # Add sales managers (customize as needed)
        sales_managers = frappe.get_all("User", 
                                      filters={
                                          "enabled": 1, 
                                          "user_type": "System User"
                                      }, 
                                      pluck="email")
        users_to_notify.extend(sales_managers)
        
        # Remove duplicates
        users_to_notify = list(set(users_to_notify))
        
        message = f"New Opportunity: {doc.opportunity_from} - {doc.customer_name}"
        title = "New Opportunity Alert"
        
        for user in users_to_notify:
            send_notification(
                message=message,
                title=title,
                user=user,
                notification_type="info",
                sound=True
            )
            
    except Exception as e:
        frappe.logger().error(f"Error in notify_new_opportunity: {str(e)}")

@frappe.whitelist()
def test_notification():
    """
    Test function to send a sample notification
    """
    return send_notification(
        message="This is a test notification from Realtime Notifications app!",
        title="Test Alert",
        notification_type="success",
        sound=True
    )

@frappe.whitelist()
def get_notification_settings():
    """
    Get current user's notification preferences
    """
    # This can be expanded to include user preferences
    return {
        "sound_enabled": True,
        "popup_enabled": True,
        "email_notifications": False
    }