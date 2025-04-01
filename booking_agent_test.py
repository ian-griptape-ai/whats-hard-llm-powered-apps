from griptape.structures import Agent
from griptape.rules import Rule
from griptape.tools import StructureRunTool, DateTimeTool
from griptape.drivers.structure_run.local_structure_run_driver import (
    LocalStructureRunDriver,
)

from griptape.events import (
    StartStructureRunEvent,
    TextChunkEvent,
    FinishActionsSubtaskEvent,
)

from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from griptape.drivers.observability.open_telemetry import (
    OpenTelemetryObservabilityDriver,
)
from griptape.observability import Observability


from griptape.utils import Chat  #   <-- Added Chat
import schema
from dotenv import load_dotenv
from rich.pretty import pprint

load_dotenv()

observability_driver = OpenTelemetryObservabilityDriver(
    service_name="hotel-booking-agent-testing",
    span_processor=BatchSpanProcessor(OTLPSpanExporter()),
)


def request_date_checker_agent() -> Agent:
    return Agent(
        id="RequestDateCheckerAgent",
        tools=[DateTimeTool()],
        rules=[
            Rule("You are a request date checker"),
            Rule("You check the dates of the request to ensure they are valid"),
            Rule(
                "If any of the dates in the a request are in the past the requests is invalid"
            ),
        ],
    )


def room_reservations_agent() -> Agent:
    return Agent(
        id="RoomReservationsAgent",
        rules=[
            Rule(
                "You handle room bookings, \
                 you focus on gathering the necessary information to complete a booking."
            ),
            Rule(
                "once you have all the required information, \
                 you will return this information to allow the booking to confirmed."
            ),
            Rule(
                "to verify the booking, you require the following information: \
                 Start Date, End Date, Room Type, Number of Guests"
            ),
            Rule(
                "Never confirm any room booking that starts or ends in the past, before today's date. Use the DateTimeTool is get today's date."
            ),
            Rule(
                "Once you have the requried information, state clearly that the booking can be confirmed."
            ),
        ],
        tools=[DateTimeTool()],
        output_schema=schema.Schema(
            {
                "start_date": str,
                "end_date": str,
                "room_type": str,
                "number_of_guests": int,
                "confirmed": bool,
            }
        ),
    )


def booking_confirmation_agent() -> Agent:
    return Agent(
        id="BookingConfirmationAgent",
        rules=[
            Rule("You confirm bookings"),  # using a tool eventually
            Rule("You confirm the booking immediately when asked to do so."),  # for now
        ],
    )


def hotel_manager_agent() -> Agent:
    return Agent(
        id="HotelManagerAgent",
        rules=[
            Rule(
                "You are the hotel manager, \
                 you handle interactions with customers in a polite and courteuous manner at all times."
            ),
            Rule(
                "Always check that the date of any request is valid and not in the past before proceeding."
            ),
            Rule(
                "If additional information is required, you ask customers for the information and provide this information to the Room Reservations Agent."
            ),
            Rule(
                "Always provide the complete text of the booking request to the RoomReservationsAgent before confirming the booking."
            ),
            Rule(
                "Once you have a json oject with the following keys: start_date, end_date, room_type and number_of_guests, ask the confirmation agent to confirm the booking"
            ),
        ],
        conversation_memory_strategy="per_structure",
        tools=[
            StructureRunTool(
                name="RoomReservationsAgent",
                description="Books rooms for customers",
                structure_run_driver=LocalStructureRunDriver(
                    create_structure=room_reservations_agent
                ),
            ),
            StructureRunTool(
                name="BookingConfirmationAgent",
                description="Provides confirmation for bookings",
                structure_run_driver=LocalStructureRunDriver(
                    create_structure=booking_confirmation_agent
                ),
            ),
            StructureRunTool(
                name="RequestDateCheckerAgent",
                description="Checks the dates of requests",
                structure_run_driver=LocalStructureRunDriver(
                    create_structure=request_date_checker_agent
                ),
            ),
        ],
    )


with Observability(observability_driver=observability_driver):
    for event in hotel_manager_agent().run_stream(
        "book a superior room from 1st to 3rd of August 2026 for 2 guests"
    ):
        if isinstance(event, StartStructureRunEvent):
            pprint(event.structure_id)
        if isinstance(event, TextChunkEvent):
            print(f"{event.token}", end="", flush=True)
        elif isinstance(event, FinishActionsSubtaskEvent):
            pprint(event.subtask_actions)

# with Observability(observability_driver=observability_driver):
#    Chat(hotel_manager_agent()).start()  #   <-- Added Chat
