const {
    access_key_ID,
    secret_access_key
} = require('./config.json')
const AWS = require('aws-sdk');

export const get_scores = () => {
    AWS.config.update({
        accessKeyId: access_key_ID, 
        secretAccessKey: secret_access_key,
        region: 'us-west-1'
    });

    var lambda = new AWS.Lambda();
    var params = {
        FunctionName: 'arn:aws:lambda:us-west-1:593661235042:function:get_scores', 
    };
    return new Promise((resolve, reject) => {
        lambda.invoke(params, (err, data) => {
            if (err) reject(err);            // an error occurred
            resolve(data);           // successful response
        });
    })
}
// get_scores().then((res) => {
//     console.log(res);
// })
// const test = async() => {
//     const x = (await get_scores()).Payload
//     console.log(JSON.parse(x));
//     for (var key in x.body){
//         console.log(key);
//     }
//     return x
// }
// test()

