const baseUrl = 'http://127.0.0.1:8010/';

const get = (url, data) => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `${baseUrl}${url}`,
            type: 'GET',
            data: data ? JSON.stringify(data) : null,
            success: function (data) {
                resolve(data);
            },
            error: function (error) {
                reject(error);
            }
        });
    });
}

const post = (url, data) => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `${baseUrl}${url}`,
            type: 'POST',
            data: data ? JSON.stringify(data) : null,
            success: function (data) {
                resolve(data);
            },
            error: function (error) {
                reject(error);
            }
        });
    });
}
