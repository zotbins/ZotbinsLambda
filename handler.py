import json
from controllers import bin_controller, metrics_controller
from datetime import datetime
from utils import encoder, errors


def hello(event, context):
    """
    Test function returning default message
    Returns
    -------
    Returns a json encoded object: dict
        Contains a default message and the event object that called this handler function
    """
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def bin(event, context):
    """
    Request type
    ------------
    GET
    ---
        Retrieves information on bin with specific uuid
        If bin doesn't exist, returns error message
        Returns
        -------
        Returns a json encoded dict: dict
            Contains encoded bin info if bin is found, else error message
    DELETE
    ------
        Removes bin with specific uuid from database
        If bin doesn't exist, returns error message
        Returns
        -------
        Returns a json encoded dict: dict
            Contains a success message is bin is successfully removed, else error message
    """
    method_type = event["routeKey"].split(" ")[0]
    uuid = event["rawPath"].split("/")[-1]

    if method_type == "GET":
        bin_info = bin_controller.get_bin_by_uuid(uuid)

        if bin_info:
            encoded_bin_info = encoder.encode_bin_info(bin_info)

            response = {
                "statusCode": 200,
                "body": json.dumps(encoded_bin_info)
            }

            return response
        else:
            response = {
                "statusCode": 404,
                "body": json.dumps({"detail": "Bin not found"})
            }

            return response
    elif method_type == "DELETE":
        try:
            bin_controller.delete_bin_by_uuid(uuid)

            response = {
                "statusCode": 200,
                "body": json.dumps({"detail": "Successfully deleted"})
            }

            return response
        except errors.BinNotFoundException as e:
            print(f"e: {e}")

            response = {
                "statusCode": e.err_code,
                "body": json.dumps({"detail": e.err_msg})
            }

            return response


def bins(event, context):
    """
    Request type
    ------------
    GET
    ---
        Retrieves all bins
        Returns
        -------
        Returns a json encoded dict: dict
            Contains all bins
    POST
    ----
        TBD
    """
    method_type = event["routeKey"].split(" ")[0]

    if method_type == "GET":
        all_bins = bin_controller.get_all_bins()

        response = {
            "statusCode": 200,
            "body": json.dumps(all_bins)
        }

        return response
    elif method_type == "POST":
        # TODO: Figure out how to get request body
        print(event["body"])
        pass


def location(event, context):
    """
    Request type
    ------------
    GET
    ---
        Retrieves location of bin with specific uuid
        If bin doesn't exist, returns an error message
        Returns
        -------
        Returns a json encoded dict: dict
            Contains the coordinates of the bin (latitude,longitude) if bin exists, else error message
    PUT
    ---
        Updates location of bin with specific uuid
        If bin doesn't exist, returns an error message
        Returns
        -------
        Returns a json encoded dict: dict
            Contains success message if location of bin was successfully updated, else error message
    """
    method_type = event["routeKey"].split(" ")[0]
    uuid = event["rawPath"].split("/")[2]

    if method_type == "GET":
        try:
            lat_and_lon = bin_controller.get_bin_location(uuid)

            response = {
                "statusCode": 200,
                "body": json.dumps(lat_and_lon)
            }

            return response
        except errors.BinNotFoundException as e:
            response = {
                "statusCode": e.err_code,
                "body": json.dumps({"detail": e.err_msg})
            }

            return response
    elif method_type == "PUT":
        try:
            bin_controller.update_bin_location(uuid, 1.0, 1.0)

            response = {
                "statusCode": 200,
                "body": {"Detail": "bin location successfully updated"}
            }

            return response
        except errors.BinNotFoundException as e:
            # TODO: refactor statuscode 404 response as a function
            response = {
                "statusCode": e.err_code,
                "body": json.dumps({"detail": e.err_msg})
            }

            return response


def all_fullness_metrics(event, context):
    """
    Request type
    ------------
    GET
    ---
        Retrieves all fullness metrics
        Returns
        -------
        Returns a json encoded dict: dict
            Contains all fullness metrics
    """
    method_type = event["routeKey"].split(" ")[0]

    if method_type == "GET":
        all_fullness = metrics_controller.get_all_fullness()

        response = {
            "statusCode": 200,
            "body": json.dumps(all_fullness)
        }

        return response


