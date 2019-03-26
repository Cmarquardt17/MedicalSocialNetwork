const AWS = require('aws-sdk');
const querystring = require('querystring');
const ddb = new AWS.DynamoDB.DocumentClient();
AWS.config.region = 'us-west-2';

const fleet = [
    {
        Name: 'Dr. Sluggett',
        Age: '25',
        Gender: 'Male',
    },
];

exports.handler = (event, context, callback) => {
    if (!event.requestContext.authorizer) {
      errorResponse('Authorization not configured', context.awsRequestId, callback);
      return;
    }



const username = event.requestContext.authorizer.claims['cognito:username'];
const fName = null;
const mName = null;
const lName = null;
const address = null;
const phone = null;
const eContact = null;
const mSurgery = null;
const ssn = null;
const dob = null;
const gender = null;
const race = null;
const smoke = null;
const meds = null;
const conds = null;
const d1 = null;
const d2 = null;
const d3 = null;
// Set this to the region you upload the Lambda function to.


exports.handler = function(evt, context, callback) {
    // Our raw request body will be in evt.body.
    const params = querystring.parse(evt.body);

    // Our field from the request.
    fName = params['fInput'];
    mName = params['mInput'];
    lName = params['lInput'];
    address = params['addressInput'];
    phone = params['numberInput'];
    eContact = params['eInfoInput'];
    mSurgery = params['msInput'];
    ssn = params['ssnInput'];
    dob = params['birthdayInput'];
    gender = params['genderInput'];
    race = params['raceInput'];
    smoke = params['smokeInput'];
    meds = params['medInput'];
    conds = params['condInput'];

    // Generate HTML.
    ////const html = `<!DOCTYPE html><p>You said: ` + my_field + `</p>`;

    // Return HTML as the result.
    ////callback(null, html);
};
    // Because we're using a Cognito User Pools authorizer, all of the claims
    // included in the authentication token are provided in the request context.
    // This includes the username as well as other attributes.

    // The body field of the event in a proxy integration is a raw string.
    // In order to extract meaningful values, we need to first parse this string
    // into an object. A more robust implementation might inspect the Content-Type
    // header first and use a different parsing strategy based on that value.
    const requestBody = JSON.parse(event.body);

    const pickupLocation = requestBody.PickupLocation;

    addUserInfo(fName, mName, lName, address, phone, eContact, mSurgery,
    ssn, dob, gender, race, smoke, meds, conds, d1, d2, d3).then(() => {
        // You can use the callback function to provide a return value from your Node.js
        // Lambda functions. The first parameter is used for failed invocations. The
        // second parameter specifies the result data of the invocation.

        // Because this Lambda function is called by an API Gateway proxy integration
        // the result object must use the following structure.
        callback(null, {
            statusCode: 201,
            body: JSON.stringify({
            User: username,
            FirstName: fName,
            MiddleName: mName,
            LastName: lName,
            Address: address,
            Phone: phone,
            EContact: eContact,
            MajorSurgery: mSurgery,
            SocialSecurityNumber: ssn,
            Date_of_Birth: dob,
            Gender: gender,
            Race: race,
            Smoker: smoke,
            Medications: meds,
            Conditions: conds,
            Doctor1: d1,
            Doctor2: d2,
            Doctor3: d3,
            }),
            headers: {
                'Access-Control-Allow-Origin': '*',
            },
        });
    }).catch((err) => {
        console.error(err);

        // If there is an error during processing, catch it and return
        // from the Lambda function successfully. Specify a 500 HTTP status
        // code and provide an error message in the body. This will provide a
        // more meaningful error response to the end client.
        errorResponse(err.message, context.awsRequestId, callback)
    });
};

// This is where you would implement logic to find the optimal doctor for
// this ride (possibly invoking another Lambda function as a microservice.)
// For simplicity, we'll just pick a doctor at random.

function toUrlString(buffer) {
    return buffer.toString('base64')
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=/g, '');
}

function addUserInfo(username, firstName, middleName, lastName,
  address, phone, eContact, majorSurgery, ssn, d_o_b,
  gender, race, smoker, meds, conds, d1, d2, d3) {
    return ddb.put({
        TableName: 'UserInfo',
        Item: {
            User: username,
            FirstName: firstName,
            MiddleName: middleName,
            LastName: lastName,
            Address: address,
            Phone: phone,
            EContact: eContact,
            MajorSurgery: majorSurgery,
            SocialSecurityNumber: ssn,
            Date_of_Birth: d_o_b,
            Gender: gender,
            Race: race,
            Smoker: smoker,
            Medications: meds,
            Conditions: conds,
            Doctor1: d1,
            Doctor2: d2,
            Doctor3: d3,
        },
    }).promise();
    }

function errorResponse(errorMessage, awsRequestId, callback) {
  callback(null, {
    statusCode: 500,
    body: JSON.stringify({
      Error: errorMessage,
      Reference: awsRequestId,
    }),
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
  });
}
