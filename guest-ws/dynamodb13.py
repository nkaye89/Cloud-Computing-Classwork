
from boto3 import resource
from boto3.dynamodb.conditions import Key

table_name = 'guestManager'

def create_table():
    ''' create the guest table and return the table object'''
    dynamodb_resource = resource('dynamodb')
    # to do
    # check the sample code https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.01.html
    # create the guest table that contains (gid, first, last)
    # return the table object
    """
    Creates an Amazon DynamoDB table that can be used to store movie data.
    The table uses the release year of the movie as the partition key and the
    title as the sort key.

    :param table_name: The name of the table to create.
    :return: The newly created table.
    """
    print('creating table\n')
    table = dynamodb_resource.create_table (
    TableName = 'guestManager',
       KeySchema = [
           {
               'AttributeName': 'gid',
               'KeyType': 'HASH'
           },
           ],
           AttributeDefinitions = [
               {
                   'AttributeName': 'gid',
                   'AttributeType': 'N'
               }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits':1,
                'WriteCapacityUnits':1
            }
          
    )
    print('waiting for table to exist')
    table.wait_until_exists()

    return table


def get_table():
    dynamodb_resource = resource('dynamodb')
    # to do
    # return the table object, when the table is already created,
    # otherwise create and return the table object
    """Encapsulates an Amazon DynamoDB table of movie data."""
    """
    Queries for movies that were released in the specified year.

    :param year: The year to query.
    :return: The list of movies that were released in the specified year.
    """

    tableName  = 'guestManager'
    tableNames = [table.name for table in dynamodb_resource.tables.all()]

    if tableName in tableNames:
        print('table', tableName, 'exists')
        for table in dynamodb_resource.tables.all():
            if table.name == 'guestManager':
                return table
    else:
        return create_table()




# all the following operations need to handle the exceptions when a gid does not exist

def read_guests(table):
    print('reading guests\n')
    # to do
    """
    table is the object returned by get_table
    Return all guests
    """

    try:
        response = table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
    except ClientError as err:
        logger.error(
            'Couldn\'t read guests. Here\'s why: %s: %s',
            err.response['Error']['Code'], err.response['Error']['Message']
        )
        raise
    else:
        return data


def add_guest(table, gid, first, last):
    print('adding guest ', gid, 'with name ', first, ' ', last, '\n')
    """
    todo: Add one item (row) to table.
    """
    
    try:
        table.put_item(
            Item={
                'gid': gid,
                'firstN': first,
                'lastN': last})
    except ClientError as err:
        logger.error(
            'Couldn\'t read guests. Here\'s why: %s: %s',
            err.response['Error']['Code'], err.response['Error']['Message']
        )
        raise


def update_guest(table, gid, first, last):
    print('updating guest ', gid, '\n')
    """
    todo: update one item (row) to table.
    """
    try:
        response = table.update_item(
        Key={
            'gid': gid
        },
        UpdateExpression='SET firstN = :newFirstN, lastN = :newLastN',
        ExpressionAttributeValues={
            ':newFirstN': first,
            ':newLastN': last
        },
        ReturnValues="UPDATED_NEW")
    except ClientError as err:
        logger.error(
            'Couldn\'t read guests. Here\'s why: %s: %s',
            err.response['Error']['Code'], err.response['Error']['Message']
        )
        raise
    else:
        return response['Attributes']


def delete_guest(table, gid):
    print('deleting guest ', gid, '\n')
    """
    todo: Delete an item (row) in table according to the gid.
    """
    try:
        table.delete_item(Key={'gid': gid})
    except ClientError as err:
        logger.error(
            'Couldn\'t read guests. Here\'s why: %s: %s',
            err.response['Error']['Code'], err.response['Error']['Message']
        )
        raise


def main():
    table = get_table()
    print(table)
    
    add_guest(table, 101, 'greg', 'heff')
    add_guest(table, 102, 'noah', 'kaye')
    #delete_guest(table, 101)
    #delete_guest(table, 102)

    data = read_guests(table)

    for d in data:
        print(d)
    
    update_guest(table, 101, 'billy', 'bob')

    data = read_guests(table)

    for d in data:
        print(d)

    delete_guest(table, 102)

    data = read_guests(table)

    for d in data:
        print(d)