def all_usage_metrics(event, context):
    """
    Request type
    ------------
    GET
    ---
        Retrieves all usage metrics
        Returns
        -------
        Returns a json encoded dict: dict
            Contains all usage metrics
    """
    method_type = event["routeKey"].split(" ")[0]

    if method_type == "GET":
        all_usage = metrics_controller.get_all_usage()

        response = {
            "statusCode": 200,
            "body": json.dumps(all_usage)
        }

        return response


def all_weight_metrics(event, context):
    """
    Request type
    ------------
    GET
    ---
        Retrieves all weight metrics
        Returns
        -------
        Returns a json encoded dict: dict
            Contains all weight metrics
    """
    method_type = event["routeKey"].split(" ")[0]

    if method_type == "GET":
        all_weight = metrics_controller.get_all_weight()

        response = {
            "statusCode": 200,
            "body": json.dumps(all_weight)
        }

        return response


def filter_fullness_metrics(event, context):
    """
    Request type
    ------------
    GET
    ---
        Retrieves fullness metrics filtered by their sensor id and timestamp attributes
        If start timestamp occurs after end timestamp, returns error message
        If sensor id doesn't exist, returns error message
        Returns
        -------
        Returns a json encoded dict: dict
            Contains fullness metrics filtered by their sensor id and timestamp attributes 
                if start timestamp occurs before end timestamp and sensor id exists, else error message
    """
    method_type = event["routeKey"].split(" ")[0]
    sensor_id = event["rawPath"].split("/")[2]
    timestamp = event["rawQueryString"].split("&")
    start_time = datetime.strptime(timestamp[0][18:].replace("%3A", ":").replace("+", " "), "%y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(timestamp[1][16:].replace("%3A", ":").replace("+", " "), "%y-%m-%d %H:%M:%S")

    if start_time < end_time:
        if method_type == "GET":
            try:
                fullness_info = metrics_controller.get_fullness_by_sensor_id_and_timestamp(sensor_id, start_time, end_time)

                response = {
                    "statusCode": 200,
                    "body": json.dumps(fullness_info)
                }

                return response
            except errors.InvalidSensorIdException as e:
                response = {
                    "statusCode": e.err_code,
                    "body": json.dumps({"detail": e.err_msg})
                }

                return response
    else:
        try:
            raise errors.InvalidTimestampOrderException
        except errors.InvalidTimestampOrderException as e:
            response = {
                "statusCode": e.err_code,
                "body": json.dumps({"detail": e.err_msg})
            }

            return response


def filter_usage_metrics(event, context):
    """
    Request type
    ------------
    GET
    ---
        Retrieves usage metrics filtered by their sensor id and timestamp attributes
        If start timestamp occurs after end timestamp, returns error message
        If sensor id doesn't exist, returns error message
        Returns
        -------
        Returns a json encoded dict: dict
            Contains usage metrics filtered by their sensor id and timestamp attributes 
                if start timestamp occurs before end timestamp and sensor id exists, else error message
    """
    method_type = event["routeKey"].split(" ")[0]
    sensor_id = event["rawPath"].split("/")[2]
    timestamp = event["rawQueryString"].split("&")
    start_time = datetime.strptime(timestamp[0][18:].replace("%3A", ":").replace("+", " "), "%y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(timestamp[1][16:].replace("%3A", ":").replace("+", " "), "%y-%m-%d %H:%M:%S")

    if start_time < end_time:
        if method_type == "GET":
            try:
                usage_info = metrics_controller.get_usage_by_sensor_id_and_timestamp(sensor_id, start_time, end_time)

                response = {
                    "statusCode": 200,
                    "body": json.dumps(usage_info)
                }

                return response
            except errors.InvalidSensorIdException as e:
                response = {
                    "statusCode": e.err_code,
                    "body": json.dumps({"detail": e.err_msg})
                }

                return response
    else:
        try:
            raise errors.InvalidTimestampOrderException
        except errors.InvalidTimestampOrderException as e:
            response = {
                "statusCode": e.err_code,
                "body": json.dumps({"detail": e.err_msg})
            }

            return response


def filter_weight_metrics(event, context):
    """
    Request type
    ------------
    GET
    ---
        Retrieves weight metrics filtered by their sensor id and timestamp attributes
        If start timestamp occurs after end timestamp, returns error message
        If sensor id doesn't exist, returns error message
        Returns
        -------
        Returns a json encoded dict: dict
            Contains weight metrics filtered by their sensor id and timestamp attributes 
                if start timestamp occurs before end timestamp and sensor id exists, else error message
    """
    method_type = event["routeKey"].split(" ")[0]
    sensor_id = event["rawPath"].split("/")[2]
    timestamp = event["rawQueryString"].split("&")
    start_time = datetime.strptime(timestamp[0][18:].replace("%3A", ":").replace("+", " "), "%y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(timestamp[1][16:].replace("%3A", ":").replace("+", " "), "%y-%m-%d %H:%M:%S")

    if start_time < end_time:
        if method_type == "GET":
            try:
                weight_info = metrics_controller.get_weight_by_sensor_id_and_timestamp(sensor_id, start_time, end_time)

                response = {
                    "statusCode": 200,
                    "body": json.dumps(weight_info)
                }

                return response
            except errors.InvalidSensorIdException as e:
                response = {
                    "statusCode": e.err_code,
                    "body": json.dumps({"detail": e.err_msg})
                }

                return response
    else:
        try:
            raise errors.InvalidTimestampOrderException
        except errors.InvalidTimestampOrderException as e:
            response = {
                "statusCode": e.err_code,
                "body": json.dumps({"detail": e.err_msg})
            }

            return response


# # Unneeded functions as of right now
# # Unneeded as fullness metric does not have uuid attribute yet
# def fullness_metrics(event, context):
#     method_type = event["routeKey"].split(" ")[0]
#     uuid = event["rawPath"].split("/")[2]
#     time_stamp = event["rawPath"].split("/")[3]
#     start_time = datetime.strptime(time_stamp[17:26], "%y-%m-%d %H-%M-%S")
#     end_time = datetime.strptime(time_stamp[42:], "%y-%m-%d %H-%M-%S")

#     if end_time < start_time:
#         response = {
#             "statusCode": 404,
#             "body": json.dumps({"detail": "Start timestamp occurs after end timestamp"})
#         }

#         return response

#     if method_type == "GET":
#         try:
#             fullness_info = metrics_controller.get_fullness_by_uuid(uuid)

#             response = {
#                 "statusCode": 200,
#                 "body": json.dumps(fullness_info)
#             }

#             return response
#         except Exception as e:
#             response = {
#                 "statusCode": 404,
#                 "body": json.dumps({"detail": "Bin not found"})
#             }

#             return response

# # Unneeded as usage metric does not have uuid attribute yet
# def usage_metrics(event, context):
#     method_type = event["routeKey"].split(" ")[0]
#     uuid = event["rawPath"].split("/")[2]
#     time_stamp = event["rawPath"].split("/")[3]
#     start_time = datetime.strptime(time_stamp[17:26], "%y-%m-%d %H-%M-%S")
#     end_time = datetime.strptime(time_stamp[42:], "%y-%m-%d %H-%M-%S")

#     if end_time < start_time:
#         response = {
#             "statusCode": 404,
#             "body": json.dumps({"detail": "Start timestamp occurs after end timestamp"})
#         }

#         return response

#     if method_type == "GET":
#         try:
#             usage_info = metrics_controller.get_usage_by_uuid(uuid)

#             response = {
#                 "statusCode": 200,
#                 "body": json.dumps(usage_info)
#             }

#             return response

#         except Exception as e:
#             response = {
#                 "statusCode": 404,
#                 "body": json.dumps({"detail": "Bin not found"})
#             }

#             return response

# # Unneeded as weight metric does not have uuid attribute yet
# def weight_metrics(event, context):
#     method_type = event["routeKey"].split(" ")[0]
#     uuid = event["rawPath"].split("/")[2]
#     time_stamp = event["rawPath"].split("/")[3]
#     start_time = datetime.strptime(time_stamp[17:26], "%y-%m-%d %H-%M-%S")
#     end_time = datetime.strptime(time_stamp[42:], "%y-%m-%d %H-%M-%S")

#     if end_time < start_time:
#         response = {
#             "statusCode": 404,
#             "body": json.dumps({"detail": "Start timestamp occurs after end timestamp"})
#         }

#         return response

#     if method_type == "GET":
#         try:
#             weight_info = metrics_controller.get_weight_by_uuid(uuid)

#             response = {
#                 "statusCode": 200,
#                 "body": json.dumps(weight_info)
#             }

#             return response
            
#         except Exception as e:
#             response = {
#                 "statusCode": 404,
#                 "body": json.dumps({"detail": "Bin not found"})
#             }

#             return response