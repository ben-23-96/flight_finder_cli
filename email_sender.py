import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:
    """
    EmailSender is a class that provides methods to send flight information emails.
    """

    def __init__(self):
        self.email = 'ben.flightfinder@gmail.com'
        self.password = 'fronpjqtodukanxw'

    def send_email(self, to_email, subject, message):
        """
        Sends an email to the specified recipient with the provided subject and message.

        Args:
            to_email (str): The recipient's email address.
            subject (str): The subject of the email.
            message (str): The content of the email.
        """
        # Create a MIME message object.
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Attempt to send the email using Gmail's SMTP server.
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, to_email, msg.as_string())
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print(f"Error: {e}")
            print("Failed to send email.")

    def create_email(self, flights, to_email):
        """
        Creates an email message with the given flight information and sends it
        to the specified recipient.

        Args:
            flights (dict): A dictionary containing flight information lists.
            to_email (str): The recipient's email address.
        """
        for city, flights_list in flights.items():
            # Compile flight information for each city.
            message = f"Flights to {city}:\n"
            for flight in flights_list:
                message += f"Departure: {flight['city from']} - {flight['departure_date']} {flight['departure_time']}\n"
                message += f"Return: {flight['city to']} - {flight['return date']} {flight['return time']}\n"
                message += f"Price: {flight['price']}\n"
                message += f"Link: {flight['link']}\n\n"

            # Set the subject for the email.
            subject = f"Flights to {city}"

            # Send the email with the compiled flight information.
            self.send_email(to_email, subject, message)
