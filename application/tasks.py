from celery import shared_task
from .mail_service import send_message
from application.models import db, ServiceReq, User, Role

@shared_task(ignore_result=True)
def daily_reminder(to, subject):
  send_message(to, subject, "hello")
  return "OK"
  


@shared_task
def notify_professionals():
    try:
        # Fetch service requests with 'Pending' status
        pending_requests = (
            db.session.query(ServiceReq, User)
            .join(User, ServiceReq.professional_id == User.id)
            .filter(ServiceReq.service_status == 'Pending')
            .all()
        )

        # Prepare and send email notifications
        for request, professional in pending_requests:
            # Email subject and body
            subject = "Pending Service Request Notification"
            body = f"""
                <html>
                <body>
                    <p>Dear {professional.name},</p>
                    <p>You have a pending service request:</p>
                    <ul>
                        <li><b>Requested Date:</b> {request.date_of_request}</li>
                    </ul>
                    <p>Please check your dashboard for more details.</p>
                    <br>
                    <p>Best regards,<br>Service Team</p>
                </body>
                </html>
            """

            # Send the email using send_message
            send_message(to=professional.email, subject=subject, content_body=body)

        return f"Notifications sent to {len(pending_requests)} professionals."

    except Exception as e:
        return f"An error occurred: {str(e)}"



from datetime import datetime, timedelta
from jinja2 import Template

@shared_task(ignore_result=True)
def monthly_service_report():
    try:
        # Get the date range for the current month
        today = datetime.today()
        first_day_of_month = datetime(today.year, today.month, 1)
        last_day_of_month = datetime(today.year, today.month + 1, 1) - timedelta(days=1) if today.month < 12 else datetime(today.year, 12, 31)

        # last_month_end = first_day_of_month - timedelta(days=1)
        # last_month_start = datetime(last_month_end.year, last_month_end.month, 1)

        # Fetch all customers (role="Customer")
        customers = User.query.filter(
            User.roles.any(name="user")
        ).all()

        # HTML template for the report
        html_template = """
        <html>
        <body>
            <h2>Monthly Service Report - {{ month_name }}</h2>
            <p>Dear {{ customer_name }},</p>
            <p>Here is your activity report for {{ month_name }}:</p>
            <h3>Requested Services</h3>
            <table border="1" cellspacing="0" cellpadding="5">
                <thead>
                    <tr>
                        <th>Service Name</th>
                        <th>Date of Request</th>
                    </tr>
                </thead>
                <tbody>
                    {% for service in requested_services %}
                    <tr>
                        <td>{{ service.name }}</td>
                        <td>{{ service.date }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            <h3>Closed Services</h3>
            <table border="1" cellspacing="0" cellpadding="5">
                <thead>
                    <tr>
                        <th>Service Name</th>
                        <th>Date of Completion</th>
                    </tr>
                </thead>
                <tbody>
                    {% for service in closed_services %}
                    <tr>
                        <td>{{ service.name }}</td>
                        <td>{{ service.date }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            <p>Thank you for using our services!</p>
            <p>Best regards,<br>Service Team</p>
        </body>
        </html>
        """

        # Generate and send reports for each customer
        for customer in customers:
            # Fetch requested services for the current month
            requested_services = ServiceReq.query.filter(
                ServiceReq.user_id == customer.id,

                # ServiceReq.date_of_request >= last_month_start,
                # ServiceReq.date_of_request <= last_month_end,

                ServiceReq.date_of_request >= first_day_of_month,
                ServiceReq.date_of_request <= last_day_of_month,
                ServiceReq.service_status.in_(["Pending", "Accepted"])
            ).all()

            # Fetch closed services for the current month
            closed_services = ServiceReq.query.filter(
                ServiceReq.user_id == customer.id,
                
                # ServiceReq.date_of_request >= last_month_start,
                # ServiceReq.date_of_request <= last_month_end,

                ServiceReq.date_of_completion >= first_day_of_month,
                ServiceReq.date_of_completion <= last_day_of_month,
                ServiceReq.service_status == "Closed"
            ).all()

            # Prepare service details
            requested_services_details = [
                {"name": service.service.name, "date": service.date_of_request}
                for service in requested_services
            ]
            closed_services_details = [
                {"name": service.service.name, "date": service.date_of_completion}
                for service in closed_services
            ]

            # Render the report using the HTML template
            rendered_html = Template(html_template).render(
                customer_name=customer.name,

                # month_name=last_month_start.strftime("%B %Y"),

                month_name=first_day_of_month.strftime("%B %Y"),
                requested_services=requested_services_details,
                closed_services=closed_services_details
            )

            # Send the email
            send_message(
                to=customer.email,

                # subject=f"Monthly Service Report - {last_month_start.strftime('%B %Y')}",

                subject=f"Monthly Service Report - {first_day_of_month.strftime('%B %Y')}",
                content_body=rendered_html
            )

        return f"Monthly reports sent to {len(customers)} customers."

    except Exception as e:
        return f"An error occurred: {str(e)}"


