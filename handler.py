import json
from controllers import bin_controller
from utils import encoder


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
        except Exception as e:
            print(f"e: {e}")

            response = {
                "statusCode": 404,
                "body": json.dumps({"detail": "Bin not found"})
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
        except Exception as e:
            response = {
                "statusCode": 404,
                "body": json.dumps({"detail": "Bin not found"})
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
        except Exception as e:
            # TODO: refactor statuscode 404 response as a function
            response = {
                "statusCode": 404,
                "body": json.dumps({"detail": "Bin not found"})
            }

            return response
