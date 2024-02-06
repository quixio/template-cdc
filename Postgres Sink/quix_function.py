import quixstreams as qx
from typing import List


class QuixFunction:

    def __init__(self, stream_consumer: qx.StreamConsumer):
        self.stream_consumer = stream_consumer

    # Callback triggered for each new parameter data.
    def on_stream_closed_handler(self, stream_consumer: qx.StreamConsumer, end_type: qx.StreamEndType):
        print("Stream", self.stream_consumer.stream_id, "closed with", end_type)

    def on_stream_properties_changed_handler(self, stream_consumer: qx.StreamConsumer):
        properties = self.stream_consumer.properties
        print("Stream properties read for stream: " + self.stream_consumer.stream_id)
        print("Name", properties.name, sep = ": ")
        print("Location", properties.location, sep = ": ")
        print("Metadata", properties.metadata, sep = ": ")
        # print(properties.metadata["meta"]) # or by index
        print("Parents", properties.parents, sep = ": ")
        # print(properties.parents[0]) # or by index
        print("TimeOfRecording", properties.time_of_recording, sep = ": ")

    def on_data_handler(self, stream_consumer: qx.StreamConsumer, data: qx.TimeseriesData):
        print("Parameter data read for stream: " + self.stream_consumer.stream_id)
        print("  Length:", len(data.timestamps))
        for index, val in enumerate(data.timestamps):
            print("    Time:", val)
            tag_string = "    Tags: "
            for tag, vals in data.timestamps[index].tags.items():
                tag_string = tag_string + tag + "=" + str(vals[index]) + ", "
            tag_string.rstrip(", ")
            print(tag_string)
            for timestamps in data.timestamps:
                for key, value in timestamps.parameters.items():
                    print("      " + key + ": " + str(value.numeric_value))
                    print("      " + key + ": " + str(value.string_value))

    def on_parameter_definitions_changed_handler(self, stream_consumer: qx.StreamConsumer):
        print("Parameter definitions read for stream: " + self.stream_consumer.stream_id)
        indent = "   "

        def print_parameters(params: List[qx.ParameterDefinition], level):
            print(level * indent + "Parameters:")
            for parameter in params:
                print((level + 1) * indent + parameter.id + ": ")
                if parameter.name is not None:
                    print((level + 2) * indent + "Name: " + parameter.name)
                if parameter.description is not None:
                    print((level + 2) * indent + "Description: " + parameter.description)
                if parameter.format is not None:
                    print((level + 2) * indent + "Format: " + parameter.format)
                if parameter.unit is not None:
                    print((level + 2) * indent + "Unit: " + parameter.unit)
                if parameter.maximum_value is not None:
                    print((level + 2) * indent + "Maximum value: " + str(parameter.maximum_value))
                if parameter.minimum_value is not None:
                    print((level + 2) * indent + "Minimum value: " + str(parameter.minimum_value))
                if parameter.custom_properties is not None:
                    print((level + 2) * indent + "Custom properties: " + parameter.custom_properties)

        print_parameters(self.stream_consumer.timeseries.definitions, 0)

    def on_event_definitions_changed_handler(self, stream_consumer: qx.StreamConsumer):
        print("Event definitions read for stream: " + self.stream_consumer.stream_id)
        indent = "   "

        def print_events(params: List[qx.EventDefinition], level):
            print(level * indent + "Events:")
            for event in params:
                print((level + 1) * indent + event.id + ": ")
                if event.name is not None:
                    print((level + 2) * indent + "Name: " + event.name)
                print((level + 2) * indent + "Level: " + str(event.level))
                if event.description is not None:
                    print((level + 2) * indent + "Description: " + event.description)
                if event.custom_properties is not None:
                    print((level + 2) * indent + "Custom properties: " + event.custom_properties)

        print_events(self.stream_consumer.events.definitions, 0)

    def on_event_data_handler(self, stream_consumer: qx.StreamConsumer, data: qx.EventData):
        print("Event data read for stream: " + self.stream_consumer.stream_id)
        print("  Time:", data.timestamp)
        print("  Id:", data.id)
        tag_string = "  Tags: "
        for tag, val in data.tags.items():
            tag_string = tag_string + tag + "=" + str(val) + ", "
        tag_string.rstrip(", ")
        print(tag_string)
        print("  Value: " + data.value)