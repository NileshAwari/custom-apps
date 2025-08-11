// realtime_notifications/public/js/realtime_notifications.js

$(document).ready(function() {
    // Initialize notification system when desk loads
    if (window.frappe && frappe.socketio) {
        initializeRealtimeNotifications();
    }
});

function initializeRealtimeNotifications() {
    console.log("Initializing Realtime Notifications...");
    
    // Listen for notification events
    frappe.realtime.on("notification", function(data) {
        showNotificationPopup(data);
    });
    
    // Add notification button to navbar
    addNotificationButton();
    
    console.log("Realtime Notifications initialized successfully");
}

function showNotificationPopup(data) {
    try {
        // Play sound if enabled
        if (data.sound) {
            playNotificationSound(data.type);
        }
        
        // Show popup notification
        let indicator = getIndicatorColor(data.type);
        
        frappe.show_alert({
            message: `<strong>${data.title}</strong><br>${data.message}`,
            indicator: indicator
        }, 8); // Show for 8 seconds
        
        // For important notifications, also show msgprint
        if (data.type === "error" || data.type === "warning") {
            frappe.msgprint({
                title: data.title,
                message: data.message,
                indicator: indicator
            });
        }
        
        // Log notification
        console.log("Notification received:", data);
        
    } catch (error) {
        console.error("Error displaying notification:", error);
    }
}

function playNotificationSound(type) {
    try {
        // Create audio element for notification sound
        let audio = new Audio();
        
        switch(type) {
            case "success":
                audio.src = "/assets/realtime_notifications/sounds/success.mp3";
                break;
            case "error":
                audio.src = "/assets/realtime_notifications/sounds/error.mp3";
                break;
            case "warning":
                audio.src = "/assets/realtime_notifications/sounds/warning.mp3";
                break;
            default:
                audio.src = "/assets/realtime_notifications/sounds/info.mp3";
        }
        
        audio.volume = 0.3;
        audio.play().catch(e => console.log("Could not play notification sound:", e));
        
    } catch (error) {
        console.log("Audio playback not supported or failed:", error);
    }
}

function getIndicatorColor(type) {
    switch(type) {
        case "success": return "green";
        case "error": return "red";
        case "warning": return "orange";
        case "info": return "blue";
        default: return "gray";
    }
}

function addNotificationButton() {
    // Add a test notification button to the navbar
    if (frappe.boot.user.roles.includes("System Manager")) {
        $(document).on('toolbar_setup', function() {
            $('<li><a href="#" onclick="testRealtimeNotification()">🔔 Test Notification</a></li>')
                .prependTo('.navbar-nav');
        });
    }
}

// Global function to test notifications
window.testRealtimeNotification = function() {
    frappe.call({
        method: "realtime_notifications.api.notifications.test_notification",
        callback: function(r) {
            if (r.message && r.message.status === "success") {
                frappe.show_alert("Test notification sent!", "green");
            } else {
                frappe.show_alert("Failed to send test notification", "red");
            }
        }
    });
}

// Global function to send custom notifications
window.sendCustomNotification = function(message, title, users, type) {
    frappe.call({
        method: "realtime_notifications.api.notifications.send_bulk_notification",
        args: {
            message: message,
            title: title || "Custom Notification",
            users: users || null,
            notification_type: type || "info"
        },
        callback: function(r) {
            if (r.message && r.message.status === "success") {
                frappe.show_alert(r.message.message, "green");
            } else {
                frappe.show_alert("Failed to send notification", "red");
            }
        }
    });
}