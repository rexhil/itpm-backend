import pandas as pd
import xlrd
import tablib
from api import logger


def flatten_input_sheet(input_sheet_path, column_to_flatten, separator='|'):
    """
    Function to Flatten given input sheet which later is passed for validation
    :param input_sheet_path: File path for input sheet
    :param column_to_flatten: Column name that needs to be flattened
    :param separator: separator that separates data in column_to_flatten
    :return: flattened input sheet as pandas data frame
    """
    book = xlrd.open_workbook(file_contents=input_sheet_path.read())
    input_sheet = pd.read_excel(book, engine='xlrd')
    input_sheet.drop_duplicates(inplace=True)
    index_col = list(input_sheet.columns)
    index_col.remove(column_to_flatten)
    input_sheet = (input_sheet.set_index(index_col).stack()
                   .str.split(separator, expand=True)
                   .stack().unstack(-2)
                   .reset_index(-1, drop=True).reset_index())
    return input_sheet


def validate_input_sheet(flattened_input_df, validation_dict):
    """
    Function to validate the given input sheet:
        First Validate Headers length, if success validate headers/column names
        then call function to validate some of column data

    :param flattened_input_df: DataFrame: Pandas data frame with flatten structure of input sheet.
    :param validation_dict: dict: contains list of valid (cities, attribute and rules) to compare against
    :return: tuple: Validation_status as boolean and list of messages
    """
    validation_messages = []
    valid_headers = {'City', 'DC', 'Slug', 'Attribute', 'Rule Type', 'Attribute value', 'start date',
                     'end date'}

    if flattened_input_df.shape[1] == len(valid_headers):
        _headers = set(flattened_input_df.columns)
        if len(_headers) == len(valid_headers):
            incorrect_headers = _headers.difference(valid_headers)
            if not incorrect_headers:
                validation_messages.extend(validate_column_data(flattened_input_df, validation_dict))
            else:
                validation_messages.append("Error in headers: {}.".format(','.join(incorrect_headers)))
        else:
            validation_messages.append("Some headers are duplicated and some headers are missing")
    else:
        validation_messages.append("Column counts are not matching.")
    if validation_messages:
        return False, '<br>'.join(validation_messages)
    return True, ['Validation Success.']


def validate_column_data(flattened_input_df, validation_dict):
    """
    Extension for validate_input_sheet function, Validates location, attribute and rule type values
    this function is created just to make code readable
    :param flattened_input_df: DataFrame: Pandas data frame with flatten structure of input sheet.
    :param validation_dict: dict: contains list of valid (cities, attribute and rules) to compare against
    :return: list of validation messages if only there is error in validation else empty list
    """
    messages = []
    valid_city_list = validation_dict['valid_locations']
    valid_attribute = validation_dict['valid_attributes']
    valid_rule_types = validation_dict['valid_rule_types']
    _cities = set(flattened_input_df['City'])
    incorrect_city = _cities.difference(valid_city_list)
    if incorrect_city:
        messages.append("Error in city names = {}.".format(','.join(incorrect_city)))
    _attribute = set(flattened_input_df['Attribute'])
    incorrect_attribute = _attribute.difference(valid_attribute)
    if incorrect_attribute:
        messages.append("Error in attribute = {}.".format(','.join(incorrect_attribute)))
    _rule_types = set(flattened_input_df['Rule Type'])
    incorrect_rule_type = _rule_types.difference(valid_rule_types)
    if incorrect_rule_type:
        messages.append("Error in rule_type = {}.".format(','.join(incorrect_rule_type)))
    return messages


def safely_write_to_db(data_resource, _data):
    """
    Step 1: Convert data to data frame if only data type of _data is list else assume its already a pandas data frame
    Step 2: Adds required field and converts data_frame to tablib data set and does a dry run of inserting into table
            if dry run does not have any error inserts data in to table.
    :param data_resource: resources object of the table to which data is to be written
    :param _data: data in format list of dict
    :return: response dict with messages and status
    """
    if isinstance(_data, (list,)):
        data_frame = pd.DataFrame(_data)
    else:
        data_frame = _data
    data_frame['id'] = ''
    data_frame.fillna('', inplace=True)
    data_set = tablib.Dataset()
    data_set.df = data_frame
    result = data_resource.import_data(data_set, dry_run=True)
    if result.has_errors():
        # print([_.error for _ in result.row_errors()[0][1]])  # TODO: May be implement later, look into it properly
        response = {"message": "Something went wrong while inserting data to table", 'status': 422}
    else:
        logger.info("Import Dry run success. Writing data to DB")
        data_resource.import_data(data_set, dry_run=False)
        response = {"message": "Upload Success", "status": 200}
    logger.debug(response)
    return response
