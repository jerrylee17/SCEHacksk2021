const {
    access_key_ID,
    secret_access_key
} = require('./config.json')
const AWS = require('aws-sdk');

const get_scores = async () => {
    AWS.config.update({
        accessKeyId: access_key_ID, 
        secretAccessKey: secret_access_key,
        region: 'us-west-1'
    });

    var lambda = new AWS.Lambda();
    var params = {
    FunctionName: 'arn:aws:lambda:us-west-1:593661235042:function:get_scores', 
    };
    let response = new Promise((resolve, reject) => {
        lambda.invoke(params, function(err, data) {
            if (err) reject(err);            // an error occurred
            else     resolve(data);           // successful response
        });
    })
    return response
}
// const data = get_scores().then((res) => {
//     console.log(res);
// })

module.exports = {get_scores}
